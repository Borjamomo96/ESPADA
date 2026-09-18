from pathlib import Path
from copy import deepcopy
import yaml
import re
import subprocess
import sys
import os
import json
from traceback import format_exc
from adplib.exceptions import ConfigurationError, RecoverableFileNotFoundError
from astropy.io.votable import parse_single_table

# Logger:
import logging
from adplib.logger import Logger
logger = Logger.get_logger()

def get_union_args(union_type):
    """
    Return the concrete types accepted by a union-like type annotation.
    """

    if hasattr(union_type, '__args__'):
        args = union_type.__args__
        # Convert None to type(None).
        return {arg if arg is not None else type(None) for arg in args}
    return {union_type}

def strict_isinstance(value, union_type):
    """
    Run isinstance() while keeping bool and int checks separate.
    """

    if not isinstance(value, union_type):
        return False
    
    # Special bool/int cases.
    union_args = get_union_args(union_type)
    
    if isinstance(value, bool) and int in union_args:
        # Reject bool values when int is allowed.
        return False
    if isinstance(value, int) and bool in union_args and type(value) is not bool:
        # Reject int values when bool is allowed, unless the value is truly bool.
        return False
    
    return True


class CatalogResult:
    """
    Result object used when resolving the catalog file passed to SIP.
    """

    def __init__(self, catalog_path=None, error_msg=None):
        """
        Store either a valid catalog path or an error message.
        """

        self.catalog_path = Path(catalog_path) if catalog_path is not None else None
        self.error_msg = error_msg
        self.success = self.catalog_path is not None
    
    def __bool__(self):
        """
        Return true when a valid catalog path was found.
        """

        return self.success


class SiPar(dict): 
    """
    Dictionary-backed representation of SIP arguments and run state.
    """

    # Static mapping from attribute names to SIP command-line shortcuts.
    ATTRIBUTE_SHORTCUTS = {
         "catalog_file": ["-c", "--catalog"],
         "channel_width": ["-cw",  "--chan_width"],
         "min_size": ["-i", "--image-size"],
         "source_id": ["-id", "--source-id"],
         "syn_beam_dimensions": ["-b", "--beam"],
         "snr_range": ["-snr", "--snr-range"],
         "surveys_list": ["-s", "--surveys"],
         "percentile_range": ["-ur", "--user-range"],
         "user_image": ["-ui", "--user-image"],
         "spec_line": ["-line", "--spectral-line"],
         "output_image_file_type": ["-x", "--suffix"],
         "combo": ["-m", "--imagemagick"],
         "spec_full_range": ["-o", "--original"],
         "no_source_id": ["-noid", "--no-source-id"],
         "channel_maps": ["-cm", "--chan-maps"],
         "spec_only": ["-spec", "--spec-only"],
         "plot_units": ["-j", "--jy-kms"],
         "overwrite": ["-ow", "--overwrite "]
    }

    # Expected parameter types.
    EXPECTED_TYPES = {
        'catalog_file': str | list | None,
        'channel_width': float | None,
        'min_size': float| int | None,
        'source_id': int | list | None,
        'syn_beam_dimensions': list | None,
        'snr_range': list | None,
        'surveys_list': list | None,
        'percentile_range': list | None,
        'user_image': str | list | None,
        'spec_line': str | list | None,
        'output_image_file_type': str | None,
        'combo': bool | str | None,
        'spec_full_range': bool, # | str | list | None,
        'no_source_id': bool | None,
        'channel_maps': bool | None,
        'spec_only': bool | None,
        'plot_units': bool | None,
        'overwrite': bool | None
    }

    GROUP_EXCLUDED_REPORT_TYPES = {
        "mom1",
        "mom2",
        "spec",
        "spec_both",
        "all_mom1",
        "all_mom2",
    }

    GROUP_DELETE_SUFFIXES = (
        "_mom1",
        "_mom2",
        "_spec",
        "_specboth",
    )


    def __init__(self, parameter_data=None, **kwargs):
        """Create independent SIP parameters from a startup snapshot or a file.

        ``parameter_data`` is a dictionary returned by ``load_parameters``.
        File-based callers may still supply ``sip_file_path`` instead. Dataset
        context is checked after the YAML values have been validated and copied.
        """
        super(SiPar, self).__init__(**kwargs)
        self.__dict__ = self
        self.configure(parameter_data=parameter_data, **kwargs)
        self.check_sip_args()

    @classmethod
    def load_parameters(cls, sip_file_path=None, sargs=None):
        """Read the YAML once and check its values before terminal arguments."""
        if sip_file_path is None:
            source_path = Path(__file__).parent / "sip_args.yaml"
        else:
            source_path = Path(sip_file_path).expanduser()
        with open(source_path, 'r') as source:
            content = source.read()
        try:
            values = yaml.safe_load(content)
        except yaml.YAMLError as error:
            raise ConfigurationError(
                f"Error parsing SIP YAML configuration file '{source_path}': {error}"
            ) from error
        cls.validate_parameters(values, source_path, sargs)
        logger.info(f"SIP parameters loaded into memory from: {source_path}")
        logger.info(
            "SIP file and terminal parameter checks passed. Dataset-specific "
            "checks and catalog resolution are still pending."
        )
        return {'path': source_path, 'content': content, 'values': values}

    def configure(self, sip_file_path=None, parameter_data=None, **kwargs):
        """Copy the validated startup values, or load them for file-based calls."""
        if parameter_data is None:
            sargs = self.sargs if self.adpalmap_config.enable_sip else None
            parameter_data = self.load_parameters(sip_file_path, sargs)
        self.update(deepcopy(parameter_data['values']))
        self.sip_file_path = parameter_data['path']
        self.sip_file_content = parameter_data['content']

    @classmethod
    def validate_parameters(cls, values, source_path, sargs=None):
        """Check the complete YAML, then the supplied terminal arguments.

        These checks need no dataset. They do not apply overrides or select
        catalogs and images; that remains part of preparing each dataset.
        """
        if not isinstance(values, dict):
            raise ConfigurationError(
                f"SIP configuration file '{source_path}' must contain a YAML mapping."
            )
        missing = [key for key in cls.EXPECTED_TYPES if key not in values]
        if missing:
            raise ValueError(
                f"Required SIP parameters missing in '{source_path}': {', '.join(missing)}"
            )

        # The file must be valid on its own, even if a terminal argument replaces a value.
        for from_terminal, parameters in ((False, values), (True, sargs or {})):
            for key, value in parameters.items():
                if from_terminal:
                    source = f"'-sarg {key}'"
                    for name, shortcuts in cls.ATTRIBUTE_SHORTCUTS.items():
                        if key in shortcuts:
                            key = name
                            break
                    else:
                        logger.warning(f"Unknown parameter '{key}' provided. It will be ignored.")
                        continue
                else:
                    source = f"'{source_path}'"
                    if key not in cls.EXPECTED_TYPES:
                        logger.warning(
                            f"Unknown parameter '{key}' in SIP configuration file {source}. "
                            "Check the parameter name."
                        )
                        continue

                expected_type = cls.EXPECTED_TYPES[key]
                if not strict_isinstance(value, expected_type):
                    raise ValueError(
                        f"SIP parameter '{key}' in {source} must be of type {expected_type}, "
                        f"but is of type {type(value)}."
                    )
                if value is None and not from_terminal:
                    continue

                ###########################---------source_id---------##############################
                if key == 'source_id':
                    if from_terminal:
                        if not isinstance(value, list) or not all(isinstance(x, int) for x in value):
                            raise ValueError(f"'source_id' in {source} must be a list of integers.")
                    elif isinstance(value, list):
                        for item in value:
                            cleaned = str(item).replace('[', '').replace(']', '').replace(',', '').strip()
                            try:
                                int(cleaned)
                            except ValueError as error:
                                raise ValueError(
                                    f"'source_id' in {source} contains a non-integer value: '{item}'"
                                ) from error
                ###########################---------syn_beam_dimensions---------##############################
                elif key == 'syn_beam_dimensions':
                    if value is None or len(value) > 3:
                        raise ValueError(f"'{key}' in {source} must be a list of at most three values.")
                    if not all(strict_isinstance(x, (int, float)) for x in value):
                        raise ValueError(f"'{key}' in {source} must contain only integers or floats.")
                ###########################---------snr_range / percentile_range---------##############################
                elif key in {'snr_range', 'percentile_range'}:
                    if value is None or len(value) != 2:
                        raise ValueError(f"'{key}' in {source} must be a list of two values.")
                ###########################---------spec_line---------##############################
                elif key == 'spec_line':
                    known_lines = ('HI', 'CO(1-0)', 'CO(2-1)', 'CO(3-2)',
                                   'OH_1612', 'OH_1665', 'OH_1667', 'OH_1720')
                    if isinstance(value, list) and len(value) > 3:
                        logger.warning(
                            f"'spec_line' in {source} should contain at most three values "
                            "(molecule, rest frequency in GHz, label)."
                        )
                    elif isinstance(value, str) and value not in known_lines:
                        logger.warning(
                            f"The line '{value}' in {source} is not among the supported "
                            "single-entry spectral line names."
                        )
                ###########################---------output_image_file_type---------##############################
                elif key == 'output_image_file_type':
                    if value not in ('png', 'jpg', 'pdf', 'svg'):
                        raise ValueError(
                            f"'{key}' in {source} must be one of png, jpg, pdf, svg; got {value!r}."
                        )

    def check_sip_args(self):
        """Validate dataset context and resolve its catalogs and ancillary image."""
        logger.info(
            f"Preparing SIP parameters for dataset '{self.input_data.stem}' "
            f"from the in-memory configuration loaded from {self.sip_file_path}."
        )
        ###########################---------catalog_file / user_image: multiple datasets---------##############################
        if len(self.number_list) > 1:
            for key in ('catalog_file', 'user_image'):
                value = getattr(self, key)
                if value is not None and not isinstance(value, list):
                    raise ValueError(
                        f"'{key}' in '{self.sip_file_path}' must be a list when processing "
                        "multiple datasets."
                    )
                if self.adpalmap_config.enable_sip and self.sargs:
                    for argument in self.ATTRIBUTE_SHORTCUTS[key]:
                        if argument in self.sargs:
                            value = self.sargs[argument]
                            if value is not None and not isinstance(value, list):
                                raise ValueError(
                                    f"'{argument}' supplied through -sarg must be a list "
                                    "when processing multiple datasets."
                                )

        ###########################---------catalog_file---------##############################
        if self.adpalmap_config.enable_sofia:
            if self.catalog_file is not None:
                logger.warning(
                    "The catalog(s) specified in the 'catalog_file' parameter in "
                    f"{self.sip_file_path} will be ignore. Those obtained from "
                    "SoFiA will be used instead, if any"
                ) 
                
        elif self.adpalmap_config.enable_group and not self.adpalmap_config.enable_sip:
            # No action required. SIP for grouped source will be handle in group with
            # the new 'group_' products from SoFiA.
            pass

        else:
            input_name = self.input_data.stem
            output_dir = self.adpalmap_config.output_dir

            if self.adpalmap_config.run_mode == "absorption":
                sofia_catalog_txt = output_dir / f"espada_{input_name}" / f"absorption_{input_name}_cat.txt"
                sofia_catalog_xml = output_dir / f"espada_{input_name}" / f"absorption_{input_name}_cat.xml"
                abs_cat_file = self.set_catalog(
                    sofia_catalog_txt, 
                    sofia_catalog_xml,
                    output_dir / f"espada_{input_name}"
                )
                if not abs_cat_file:
                    logger.error(abs_cat_file.error_msg)
                    raise RecoverableFileNotFoundError(abs_cat_file.error_msg)
                self.catalog_file = abs_cat_file.catalog_path

            elif self.adpalmap_config.run_mode == "emission":
                sofia_catalog_txt = output_dir / f"espada_{input_name}" / f"emission_{input_name}_cat.txt"
                sofia_catalog_xml = output_dir / f"espada_{input_name}" / f"emission_{input_name}_cat.xml"             
                emi_cat_file = self.set_catalog(
                    sofia_catalog_txt, 
                    sofia_catalog_xml,
                    output_dir / f"espada_{input_name}" 
                )
                if not emi_cat_file:
                    logger.error(emi_cat_file.error_msg)
                    raise RecoverableFileNotFoundError(emi_cat_file.error_msg)
                self.catalog_file = emi_cat_file.catalog_path  

            elif self.adpalmap_config.run_mode == "both":
                emi_sofia_catalog_txt = output_dir / f"espada_{input_name}" / f"emission_{input_name}_cat.txt"
                emi_sofia_catalog_xml = output_dir / f"espada_{input_name}" / f"emission_{input_name}_cat.xml"
                abs_sofia_catalog_txt = output_dir / f"espada_{input_name}" / f"absorption_{input_name}_cat.txt"
                abs_sofia_catalog_xml = output_dir / f"espada_{input_name}" / f"absorption_{input_name}_cat.xml"
                
        
                # Check before set any value to self.catalogue. Otherwise the second set_catalog
                # will show wrong errors. (Check if within set_catalog for more information)
                abs_cat_file = self.set_catalog(
                    abs_sofia_catalog_txt, 
                    abs_sofia_catalog_xml,
                    output_dir/ f"espada_{input_name}"
                )
                if not abs_cat_file:
                    logger.warning(abs_cat_file.error_msg)

                emi_cat_file = self.set_catalog(
                    emi_sofia_catalog_txt, 
                    emi_sofia_catalog_xml,
                    output_dir / f"espada_{input_name}"
                )
                if not emi_cat_file:
                    logger.warning(emi_cat_file.error_msg)

                self.catalog_file = []
                self.catalog_file.append(abs_cat_file.catalog_path)
                self.catalog_file.append(emi_cat_file.catalog_path)
                
                if all(cat is None for cat in self.catalog_file):
                    error_msg = "No catalog could be set in any mode to run SIP. SIP execution aborted."
                    logger.error(error_msg)
                    raise RecoverableFileNotFoundError(abs_cat_file.error_msg) 
        ##############################################################################################

        ###########################---------user_image---------##############################
        if hasattr(self, 'user_image') and getattr(self, 'user_image') is not None:
            attr_value = getattr(self, 'user_image')
            if self.adpalmap_config.enable_tap_service and self.ancillary_data:
                logger.warning(
                    f"The continuous images provided in the 'user_image' parameter in "
                    f"{self.sip_file_path} will be ignored. Those obtained from the archive "
                    "will be used."
                )
                self.user_image = self.ancillary_data

            else:
                if isinstance(attr_value, list):
                    if len(self.number_list) != len(attr_value):
                        error_msg = (
                            f"The number of continuum images provided in {self.sip_file_path} is "
                            " different from the number of datasets. There must be one images per "
                            "dataset. Use "" if you do not want to include an image for a dataset"
                        )
                        Logger.log_to_file(logging.ERROR, error_msg)
                        raise ValueError(error_msg)
                    else:
                        self.user_image = attr_value[self.id_number]
                        if not Path(self.user_image).exists():
                            error_msg = (
                                f"The continuum image '{self.user_image}' does not exist."
                            )
                            Logger.log_to_file(logging.ERROR, error_msg)
                            raise FileNotFoundError(error_msg)
                        if self.adpalmap_config.run_mode == "both":
                            logger.warning(
                                "In both mode, SIP will run twice with the same continuum image"
                                f" provided in {self.sip_file_path}, for each dataset."
                            )    
                else:
                    if not Path(self.user_image).exists():
                        error_msg = (
                            f"The continuum image  '{self.user_image}' does not exist."
                        )
                        Logger.log_to_file(logging.ERROR, error_msg)
                        raise FileNotFoundError(error_msg)
        ##############################################################################################


    def update_input_parameters(self):
        """Apply CLI overrides after YAML and dataset checks, preserving priority."""
        if self.sargs is not None:
            for key, value in self.sargs.items():
                for matched_attr, shortcuts in self.ATTRIBUTE_SHORTCUTS.items():
                    if key in shortcuts:
                        break
                else:
                    continue

                ###########################---------catalog_file---------##############################
                if matched_attr == "catalog_file" and not self.adpalmap_config.enable_sofia:
                    # Previous catalogs were found and take priority.
                    if(self.catalog_file is not None):
                        logger.warning(
                            "The catalog(s) provide via -sarg will be ignored because those found from"
                            " previous run have priority"
                        )
                        continue
                    # If only -sarg is present in this case, check_sip_args leaves
                    # self.catalog_file as None.
                    elif(self.catalog_file is None):
                        if len(self.number_list) != len(value):
                            error_msg = (
                                "The number of catalogs provided in via -sarg argument is "
                                " different from the number of datasets. There must be one "
                                "catalog per dataset."
                            )
                            Logger.log_to_file(logging.ERROR, error_msg)
                            raise ValueError(error_msg)
                        else:
                            setattr(self, matched_attr, value[self.id_number])
                            if self.adpalmap_config.run_mode == "both":
                                logger.warning(
                                    "In both mode, SIP will run twice with the same catalogs provided"
                                    f" via -sarg, for each dataset."
                                )
                                catalog_file = []
                                # Lo duplico para que no haya conflicto con el resto de casos en run_sip.
                                catalog_file.append(self.catalog_file)
                                catalog_file.append(self.catalog_file)
                                self.catalog_file = catalog_file     
                            continue
        ##############################################################################################

                ###########################---------user_image---------##############################
                elif matched_attr == "user_image":
                    if self.adpalmap_config.enable_tap_service and self.ancillary_data:
                        logger.warning(
                            f"The continuous images provided in the 'user_image' parameter via "
                            f"-sargs will be ignored. Those obtained from the archive "
                            "will be used"
                        )
                        self.user_image = self.ancillary_data

                    else:
                        if isinstance(value, list):
                            if len(self.number_list) != len(value):
                                error_msg = (
                                    f"The number of continuum images provided via -sargs is "
                                    " different from the number of datasets. There must be one images per"
                                    " dataset. Use "" if you do not want to include an image for a dataset"
                                )
                                Logger.log_to_file(logging.ERROR, error_msg)
                                raise ValueError(error_msg)
                            else:
                                self.user_image = value[self.id_number]
                                if not Path(self.user_image).exists():
                                    error_msg = (
                                        f"The continuum image '{self.user_image}' does not exist."
                                    )
                                    Logger.log_to_file(logging.ERROR, error_msg)
                                    raise FileNotFoundError(error_msg)
                                if self.adpalmap_config.run_mode == "both":
                                    logger.warning(
                                        "In both mode, SIP will run twice with the same continuum image"
                                        f" provided in {self.sip_file_path}, for each dataset."
                                    )   
                        else:
                            if not Path(self.user_image).exists():
                                error_msg = (
                                    f"The continuum image  '{self.user_image}' does not exist."
                                )
                                Logger.log_to_file(logging.ERROR, error_msg)
                                raise FileNotFoundError(error_msg)                                 
        ##############################################################################################

                # Keep mutable CLI values local to this dataset too.
                setattr(self, matched_attr, deepcopy(value))


    def run_sip(self, sopar=None, run=-1, product_profile="regular"):
        """
        Run the SIP (Source Identification Pipeline) process with the specified configuration.

        This method executes the SIP process by generating the appropriate command and running it 
        via a subprocess. It also determines which catalog file (TXT or XML) to use for the SIP 
        process, based on the output directory of the `sopar` object. If no valid catalog file is 
        found, the method logs a critical error and terminates execution.

        Parameters:
        ----------
        adpalmap_config: Config() class object with configuration from the configuration file.
        sopar (optional): SoPar() class object with parameters from the SoFiA parameters file.
                          Default=None
                        

        Returns:
        ----------
            None

        Raises:
        ----------
            SystemExit: If no valid catalog file is found in the `sopar.output_directory` or if 
                        there is an error while executing the SIP subprocess.

        
        """

        # Create SIP report
        sip_report = {
                        "software_id" :'SIP',
                        "PID": self.pid,
                        "input_name": self.input_data.stem,
                        "input_path": str(self.input_data),
                        "mode": "",  
                        "log_path": "",
                        "outputs": {"images": [],  "files": []}
                    }
        
        ##############################################################################################
        # Check the catalog files availables|set 

        if sopar: # Equivalent to adpalmap_config.enable_sofia for this branch.

            # Check the current run before considering any older catalogs on disk.
            if getattr(sopar, "last_exit_code", None) == 8:
                reason = "SIP skipped: SoFiA detected no sources (exit code 8)."
                sip_report.update({
                    "mode": sopar.mode,
                    "status": "no_sources",
                    "skip_reason": reason,
                    "exit_code": None,
                    "command": [],
                    "error": "",
                })
                logger.info(f"{reason} Mode: {sopar.mode}.")
                return sip_report
            
            base_name = sopar.output_filename
            sip_output_dir = sopar.output_directory / f"{base_name}_figures"
                    
            sofia_catalog_txt = sopar.output_directory / f"{base_name}_cat.txt"
            sofia_catalog_xml = sopar.output_directory / f"{base_name}_cat.xml"

            if sofia_catalog_txt.exists() or sofia_catalog_xml.exists():
                pass
            else:
                sofia_catalog_txt = None
                sofia_catalog_xml = None

            # Update SIP report
            sip_report["mode"]     = sopar.mode
            sip_report["log_path"] = sopar.output_directory / f"{base_name}_sip.log"

    
            if sofia_catalog_txt:
                self.catalog_file = sofia_catalog_txt
            elif sofia_catalog_xml:
                self.catalog_file = sofia_catalog_xml
            else:
                error_msg = (
                    "No valid .txt or .xml catalog for SIP found within the  "
                    f"{sopar.output_directory} directory."
                )
                logger.error(error_msg)
                if self.adpalmap_config.run_mode == 'both' and run!=0:
                    logger.info(f"SIP execution skipped. Run: {sopar.mode}")
                    sip_report.update({'command': '', 'error': error_msg})
                    return sip_report
                else:
                    logger.info(f"SIP execution aborted. Run: {sopar.mode}.")
                    sip_report.update({'command': '', 'error': error_msg})
                    return sip_report

        else:
            if self.adpalmap_config.run_mode == "both":             
                if run != 0:
                    #En 0 guardo el catalago de absorciones
                    self.aux_catalog_file = self.catalog_file
                    self.catalog_file = self.catalog_file[0]  

                    if self.catalog_file is None:
                        logger.info("SIP execution skipped. Mode: absorption")
                        sip_report.update({'command': '', 'error': ''})
                        return sip_report

                    base_name = self.catalog_file.name.replace('_cat.txt', '').replace('_cat.xml', '')
                    sip_output_dir = self.catalog_file.parent / f"{base_name}_figures"
                    
                    #Update SIP report
                    sip_report["mode"]     = "absorption"
                    sip_report["log_path"] = self.catalog_file.parent / f"{base_name}_sip.log"
                            
                else:
                    #En 1 guardo el catalago de emisiones
                    self.catalog_file = self.aux_catalog_file
                    self.catalog_file = self.catalog_file[1]

                    if self.catalog_file is None:
                        logger.info("SIP execution skipped. Mode: emission")
                        sip_report.update({'command': '', 'error': ''})
                        return sip_report
                    
                    base_name = self.catalog_file.name.replace('_cat.txt', '').replace('_cat.xml', '')
                    sip_output_dir = self.catalog_file.parent / f"{base_name}_figures"

                    #Update SIP report
                    sip_report["mode"]     = "emission"
                    sip_report["log_path"] = self.catalog_file.parent / f"{base_name}_sip.log"
                    
            elif self.adpalmap_config.run_mode == "absorption":
                base_name = self.catalog_file.name.replace('_cat.txt', '').replace('_cat.xml', '')
                sip_output_dir = self.catalog_file.parent / f"{base_name}_figures"

                #Update SIP report
                sip_report["mode"]     = "absorption"
                sip_report["log_path"] = self.catalog_file.parent / f"{base_name}_sip.log"
           
            elif self.adpalmap_config.run_mode == "emission":
                base_name = self.catalog_file.name.replace('_cat.txt', '').replace('_cat.xml', '')
                sip_output_dir = self.catalog_file.parent / f"{base_name}_figures"

                #Update SIP report
                sip_report["mode"]     = "emission"
                sip_report["log_path"] = self.catalog_file.parent / f"{base_name}_sip.log"            

        ##############################################################################################

        # Remove existing log file
        if  sip_report["log_path"].exists():
            try:
                sip_report["log_path"].unlink()
            except:
                logger.warning(
                    "Error trying to delete existing log file. The new log "
                    "entries will be appended to it."
                )

        ##############################################################################################

        # Generate the command
        cmd = self.generate_command(
            exclude=["aux_catalog_file"], 
            log_path=sip_report["log_path"]
        )

        # Update the report
        sip_report.update({'command':cmd})

        error = ''
        try:
            
            #Logger.raw("================================")
            if self.adpalmap_config.run_mode == "both" and run!=0:
                logger.info(f"SIP start. Mode: absorption. Input data: {self.input_data.stem}")
            elif self.adpalmap_config.run_mode == "both" and run==0:
                logger.info(f"SIP start. Mode: emission. Input data: {self.input_data.stem}")
            else:
                logger.info(
                    f"SIP start. Mode: {self.adpalmap_config.run_mode}. "
                    f"Input data: {self.input_data.stem}"
                )
            Logger.raw(
                f"[{self.pid}]ESPADA_EVENT external_log "
                + json.dumps(
                    {
                        "software_id": "SIP",
                        "mode": sip_report["mode"],
                        "input_name": self.input_data.stem,
                        "input_path": str(self.input_data),
                        "log_path": str(sip_report["log_path"]),
                        "is_group": str(base_name).startswith("group_"),
                    },
                    sort_keys=True,
                )
            )
            #Logger.raw("================================")

            logger.info(f"Command used to run SIP: {' '.join(cmd)}")
            
            # Execute SIP
            subprocess.run(
                cmd, 
                text=True, 
                check=True, 
                capture_output=not self.adpalmap_config.verbose
                )       
                               
            #Logger.raw("================================")
            logger.info(f"SIP finished.")
            #Logger.raw("================================")
            
            # Add output to SIP report 
            if self.adpalmap_config.make_report:
                try:
                    self.report_outputs(
                        sip_report,
                        sip_output_dir,
                        base_name,
                        product_profile=product_profile
                    )  
                except Exception as e:
                    logger.warning(f"Error adding outputs for the html report (non-critical): {e}")


        except FileNotFoundError as e:
            logger.critical(f"Command not found: {cmd[0]}. Error: {e}")
            raise

        except subprocess.CalledProcessError as e:
            error = str(e)

            # sip_report["mode"] contains the right mode name but if some error occurs before this
            # will cause another error here. This way will always works
            if self.adpalmap_config.run_mode == "both" and run!=0:
                logger.error(f"Error running SIP. Mode: absorption. Error: {e}")         
            elif self.adpalmap_config.run_mode == "both" and run==0:
                logger.error(f"Error running SIP. Mode: emission. Error: {e}")
            else:
                logger.error(f"Error running SIP. Mode: {self.adpalmap_config.run_mode}. Error: {e}")

            logger.info(f"SIP execution aborted.")
     
        except Exception as e:
            logger.error(f"{e}")

        finally:
            sip_report.update({'error': error})
            return sip_report
        
  
    def generate_command(self, exclude=None, log_path=None):
        """
        Generates a command based on the shortcuts defined in ATTRIBUTE_SHORTCUTS and 
        the non-None attributes of the instance.

        Parameters:
        ----------
        exclude: List with the attribute to exclude in the command generation

        Returns:
        ----------
        list: List with the shortcuts and values in the format ["-c", "value", ...].
        """

        if exclude is None:
            exclude = []  # Initialize as an empty list when omitted.

        cmd = ["sofia_image_pipeline"]

        for attr_name, shortcut in self.ATTRIBUTE_SHORTCUTS.items():
            
            if attr_name in exclude:  
                continue
        ###########################--------------bool-type--------------##############################
            if attr_name == "combo" and getattr(self, attr_name) is not None:  
                attr_value = getattr(self, attr_name)
                if isinstance(attr_value, bool) and attr_value: 
                    cmd.append(shortcut[0])
                elif isinstance(attr_value, str): 
                    cmd.append(shortcut[0])
                    cmd.append(attr_value)
                continue  

            elif attr_name in {"no_source_id", "channel_maps", "spec_only", "plot_units", "overwrite"}:
                attr_value = getattr(self, attr_name)
                if attr_value:
                    cmd.append(shortcut[0])

            elif attr_name == "spec_full_range":
                attr_value = getattr(self, attr_name)
                if attr_value:
                    cmd.append(shortcut[0])
                    cmd.append(str(self.input_data))
        ##############################################################################################
            
        ###########################--------------list-type--------------##############################
            elif attr_name == "source_id":
                attr_value = getattr(self, attr_name, None) 
                if attr_value:
                    cmd.append(shortcut[0])
                    if isinstance(attr_value, list):
                        for value in attr_value:
                            cmd.append(str(value))
                    else: 
                        cmd.append(str(attr_value))  
                else:
                    #pass
                    cmd.append(shortcut[0])
                    cmd.append(str(-1))
                    self.source_id = int(-1)
                    logger.info(
                        "No value set for 'source_id' parameter. Setting 'source_id' to -1 " 
                        "to get images for all sources and summary images"
                    )
            
            elif attr_name == "syn_beam_dimensions":               
                attr_value = getattr(self, attr_name, None) 
                if attr_value:
                    cmd.append(shortcut[0])
                    cmd.append(",".join(str(x) for x in attr_value))# Must be comma-separated no space     

            elif (attr_name in {"snr_range", "surveys_list", "percentile_range"} and 
                getattr(self, attr_name) is not None):
                    cmd.append(shortcut[0])
                    for value in getattr(self, attr_name):
                        cmd.append(str(value))
          
        ##############################################################################################

        ###########################-------------catalog-type------------##############################
            # The cont image is set only if the TAP service is used and the user does 
            # not specify any value.
            elif (attr_name == "user_image"): 
                attr_value = getattr(self, attr_name, None) 
                if attr_value is not None:
                    cmd.append(shortcut[0])
                    cmd.append(str(attr_value))
                    if self.adpalmap_config.enable_tap_service and self.ancillary_data:
                        logger.info(
                            f"Continuum image set for the 'user_image' parameter in {self.sip_args_path} "
                            "or via -sarg. It will be used instead of the one available from the archive"
                        )
                else:
                    if self.adpalmap_config.enable_tap_service and self.ancillary_data:  
                        logger.info(
                            f"Continuum image '{self.ancillary_data}' from the archive loaded into "
                            "'user_image' parameter."
                        )
                        cmd.append(shortcut[0])
                        cmd.append(str(self.ancillary_data))                 
        ##############################################################################################

        ###########################----------------no-type--------------##############################
            elif hasattr(self, attr_name) and getattr(self, attr_name) is not None:  
                cmd.append(shortcut[0])  
                cmd.append(str(getattr(self, attr_name))) 
        ##############################################################################################
        
        cmd.append("-log")
        cmd.append(str(log_path))

        return cmd


    def make_summary(self, cmd):
        """
        Generates a command based on the instance attributes, ensuring that the `-id` argument 
        has the value `0`, even if it was not in the original command.

        Returns:
        ----------
        list: List with the command set, where `-id` has the value `0`.
        """

        # Ensure that `-id` is present with value `0`.
        if "-id" in cmd:
            id_index = cmd.index("-id")
            cmd[id_index + 1] = "0"  # Replace the value with "0".
        else:
            # Add `-id` at the end if it is not already in the command.
            cmd.extend(["-id", "0"])

        return cmd
    

    def set_catalog(self, sofia_catalog_txt, sofia_catalog_xml, output_directory):
        """
        Resolve the catalog file that SIP should use.

        Parameters
        ----------
        sofia_catalog_txt : pathlib.Path
            Expected SoFiA TXT catalog path.
        sofia_catalog_xml : pathlib.Path
            Expected SoFiA XML catalog path.
        output_directory : pathlib.Path
            Directory searched for catalogs from previous runs.

        Returns
        -------
        CatalogResult
            Catalog path or error message describing why no catalog could be resolved.
        """


        existing_files = [file for file in [sofia_catalog_txt, sofia_catalog_xml] if file.exists()]

        if existing_files:
            logger.info(
                "Valid catalog from previous runs found for the dataset. Catalog: "
                f"{existing_files[0]}"
            )
            return CatalogResult(catalog_path=existing_files[0])
        else:
            logger.warning(
                f"No valid .txt or .xml catalog for SIP found within the {output_directory} directory "
                "from previous runs. "
                f"Catalogs searched: {sofia_catalog_txt} || {sofia_catalog_xml}"
            )
            # No catalog is set in sip_args.yaml or -sarg.
            if self.catalog_file is None and not self.sargs:
                error_msg = (
                    "No 'catalog_file' parameter was provided either in file 'sip_args.yaml' or via "
                    "the '-sarg|--sip-arguments'."
                )
                #logger.error(f"ValueError: {error_msg}")
                return CatalogResult(error_msg=error_msg)
                
            # No catalog is set in the file, so check whether -c or --catalog was passed.
            elif self.catalog_file is None and self.sargs:
                if '-c' not in self.sargs and '--catalog' not in self.sargs:
                    error_msg = (
                        "No 'catalog_file' parameter was found either in file 'sip_args.yaml' or "
                        "via the '-sarg|--sip-arguments'."
                    )
                    #logger.error(f"ValueError: {error_msg}")
                    return CatalogResult(error_msg=error_msg)
                else:
                    catalog_path = self.sargs.get('-c', self.sargs.get('--catalog'))
                    if Path(catalog_path).exists():
                        return CatalogResult(catalog_path=catalog_path)
                    else:
                        error_msg = (
                            f"The catalog file '{catalog_path}' does not exist."
                        )
                        return CatalogResult(error_msg=error_msg)
                
            # A file-defined catalog must have the correct length.
            elif self.catalog_file is not None:
                catalog_list = self.catalog_file
                if isinstance(catalog_list, list) and len(self.number_list) != len(catalog_list):
                    error_msg = (
                        f"The number of catalogs provided in 'catalog_file' parameter is "
                        " different from the number of datasets. There must be one "
                        "catalog per dataset."
                    )
                    #logger.error(f"ValueError: {error_msg}")
                    return CatalogResult(error_msg=error_msg)
                
                elif isinstance(catalog_list, list) and len(self.number_list) == len(catalog_list):
                    logger.info(
                        f"Valid lenth for the 'catalog_file' parameter in 'sip_args.yaml'."
                    )
                    if self.adpalmap_config.run_mode == "both":
                        logger.warning(
                            "In both mode, SIP will run twice with the same catalogs provided in "
                            f"{self.sip_file_path}, for each dataset."
                        )
                    missing_cat = [cat for cat in catalog_list if not Path(cat).exists()]
                    if missing_cat:
                        missing_list = "--".join(str(p) for p in missing_cat)
                        error_msg = (
                            f"The following catalog{'s' if len(missing_list) != 1 else ''} "
                            f"do{' not' if len(missing_list) != 1 else 'es not'} exist: {missing_list}"
                        )
                        return CatalogResult(error_msg=error_msg)
                    else:
                        return CatalogResult(catalog_path=catalog_list[self.id_number])
                
                elif isinstance(catalog_list, str):
                    if Path(catalog_list).exists():
                        return CatalogResult(catalog_path=catalog_list)
                    else:
                        error_msg = f"The catalog file '{catalog_list}' does not exist."
                        return CatalogResult(error_msg=error_msg)
                else:
                    logger.critical(
                        "You have found a case that has not been taken into "
                        "account and may be misleading. Please open an issue on "
                        "https://github.com/Borjamomo96/ESPADA with your specific case."
                    )
                    raise
            else:
                logger.critical(
                    "You have found a case that has not been taken into "
                    "account and may be misleading. Please open an issue on "
                    "https://github.com/Borjamomo96/ESPADA.git with your specific case."
                )
                raise
              

    def report_outputs(self, sip_report, output_dir, base_name, product_profile="regular"):
        """
        Register expected SIP output products in a report entry.

        Parameters
        ----------
        sip_report : dict
            Report dictionary for the current SIP execution.
        output_dir : pathlib.Path
            Directory containing per-source SIP figures.
        base_name : str
            Base filename used by SIP products.
        product_profile : str, optional
            Product profile used to filter group-only outputs.
        """

        if self.output_image_file_type:
            suffix = self.output_image_file_type
        else:
            suffix = 'png'

        def add_image(image_info):
            """
            Add an image entry unless it is excluded for the current product profile.
            """

            if (
                product_profile == "group" and
                image_info.get("type") in self.GROUP_EXCLUDED_REPORT_TYPES
            ):
                return
            sip_report['outputs']['images'].append(image_info)

        num_sources = self.detect_source_count() 

        if self.source_id is None:
            individual_sources = range(1, num_sources+1)
            create_summary = False
        elif self.source_id == -1:
            individual_sources = range(1, num_sources+1)
            create_summary = True     
        elif self.source_id == 0:
            individual_sources = []
            create_summary = True       
        elif isinstance(self.source_id, list):
            if -1 in self.source_id:
                individual_sources = range(1, num_sources+1)
                create_summary = True 
            else: # In case of 0 or id > number of sources
                create_summary = 0 in self.source_id
                cleaned_sources = [s for s in self.source_id if s != 0]
                valid_sources = [s for s in cleaned_sources if 1 <= s <= num_sources]
                individual_sources = valid_sources

        for i in individual_sources:
            source_prefix = f"_{i}"

            # The order of the images here rules the order of the images in the report
            add_image({
                "type": "mom0",
                "path": output_dir / f"{base_name}{source_prefix}_mom0.{suffix}",
                "source_id": i,
                "description": "Moment 0 image",
                "software-id": "sip"
            })
            if hasattr(self, 'source_id') and getattr(self, 'source_id') is not None:
                add_image({
                    "type": "mom0_usr",
                    "path": output_dir / f"{base_name}{source_prefix}_mom0_usr.{suffix}",
                    "source_id": i,
                    "description": "Moment 0 image (continuum overlaid)",
                    "software-id": "sip"
                })
            add_image({
                "type": "snr",
                "path": output_dir / f"{base_name}{source_prefix}_snr.{suffix}",
                "source_id": i,
                "description": "SNR image",
                "software-id": "sip"
            })   
            add_image({
                "type": "mom1",
                "path": output_dir / f"{base_name}{source_prefix}_mom1.{suffix}",
                "source_id": i,
                "description": "Moment 1 image",
                "software-id": "sip"
            })
            add_image({
                "type": "mom2",
                "path": output_dir / f"{base_name}{source_prefix}_mom2.{suffix}",
                "source_id": i,
                "description": "Moment 2 image",
                "software-id": "sip"
            })
            add_image({
                "type": "spec",
                "path": output_dir / f"{base_name}{source_prefix}_spec.{suffix}",
                "source_id": i,
                "description": "Spectrum plot",
                "software-id": "sip"
            })
            add_image({
                "type": "spec_full",
                "path": output_dir / f"{base_name}{source_prefix}_specfull.{suffix}",
                "source_id": i,
                "description": "Full spectrum plot",
                "software-id": "sip"
            })
            add_image({
                "type": "spec_both",
                "path": output_dir / f"{base_name}{source_prefix}_specboth.{suffix}",
                "source_id": i,
                "description": "Both spectrum plot",
                "software-id": "sip"
            })
            add_image({
                "type": "pv",
                "path": output_dir / f"{base_name}{source_prefix}_pv.{suffix}",
                "source_id": i,
                "description": "Major axis Position-Velociy plot",
                "software-id": "sip"
            })
            add_image({
                "type": "pv_min",
                "path": output_dir / f"{base_name}{source_prefix}_pv_min.{suffix}",
                "source_id": i,
                "description": "Minor axis Position-Velociy plot",
                "software-id": "sip"
            })

            if self.surveys_list and self.surveys_list != ['none']:
                for survey in self.surveys_list:
                    if survey != 'none':
                        survey_nospace = survey.replace(" ", "").lower()
                        survey_path = (
                            output_dir / f"{base_name}{source_prefix}_mom0_{survey_nospace}.{suffix}"
                        )
                        add_image({
                            "type": f"mom0_{survey_nospace}",
                            "path": survey_path,
                            "source_id": i,
                            "description": f"Moment 0 image ({survey})",
                            "software-id": "sip"
                        })                
        
        if create_summary:
            add_image({
                    "type": "all_mom0",
                    "path": output_dir.parent / f"{base_name}_mom0.{suffix}",
                    "source_id": -1,
                    "description": "Moment 0 image of all sources",
                    "software-id": "sip"
                })
            
            add_image({
                    "type": "all_mom1",
                    "path": output_dir.parent / f"{base_name}_mom1.{suffix}",
                    "source_id": -1,
                    "description": "Moment 1 image of all sources",
                    "software-id": "sip"
                })
            
            add_image({
                    "type": "all_mom2",
                    "path": output_dir.parent / f"{base_name}_mom2.{suffix}",
                    "source_id": -1,
                    "description": "Moment 2 image of all sources",
                    "software-id": "sip"
                })
            
            add_image({
                    "type": "all_sources",
                    "path": output_dir.parent / f"{base_name}_sources.{suffix}",
                    "source_id": -1,
                    "description": "Identifying image of all sources",
                    "software-id": "sip"
                })

            sip_report['outputs']['files'].append({
                    "type": "par_file",
                    "path": self.sip_file_path,
                    "format": ".par",
                    "software-id": "sip"
                })
            
            if self.surveys_list and self.surveys_list != ['none']:
                for survey in self.surveys_list:
                    if survey != 'none':
                        survey_nospace = survey.replace(" ", "").lower()
                        # HERE YOU NEED TO ENTER THE CORRECT PATH, WAITING FOR IT TO RESOLVES THE SIP PROBLEM
                        survey_path = (
                            output_dir.parent / f"{base_name}_mom0_{survey_nospace}.{suffix}"
                        )
                        add_image({
                            "type": f"mom0_{survey_nospace}",
                            "path": survey_path,
                            "source_id": -1,
                            "description": f"Momment 0 image ({survey})",
                            "software-id": "sip"
                        }) 


    def cleanup_group_outputs(self, sip_report):
        """
        Remove Group-only SIP products that should not be kept after execution.
        """

        if not sip_report.get("command"):
            logger.debug("Skipping SIP Group cleanup because SIP was not executed.")
            return

        log_path = sip_report.get("log_path")
        if not log_path:
            return

        log_path = Path(log_path)
        if not log_path.name.endswith("_sip.log"):
            logger.debug("Skipping SIP Group cleanup because log path has an unexpected name.")
            return

        base_name = log_path.name[:-len("_sip.log")]
        if not base_name.startswith("group_"):
            logger.debug("Skipping SIP Group cleanup for non-group output.")
            return

        suffix = self._output_suffix_from_report(sip_report)
        output_dir = log_path.parent
        figures_dir = output_dir / f"{base_name}_figures"

        for product_suffix in self.GROUP_DELETE_SUFFIXES:
            file_suffix = f"{product_suffix}.{suffix}"
            self._remove_group_output(output_dir / f"{base_name}{file_suffix}")

            if figures_dir.is_dir():
                for candidate in figures_dir.iterdir():
                    if (
                        candidate.name.startswith(f"{base_name}_") and
                        candidate.name.endswith(file_suffix)
                    ):
                        self._remove_group_output(candidate)


    def _output_suffix_from_report(self, sip_report):
        """
        Infer the SIP image suffix from the executed command stored in the report.

        Parameters
        ----------
        sip_report : dict
            SIP report dictionary containing the executed command.

        Returns
        -------
        str
            Output image suffix, defaulting to png.
        """

        command = sip_report.get("command") or []
        for option in ("-x", "--suffix"):
            if option in command:
                option_index = command.index(option)
                if option_index + 1 < len(command):
                    return str(command[option_index + 1]).lstrip(".")
        return "png"


    def _remove_group_output(self, path):
        """
        Remove a single unwanted group output file if it exists.

        Parameters
        ----------
        path : str or pathlib.Path
            Candidate file to remove.
        """

        path = Path(path)

        if not path.exists():
            logger.debug(f"Group cleanup target not present: {path}")
            return

        if not path.is_file():
            logger.warning(f"Skipping Group cleanup target because it is not a file: {path}")
            return

        try:
            path.unlink()
            logger.info(f"Removed unwanted SIP Group output file: {path}")
        except Exception as e:
            logger.warning(f"Could not remove SIP Group output '{path}': {e}")
            

    def detect_source_count(self):
        """
        Count catalog sources for report product registration.

        Returns
        -------
        int
            Number of sources detected in the catalog, or 0 if it cannot be read.
        """

        if not self.catalog_file:
            return 0
        
        # Check whether the file exists.
        if not self.catalog_file.exists():
            # Check whether the extension is valid.
            valid_extensions = ['.txt', '.xml']
            if self.catalog_file.suffix.lower() in valid_extensions:
                logger.warning(
                    f"Catalog file '{self.catalog_file}' does not exist. "
                    f"Unable to detect sources for reporting."
                )
            else:
                logger.error(
                    f"Invalid extension for catalog file: '{self.catalog_file.suffix}'. "
                    f"Allowed extensions: {valid_extensions}"
                )
            return 0
        
        # If the file exists.
        if self.catalog_file.suffix.lower() == '.txt':
            try:
                with open(self.catalog_file, 'r') as f:
                    return sum(1 for line in f if line.strip().startswith('"'))
            except Exception as e:
                logger.warning(
                    f"Error counting sources in {self.catalog_file}: {str(e)}. "
                    "Returning 0 sources for reporting."
                )
                return 0
        
        elif self.catalog_file.suffix.lower() == '.xml':
            try:
                table = parse_single_table(self.catalog_file)
                count = len(table.array)
                logger.debug(f"Detected {count} sources in XML catalog: {self.catalog_file}")
                return count
            except Exception as e:
                logger.warning(
                    f"XML catalog parsing failed ({self.catalog_file}): {str(e)}. "
                    "Returning 0 sources for reporting."
                )
                return 0
        
        else:
            logger.error(
                f"Invalid extension for catalog file: '{self.catalog_file.suffix}'. "
                "Allowed extensions: '.txt' or '.xml'"
            )
            return 0
        
        
   
