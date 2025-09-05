from pathlib import Path
import yaml
import subprocess
import sys
import os
from traceback import format_exc
from adplib.exceptions import RecoverableError, RecoverableValueError, RecoverableFileNotFoundError
from astropy.io.votable import parse_single_table

from traceback import format_exc
# Logger:
import logging
from adplib.logger import Logger
logger = Logger.get_logger()

class CatalogResult:
    def __init__(self, catalog_path=None, error_msg=None):
        
        self.catalog_path = Path(catalog_path) if catalog_path is not None else None
        self.error_msg = error_msg
        self.success = self.catalog_path is not None
    
    def __bool__(self):
        return self.success


class SiPar(dict): 

    # Diccionario estático que mapea nombres de atributos a shortcuts
    ATTRIBUTE_SHORTCUTS = {
         "catalog_file": ["-c", "--catalog"],
         "source_id": ["-id", "--source-id"],
         "output_image_file_type": ["-x", "--suffix"],
         "spec_full_range": ["-o", "--original"],
         "syn_beam_dimensions": ["-b", "--beam"],
         "channel_width": ["-cw",  "--chan_width"],
         "min_size": ["-i", "--image-size"],
         "snr_range": ["-snr", "--snr-range"],
         "surveys_list": ["-s", "--surveys"],
         "combo": ["-m", "--imagemagick"],
         "user_image": ["-ui", "--user-image"],
         "percentile_range": ["-ur", "--user-range"],
         "spec_line": ["-line", "--spectral-line"]
    }


    def __init__(self, **kwargs):
        """
        Reads the SIP optional parameters|command file and creates a SiPar object.
        
        Parameters
        ----------
        sip_file_path: str, default None
            Path to the configuration file. 

        Returns
        -------
        self

        Attributes
        ----------
        All the optional parameters|command that could be enter into the terminal while running SIP 
        """

        super(SiPar, self).__init__(**kwargs)
        self.__dict__ = self 
        
        self.configure(**kwargs)
        
        #Check the parameter from the sip_args.yaml
        self.check_sip_args()

    
    def configure(self, sip_file_path=None, **kwargs):
        
        
        if sip_file_path is None:

            script_dir = Path(__file__).parent
            sip_file_path = script_dir / "sip_args.yaml"
            self.sip_file_path = sip_file_path

            if not sip_file_path.exists():
                error_msg = (
                    "No SIP configuration file was provided and the default configuration file "
                    f"{sip_file_path} could not be found. Provide a valid SIP configuration "
                    "file or check if you have deleted or moved the default file."
                )
                Logger.log_to_file(logging.ERROR, error_msg)
                raise FileNotFoundError(error_msg)
            else:
                logger.info(f"The file in {sip_file_path} have been loaded successfully")

        else:
            sip_file_path = Path(os.path.expanduser(sip_file_path))
            self.sip_file_path = sip_file_path

            if not sip_file_path.exists():
                error_msg = f"Sip arguments file {sip_file_path} not found."
                Logger.log_to_file(logging.ERROR, error_msg)
                raise FileNotFoundError(error_msg)
            else:
                logger.info(f"The file in {sip_file_path} have been loaded successfully")

            
        with open(sip_file_path, 'r') as f:
            sip_args_dict = yaml.safe_load(f)
        
        for k, v in sip_args_dict.items():
            
            setattr(self, k, v)


    def check_sip_args(self):
        """
        Validate the attributes for the SiPar class readed from the SIP arguments file.

        Raises:
        ----------
            ValueError: If any parameter is missing or does not have the expected type.
        """
        #Tipos esperados en los parámetros
        expected_types = {
            'source_id': int | list | None,
            'output_image_file_type': str | None,
            'spec_full_range': bool | str | None,
            'syn_beam_dimensions': list | None,
            'channel_width': float | None,
            'min_size': int | float | None,
            'snr_range': list | None,
            'surveys_list': list | None,
            'combo': bool | str | None,
            'user_image': str | None,
            'percentile_range': list | None,
            'spec_line': str | None,
        }

        #Los parámetros obligatorios, hasta la fecha
        required_params = list(expected_types.keys())

        #Comprobamos los parámetros obligatorios
        missing_params = [param for param in required_params if not hasattr(self, param)]
        if missing_params:
            param_list = ", ".join(missing_params)
            plural = "s are" if len(missing_params) > 1 else " is"
            raise ValueError(
                f"The following required parameter{plural} missing in "
                f"'{self.sip_file_path.name}': {param_list}"
            )

        if (len(self.number_list)>1):
            expected_types['catalog_file'] =  list | None
        else:
            expected_types['catalog_file'] =  str | list | None


       # Valido tipos de datos
        for param, expected_type in expected_types.items():
            if hasattr(self, param):
                value = getattr(self, param)
                if not isinstance(value, expected_type):
                    error_msg = (
                        f"The parameter '{param}' in the sip_args.yaml file must be of "
                        f"type {expected_type}, but is of type {type(value)}."
                    )
                    Logger.log_to_file(logging.ERROR, error_msg)
                    raise ValueError(error_msg)
            else:
                error_msg = (
                    f"The required parameter '{param}' is not defined in the"
                    " sip_args.yaml file."
                )
                Logger.log_to_file(logging.ERROR, error_msg)
                raise ValueError(error_msg)


        #-----------------catalog_file---------------------# 
        if self.adpalmap_config.enable_sofia:
            if self.catalog_file is not None:
                logger.warning(
                    "The catalog(s) specified in the 'catalog_file' parameter in "
                    "'sip_args.yaml' will be ignore. Those obtained from "
                    "SoFiA will be used instead, if any"
                ) 

        else:
            if self.adpalmap_config.enable_tap_service:
                input_name = self.input_data.stem
                cwd_file = Path.cwd().resolve()


                if self.adpalmap_config.run_mode == "absorption":
                    sofia_catalog_txt = cwd_file / "adpalmap_outputs_absorption" / f"{input_name}_cat.txt"
                    sofia_catalog_xml = cwd_file / "adpalmap_outputs_absorption" / f"{input_name}_cat.xml"
                    abs_cat_file = self.set_catalog(
                        sofia_catalog_txt, 
                        sofia_catalog_xml,
                        cwd_file / "adpalmap_outputs_absorption" 
                    )
                    if not abs_cat_file:
                        logger.error(abs_cat_file.error_msg)
                        raise RecoverableFileNotFoundError(abs_cat_file.error_msg)
                    self.catalog_file = abs_cat_file.catalog_path


                elif self.adpalmap_config.run_mode == "emission":
                    sofia_catalog_txt = cwd_file / "adpalmap_outputs_emission" / f"{input_name}_cat.txt"
                    sofia_catalog_xml = cwd_file / "adpalmap_outputs_emission" / f"{input_name}_cat.xml"              
                    emi_cat_file = self.set_catalog(
                        sofia_catalog_txt, 
                        sofia_catalog_xml,
                        cwd_file / "adpalmap_outputs_emission" 
                    )
                    if not emi_cat_file:
                        logger.error(emi_cat_file.error_msg)
                        raise RecoverableFileNotFoundError(emi_cat_file.error_msg)
                    self.catalog_file = emi_cat_file.catalog_path  
   

                elif self.adpalmap_config.run_mode == "both":
                    emi_sofia_catalog_txt = cwd_file / "adpalmap_outputs_emission" / f"{input_name}_cat.txt"
                    emi_sofia_catalog_xml = cwd_file / "adpalmap_outputs_emission" / f"{input_name}_cat.xml"
                    abs_sofia_catalog_txt = cwd_file / "adpalmap_outputs_absorption" / f"{input_name}_cat.txt"
                    abs_sofia_catalog_xml = cwd_file / "adpalmap_outputs_absorption" / f"{input_name}_cat.xml"
                    
            
                    # Check before set any value to self.catalogue. Otherwise the second set_catalog
                    # will show wrong errors. (Check if within set_catalog for more information)
                    abs_cat_file = self.set_catalog(
                        abs_sofia_catalog_txt, 
                        abs_sofia_catalog_xml, 
                        cwd_file/ "adpalmap_outputs_absorption"
                    )
                    if not abs_cat_file:
                        logger.warning(abs_cat_file.error_msg)

                    emi_cat_file = self.set_catalog(
                        emi_sofia_catalog_txt, 
                        emi_sofia_catalog_xml,
                        cwd_file / "adpalmap_outputs_emission"
                    )
                    if not emi_cat_file:
                        logger.warning(emi_cat_file.error_msg)

                    self.catalog_file = []
                    self.catalog_file.append(abs_cat_file.catalog_path)
                    self.catalog_file.append(emi_cat_file.catalog_path)
                    
                    if all(cat is None for cat in self.catalog_file):
                        error_msg = "No valid catalogs found for any mode"
                        logger.error(error_msg)
                        raise RecoverableFileNotFoundError(error_msg)
        
            else:
                #Si no hay en sip_args.yaml y no hay sargs
                if self.catalog_file is None and not self.sargs:
                    error_msg = (
                        "The parameter 'catalog_file' must be set via the corresponding "
                        " parameter in 'sip_args.yaml' or via terminal using the -sarg argument."
                    )
                    Logger.log_to_file(logging.ERROR, error_msg)
                    raise ValueError(error_msg)
                
                #Si no hay en archivo y hay sargs, compruebo que haya -c o -catalog
                elif self.catalog_file is None and self.sargs:
                    if (('-c' or '--catalog') not in self.sargs.keys()):
                        error_msg = (
                            "The parameter 'catalog_file'  must be set via the corresponding "
                            " parameter in 'sip_args.yaml' or via terminal using the -sarg argument."
                        )
                        Logger.log_to_file(logging.ERROR, error_msg)
                        raise ValueError(error_msg)
                    
                #Si hay en archivo, debo comprobar que sea correcto en longitud.
                elif self.catalog_file is not None:
                    catalog_list = self.catalog_file
                    if isinstance(catalog_list, list) and len(self.number_list) != len(catalog_list):
                        error_msg = (
                            f"The number of catalogs provided in 'catalog_file' parameter is "
                            " different from the number of datasets. There must be one "
                            "catalog per dataset."
                        )
                        Logger.log_to_file(logging.ERROR, error_msg)
                        raise ValueError(error_msg)
                    
                    elif isinstance(catalog_list, list) and len(self.number_list) == len(catalog_list):
                        setattr(self, 'catalog_file', Path(catalog_list[self.number]))
                    else:
                        pass
                else:
                    logger.error(
                        "You have found a combination of parameters that has not been taken into "
                        "account and may be misleading. Please open an issue on "
                        "https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific case."
                    )
                    raise
        #--------------------------------------------------# 

        # Valido valores permitidos en ciertos parámetros
        valid_values = {
            'output_image_file_type': ['png', 'jpg', 'pdf', 'svg'],
            'spec_line': ['HI', 
                          'CO(1-0)', 'CO(2-1)', 'CO(3-2)', 
                          'OH_1612', 'OH_1665', 'OH_1667', 'OH_1720'],
        }

        for param, valid_values_list in valid_values.items():
            if hasattr(self, param):
                value = getattr(self, param)
                
                if value not in valid_values_list:
                    if param == 'spec_line':
                        logger.warning(
                            f"The value '{value}' is not valid for parameter '{param}'. " 
                            "It will be set as 'Unknown'"
                        )
                        self.spec_line = 'Unknown'
                    else:
                        error_msg = (
                            f"The parameter '{param}' must have one of the following values:"
                            f" {valid_values_list}. Value provided: '{value}'."
                        )
                        Logger.log_to_file(logging.ERROR, error_msg)
                        raise ValueError(error_msg)

        # Valido parámetros que solo admiten listas con una cierta longitud
        if hasattr(self, 'snr_range') and getattr(self, 'snr_range') is not None:
            snr_range = getattr(self, 'snr_range')
            if not (isinstance(snr_range, list) and len(snr_range) == 2):
                error_msg = (
                        f"The 'snr_range' parameter must be a list of two values."
                        f" Provided value: {snr_range}."
                    )
                Logger.log_to_file(logging.ERROR, error_msg)
                raise ValueError(error_msg)
                
        if hasattr(self, 'percentile_range') and getattr(self, 'percentile_range') is not None:
            percentile_range = getattr(self, 'percentile_range')
            if not (isinstance(percentile_range, list) and len(percentile_range) == 2):
                error_msg = (
                    f"The 'percentile_range' parameter must be a list of two values."
                    f" Provided value: {percentile_range}."
                )
                Logger.log_to_file(logging.ERROR, error_msg)
                raise ValueError(error_msg)

        #logger.info("All parameters are valid.")


    def update_input_parameters(self, sip_args, adpalmap_config):
        """
        Updates the parameters of the SiPar class with the values provided in the terminal arguments.

        Parameters:
        ----------
        sip_args (dict): Dictionary with arguments provided from the terminal 
                         (-sarg or --sip-arguments).
        adpalmap_config: Config() class object with configuration from the configuration file.

        Returns:
        ----------
        None: Directly updates the class attributes.
        """
    
        
        if sip_args is not None:
            for key, value in sip_args.items():
                #Check if the key matches any shortcut in ATTRIBUTE_SHORTCUTS
                matched_attr = None
                for attr_name, shortcut in self.ATTRIBUTE_SHORTCUTS.items():
                    if key in shortcut:  
                        matched_attr = attr_name
                        break

                if matched_attr is not None:
                    # Special case for 'catalog_file' or '-c'
                    if matched_attr == "catalog_file" and adpalmap_config.enable_sofia:
                        logger.warning(
                            f"Ignoring argument '{key}' provided because the catalog provided by"
                            f" SoFiA will be used in this run."
                        )
                        continue  
                    elif matched_attr == "catalog_file" and not adpalmap_config.enable_sofia:
                        #Quiere decir que ha encontrado catalogos validos de TAP, tienen prioriodad
                        if(adpalmap_config.enable_tap_service 
                           and self.catalog_file is not None
                        ):
                            logger.warning(
                                "The catalog(s) provide via -sarg will be ignored. Existing "
                                " catalgos correspondings to the downloaded data will be used "
                                "instead."
                            )
                            continue
                        #Esto se da porque en check args en este caso específico cuadno hay sarg
                        #y nada maś simplemente se pasa y self.catalog_file permanece None
                        elif(adpalmap_config.enable_tap_service 
                           and self.catalog_file is None
                        ):
                            if len(self.number_list) != len(value):
                                error_msg = (
                                    f"The number of catalogs provided in 'catalog_list' is "
                                    "different from the number of datasets. There must be "
                                    "one catalog per dataset."
                                )
                                Logger.log_to_file(logging.ERROR, error_msg)
                                raise ValueError(error_msg)
                            else:
                                setattr(self, matched_attr, value[self.number])
                                continue

                    # Update the attribute with the new value
                    setattr(self, matched_attr, value)
                else:
                    logger.warning(f"Unknown argument '{key}' provided. Ignoring it.")
        

    def run_sip(self, adpalmap_config, sopar=None, run=-1):
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
        cwd_file = Path.cwd().resolve()
        
        if sopar: # if adpalmap_config.enable_sofia: debería ser equivalente, a elección
            sofia_output_dir = Path(sopar.output_directory)
            sip_output_dir = Path(sopar.output_directory) / f"{self.input_data.stem}_figures"
            input_file_name = Path(sopar.input_data).stem
                    
            sofia_catalog_txt = sofia_output_dir / f"{input_file_name}_cat.txt"
            sofia_catalog_xml = sofia_output_dir / f"{input_file_name}_xml.fits"

            if sofia_catalog_txt.exists() or sofia_catalog_xml.exists():
                pass
            else:
                sofia_catalog_txt = None
                sofia_catalog_xml = None

            sip_report = {
                        "software_id" :'SIP',
                        "PID": sopar.pid,
                        "input_name": sopar.input_data.stem,
                        "mode": sopar.sopar_mode,  
                        "log_path": sopar.output_directory / f"{self.input_data.stem}_sip.log",
                        "outputs": {"images": [],  "files": []}
                    }
    
            if sofia_catalog_txt and sofia_catalog_xml:
                self.catalog_file = sofia_catalog_txt
            elif sofia_catalog_txt:
                self.catalog_file = sofia_catalog_txt
            elif sofia_catalog_xml: 
                self.catalog_file = sofia_catalog_xml
            else:
                error_msg = (
                    f"No valid .txt or .xml catalog for SIP found within the  {sopar.output_directory} "
                    " directory."
                )
                logger.error(error_msg)
                if adpalmap_config.run_mode == 'both' and run!=0:
                    logger.info(f"SIP execution skipped. Run: {sopar.sopar_mode}")
                    sip_report.update({'command': '', 'error': error_msg})
                    return sip_report
                else:
                    logger.info(f"SIP execution aborted. Run: {sopar.sopar_mode}.")
                    sip_report.update({'command': '', 'error': error_msg})
                    return sip_report


        else:
            if adpalmap_config.run_mode == "both":             
                if run != 0:
                    #En 0 guardo el catalago de absorciones
                    self.aux_catalog_file = self.catalog_file
                    self.catalog_file = self.catalog_file[0]                
                    output_dir = (
                        cwd_file / "adpalmap_outputs_absorption" / f"{self.input_data.stem}_figures"
                    )
                    sip_report = {
                        "software_id" :'SIP',
                        "PID": self.pid,
                        "input_name": self.input_data.stem,
                        "mode": "absorption",  
                        "log_path": output_dir.parent / f"{self.input_data.stem}_sip.log",
                        "outputs": {"images": [], "files": []}
                    }
                    if self.catalog_file is None:
                        logger.info("SIP execution skipped. Mode: absorption")
                        sip_report.update({'command': '', 'error': ''})
                        return sip_report
                    
                else:
                    #En 1 guardo el catalago de emisiones
                    self.catalog_file = self.aux_catalog_file
                    self.catalog_file = self.catalog_file[1]
                    output_dir = (
                        cwd_file / "adpalmap_outputs_emission" / f"{self.input_data.stem}_figures"
                    )
                    sip_report = {
                        "software_id" :'SIP',
                        "PID": self.pid,
                        "input_name": self.input_data.stem,
                        "mode": "emission",  
                        "log_path": output_dir.parent / f"{self.input_data.stem}_sip.log",
                        "outputs": {"images": [],  "files": []}
                    }
                    if self.catalog_file is None:
                        logger.info("SIP execution skipped. Mode: emission")
                        sip_report.update({'command': '', 'error': ''})
                        return sip_report
                    
            elif adpalmap_config.run_mode == "absorption":
                output_dir = (
                    cwd_file / "adpalmap_outputs_absorption" / f"{self.input_data.stem}_figures"
                )
                #The self.catalog_file already contains the correct file
                sip_report = {
                    "software_id" :'SIP',
                    "PID": self.pid,
                    "input_name": self.input_data.stem,
                    "mode": "absorption",  
                    "log_path": output_dir.parent / f"{self.input_data.stem}_sip.log",
                    "outputs": {"images": [], "files": []}
                }
                
            elif adpalmap_config.run_mode == "emission":
                output_dir = (
                    cwd_file / "adpalmap_outputs_emission" / f"{self.input_data.stem}_figures"
                )
                #The self.catalog_file already contains the correct file
                sip_report = {
                    "software_id" :'SIP',
                    "PID": self.pid,
                    "input_name": self.input_data.stem,
                    "mode": "emission",  
                    "log_path": output_dir.parent / f"{self.input_data.stem}_sip.log",
                    "outputs": {"images": [], "files": []}
                }

            # At the end of this case it needs to save output_dir as sip_output_dir for the 
            # html outputs
            sip_output_dir = output_dir
                    
        if  sip_report["log_path"].exists():
            try:
                sip_report["log_path"].unlink()
            except:
                logger.warning(
                    "Error trying to delete existing log file. The new log "
                    "entries will be appended to it."
                )
            
        cmd = self.generate_command(exclude=["aux_catalog_file"], output_dir=sip_output_dir)
        error = ''
        sip_report.update({'command':cmd})
        try:
            Logger.raw("================================")
            if sopar:
                logger.info(
                    f"SIP start. Mode: {sopar.sopar_mode}. Input data: "
                    f"{input_file_name}"
                    )
            else:
                if adpalmap_config.run_mode == "both": 
                    if run != 0:
                        logger.info(f"SIP start. Mode: absorption. Input data: {self.input_data.stem}")
                    else:
                        logger.info(f"SIP start. Mode: emission. Input data: {self.input_data.stem}")
                elif adpalmap_config.run_mode == "absorption":
                    logger.info(f"SIP start. Mode: absorption. Input data: {self.input_data.stem}")
                elif adpalmap_config.run_mode == "emission":
                    logger.info(f"SIP start. Mode: emission. Input data: {self.input_data.stem}")
                
            Logger.raw("================================")
            logger.info(f"Command used to run SIP: {' '.join(cmd)}")
            
            subprocess.run(
                cmd, 
                text=True, 
                check=True, 
                capture_output=not adpalmap_config.verbose
                )       
                               
            Logger.raw("================================")
            if sopar:
                logger.info(f"SIP finished. Mode: {sopar.sopar_mode}")
            else:
                logger.info(f"SIP finished.")
            Logger.raw("================================")
            
            #Intentamos correr una segunda vez SIP para generar el plot resumen por fuente
            """try:
                cmd = self.make_summary(cmd)
                subprocess.run(
                    cmd, 
                    text=True, 
                    check=True, 
                    capture_output= not adpalmap_config.verbose
                )  
            except subprocess.CalledProcessError as e:
                logger.critical(f"Error running SIP making summary images: {e}")"""

            #Añadimos los outputs al report
            if self.adpalmap_config.html_report:
                try:
                    self.report_outputs(sip_report, sip_output_dir)  
                except Exception as e:
                    logger.warning(f"Error adding outputs for the html report (non-critical): {e}")


        except FileNotFoundError as e:
            logger.critical(f"Command not found: {cmd[0]}. Error: {e}")
            raise

        except subprocess.CalledProcessError as e:
            error = str(e)
            # In case of error this show the message and exit code of SIP
            if sopar:
                logger.error(f"Error running SIP. Mode: {sopar.sopar_mode}. Error: {e}")
            else:
                if adpalmap_config.run_mode == "both": 
                    if run != 0:
                        logger.error(f"Error running SIP. Mode: absorption. Error: {e}")
                    else: 
                        logger.error(f"Error running SIP. Mode: emission. Error: {e}")
                elif adpalmap_config.run_mode == "absorption":
                    logger.error(f"Error running SIP. Mode: absorption. Error: {e}")
                elif adpalmap_config.run_mode == "emission":
                    logger.error(f"Error running SIP. Mode: emission. Error: {e}")


            if adpalmap_config.run_mode == 'both' and run !=0:
                if sopar:
                    logger.info(f"SIP execution skipped. Mode: {sopar.sopar_mode}")
                    return
                else:
                    logger.error(f"SIP execution skipped. Mode: absorption.")

            else:
                if sopar:
                    logger.info(f"SIP execution aborted. Mode: {sopar.sopar_mode}")
                else:
                    if adpalmap_config.run_mode == 'absorption':
                        logger.info(f"SIP execution aborted. Mode: absorption")
                    elif adpalmap_config.run_mode == 'emission':
                        logger.info(f"SIP execution aborted. Mode: emission")
                sys.exit(-1)

        finally:
            sip_report.update({'error': error})
            return sip_report
        
        #DESCOMENTAR Cuando hable con Kelley
        '''try: 
            cmd = self.make_summary(cmd)
            subprocess.run(cmd, text=True, check=True, not capture_output= not adpalmap_config.verbose)  
        except subprocess.CalledProcessError as e:
            logger.critical(f"Error running SIP making summary images: {e}")
            sys.exit(-1)'''
        
    
    def generate_command(self, exclude=None, output_dir=None):
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
            exclude = []  # Si no se pasa, inicializamos como lista vacía

        cmd = ["sofia_image_pipeline"]
        for attr_name, shortcut in self.ATTRIBUTE_SHORTCUTS.items():

            if attr_name in exclude:  
                continue

            if attr_name == "combo":  # Special case for the 'combo' attribute
                value = getattr(self, attr_name, None)
                if value:  # If True, add only '-m'
                    cmd.append(shortcut[0])
                elif isinstance(value, str):  # If a string (path), add '-m' followed by the value
                    cmd.append(shortcut[0])
                    cmd.append(value)
                continue  #Skip further processing for 'combo

            elif attr_name in {
                "snr_range", "surveys_list", "percentile_range"
                } and getattr(self, attr_name) is not None:
                
                cmd.append(shortcut[0])
                for value in getattr(self, attr_name):
                    cmd.append(str(value))

            elif attr_name == "source_id" and getattr(self, attr_name) is not None:
                cmd.append(shortcut[0])
                attr_value = getattr(self, attr_name)
                if isinstance(attr_value, list):
                    for value in attr_value:
                        cmd.append(str(value))
                else: 
                    cmd.append(str(attr_value))  
            
            elif attr_name == "spec_full_range" and getattr(self, attr_name) is not None:
                attr_value =  getattr(self, attr_name)

                if self.adpalmap_config.enable_sofia or self.adpalmap_config.enable_tap_service: 
                    
                    if isinstance(attr_value, bool) and attr_value:
                        cmd.append(shortcut[0])
                        cmd.append(str(self.input_data))
                    elif isinstance(attr_value, str):
                        cmd.append(shortcut[0]) 
                        cmd.append(str(attr_value))  
                    else:
                        continue
                else:
                    
                    if isinstance(attr_value, bool) and attr_value:
                        logger.warning(
                            f"'spec_full_range' parameter in {self.sip_file_path} "
                            "cannot be set to True while the 'enable_sofia' and 'enable_tap' "
                            f"parameters in the {self.adpalmap_config.config_path}. file parameter "
                            " are set to False."
                        )
                    elif isinstance(attr_value, str):
                        cmd.append(shortcut[0]) 
                        cmd.append(str(attr_value))  
                    else: 
                        continue



            elif hasattr(self, attr_name) and getattr(self, attr_name) is not None:  
                cmd.append(shortcut[0])  
                cmd.append(str(getattr(self, attr_name))) 

        cmd.append("-log")
        log__name = str(output_dir.parent / f"{self.input_data.stem}_sip.log")
        cmd.append(log__name)

        return cmd


    def make_summary(self, cmd):
        """
        Generates a command based on the instance attributes, ensuring that the `-id` argument 
        has the value `0`, even if it was not in the original command.

        Returns:
        ----------
        list: List with the command set, where `-id` has the value `0`.
        """

        # Asegurar que `-id` esté presente con el valor `0`
        if "-id" in cmd:
            id_index = cmd.index("-id")
            cmd[id_index + 1] = "0"  # Reemplazar el valor por "0"
        else:
            # Si `-id` no está en el comando, agregarlo al final
            cmd.extend(["-id", "0"])

        return cmd
    

    def set_catalog(self, sofia_catalog_txt, sofia_catalog_xml, output_directory):


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
                f"from previous runs. Catalogs searched: {sofia_catalog_txt} || {sofia_catalog_xml}"
            )
            #Si no hay en sip_args.yaml y no hay sargs
            if self.catalog_file is None and not self.sargs:
                error_msg = (
                    "No 'catalog_file' parameter was found either in file 'sip_args.yaml' or via "
                    "the '-sarg|--sip-arguments'."
                )
                #logger.error(f"ValueError: {error_msg}")
                return CatalogResult(error_msg=error_msg)
                
            #Si no hay en archivo y hay sargs, compruebo que haya -c o -catalog
            elif self.catalog_file is None and self.sargs:
                if (('-c' or '--catalog') not in self.sargs.keys()):
                    error_msg = (
                        "No 'catalog_file' parameter was found either in file 'sip_args.yaml' or "
                        "via the '-sarg|--sip-arguments'."
                    )
                    #logger.error(f"ValueError: {error_msg}")
                    return CatalogResult(error_msg=error_msg)
                
            #Si hay en archivo, debo comprobar que sea correcto en longitud.
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
                    return CatalogResult(catalog_path=catalog_list[self.number])
                else:
                    pass
            else:
                logger.critical(
                    "You have found a case that has not been taken into "
                    "account and may be misleading. Please open an issue on "
                    "https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific case."
                )
                raise


    def report_outputs(self, sip_report, output_dir):
        
        num_sources = self.detect_source_count() 
    
        for i in range(num_sources):
            source_prefix = f"_{i+1}"
            sip_report['outputs']['images'].append({
                "type": "mom0",
                "path": output_dir / f"{self.input_data.stem}{source_prefix}_mom0.png",
                "source_id": i+1,
                "description": "Momment 0 image",
                "software-id": "sip"
            })
            sip_report['outputs']['images'].append({
                "type": "mom1",
                "path": output_dir / f"{self.input_data.stem}{source_prefix}_mom1.png",
                "source_id": i+1,
                "description": "Momment 1 image",
                "software-id": "sip"
            })
            sip_report['outputs']['images'].append({
                "type": "mom2",
                "path": output_dir / f"{self.input_data.stem}{source_prefix}_mom2.png",
                "source_id": i+1,
                "description": "Momment 2 image",
                "software-id": "sip"
            })
            sip_report['outputs']['images'].append({
                "type": "spec",
                "path": output_dir / f"{self.input_data.stem}{source_prefix}_spec.png",
                "source_id": i+1,
                "description": "Spectrum plot",
                "software-id": "sip"
            })
            sip_report['outputs']['images'].append({
                "type": "pv",
                "path": output_dir / f"{self.input_data.stem}{source_prefix}_pv.png",
                "source_id": i+1,
                "description": "Position-Velociy (major axis) plot",
                "software-id": "sip"
            })
            sip_report['outputs']['images'].append({
                "type": "pv_min",
                "path": output_dir / f"{self.input_data.stem}{source_prefix}_pv_min.png",
                "source_id": i+1,
                "description": "Position-Velociy (minor axis) plot",
                "software-id": "sip"
            })
        
        sip_report['outputs']['files'].append({
                "type": "par_file",
                "path": self.sip_file_path,
                "format": ".par",
                "software-id": "sip"
            })
                    

    def detect_source_count(self):
        if not self.catalog_file:
            return 0
        
        # Verifico si el archivo existe
        if not self.catalog_file.exists():
            # Verifico si la extensión es válida
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
        
        # Si el archivo existe
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
        
        

    

