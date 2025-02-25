
import os, yaml, logging, sys
from pathlib import Path

# Logger:
from adplib.logger import Initial_Logger
logger = Initial_Logger.get_initial_logger()


def get_data_path(line, input_path, line_number):

    
    expanded_path = os.path.expandvars(os.path.expanduser(line.strip()))
    
    line_path = Path(expanded_path)

    if not line_path.is_absolute():
        
        data_path = (input_path.parent / line_path).resolve()
    else:
        data_path = line_path.resolve()  
    
    if data_path.exists():
        return data_path
    else:
        raise FileNotFoundError(
            f"File: {data_path} indicated in line {line_number} within {input_path} was not found."
        )
    
    
def get_pb_path(line, pb_path, line_number):
    
    if line=="\n":
        return ""
    else:
        expanded_path = os.path.expandvars(os.path.expanduser(line))
        
        line_path = Path(expanded_path)

        if not line_path.is_absolute():
            
            data_path = (pb_path.parent / line_path).resolve()
        else:
            data_path = line_path.resolve()  
        
        if data_path.exists():
            return data_path
        else:
            raise FileNotFoundError(
                f"File: {data_path} indicated in line {line_number} within {pb_path} was not found."
            )


class Config(dict):
    r""" Configuration class for ADP ALMA Pipeline.
    
    This class is a singleton, that is, it always returns the same instance of the class.
    """

    #Configure as a singleton 

    _instance = None
    _configured = False
    
    #This turn Config class into a singleton
    def __new__(cls, *args, **kwargs):
        """ returns always the same instance of the class. """
        if Config._instance is None:
            Config._instance =  super().__new__(cls)
        return Config._instance


    def __init__(self, reconfigure=False, **kwargs):
        """
        Reads the specified config file and creates a configuration object.
        
        The configuration is performed only once, the first time it is called, unless you pass reconfigure=True.

        Parameters
        ----------
        config_path: str, default None
            Path to the configuration file. If None, it will display an error.

        Returns
        -------
        self

        Attributes
        ----------
        Different configuration parameters such as database path, log format, server
        for data download from remote sources, etc.
        """

        #The dict constructor is used and every key phrase in the .yaml file become an attribute of this class
        super(Config, self).__init__(**kwargs)
        #Garantiza que cualquier acceso futuro al diccionario o la adición de nuevas claves también se refleje
        #en la estructura de atributos de la instancia.
        self.__dict__ = self # Load config file and set attributes
        
        if reconfigure or not Config._configured:
            self.configure(**kwargs)


    def configure(self, config_path=None, **kwargs):

        if config_path is None:
            
            script_dir = Path(__file__).parent
            config_path = script_dir/ "config.yaml"
            self.config_path = config_path

            if not config_path.exists():
                raise FileNotFoundError(
                    f"Config default file {config_path} not found in the directory the"
                    " main script directory. Please specify a valid directory via the '-c/--config_file'"
                    f" <path_to_configuration_file> argument or download the default {config_path} file"
                    " included at https://gitlab.com/adp-group1/adp-alma-pipeline"
                )
            else:
                logger.info(f"The file in {config_path} have been loaded successfully")
                   
        elif config_path is not None:
            
            config_path = Path(config_path)

            if not config_path.exists():
                raise FileNotFoundError(f"Config file {config_path} not found.")
            else:
                logger.info(f"The file in {config_path} have been loaded successfully")

        else:
            
            raise FileNotFoundError(f"Something with the config_path or the config file went wrong")
            
        with open(config_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        
        #Inicializa los datos específicos directos desde el config.yaml. No contempla posibles futuras 
        # modificaciones de self (e.g añadiendo nuevos valores dentro del programa) 
        for k, v in config_dict.items():
            setattr(self, k, v)
        
        #Check the parameter from the config.yaml
        self.check_config_par()

        #Check the logic for the input parameters
        self.check_logic_input()

            
    def check_config_par(self):
        """
        Validate the attributes for the Config class readed from the configuration file.

        """
        #Tipos esperados en los parámetros
        expected_types = {
            'quality_assesment': bool,
            'capture_outputs': bool,
            'num_cores': int | None,
            'input_data': str | None,
            'input_primaryBeam': str | None,
            'input_data_list': bool | None,
            'clear_logs': bool,
            'log_file': str,
            'enable_tap_service': bool,
            'download_par_file': str | None,
            'enable_sofia': bool,
            'run_mode': str,
            'abs_flag_cube': bool,
            'auto_setup': bool,
            'sofia_abs_file': str | None,
            'sofia_emi_file': str | None,
            'enable_sip': bool,
            'sip_par_file': str | None,
        }

        #Los parámetros obligatorios, hasta la fecha
        required_params = [
            'quality_assesment',
            'capture_outputs',
            'num_cores',
            'input_data',
            'input_primaryBeam',
            'input_data_list',
            'clear_logs',
            'log_file',
            'enable_tap_service',
            'download_par_file',
            'enable_sofia',
            'run_mode',
            'abs_flag_cube',
            'auto_setup',
            'sofia_abs_file',
            'sofia_emi_file',
            'enable_sip',
            'sip_par_file',
        ]

        #Comprobamos los parámetros obligatorios
        missing_params = [param for param in required_params if not hasattr(self, param)]
        if missing_params:
            raise ValueError(
                f"The following required parameters are missing in config.yaml: {missing_params}"
            )

        #Comprobamos el tipo
        for param, expected_type in expected_types.items():
            if hasattr(self, param):
                value = getattr(self, param)
                if not isinstance(value, expected_type):
                    raise ValueError(
                        f"Parameter '{param}' must be of type {expected_type.__name__}, "
                        f"but got {type(value).__name__}, '{value}'."
                    )
                    
        #Compruebo especificamente los valores de run_mode
        # Valores permitidos para parámetros específicos
        valid_values = {
            'run_mode': ['emission', 'absorption', 'both'],
        }
        for param, valid_values_list in valid_values.items():
            if hasattr(self, param):
                value = getattr(self, param)
                
                if value not in valid_values_list:
                    raise ValueError(
                        f"The parameter '{param}' must have one of the following values: {valid_values_list}. "
                        f"Value provided: '{value}'."
                    )
                
        # Detecto y manejar parámetros no esperados
        internal_attributes = ['config_path'] #Parámetros creados dentro de la clase
        all_params = set(self.__dict__.keys())  # Todos los atributos actuales de la instancia
        allowed_params = set(expected_types.keys())  # Parámetros esperados
        allowed_params.update(internal_attributes)
        unexpected_params = all_params - allowed_params  # Parámetros inesperados

        for param in unexpected_params:
            logger.warning(
                f"Unexpected parameter '{param}' found in config.yaml. It will be ignored."
            )
            delattr(self, param) 


    def check_logic_input(self):
        """
        Validate the logic for the parameters readed from the configuration file.

        """
        #Si inupt_data tiene valores y TAP es True, da error, solo uno es posible.
        if self.enable_tap_service and self.input_data:
            raise ValueError(
                "Error in config.yaml: When 'enable_tap_service' is True, 'input_data' must be "
                "empty or None. If 'input_data' is provided, 'enable_tap_service' must be False "
                "or None. Both cannot be active simultaneously."
            )
        
        elif not self.enable_tap_service and not self.input_data: #self.input_data_list:

            raise ValueError(
                f"The parameter 'input_data' cannot be NoneType if 'enable_tap_service' is False. "
                "Please type a valid 'input_data' or change 'enable_tap_service' to False."
            )
            
        elif not self.enable_tap_service:

            input_path = Path(self.input_data)

            if not self.input_data_list:

                #Compruebo aquí que input_data existe, de lo contrario se 
                # comprobaría en otro módulo posteriormente y perdería lógica. Esto con list True.
                if not input_path.exists():
                    raise FileNotFoundError(
                        f"Input file '{input_path}' not found."
                        )
                
                elif input_path.suffix.lower() != ".fits":
                    raise ValueError(
                        f"Input file '{input_path}' is not a FITS file. "
                        f"Detected extension: '{input_path.suffix}' but "
                        "'input_data' must be a '.fits' file when 'input_data_list' is False"
                    )
                
                else:
                    self.input_data = [input_path]

                #Compruebo tb que el PB sea un .fits si lo hay.
                if self.input_primaryBeam:

                    pb_path = Path(self.input_primaryBeam)

                    if not pb_path.exists():
                        raise FileNotFoundError(
                            f"Input primary beam file '{pb_path}' not found."
                            )
                
                    elif pb_path.suffix.lower() != ".fits":
                        raise ValueError(
                            f"Input primary beam file '{pb_path}' is not a FITS file. "
                            f"Detected extension: '{pb_path.suffix}' but "
                            "'input_primaryBeam' must be a '.fits' file when 'input_data_list'"
                            " is False."
                        )
                    
                    else:
                        self.input_primaryBeam = [pb_path]
                
            else: #self.input_data_list True
                
                if not input_path.exists():
                    raise FileNotFoundError(
                        f"File '{input_path}' not found. "
                        "'input_data' must be a text file when 'input_data_list' is True."
                    )
                # Check .txt extension
                elif input_path.suffix != ".txt":
                    raise ValueError(
                        f"Input file '{input_path}' is not a TXT file. "
                        f"Detected extension: '{input_path.suffix}' but "
                        "'input_data' must be a '.txt' file when 'input_data_list' is True."
                    )
                #Por ultimo comprobar si esta vacío y si no guardarlo
                else:   
                    with open(input_path, 'r') as f:
                        lines = f.readlines()
                        if len(lines) == 0:
                            raise ValueError(f"The file'{input_path}' is empty")
                        else:
                            #Necesito obtener la ruta abssoluta de los archivos y comprobar que 
                            #cada uno de ellos existe
                            data_path_list = [
                                get_data_path(line, input_path, line_number)
                                for line_number, line in enumerate(lines)
                            ]

                            self.input_data = data_path_list


                #compruebo que input_primaryBeam, sea una lista si input_primaryBeam es True   
                if self.input_primaryBeam:
                    
                    pb_path = Path(self.input_primaryBeam)
                    
                    if not pb_path.exists():
                        raise FileNotFoundError(
                            f"File '{pb_path}' not found. "
                            "'input_data' must be a text file when 'input_data_list' is True."
                        )
                    
                    # Check .txt extension
                    elif input_path.suffix != ".txt":
                        raise ValueError(
                            f"Input file '{input_path}' is not a TXT file. "
                            f"Detected extension: '{input_path.suffix}' but "
                            "'input_data' must be a '.txt' file when 'input_data_list' is True."
                        )
                    #Por ultimo comprobar si esta vacío y coincide en lineas con input_data
                    #Si cumple lo guardardo
                    else:
                        with open(pb_path, 'r') as f:
                            lines = f.readlines()
                            if len(lines) == 0:
                                raise ValueError(f"The file'{pb_path}' is empty")
                            else:
                                pb_path_list = [
                                    get_pb_path(line, pb_path, line_number)
                                    for line_number, line in enumerate(lines)
                                ]
                                self.input_primaryBeam = pb_path_list
                        

                    with open(input_path, 'r') as data_file, \
                        open(pb_path, 'r') as pb_file:
                        
                        data_lines = [line.strip() for line in data_file if line.strip()]
                        pb_lines = pb_file.readlines() 
                        
                        if len(data_lines) != len(pb_lines):
                            raise ValueError(
                                f"The input_data  and input_primaryBeam  lines files must have"
                                " the same number of inputs. Note that blank or commented lines"
                                " in the primary beams file mean that their counterpart in "
                                "input_data will be processed without primary beam. Be "
                                "especially careful with unwanted trailing blank lines."
                            )
                
        


        #print("All parameters are valid.")

