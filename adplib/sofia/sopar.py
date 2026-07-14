import os
import sys
import subprocess
#import tempfile 
import json
import numpy as np
from pathlib import Path
from astropy.io import fits
import matplotlib.pyplot as plt
from adplib.exceptions import RecoverableError, RecoverableValueError, RecoverableFileNotFoundError
from astropy.io.votable import parse_single_table
from adplib.sofia.region import (
    apply_input_region_crop,
    extract_input_region_from_header,
    format_input_region,
    parse_input_region,
    serialize_input_region,
)

# Logger:
import logging
from adplib.logger import Logger
logger = Logger.get_logger()


SOFIA_UNKNOWN_EXIT_MESSAGE = (
    "SoFiA returned an exit code that is not registered in "
    "SOFIA_EXIT_MESSAGES. Check the SoFiA log for details."
)


SOFIA_EXIT_MESSAGES = {
    1: "An unspecified error occurred.",
    2: "A NULL pointer was encountered.",
    3: "A memory allocation error occurred. This could indicate that the "
       "data cube is too large for the amount of memory available on the "
       "machine.",
    4: "An array index was found to be out of range.",
    5: "An error occurred while trying to read or write a file or check if "
       "a directory or file is accessible.",
    6: "An integer overflow occurred.",
    7: "The pipeline was aborted due to invalid user input. This could be "
       "due to an invalid parameter setting or the wrong input file being "
       "provided.",
    8: "No specific error occurred, but no sources were detected either.",
}


SOFIA_PARAMETER = [
    "pipeline.verbose",
    "pipeline.pedantic",
    "pipeline.threads",
    "input.data",
    "input.primaryBeam",
    "input.region",
    "input.gain",
    "input.noise",
    "input.weights",
    "input.mask",
    "input.invert",
    "flag.region",
    "flag.catalog",
    "flag.radius",
    "flag.auto",
    "flag.threshold",
    "flag.log",
    "flag.cube",
    "contsub.enable",
    "contsub.order",
    "contsub.threshold",
    "contsub.shift",
    "contsub.padding",
    "scaleNoise.enable",
    "scaleNoise.mode",
    "scaleNoise.statistic",
    "scaleNoise.fluxRange",
    "scaleNoise.windowXY",
    "scaleNoise.windowZ",
    "scaleNoise.gridXY",
    "scaleNoise.gridZ",
    "scaleNoise.interpolate",
    "scaleNoise.scfind",
    "background.enable",
    "background.statistic",
    "background.windowXY",
    "background.windowZ",
    "background.gridXY",
    "background.gridZ",
    "background.interpolate",
    "scfind.enable",
    "scfind.kernelsXY",
    "scfind.kernelsZ",
    "scfind.threshold",
    "scfind.replacement",
    "scfind.statistic",
    "scfind.fluxRange",
    "threshold.enable",
    "threshold.threshold",
    "threshold.mode",
    "threshold.statistic",
    "threshold.fluxRange",
    "filter.discardNegative",
    "filter.minSNR",
    "filter.minPixels",
    "linker.enable",
    "linker.radiusXY",
    "linker.radiusZ",
    "linker.minSizeXY",
    "linker.minSizeZ",
    "linker.maxSizeXY",
    "linker.maxSizeZ",
    "linker.minPixels",
    "linker.maxPixels",
    "linker.minFill",
    "linker.maxFill",
    "linker.positivity",
    "reliability.enable",
    "reliability.parameters",
    "reliability.threshold",
    "reliability.scaleKernel",
    "reliability.autoKernel",
    "reliability.iterations",
    "reliability.tolerance",
    "reliability.catalog",
    "reliability.plot",
    "reliability.debug",
    "dilation.enable",
    "dilation.iterationsXY",
    "dilation.iterationsZ",
    "dilation.threshold",
    "parameter.enable",
    "parameter.wcs",
    "parameter.physical",
    "parameter.prefix",
    "parameter.offset",
    "output.directory",
    "output.filename",
    "output.dataFormat",
    "output.writeCatASCII",
    "output.writeCatXML",
    "output.writeCatSQL",
    "output.writeDiagnosticPlot"
    "output.writeKarma",
    "output.writeNoise",
    "output.writeFiltered",
    "output.writeMask",
    "output.writeMask2d",
    "output.writeRawMask",
    "output.writeMoments",
    "output.writeCubelets",
    "output.writePV",
    "output.marginAperSpec",
    "output.marginCubeletsXY",
    "output.marginCubeletsZ",
    "output.thresholdMom12",
    "output.overwrite",

]


def strip_inline_comment(line):
    """
    Remove SoFiA-style inline comments from a parameter file line.
    """

    return line.split("#", 1)[0].strip()


def parse_parfile(file_path):
    config = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = strip_inline_comment(line)
            if not line:
                continue
            if '=' in line:
                key, value = map(str.strip, line.split('=', 1))
                config[key] = value
    return config


def compare_parfiles(file_path, temp_file_path):

    original = parse_parfile(file_path)
    modified = parse_parfile(temp_file_path)

    changes = {}
    for key, new_value in modified.items():
        old_value = original.get(key)
        if old_value != new_value:
            changes[key] = new_value

    return changes


def get_sofia_exit_message(exit_code):
    """
    Return the ESPADA-side message associated with a SoFiA exit code.
    """

    return SOFIA_EXIT_MESSAGES.get(exit_code, SOFIA_UNKNOWN_EXIT_MESSAGE)


def mask_float2int(file_path):

    file_path = Path(file_path)
    new_file_path = file_path.with_name(file_path.stem + '_int' + file_path.suffix)
    
    if new_file_path.exists():
        logger.info(f"Found cached mask integer file '{new_file_path}'")
        return new_file_path

    try:
        with fits.open(file_path) as hdul:
            data = hdul[0].data
            header = hdul[0].header

            if data.dtype.kind == 'f':
                int_data = np.round(data).astype(np.int16)
                header['BITPIX'] = 16
                new_hdu = fits.PrimaryHDU(data=int_data, header=header)
                new_hdu.writeto(new_file_path, overwrite=True)
                logger.info(
                    f"Integer-type version of the mask '{file_path}' has been created: "
                    f"{new_file_path}"
                )
                return new_file_path
            else:
                return file_path
            
    except Exception as e:
        logger.error(f"Mask conversion to integer failed. File: {file_path}. Error: {e}")
        return ""


def find_previous_qa_reports(input_data, adpalmap_config, pid, logger):
    """
    Build QA report entries from standard QA images generated in previous runs.
    """

    qa_reports = []
    input_stem = Path(input_data).stem
    qa_output_dir = (
        adpalmap_config.output_dir
        / f"espada_{input_stem}"
        / "quality_assesment_products"
    )

    if adpalmap_config.run_mode == "both":
        modes = ("absorption", "emission")
    else:
        modes = (adpalmap_config.run_mode,)

    logger.info(f"Looking for previous QA outputs for dataset '{input_stem}'")

    for mode in modes:
        qa_image_path = qa_output_dir / f"{mode}_{input_stem}_QA.png"

        if not qa_image_path.exists():
            logger.info(f"No previous QA image found for {mode}: {qa_image_path}")
            continue

        logger.info(f"Previous QA image found for {mode}: {qa_image_path}")
        qa_reports.append({
            "software_id": "QA",
            "PID": pid,
            "input_name": input_stem,
            "input_path": str(input_data),
            "mode": mode,
            "log_path": "",
            "outputs": {
                "images": [{
                    "type": "mom8",
                    "path": qa_image_path,
                    "description": "Previous QA image",
                    "software-id": "qa"
                }],
                "files": []
            },
            "cube_statistics": {},
            "mask_comparison": {}
        })

    return qa_reports


class SoPar(dict): 

    GROUP_DELETE_SUFFIXES = (
        "_mom1.fits",
        "_mom2.fits",
        "_spec.txt",
    )

    def __init__(self, **kwargs):
        """
        Reads the SoFia parameters file and creates a SoPar object.
        
        Parameters
        ----------
        config_path: str, default None
            Path to the configuration file. If None, it will used the default SoFia parameters file.

        Returns
        -------
        self

        Attributes
        ----------
        All the parameters include in the SoFia parameter file
        """

        super(SoPar, self).__init__(**kwargs)
        self.__dict__ = self
        
        self.configure(**kwargs)
        self.group = False

        
    def configure(self, sofia_file_path=None, **kwargs):


        if sofia_file_path is None:
            
            script_dir = Path(__file__).parent
            sofia_file_path = script_dir/'sofia_default.par'
            self.sofia_file_path = sofia_file_path

            if Path(sofia_file_path).exists():
                self.read_sofia_par_file(sofia_file_path)
                self.sofia_file_path = Path(sofia_file_path)

            else:
                error_msg = (
                    f"Download file {Path(sofia_file_path)} not found."
                    "No SoFiA parameter file was provided and the default parameter file "
                    f"{sofia_file_path} could not be found. Provide a valid SoFiA parameter "
                    "file or check if you have deleted or moved the default file."
                    )
                Logger.log_to_file(logging.ERROR, error_msg)
                raise FileNotFoundError(error_msg)
            
        else:
            sofia_file_path = Path(os.path.expanduser(sofia_file_path))
            self.sofia_file_path = sofia_file_path

            if not sofia_file_path.exists():
                error_msg = f"Parameter file '{sofia_file_path}' not found."
                Logger.log_to_file(logging.ERROR, error_msg)
                raise FileNotFoundError(error_msg)
            else:
                logger.info(f"The file in '{sofia_file_path}' have been loaded successfully")

            self.read_sofia_par_file(sofia_file_path)

    
    def read_sofia_par_file(self, sofia_file_path):
        """
        Reads a Sofia parameter file and dynamically sets attributes on the class instance.

        The file is expected to contain lines in the format `key=value`. Blank lines and lines
        starting with `#` are ignored. The keys are sanitized by replacing dots (`.`) with
        underscores (`_`). Values are automatically converted to integers or floats if possible;
        otherwise, they remain as strings.

        Parameters:
        ----------
        sofia_file_path (str): Path to the Sofia parameter file.
        
        Returns:
        ----------
        """


        with open(sofia_file_path, 'r') as file:
                for raw_line in file:
                    
                    # Remove comments and surrounding whitespace before parsing.
                    line = strip_inline_comment(raw_line)
                    if not line:
                        continue
                    
                    try:
                        k, v = line.split("=", 1)
                        k = k.strip().replace(".", "_")
                        k = k.strip()
                        v = v.strip()
                        
                        # Convert v, if possible, to int or float, otherwise it remains as string.
                        if v.isdigit():
                            v = int(v)
                        else:
                            try:
                                v = float(v)
                            except ValueError:
                                pass
         
                        # Set attributes to the class dinamically
                        setattr(self, k, v)
                        
                    except: #CHANGE. Check is ValueError cover all the posibilities.
                        error_msg = (
                            f"The line '{line}' has not a valid format "
                                     "(module.parameter = value)."
                        )
                        Logger.log_to_file(logging.ERROR, error_msg)
                        raise ValueError(error_msg)


    def update_input_parameters(
            self, sop_par, 
            input_data, primary_beam=None, mask=None,
            run=-1,
        ):
        """
        Updates the attributes of the SoPar object with the values provided in sop_params and
        manage some key parameters


        Parameters:
        ----------
        sop_par (dict): Dictionary with parameters provided via -sop.

        Returns:
        ----------
        None: Updates the attributes of the SoPar object directly.
        """
        
        logger.info(
            f"Reading parameters from {self.sofia_file_path} and via -sop. Mode: {self.mode}."
        )
        
        ##############################################################################################
        if sop_par is not None:

            for key, value in sop_par.items():
                normalized_key = key.replace('.', '_')

                if key in {
                    "input.data",
                    "input.primaryBeam",
                    "input.mask",
                    "input.invert",
                    "pipeline.threads",
                    "output.directory", 
                }: continue

                # Actualizar o añadir parámetros
                if hasattr(self, normalized_key):
                    setattr(self, normalized_key, value)
                else:
                    # Añadir como nuevo atributo si no existe
                    setattr(self, normalized_key, value)
                    logger.warning(f"Added new parameter '{key}' with value '{value}'.")
        ##############################################################################################
        
        ###########################-------------input.data--------------##############################
        # The parameter 'input.data' is managed in the main function.
        if (sop_par is not None 
                    and 'input.data' in sop_par 
                    and sop_par['input.data'] is not None):
                logger.warning(
                    f"Ignoring value '{sop_par['input.data']}' for the 'input_data' parameter "
                    "provided vía '-sop' comand. This must be set in the "
                    "'input_dataset' or 'input_file' parameters in the "
                    f"{self.adpalmap_config.config_path} file"
                )
        if hasattr(self, 'input_data') and getattr(self, 'input_data') is not None:
            logger.warning(
                f"Ignoring value '{self.input_data}' for the 'input.data' parameter provided "
                f"in the parameter file {self.sofia_file_path}.  This must be set in the "
                f"'input_dataset' or 'input_file' parameters in the {self.adpalmap_config.config_path}"
                " file"
            )
                
        self.input_data = input_data
        ##############################################################################################

        #######################-------------input.primaryBeam--------------###########################
             
        if (sop_par is not None 
                and 'input.primaryBeam' in sop_par 
                and sop_par['input.primaryBeam'] is not None):
            logger.warning(
                f"Ignoring value '{sop_par['input.primaryBeam']}' for the 'input.primaryBeam' "
                "parameter provided vía '-sop' comand. This must be set in the 'input_dataset'"
                f" or 'input_file' parameters in the {self.adpalmap_config.config_path} file"
            )
        if(hasattr(self, "input_primaryBeam") and  self.input_primaryBeam):
            logger.warning(
                f"Ignoring value '{self.input_primaryBeam}' for the 'input.primaryBeam' parameter"
                f" provided in {self.sofia_file_path}. This must be set in the 'input_dataset'"
                f" or 'input_file' parameters in the {self.adpalmap_config.config_path} file"
            )
            
        # If exist it will always be used
        if primary_beam: 
            logger.info(f"The primary beam '{primary_beam}' set as 'input.primaryBeam'.")
            self.input_primaryBeam = primary_beam
        else:
            # It should be "" at this point. No changes need it
            pass
        ##############################################################################################

        ###########################-------------input.mask--------------##############################     
        if (sop_par is not None 
                and 'input.mask' in sop_par 
                and sop_par['input.mask'] is not None):
            logger.warning(
                f"Ignoring value '{sop_par['input.mask']}' for the 'input.mask' parameter provided "
                "vía '-sop' comand. This must be set in the 'input_dataset'"
                f" or 'input_file' parameters in the {self.adpalmap_config.config_path} file"
            )
        if(hasattr(self, "input_mask") and self.input_mask):
            logger.warning(
                f"Ignoring value '{self.input_mask}' for the 'input.mask' parameter provided "
                f"in the parameter file {self.sofia_file_path}. This must be set in the "
                "'input_dataset' or 'input_file' parameters in the "
                f"{self.adpalmap_config.config_path} file"
            )
        
        if mask:
            #Comprueba si la máscara es descargada o no. Si no compruebo que sea tipo int()
            if self.adpalmap_config.enable_tap_service:
                if self.adpalmap_config.use_mask:
                    logger.info(f"The mask '{mask}' set as 'input.mask'.")
                    self.input_mask = mask
                else:
                    logger.warning(
                        f"'use_mask' set to False: the mask '{mask}' will no be used as 'input.mask'"
                        )
                    self.input_mask = ""
            else:
                if self.adpalmap_config.use_mask:
                    self.input_mask = mask_float2int(mask)
                else:
                    logger.warning(
                        f"'use_mask' set to False: the mask '{mask}' will no be used as 'input.mask'"
                        )
                    self.input_mask = ""                    
        else:
            pass

        ##############################################################################################

        ##########################-------------input.invert--------------#############################
        if hasattr(self, "input_invert"):
            logger.warning(
                f"Ignoring value '{self.input_invert}' for the 'input.invert' parameter provided "
                f"in the parameter file {self.sofia_file_path}. This must be set through the "
                f"'run_mode' parameter in the {self.adpalmap_config.config_path} file"
            )

        if sop_par is not None and "input.invert" in sop_par:
            input_invert_value = sop_par["input.invert"]
        else:
            input_invert_value = getattr(self, "input_invert", None)

        
        if self.adpalmap_config.run_mode == 'emission':
            if input_invert_value == 'true':
                logger.warning("Parameter 'input.invert=true' is not allowed in 'emission' mode. "
                            "Setting 'input.invert' to 'false'.")
                self.input_invert = 'false'
            else:
                self.input_invert = 'false'   

        elif self.adpalmap_config.run_mode == 'absorption':
            if input_invert_value == 'false':
                logger.warning("Parameter 'input.invert=false' is not allowed in 'absorption' mode. "
                            "Setting 'input.invert' to 'true'.")
                self.input_invert = 'true'
            else:
                self.input_invert = 'true'
          
        elif self.adpalmap_config.run_mode == 'both' and run != 0:
            if input_invert_value == 'false':
                logger.warning("Parameter 'input.invert=false' is not allowed in 'both' mode for "
                            "the first run. Setting 'input.invert' to 'true'.")
                self.input_invert = 'true'
            else:
                self.input_invert = 'true'
                
        elif self.adpalmap_config.run_mode == 'both' and run == 0:
            if input_invert_value == 'true':
                logger.warning("Parameter 'input.invert=true' is not allowed in 'both' mode for "
                            "the second run. Setting 'input.invert' to 'false'.")
                self.input_invert = 'false'
            else:
                self.input_invert = 'false'
                
        else:
            logger.critical("Oops, you should not have come here. Please open an"
                            " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with "
                            "your specific case.")
        
        ##############################################################################################        
        
        #########################-------------scfind.enable--------------#############################
        #########################------------contsub.enable--------------#############################
        #########################-----------scaleNoise.enable------------#############################
        #########################----------rippleFilter.enable-----------#############################
        #########################-----------threshold.enable-------------#############################
        #########################----------reliability.enable------------#############################
        #########################------------dilation.enable-------------#############################

        if (mask and self.adpalmap_config.use_mask):
            logger.info("The 'scfind.enable' parameter has set to 'false'. If a mask file is "
                        " available and 'use_mask' parameter is set to True, it assumes that no further "
                        "sources need to be searched or discarded.")
            logger.info("The 'reliability.enable' parameter has set to 'false'. If a mask file is "
                        "available and 'use_mask' parameter is set to True, it assumes that no further "
                        "sources need to be searched or discarded.")
            logger.info("The 'contsub.enable' parameter has set to 'false' because there is a mask" 
            "available and 'use_mask' parameter is set to True")
            logger.info("The 'scaleNoise.enable' parameter has set to 'false' because there is a mask" 
            "available and 'use_mask' parameter is set to True")
            logger.info("The 'rippleFilter.enable' parameter has set to 'false' because there is a mask" 
            "available and 'use_mask' parameter is set to True")
            logger.info("The 'threshold.enable' parameter has set to 'false' because there is a mask" 
            "available and 'use_mask' parameter is set to True")
            logger.info("The 'dilation.enable' parameter has set to 'false' because there is a mask" 
            "available and 'use_mask' parameter is set to True")
            logger.warning("Carefully review the parameters set in the linker section")
            
            self.scfind_enable = 'false'
            self.reliability_enable = 'false'
            self.contsub_enable = 'false'
            self.scaleNoise_enable = 'false'
            self.rippleFilter_enable = 'false'
            self.threshold_enable = 'false'
            self.dilation_enable = 'false'
            
            if (sop_par and 'scfind.enable' in sop_par):
                logger.warning(
                    f"Ignoring value '{sop_par['scfind.enable']}' for the 'scfind.enable' "
                    "parameter provided in vía '-sop' comand."
                )
            if (sop_par and 'reliability.enable' in sop_par):
                logger.warning(
                    f"Ignoring value '{sop_par['reliability.enable']}' for the 'reliability.enable' "
                    "parameter provided in vía '-sop' comand."
                )
            if (sop_par and 'contsub.enable' in sop_par):
                logger.warning(
                    f"Ignoring value '{sop_par['contsub.enable']}' for the 'scfind.enable' "
                    "parameter provided in vía '-sop' comand."
                )
            if (sop_par and 'scaleNoise.enable' in sop_par):
                logger.warning(
                    f"Ignoring value '{sop_par['scaleNoise.enable']}' for the 'scaleNoise.enable' "
                    "parameter provided in vía '-sop' comand."
                )
            if (sop_par and 'rippleFilter.enable' in sop_par):
                logger.warning(
                    f"Ignoring value '{sop_par['rippleFilter.enable']}' for the 'rippleFilter.enable' "
                    "parameter provided in vía '-sop' comand."
                )
            if (sop_par and 'threshold.enable' in sop_par):
                logger.warning(
                    f"Ignoring value '{sop_par['threshold.enable']}' for the 'threshold.enable' "
                    "parameter provided in vía '-sop' comand."
                )
            if (sop_par and 'dilation.enable' in sop_par):
                logger.warning(
                    f"Ignoring value '{sop_par['dilation.enable']}' for the 'dilation.enable' "
                    "parameter provided in vía '-sop' comand."
                )
            
            
        ##############################################################################################

        ########################-------------pipeline.threads--------------###########################
        if (sop_par and "pipeline.threads" in sop_par) or hasattr(self, "pipeline_threads"):
            logger.warning(
                "The parameter 'self.pipeline_threads' indicated via -sop or in the "
                f" {self.sofia_file_path} will be ignored. This pipeline manages the threads "
                "used based on the 'num_cores' parameter, the number of datasets, and their size. "
                "Based on this, the optimal thread usage is estimated according to the number of "
                "available cores and RAM."
            )
        
        self.pipeline_threads = self.sofia_threads
        ##############################################################################################

        ########################-------------output.directory--------------########################### 
            
        if sop_par and "output.directory" in sop_par: 
            logger.warning(
                    f"Ignoring value '{sop_par['output.directory']}' for the 'input_data' parameter "
                    "provided vía '-sop' comand. This must be set in the "
                    f"'output.directory' parameter in the {self.adpalmap_config.config_path} file"
            )
        if hasattr(self, "output_directory") and self.output_directory:  
            logger.warning(
                f"Ignoring value '{self.output_directory}' for the 'output.directory' parameter" 
                f" provided in the parameter file {self.sofia_file_path}.  This must be set in " 
                f"the 'output_directory' parameter in the {self.adpalmap_config.config_path}"
                " file"
            )

        self.output_directory = self.adpalmap_config.output_dir / f"espada_{input_data.stem}"
        ##############################################################################################

        ########################--------------output.filename--------------###########################       
        if self.adpalmap_config.run_mode == 'absorption':
            if hasattr(self, "output_filename") and self.output_filename:
                self.output_filename = f"absorption_{self.output_filename}"
                sopar_log_path = f"{self.output_filename}_logfile.log"
            else:
                self.output_filename = f"absorption_{self.input_data.stem}"
                sopar_log_path = f"absorption_{self.input_data.stem}_logfile.log"

        elif self.adpalmap_config.run_mode == 'emission':
            if hasattr(self, "output_filename") and self.output_filename:
                self.output_filename = f"emission_{self.output_filename}"
                sopar_log_path = f"{self.output_filename}_logfile.log"
            else:
                self.output_filename = f"emission_{self.input_data.stem}"
                sopar_log_path = f"emission_{self.input_data.stem}_logfile.log"  

        elif self.adpalmap_config.run_mode == 'both' and run!=0:
            if hasattr(self, "output_filename") and self.output_filename:
                self.output_filename = f"absorption_{self.output_filename}"
                sopar_log_path = f"{self.output_filename}_logfile.log"
            else:
                self.output_filename = f"absorption_{self.input_data.stem}"
                sopar_log_path = f"absorption_{self.input_data.stem}_logfile.log"

        elif self.adpalmap_config.run_mode == 'both' and run==0:
            if hasattr(self, "output_filename") and self.output_filename:
                # Safe the original 'output.filename' for 'flag.cube'
                self.original_output_filename = self.output_filename
                self.output_filename = f"emission_{self.output_filename}"
                sopar_log_path = f"{self.output_filename}_logfile.log"
            else:
                self.original_output_filename = self.input_data.stem
                self.output_filename = f"emission_{self.input_data.stem}"
                sopar_log_path = f"emission_{self.input_data.stem}_logfile.log" 

        # Safe the logfile and make sure that is Path() object
        self.sopar_logfile = self.output_directory / sopar_log_path
        ##############################################################################################

        ########################--------------output.writeCAT---------------##########################
        if self.output_writeCatXML=='false':
            logger.warning(
                f"Ignoring value '{self.output_writeCatXML}' for the 'output.writeCatXML' parameter. "
                "This must be set to 'true' always."
            )
            
            self.output_writeCatXML = 'true'

        else:
            pass
        ##############################################################################################

        ########################------------output.writeCubelets------------##########################
        if self.output_writeCubelets=='false':
            logger.warning(
                f"Ignoring value '{self.output_writeCubelets}' for the 'output.writeCubelets' "
                "parameter. This must be set to 'true' always."
            )
            
            self.output_writeCubelets = 'true'

        else:
            pass


        logger.info(f"Parameters updated. Mode: {self.mode}.")


    def update_group_parameters(self, group_mask, input_region_from_mask=None):

        """
        Updates the attributes of the SoPar object to being able to Run SoFiA for Groups.

        Parameters:
        ----------
        group_mask (Path): Grouped source mask to be used as input.mask.
        input_region_from_mask (tuple, optional): input.region recovered from the
            previous SoFiA mask used for grouping.

        Returns:
        ----------
        None: Updates the attributes of the SoPar object directly.
        """

        logger.info(f"Updating SoFiA parameters for source grouping. Mode: {self.mode}.")
        
        self.input_mask = group_mask

        if not self.adpalmap_config.enable_sofia:
            current_region = parse_input_region(
                getattr(self, "input_region", None), 
                logger=logger
            )
            mask_region = parse_input_region(input_region_from_mask, logger=logger)

            if mask_region is not None:
                if current_region is not None and current_region != mask_region:
                    logger.warning(
                        (
                            "enable_sofia=False: previous SoFiA mask was generated "
                            f"with input.region {format_input_region(mask_region)}, "
                            "but the current SoFiA parameter file contains "
                            f"input.region {format_input_region(current_region)}. "
                            "Using the previous mask region for the grouped SoFiA run. "
                            "Rerun SoFiA to apply the new input.region."
                        )
                    )
                else:
                    logger.info(
                        (
                            "enable_sofia=False: using input.region from previous "
                            f"SoFiA mask for grouped SoFiA run: "
                            f"{format_input_region(mask_region)}"
                        )
                    )

                # This function turn mask_region in the valid format for SoFiA
                self.input_region = serialize_input_region(mask_region)

            elif current_region is not None:
                logger.warning(
                    (
                        "enable_sofia=False: previous SoFiA mask has no input.region "
                        "in its header. Ignoring the current SoFiA parameter file "
                        f"input.region {format_input_region(current_region)} for the "
                        "grouped SoFiA run. Rerun SoFiA to apply this input.region."
                    )
                )
                self.input_region = ""

        if self.mode == "absorption":
            self.input_invert = "true"
        elif self.mode == "emission":
            self.input_invert = "false"

        self.scfind_enable = "false"

        self.linker_enable = "false" 

        self.reliability_enable = "false"

        self.output_filename = f"group_{self.output_filename}"
        
        # '{self.output_filename}' Already contain prefixx 'group_'
        self.sopar_logfile = self.output_directory / f"{self.output_filename}_logfile.log"

        logger.info(f"Parameters ready for source grouping. Mode: {self.mode}.")


    def auto_setup(self):
        """
        Automatically configures attributes based on the FITS file header information.

        This method reads the FITS file specified in `self.input_data` and updates class attributes
        based on the header values. It calculates and sets parameters such as `scfind_kernelsXY`,
        `linker_minSizeXY`, and `reliability_minSNR` using specific rules derived from the header.

        
        Raises:
        ----------
        SystemExit: If `self.input_data` is not defined, is empty, or the FITS file does not exist.
        """

        logger.info(f"Auto-setup start. Mode: {self.mode}")

        if not hasattr(self, "input_data") or not self.input_data:
            logger.critical(
                "Attribute 'input_data' is not defined or is None. Fatal error. Please open an"
                " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
                "case."
            )
            raise

        fits_path = Path(self.input_data)


        if not fits_path.exists():
            logger.critical(
                f"File FITS '{fits_path}' does not exist. Fatal error. Please open an"
                " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
                "case.")
            raise

        with fits.open(fits_path) as hdul:
            header = hdul[0].header

        
        # Update attributes based on header and defined operations
        if "BMAJ" in header and "BMIN" in header and "CDELT1" in header:
            bmaj = header["BMAJ"]
            bmin = header["BMIN"]
            cdelt1 = abs(header["CDELT1"])

            # Calculate values ​​for scfind.kernelsXY and linker.minSizeXY
            x = (bmaj + bmin) / (2 * cdelt1)
            self.scfind_kernelsXY = f"0, {x:.0f}, {2*x:.0f}"  # Format "0, x, 2x"
            self.linker_minSizeXY = round(x)  
            logger.info(
                "The 'self.scfind_kernelsXY' parameter has been update to: "
                f"{self.scfind_kernelsXY}"
            )
            logger.info(
                "The 'self.linker_minSizeXY' parameter has been update to: "
                f"{self.linker_minSizeXY}"
            )

        # filter.minSNR
        if "BMAJ" in header and "BMIN" in header:
            self.filter_minSNR = 3.0 
            logger.info(
                "The 'self.filter_minSNR' parameter has been update to: "
                f"{self.filter_minSNR}"
            ) 

        else:            
            a = 3
            b = 3
            x = (3 / 2) * np.sqrt((np.pi * a * b) / np.log(2))
            self.filter_minSNR = x
            logger.info(
                "The 'self.filter_minSNR' parameter has been update to: "
                f"{self.filter_minSNR}"
            )
                

        # Otros parámetros pueden ser añadidos según las reglas específicas...
        logger.info(f"Auto-setup done. Mode: {self.mode}")


    def run_sofia(self, run=-1):        
        """
        Runs the SoFia tool in different modes (absorption, emission, or both) based on 
        the provided configuration.

        This method executes SoFia with the specified mode and handles the creation of 
        output directories, logging, and error handling. It also manages temporary files and 
        ensures proper cleanup.

        Parameters:
        ----------
        mode (str, optional): Mode to run SoFia in. Can be 'absorption', 'emission', or 'both'.
                              Defaults to None.
        run (int, optional): Indicates the run iteration when mode is 'both'. Used to handle 
                             sequential runs. -1 for single runs, 0 for the second run in 'both' 
                             mode. Defaults to -1.

        Raises:
        ----------
        SystemExit: If SoFia encounters an error during execution.
        """
    
        os.makedirs(self.output_directory, exist_ok=True)
        self.output_directory = Path(self.output_directory)
    ##############################################################################################
        # Set source from absorption run as a 'flag_cube' in the emission run in the 'both' mode
        if self.adpalmap_config.run_mode == "both" and run ==0:

            if self.adpalmap_config.abs_flag_cube:                    
                flag_cube = self.output_directory / f"absorption_{self.original_output_filename}_mask.fits"

                if flag_cube.exists():
                    self.flag_cube = flag_cube
                    logger.info("The mask obtained from the absorption run will be used as"
                                " input for the 'flag.cube' parameter")
                else:
                    logger.warning("There is no mask available from the absorption run. "
                                    "The parameter 'flag_cube' will not be used")
            else:
                logger.info("The mask from the absorption run will not be used as "
                            "a 'flag_cube'. "
                            f"Mode: {self.mode}.")
    ##############################################################################################

        # Create a SoFiA-2 report 
        sopar_report = {
                "software_id" :'SoFiA-2',
                "PID": self.pid,
                "input_name": self.input_data.stem,
                "input_path": str(self.input_data),
                "mode": self.mode,  
                "log_path": self.sopar_logfile,
                "sofia_parfile" : self.sofia_file_path,
                "command": [],
                "exit_code": 0,
                "sofia_exit_message": "",
                "sofia_subprocess_error": "",
                "outputs" : {'images' : [], 'files': []}
            }
            
        # Create a temp file with the updated parameters for SoFiA
        temp_file_path = self.create_tempfile()

        # Update the report 
        sopar_report.update(
            {'sofia_par_changes' : compare_parfiles(self.sofia_file_path, temp_file_path)}
        )

        # Remove existing log file
        if  sopar_report["log_path"].exists():
            try:
                sopar_report["log_path"].unlink()
            except:
                logger.warning(
                    "Error trying to delete existing log file. The new log "
                    "entries will be appended to it."
                )

        error = ''

    ##############################################################################################
    
        try:
            # Safe in the log the parameters fotr the run 
            self.log_parameters()
            #Logger.raw("================================")
            logger.info(
                f"SoFia start. Mode: {self.mode}. Input data: "
                f"{Path(self.input_data).stem}"
            )
            Logger.raw(
                f"[{self.pid}]ESPADA_EVENT external_log "
                + json.dumps(
                    {
                        "software_id": "SoFiA-2",
                        "mode": self.mode,
                        "input_name": self.input_data.stem,
                        "input_path": str(self.input_data),
                        "log_path": str(self.sopar_logfile),
                        "is_group": str(self.output_filename).startswith("group_"),
                    },
                    sort_keys=True,
                )
            )
            #Logger.raw("================================")

            # Execute SoFiA-2 
            cmd = ["sofia", f"{temp_file_path}"]
            sopar_report.update({"command": cmd})
            subprocess.run(
                cmd,
                text=True,
                check=True,
                capture_output=not self.adpalmap_config.verbose
            )
            #Logger.raw("================================")
            logger.info(f"SoFia finished. Mode: {self.mode}")
            #Logger.raw("================================")

            # Safe the 3D-mask for the group module
            if self.adpalmap_config.enable_group:
                self.mask3d = (
                    self.output_directory 
                    / f"{self.mode}_{self.input_data.stem}_mask.fits"
                )

        except subprocess.CalledProcessError as e:
            if self.adpalmap_config.enable_group:
                # If this attribute change from None to any other, find_mask_sofia() in group.py
                # have to be changed as well
                self.mask3d = None
            sofia_exit_code = e.returncode
            sofia_exit_message = get_sofia_exit_message(sofia_exit_code)
            error = (
                f"SoFiA failed with exit code {sofia_exit_code}: "
                f"{sofia_exit_message} Mode: {self.mode}. "
                f"Input data: {self.input_data}."
            )
            sopar_report.update({
                "exit_code": sofia_exit_code,
                "sofia_exit_message": sofia_exit_message,
                "sofia_subprocess_error": str(e),
            })
            logger.error(error)
            logger.info(f"SoFia execution aborted")
            
            if self.adpalmap_config.run_mode == 'both' and run!=0:
                # Exits the function without propagating an error to run in 'absorption'
                logger.info(f"SoFiA will try to run again in mode: emission.")
        
        except Exception as e:
            logger.error(f"{e}")

        finally:
            # This step should be here if we want to add outputs from SoFiA-2 no matter if it fails or
            # not. The reliability and diagnostic plot should always be in the report.  
            # Add outputs for the html report
            if self.adpalmap_config.make_report:
                try:
                    self.report_outputs(sopar_report)  
                except Exception as e:
                    logger.warning(f"Error adding outputs for the html report (non-critical): {e}")

            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            sopar_report.update({"error": error})
            return sopar_report
        
        ##############################################################################################
                

    def create_tempfile(self):
        """
        Create a temporary file containing key-value pairs of the object's attributes.

        This method generates a temporary file in the same directory as the object's 
        `path` attribute (or the current directory if `path` is not defined). The file 
        will include all parameters defined in SOFIA_PARAMETER and the values of the 
        corresponding attribute in self.

        Returns:
        ----------
        str: The path to the created temporary file as a string.
        """

        original_path = Path.cwd()     
        temp_file_name = (
            self.sofia_file_path.stem + "_tmp_PID" + str(self.pid) + self.sofia_file_path.suffix
        )
        temp_file_path = original_path / temp_file_name


        with open(temp_file_path, 'w') as tf:
            for key, value in self.__dict__.items():

                key_transformed = key.replace("_", ".")
                if key_transformed in SOFIA_PARAMETER:
                    tf.write(f"{key_transformed}={value}\n")

        logger.info(
            "Creating temporary SoFiA parameter file based on the parameter file "
            f"{self.sofia_file_path}."
            )
        return str(temp_file_path)
                

    def log_parameters(self):
        """
        Log the object's parameters, excluding specific attributes.

        This method logs all key-value pairs of the object's attributes, except for 
        those explicitly excluded (`sofia_file_path`, `path`, and `base_output_directory`). 
        Attribute names are transformed by replacing underscores with dots before logging. 
        The parameters are logged using the `Logger.raw_file` method.

        Returns:
        ----------
            None
        """

        logger.info("Parameters set for the run: \n")

        for par in SOFIA_PARAMETER:
            par_underscore = par.replace(".", "_") 
            
            if hasattr(self, par_underscore):
                Logger.raw(f"[{self.pid}]{par}={getattr(self, par_underscore)}")
            else:
                Logger.raw(f"[{self.pid}]{par}= ")


    def report_outputs(self, sopar_report):
        
        mode = sopar_report["mode"]

        sopar_report['outputs']['images'].append({
            "type": "diag",
            "path": self.output_directory / f"{mode}_{self.input_data.stem }_diagnostic.eps",
            "description": "Diagnostic Plot",
            "software-id": "sofia"
        })
        sopar_report['outputs']['images'].append({
            "type": "rel",
            "path": self.output_directory / f"{mode}_{self.input_data.stem }_rel.eps",
            "description": "Realibiliy Plot",
            "software-id": "sofia"
        })
        sopar_report['outputs']['images'].append({
            "type": "skellman",
            "path": self.output_directory / f"{mode}_{self.input_data.stem}_skellam.eps",
            "description": "Skellam Plot",
            "software-id": "sofia"
        })
        sopar_report['outputs']['files'].append({
            "type": "par_file",
            "path": self.sofia_file_path,
            "format": ".par",
            "software-id": "sofia"
        })    
        sopar_report['outputs']['files'].append({
            "type": "catalog_txt",
            "path": self.output_directory / f"{mode}_{self.input_data.stem}_cat.txt",
            "format": "txt",
            "software-id": "sofia"
        })
        sopar_report['outputs']['files'].append({
            "type": "catalog_xml",
            "path": self.output_directory / f"{mode}_{self.input_data.stem}_xlm.txt",
            "format": "xlm",
            "software-id": "sofia"
        })


    def cleanup_group_outputs(self):
        """
        Remove Group-only SoFiA products that should not be kept after execution.
        """

        output_filename = str(getattr(self, "output_filename", ""))
        output_dir = getattr(self, "output_directory", None)

        if not output_filename.startswith("group_") or output_dir is None:
            logger.debug("Skipping SoFiA Group cleanup for non-group output.")
            return

        output_dir = Path(output_dir)
        for suffix in self.GROUP_DELETE_SUFFIXES:
            self._remove_group_output(output_dir / f"{output_filename}{suffix}")

        cubelets_dir = output_dir / f"{output_filename}_cubelets"
        self._cleanup_group_cubelet_outputs(cubelets_dir, output_filename)


    def _cleanup_group_cubelet_outputs(self, cubelets_dir, output_filename):
        if not cubelets_dir.is_dir():
            logger.debug(f"No SoFiA Group cubelets directory found for cleanup: {cubelets_dir}")
            return

        output_prefix = f"{output_filename}_"
        for candidate in cubelets_dir.iterdir():
            if not candidate.is_file():
                continue
            if not candidate.name.startswith(output_prefix):
                continue
            if any(candidate.name.endswith(suffix) for suffix in self.GROUP_DELETE_SUFFIXES):
                self._remove_group_output(candidate)


    def _remove_group_output(self, path):
        path = Path(path)

        if not path.exists():
            logger.debug(f"Group cleanup target not present: {path}")
            return

        if not path.is_file():
            logger.warning(f"Skipping Group cleanup target because it is not a file: {path}")
            return

        try:
            path.unlink()
            logger.info(f"Removed unwanted SoFiA Group output file: {path}")
        except Exception as e:
            logger.warning(f"Could not remove SoFiA Group output '{path}': {e}")


    def quality_assesment(self, provided_mask_file=None):
        """
        Perform a quality assessment by visualizing and comparing masks and moment images.

        This method evaluates the quality of the data by generating visualizations of:
        - The moment 8 image.
        - The Sofia 2D mask (if available).
        - The mask (if provided via `adpalmap_datap` or by the user).
        """

        logger.info(f"Quality assesment start. Mode: {self.mode}.")

        # At the moment there is just one singles images but do it in this way allows add
        # additional images easly in the future
        qa_report = {
                "software_id" :'QA',
                "PID": self.pid,
                "input_name": self.input_data.stem,
                "input_path": str(self.input_data),
                "mode": self.mode,  
                "log_path": "",
                "outputs" : {'images' : [], 'files': []},
                "cube_statistics": {}
            }
        
        ##############################################################################################
        # Extract cube statistics from XML
        xml_catalog_path = self.output_directory / f"{self.mode}_{self.input_data.stem}_cat.xml"
        if xml_catalog_path.exists():
            try:
                from astropy.io.votable import parse
                votable = parse(xml_catalog_path)
                resource = votable.resources[0]
                
                # Extract noise parameters
                for param in resource.params:
                    if param.name in ['NoiseMean','NoiseStd', 'NoiseSkew','NoiseKurt']:
                        qa_report['cube_statistics'][param.name] = param.value
                
                # Count sources
                table = votable.get_first_table()
                if table is not None and table.array is not None:
                    qa_report['cube_statistics']['n_sources'] = len(table.array)
                else:
                    qa_report['cube_statistics']['n_sources'] = 0
                    
                logger.info(f"Extracted cube statistics from XML: {qa_report['cube_statistics']}")
            except Exception as e:
                logger.warning(f"Could not extract cube statistics from XML: {e}")
        else:
            logger.warning(f"XML catalog not found: {xml_catalog_path}")
        
        ##############################################################################################

        #  Generate moment 8 image of input data
        try:
            mom8_ima = self.moment8_ima(self.mode)
        except Exception as e:
            logger.error(f"Failed to generate moment 8 image: {e}")
            logger.info("Quality assesment ended.")
            return qa_report
        
        # Check for SoFiA 2D mask
        sofia_output_dir = Path(self.output_directory)
        input_file_name = Path(self.input_data).stem

        file_2d_mask = (
            sofia_output_dir / f"{self.mode}_{input_file_name}_mask-2d.fits"
        )
        if not file_2d_mask.exists():
            logger.warning(
                f"2D-Mask file from SoFia not found in {self.output_directory}."            
            )
            logger.info("Quality assesment ended.")
            return qa_report       

        try:
            with fits.open(file_2d_mask) as hdul:
                sofia_2d_mask = hdul[0].data
                # Basic squeeze for 4D cases if needed
                if sofia_2d_mask.ndim == 4 and sofia_2d_mask.shape[0] == 1:
                    sofia_2d_mask = np.squeeze(sofia_2d_mask, axis=0)
        except Exception as e:
            logger.error(f"Failed to load SoFiA 2D mask: {e}")
            logger.info("Quality assesment ended.")
            return qa_report


        # Mask provide by the user or from the ALMA archive
        provided_mask_proj = None
        if provided_mask_file:
            try:
                with fits.open(provided_mask_file) as hdul:
                    mask_3d = hdul[0].data
                    # Basic squeeze for 4D cases
                    if mask_3d.ndim == 4 and mask_3d.shape[0] == 1:
                        mask_3d = np.squeeze(mask_3d, axis=0)
                    # Create 2D projection for visualization
                    if mask_3d.ndim >= 3:
                        provided_mask_proj = np.any(mask_3d > 0, axis=0).astype(int)
                    elif mask_3d.ndim == 2:
                        provided_mask_proj = mask_3d
            except Exception as e:
                logger.warning(
                    f"Failed to load provided mask '{provided_mask_file}' for visualization: {e}"
                )


        if provided_mask_proj is not None:
            fig, axs = plt.subplots(1, 3, figsize=(15, 6))
        else:
            fig, axs = plt.subplots(1, 2, figsize=(15, 6))
        
        try:
            ax = axs[0]
            if self.mode == "absorption":
                ax.set_title("Moment 8 Image (Absorption - Min Projection)")
            else:
                ax.set_title("Moment 8 Image (Emission - Max Projection)")
            ax.imshow(mom8_ima, cmap='viridis', origin='lower')
            ax.imshow(mom8_ima, cmap='viridis', origin='lower')
            #ax.colorbar(label="Intensity")

            ax = axs[1]
            ax.set_title("SoFiA mask projection")
            ax.imshow(sofia_2d_mask, cmap='viridis', origin='lower')
            #ax.colorbar(label="Intensity")

            if provided_mask_proj is not None:
                ax = axs[2]
                ax.set_title("Provided mask projection")
                ax.imshow(provided_mask_proj, cmap='viridis', origin='lower')

            qa_output_dir = Path(self.output_directory) / "quality_assesment_products"
            qa_output_dir.mkdir(parents=True, exist_ok=True)  
            qa_output_file = Path(f"{qa_output_dir / Path(self.output_filename)}_QA.png")

            plt.savefig(qa_output_file, bbox_inches='tight')
            logger.info(
                f"QA mask image saved in {qa_output_dir}. Mode: {self.mode}"
                )
            
            qa_report['outputs']['images'].append({
            "type": "mom8",
            "path": qa_output_file,
            "description": "Mask comparison image",
            "software-id": "qa"
            })
            
        except Exception as e:
            logger.warning(f"Failed to save QA mask image comparison: {e}")
            logger.info(f"Quality assement ended . Mode: {self.mode}")
            return qa_report
    ##############################################################################################

    ##############################################################################################        

        # 3D Mask for quantitative comparison 
        file_3d_mask = (
            sofia_output_dir / f"{self.mode}_{input_file_name}_mask.fits"
        )

        if not file_3d_mask.exists():
            logger.info("3D SoFiA mask not found - skipping quantitative comparison")
            logger.info(f"Quality assement ended . Mode: {self.mode}")
            return qa_report
        
        if not provided_mask_file:
            logger.info("Mask file not provided - skipping quantitative comparison")
            logger.info(f"Quality assement ended . Mode: {self.mode}")
            return qa_report
        
        # Load data cube
        try:
            with fits.open(self.input_data) as hdul:
                data_cube = hdul[0].data
                if data_cube.ndim == 4 and data_cube.shape[0] == 1:
                    data_cube = np.squeeze(data_cube, axis=0)
        except Exception as e:
            logger.warning(
                f"Cannot load input data cube {self.input_data} for quantitative comparison: {e}"
            )
            logger.info(f"Quality assement ended . Mode: {self.mode}")
            return qa_report
        
        # Load SoFiA 3D mask
        try:
            with fits.open(file_3d_mask) as hdul:
                sofia_mask_3d = hdul[0].data
                sofia_mask_3d_header = hdul[0].header
                if sofia_mask_3d.ndim == 4 and sofia_mask_3d.shape[0] == 1:
                    sofia_mask_3d = np.squeeze(sofia_mask_3d, axis=0)
        except Exception as e:
            logger.warning(
                f"Cannot load SoFiA 3D mask {file_3d_mask} for quantitative comparison: {e}"
            )
            logger.info(f"Quality assement ended . Mode: {self.mode}")
            return qa_report


        # Load provided mask by the user or from the ALMA archive
        try:
            with fits.open(provided_mask_file) as hdul:
                mask_3d = hdul[0].data
                if mask_3d.ndim == 4 and mask_3d.shape[0] == 1:
                    mask_3d = np.squeeze(mask_3d, axis=0)
        except Exception as e:
            logger.warning(
                f"Cannot load mask {provided_mask_file} for quantitative comparison: {e}"
            )
            logger.info(f"Quality assement ended . Mode: {self.mode}")
            return qa_report
        
        # Extract region from SoFiA mask
        region = extract_input_region_from_header(sofia_mask_3d_header, logger=logger)
       
        # Crop if it is necessary
        if region is not None:
            logger.info(f"Cropping provided mask to match SoFiA region")
            mask_3d = apply_input_region_crop(mask_3d, region, logger)
            # Rocorto data_cube para poder usarlo más adelante
            data_cube = apply_input_region_crop(data_cube, region, logger)
            logger.info(f"Cropped shapes - data: {data_cube.shape}, mask: {mask_3d.shape}")
        
        
        if data_cube.shape != sofia_mask_3d.shape:
            logger.warning(f"Shape mismatch: data {data_cube.shape} vs SoFiA mask {sofia_mask_3d.shape}")
            logger.info("Quality assessment aborted: shape mismatch")
            return qa_report
        
        if data_cube.shape != mask_3d.shape:
            logger.warning(f"Shape mismatch: data {data_cube.shape} vs provided mask {mask_3d.shape}")
            logger.info("Quality assessment aborted: shape mismatch")
            return qa_report

        logger.info("Starting quantitative mask comparison...")
    
        # Determine number of sources in SoFiA mask
        n_src = int(np.nanmax(sofia_mask_3d))
        if n_src < 1:
            logger.info("No sources found in SoFiA 3D mask - skipping per-source statistics")
            logger.info(f"Quality assement ended . Mode: {self.mode}")
            return qa_report
        
        logger.info(f"Found {n_src} sources in SoFiA mask.")
        
        # Global statistics
        npix_sofia_total = np.nansum(sofia_mask_3d > 0)
        npix_mask_total = np.nansum(mask_3d > 0)
        npix_overlap = np.nansum((sofia_mask_3d > 0) & (mask_3d > 0))
        pixel_frac_sofia = 100.0 * npix_overlap / npix_sofia_total if npix_sofia_total > 0 else 0.0
        pixel_frac_provided = 100.0 * npix_overlap / npix_mask_total if npix_mask_total > 0 else 0.0
        
        flux_sofia_total = np.nansum(data_cube[sofia_mask_3d > 0])
        flux_mask_total = np.nansum(data_cube[mask_3d > 0])
        flux_overlap = np.nansum(data_cube[(sofia_mask_3d > 0) & (mask_3d > 0)])
        flux_frac_sofia = 100.0 * flux_overlap / flux_sofia_total if flux_sofia_total != 0 else 0.0
        flux_frac_provided = 100.0 * flux_overlap / flux_mask_total if flux_mask_total != 0 else 0.0
        
        # Log global statistics
        logger.info("=== GLOBAL MASK COMPARISON ===")
        logger.info(f"SoFiA mask pixels: {npix_sofia_total}")
        logger.info(f"Provided mask pixels: {npix_mask_total}")
        logger.info(f"Overlap pixels: {npix_overlap}")
        logger.info(f"(SoFiA ∩ Provided mask) / SoFiA = {pixel_frac_sofia:.2f}% of SoFiA pixels")
        logger.info(
            f"(SoFiA ∩ Provided mask) / Provided mask = {pixel_frac_provided:.2f}% of Provided mask pixels"
        )
        logger.info(f"SoFiA total flux: {flux_sofia_total:.2f}")
        logger.info(f"Provided mask total flux: {flux_mask_total:.2f}")
        logger.info(f"(SoFiA ∩ Provided mask) / SoFiA = {flux_frac_sofia:.2f}% of SoFiA flux")
        logger.info(
            f"(SoFiA ∩ Provided mask) / Provided mask = {flux_frac_provided:.2f}% of Provided mask flux"
        )
        
        stats_lines = []
        stats_lines.append(f"QUALITY ASSESSMENT COMPARISON STATISTICS\n")
        stats_lines.append(f"========================================\n")
        stats_lines.append(f"Mode: {self.mode}\n")
        stats_lines.append(f"Input: {self.input_data.stem}\n\n")
        stats_lines.append(f"GLOBAL STATISTICS:\n")
        stats_lines.append(f"  SoFiA mask pixels: {npix_sofia_total}\n")
        stats_lines.append(f"  Provided mask pixels:  {npix_mask_total}\n")
        stats_lines.append(f"  Overlap pixels:    {npix_overlap}\n")
        stats_lines.append(
            f"  (SoFiA ∩ Provided mask) / SoFiA = {pixel_frac_sofia:.2f}% of SoFiA pixels\n"
        )
        stats_lines.append(
            f"  (SoFiA ∩ Provided mask) / Provided mask = {pixel_frac_provided:.2f}% of Provided mask pixels\n"
        )
        stats_lines.append(f"  SoFiA total flux: {flux_sofia_total:.2f}\n")
        stats_lines.append(f"  Provided mask total flux:  {flux_mask_total:.2f}\n")
        stats_lines.append(
            f"  (SoFiA ∩ Provided mask) / SoFiA = {flux_frac_sofia:.2f}% of SoFiA flux\n"
        )
        stats_lines.append(
            f"  (SoFiA ∩ Provided mask) / Provided mask = {flux_frac_provided:.2f}% of Provided mask flux\n\n"
        )
        """
        # Per-source statistics
        logger.info("=== PER-SOURCE COMPARISON ===")
        stats_lines.append(f"PER-SOURCE STATISTICS:\n")
        
        for src in range(1, n_src + 1):
            data_masked = data_cube[sofia_mask_3d == src]
            npix_sofia = np.nansum(sofia_mask_3d == src)
            npix_mask = np.nansum(mask_3d[sofia_mask_3d == src] > 0)
            flux_sofia = np.nansum(data_masked)
            flux_mask = np.nansum(data_masked[mask_3d[sofia_mask_3d == src] > 0])
            
            # Avoid division by zero
            pixel_pct = 100.0 * npix_mask / npix_sofia if npix_sofia > 0 else 0
            flux_pct = 100.0 * flux_mask / flux_sofia if flux_sofia != 0 else 0
            
            logger.info(
                f"Source {src}: N_SoFiA={npix_sofia:5d} N_PMask={npix_mask:5d} | "
                f"F_SoFiA={flux_sofia:8.2f} F_PMask={flux_mask:8.2f} | "
                f"PixelFrac={pixel_pct:5.2f}% FluxFrac={flux_pct:5.2f}%"
            )

            stats_lines.append(f"  Source {src}:\n")
            stats_lines.append(f"    N_SoFiA = {npix_sofia}\n")
            stats_lines.append(f"    N_Mask  = {npix_mask}\n")
            stats_lines.append(f"    F_SoFiA = {flux_sofia:.2f}\n")
            stats_lines.append(f"    F_Mask  = {flux_mask:.2f}\n")
            stats_lines.append(f"    Provided mask pixel fraction: {pixel_pct:.2f}%\n")
            stats_lines.append(f"    Provided mask flux fraction:  {flux_pct:.2f}%\n\n")"""
        
        # Add statistics to the report
        qa_report['mask_comparison'] = {
            'npix_sofia': int(npix_sofia_total),
            'npix_provided': int(npix_mask_total),
            'npix_overlap': int(npix_overlap),
            'pixel_overlap_fraction_sofia': round(100.0 * npix_overlap / npix_sofia_total, 2) if npix_sofia_total > 0 else 0.0,
            'pixel_overlap_fraction_provided': round(100.0 * npix_overlap / npix_mask_total, 2) if npix_mask_total > 0 else 0.0,
            'flux_sofia': round(flux_sofia_total, 2),
            'flux_provided': round(flux_mask_total, 2),
            'flux_overlap_fraction_sofia': round(100.0 * flux_overlap / flux_sofia_total, 2) if flux_sofia_total != 0 else 0.0,
            'flux_overlap_fraction_provided': round(100.0 * flux_overlap / flux_mask_total, 2) if flux_mask_total != 0 else 0.0
        }
        
        # Save statistics to file
        try:
            qa_output_dir = Path(self.output_directory) / "quality_assesment_products"
            stats_file = qa_output_dir / f"{Path(self.output_filename).stem}_comparison_stats.txt"
            
            with open(stats_file, 'w') as f:
                f.writelines(stats_lines)
            
            logger.info(f"Comparison statistics saved to {stats_file}")
            
            qa_report['outputs']['files'].append({
                "type": "qa_statistics",
                "path": stats_file,
                "format": "txt",
                "description": "Mask comparison statistics",
                "software-id": "qa"
            })
            
        except Exception as e:
            logger.warning(f"Failed to save statistics file: {e}")
        
        logger.info(f"Quality assesment completed successfully. Mode: {self.mode}")
        return qa_report


    def moment8_ima(self, mode):

        """
        Reads a FITS file containing a data cube and creates a 2D image by
        taking the maximum value along the z-axis for each (x, y).

        Parameters:
            input_fits (str): Path to the input FITS file containing the data cube.
            output_fits (str, optional): Path to save the output FITS file with the 2D image.
                                        If None, the output is not saved to a file.

        Returns:
            np.ndarray: 2D array with the maximum values along the z-axis.
        """
        if not hasattr(self, "input_data") or not self.input_data:
            logger.critical(
                "Attribute 'input_data' is not defined or is None. Fatal error. Please open an"
                " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
                "case."
            )
            raise

        fits_path = Path(self.input_data)

        if not fits_path.exists():
            logger.critical(
                f"File FITS '{fits_path}' does not exist. Fatal error. Please open an"
                " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
                "case.")
            raise

        with fits.open(fits_path) as hdul:
            data_cube = hdul[0].data

        if data_cube is None:
            error_msg = (
                f"The FITS file '{data_cube}' does not contain data in the primary HDU." 
                "Quality assement aborted."
            )
            logger.error(error_msg)
            raise RecoverableValueError(error_msg)

        if data_cube.ndim == 4:
            data_cube = np.squeeze(data_cube, axis=0)
        elif data_cube.ndim > 4:
            error_msg = (
                "ADP Alma pipeline is not designed to handle data files with more than 4 dimensions. "
                "Quality assesment ended. "
                "Please open an issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git" 
                "with your specific case.")
            logger.error(error_msg)
            raise RecoverableValueError(error_msg)

        # The relevant information about primary beam is on 'primary_beam'
        # the input_primaryBeam parameter is subject to changes
        if hasattr(self, "input_primaryBeam") and self.input_primaryBeam:

            pb_path = Path(self.input_primaryBeam)

            if not pb_path.exists():
                logger.critical(
                    f"File FITS '{pb_path}' does not exist. Fatal error. Please open an"
                    " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your" 
                    "specific case.")
                raise

            with fits.open(pb_path) as hdul:
                
                pb_cube = hdul[0].data

            if pb_cube is None:
                error_msg = (
                    f"The FITS file '{pb_cube}' does not contain data in the primary HDU." 
                    "Quality assement aborted."
                )
                logger.error(error_msg)
                raise RecoverableValueError(error_msg)
            
            if pb_cube.ndim == 4:
                pb_cube = np.squeeze(pb_cube, axis=0)
            elif pb_cube.ndim > 4:
                error_msg = (
                    "ADP Alma pipeline is not designed to handle data files with more than 4 dimensions. "
                    " Quality assesment aborted. "
                    "Please open an issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git" 
                    "with your specific case.")
                logger.error(error_msg)
                raise RecoverableValueError(error_msg)

            final_data_cube = data_cube * pb_cube
                    
        else:
            logger.warning(
                "No data cube has been specified with Primary Beam information."
            )
            
            final_data_cube = data_cube

        if mode == "absorption":
            logger.info(f"Creating moment 8 image for absorption (minimum along spectral-axis)")
            projection = np.min(final_data_cube, axis=0)
            projection_viz = -projection  
        else:  
            logger.info(f"Creating moment 8 image for emission (maximum along spectral-axis)")
            projection = np.max(final_data_cube, axis=0)
            projection_viz = projection

        return projection_viz
