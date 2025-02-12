from pathlib import Path
import yaml
import subprocess
import sys


# Logger:
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
         "spec_line": ["-l", "--spectral-line"]
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

        
    def configure(self, sip_file_path=None, **kwargs):
        
        
        if sip_file_path is None:
            script_dir = Path(__file__).parent
            sip_file_path = script_dir / "sip_args.yaml"

            if not sip_file_path.exists():
                raise FileNotFoundError(
                    f"Sip arguments file {sip_file_path} not found. Checked if the "
                    "'tap/download_par.yaml' have been deleted or the structure have changed. "
                    "See README for furhter details"
                )
            else:
                logger.info(f"The file in {sip_file_path} have been loaded successfully")

        elif sip_file_path is not None:
            sip_file_path = Path(sip_file_path)

            if not sip_file_path.exists():
                raise FileNotFoundError(f"Sip arguments file {sip_file_path} not found.")
            else:
                logger.info(f"The file in {sip_file_path} have been loaded successfully")

        else:
            raise FileNotFoundError(
                f"Critial error. Something with the Sip file path or the Sip file went wrong"
            )
            
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
            'catalog_file': str | None,
<<<<<<< HEAD
            'source_id': int | list | None,
=======
            'source_id': (int | list | None),
>>>>>>> 66c5551 (Minor changes)
            'output_image_file_type': str,
            'spec_full_range': str | None,
            'syn_beam_dimensions': list | None,
            'channel_width': float | None,
            'min_size': int | float | None,
            'snr_range': list,
            'surveys_list': list,
            'combo': bool,
            'user_image': str | None,
            'percentile_range': list,
            'spec_line': str,
        }

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
                    raise ValueError(
                        f"The parameter '{param}' must be of type {expected_type}, "
                        f"but is of type {type(value)}."
                    )
            else:
                raise ValueError(f"The required parameter '{param}' is not defined in the"
                                 " sip_args.yaml file.")

        # Valido valores permitidos
        for param, valid_values_list in valid_values.items():
            if hasattr(self, param):
                value = getattr(self, param)
                if value not in valid_values_list:
                    raise ValueError(
                        f"The parameter '{param}' must have one of the following values:"
                        f" {valid_values_list}. Value provided: '{value}'."
                    )

        # Valido listas específicas
        if hasattr(self, 'snr_range'):
            snr_range = getattr(self, 'snr_range')
            if not (isinstance(snr_range, list) and len(snr_range) == 2):
                raise ValueError(
                    f"The 'snr_range' parameter must be a list of two values."
                    " Provided value: {snr_range}."
                )
        if hasattr(self, 'percentile_range'):
            percentile_range = getattr(self, 'percentile_range')
            if not (isinstance(percentile_range, list) and len(percentile_range) == 2):
                raise ValueError(
                    f"The 'percentile_range' parameter must be a list of two values."
                     " Provided value: {percentile_range}."
                )

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
                            f"Ignoring argument '{key}' provided because  enable_sofia=True in"
                            f"the file {adpalmap_config.config_path}.")
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
        
        if sopar: # if adpalmap_config.enable_sofia: debería ser equivalente, a elección
<<<<<<< HEAD
            sofia_output_dir = Path(sopar.output_directory)
            input_file_name = Path(sopar.input_data).stem
                    
            sofia_catalog_txt = sofia_output_dir / f"{input_file_name}_cat.txt"
            sofia_catalog_xml = sofia_output_dir / f"{input_file_name}_xml.fits"

            if sofia_catalog_txt.exists() or sofia_catalog_xml.exists():
                pass
            else:
                sofia_catalog_txt = None
                sofia_catalog_xml = None
=======
            
            output_cubelets = Path(f"{sopar.output_directory}")

            try:     
                sofia_catalog_txt = list(output_cubelets.glob('*_cat.txt'))[0]
                sofia_catalog_xml = list(output_cubelets.glob('*_cat.xml'))[0]
            except:
                sofia_catalog_txt = None
                sofia_catalog_txt = None
>>>>>>> 66c5551 (Minor changes)
    
            if sofia_catalog_txt and sofia_catalog_xml:
                self.catalog_file = sofia_catalog_txt
            elif sofia_catalog_txt:
                self.catalog_file = sofia_catalog_txt
            elif sofia_catalog_xml: 
                self.catalog_file = sofia_catalog_xml
            else:
                logger.error(f"No valid .txt or .xml catalog for SIP found within the"
                                f" {sopar.output_directory} directory.")
<<<<<<< HEAD
                if adpalmap_config.run_mode == 'both' and run!=0:
                    return
                else:
                    logger.info(f"Exiting pipeline...")
                    sys.exit(-1)
=======
                return
>>>>>>> 66c5551 (Minor changes)

        
        cmd = self.generate_command()
        

        try:
            Logger.raw("================================")
            logger.info("Starting to run SIP...")
            Logger.raw("================================")
            logger.info(f"Command used to run SIP: {' '.join(cmd)}")

            subprocess.run(
                cmd, 
                text=True, 
                check=True, 
                capture_output=adpalmap_config.capture_outputs
                )              
            Logger.raw("================================")
            logger.info("SIP ended...")
            Logger.raw("================================")

        except subprocess.CalledProcessError as e:
            # In case of error this show the message and exit code of SIP
            logger.error(f"Error running SIP: {e}")
            if adpalmap_config.run_mode == 'both' and run !=0:
                logger.info(f"Skipping runs SIP")
                return
            else:
                logger.info("Exiting pipeline")
                sys.exit(-1)
        
        #DESCOMENTAR Cuando hable con Kelley
        '''try: 
            cmd = self.make_summary(cmd)
            subprocess.run(cmd, text=True, check=True, capture_output=config.capture_outputs)  
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
                if value is True:  # If True, add only '-m'
                    cmd.append(shortcut[0])
                elif isinstance(value, str):  # If a string (path), add '-m' followed by the value
                    cmd.append(shortcut[0])
                    cmd.append(value)
                continue  #Skip further processing for 'combo'

            if hasattr(self, attr_name):  
                value = getattr(self, attr_name)
                if value is not None:  
                    cmd.append(shortcut[0])  
                    cmd.append(str(value)) 

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

    

