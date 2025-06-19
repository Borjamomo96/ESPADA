from pathlib import Path
import yaml
import subprocess
import sys
import os
from traceback import format_exc
from adplib.exceptions import RecoverableError, RecoverableValueError, RecoverableFileNotFoundError


# Logger:
import logging
from adplib.logger import Logger
logger = Logger.get_logger()



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
        Reads the SIP optional parameters|comand file and creates a SiPar object.
        
        Parameters
        ----------
        sip_file_path: str, default None
            Path to the configuration file. 

        Returns
        -------
        self

        Attributes
        ----------
        All the optional parameters|comand that could be enter into the terminal while running SIP 
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

        if (len(self.number_list)>1):
            expected_types['catalog_file'] =  list | None
        else:
            expected_types['catalog_file'] =  str | list | None


        #Extra check en algunos parámetros
        valid_values = {
            'output_image_file_type': ['png', 'jpg', 'pdf', 'svg'],
            'spec_line': ['HI', 'CO', 'OH'],
        }

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
                if self.adpalmap_config.run_mode == "emission":
                    sofia_catalog_txt = cwd_file / "adpalmap_outputs_emission" / f"{input_name}_cat.txt"
                    sofia_catalog_xml = cwd_file / "adpalmap_outputs_emission" / f"{input_name}_cat.xml"
                    self.catalog_file = self.set_catalog(
                        sofia_catalog_txt, 
                        sofia_catalog_xml,
                        cwd_file / "adpalmap_outputs_emission" 
                    )

                elif self.adpalmap_config.run_mode == "absorption":
                    sofia_catalog_txt = cwd_file / "adpalmap_outputs_absorption" / f"{input_name}_cat.txt"
                    sofia_catalog_xml = cwd_file / "adpalmap_outputs_absorption" / f"{input_name}_cat.xml"
                    self.catalog_file = self.set_catalog(
                        sofia_catalog_txt, 
                        sofia_catalog_xml,
                        cwd_file / "adpalmap_outputs_absorption" 
                    )

                elif self.adpalmap_config.run_mode == "both":
                    
                    emi_sofia_catalog_txt = cwd_file / "adpalmap_outputs_emission" / f"{input_name}_cat.txt"
                    emi_sofia_catalog_xml = cwd_file / "adpalmap_outputs_emission" / f"{input_name}_cat.xml"
                    abs_sofia_catalog_txt = cwd_file / "adpalmap_outputs_absorption" / f"{input_name}_cat.txt"
                    abs_sofia_catalog_xml = cwd_file / "adpalmap_outputs_absorption" / f"{input_name}_cat.xml"
                    #Guardo ambos, si los hubiera 
                    self.catalog_file = [
                        self.set_catalog(abs_sofia_catalog_txt, abs_sofia_catalog_xml, 
                                    cwd_file/ "adpalmap_outputs_absorption"
                        ),
                        self.set_catalog(emi_sofia_catalog_txt, emi_sofia_catalog_xml,
                                    cwd_file / "adpalmap_outputs_emission"
                        )
                    ]
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
                        setattr(self, 'catalog_file', catalog_list[self.number])
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


        # Valido valores permitidos
        for param, valid_values_list in valid_values.items():
            if hasattr(self, param):
                value = getattr(self, param)
                
                if value not in valid_values_list:
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
            input_file_name = Path(sopar.input_data).stem
                    
            sofia_catalog_txt = sofia_output_dir / f"{input_file_name}_cat.txt"
            sofia_catalog_xml = sofia_output_dir / f"{input_file_name}_xml.fits"

            if sofia_catalog_txt.exists() or sofia_catalog_xml.exists():
                pass
            else:
                sofia_catalog_txt = None
                sofia_catalog_xml = None
    
            if sofia_catalog_txt and sofia_catalog_xml:
                self.catalog_file = sofia_catalog_txt
            elif sofia_catalog_txt:
                self.catalog_file = sofia_catalog_txt
            elif sofia_catalog_xml: 
                self.catalog_file = sofia_catalog_xml
            else:
                logger.error(f"No valid .txt or .xml catalog for SIP found within the"
                                f" {sopar.output_directory} directory.")
                if adpalmap_config.run_mode == 'both' and run!=0:
                    logger.info(f"Skipping running SIP. Run: {sopar.sopar_mode}")
                    return
                else:
                    logger.info(f"Aborting process... Run: {sopar.sopar_mode}.")
                    sys.exit(-1)

        
            sip_log_record = {
                        "PID": sopar.pid,
                        "input_name": sopar.input_data.stem,
                        "mode": sopar.sopar_mode,  
                        "log_path": sopar.output_directory / f"{self.input_data.stem}_sip.log"
                    }

        else:
            if adpalmap_config.enable_tap_service:
                if adpalmap_config.run_mode == "both":             
                    if run != 0:
                        #En 0 guardo el catalago de absorciones
                        self.catalog_file = self.catalog_file[0]
                        sip_log_record = {
                            "PID": self.pid,
                            "input_name": self.input_data.stem,
                            "mode": "absorption",  
                            "log_path": cwd_file / "adpalmap_outputs_absorption" / f"{self.input_data.stem}_sip.log"
                        }
                    else:
                        #En 1 guardo el catalago de emisiones
                        self.catalog_file = self.catalog_file[1]
                        sip_log_record = {
                                    "PID": self.pid,
                                    "input_name": self.input_data.stem,
                                    "mode": "emission",  
                                    "log_path": cwd_file / "adpalmap_outputs_emission" / f"{self.input_data.stem}_sip.log"
                            }
                        
                elif adpalmap_config.run_mode == "absorption":
                    #The self.catalog_file already contains the correct file
                    sip_log_record = {
                            "PID": self.pid,
                            "input_name": self.input_data.stem,
                            "mode": "absorption",  
                            "log_path": cwd_file / "adpalmap_outputs_absorption" / f"{self.input_data.stem}_sip.log"
                        }
                    
                elif adpalmap_config.run_mode == "emission":
                    #The self.catalog_file already contains the correct file
                    sip_log_record = {
                                "PID": self.pid,
                                "input_name": self.input_data.stem,
                                "mode": "emission",  
                                "log_path": cwd_file / "adpalmap_outputs_emission" / f"{self.input_data.stem}_sip.log"
                        }

        cmd = self.generate_command()

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

        except subprocess.CalledProcessError as e:
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
                    logger.info(f"Skipping running SIP. Mode: {sopar.sopar_mode}")
                    return
                else:
                    logger.error(f"Skipping running SIP. Mode: absorption.")

            else:
                if sopar:
                    logger.info(f"Aborting process... Mode: {sopar.sopar_mode}")
                else:
                    if adpalmap_config.run_mode == 'absorption':
                        logger.info(f"Aborting process... Mode: absorption")
                    elif adpalmap_config.run_mode == 'emission':
                        logger.info(f"Aborting process... Mode: emission")
                sys.exit(-1)

        finally:
            return sip_log_record
        
        #DESCOMENTAR Cuando hable con Kelley
        '''try: 
            cmd = self.make_summary(cmd)
            subprocess.run(cmd, text=True, check=True, not capture_output= not adpalmap_config.verbose)  
        except subprocess.CalledProcessError as e:
            logger.critical(f"Error running SIP making summary images: {e}")
            sys.exit(-1)'''
        
    
    def generate_command(self, exclude=None):
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
        log__name = str(self.catalog_file.parent / f"{self.input_data.stem}_sip.log")
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
            return existing_files[0]  
        else:
            logger.warning(
                f"No valid .txt or .xml catalog for SIP found within the {output_directory} directory "
                f"from previous runs. Catalogs searched: {sofia_catalog_txt} || {sofia_catalog_xml}"
            )
            #Si no hay en sip_args.yaml y no hay sargs
            if self.catalog_file is None and not self.sargs:
                error_msg = (
                    "No 'catalog_file' parameter was found either in file 'sip_args.yaml' or via "
                    "the '-sarg|--sip-arguments'. Aborting SIP..."
                )
                logger.error(f"ValueError: {error_msg}")
                raise RecoverableValueError(error_msg)
                
            #Si no hay en archivo y hay sargs, compruebo que haya -c o -catalog
            elif self.catalog_file is None and self.sargs:
                if (('-c' or '--catalog') not in self.sargs.keys()):
                    error_msg = (
                        "No 'catalog_file' parameter was found either in file 'sip_args.yaml' or "
                        "via the '-sarg|--sip-arguments'. Aborting SIP..."
                    )
                    logger.error(f"ValueError: {error_msg}")
                    raise RecoverableValueError(error_msg)
                
            #Si hay en archivo, debo comprobar que sea correcto en longitud.
            elif self.catalog_file is not None:
                catalog_list = self.catalog_file
                if isinstance(catalog_list, list) and len(self.number_list) != len(catalog_list):
                    error_msg = (
                        f"The number of catalogs provided in 'catalog_file' parameter is "
                        " different from the number of datasets. There must be one "
                        "catalog per dataset."
                    )
                    logger.error(f"ValueError: {error_msg}")
                    raise RecoverableValueError(error_msg)
                
                elif isinstance(catalog_list, list) and len(self.number_list) == len(catalog_list):
                    logger.info(
                        f"Valid 'catalog_file' parameter found in 'sip_args.yaml'."
                    )
                    return catalog_list[self.number]
                else:
                    pass
            else:
                logger.critical(
                    "You have found a case that has not been taken into "
                    "account and may be misleading. Please open an issue on "
                    "https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific case."
                )
                raise
        

    

