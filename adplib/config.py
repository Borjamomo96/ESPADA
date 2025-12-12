
import os, yaml, logging, sys
from pathlib import Path

# Logger:
from adplib.logger import Initial_Logger
logger = Initial_Logger.get_initial_logger()



def parse_single_dataset(data_set, id):
    """Procesa un único conjunto de datos (ya sea string, lista o lista con strings anidados)."""
    files = []
    no_valid_entries = ['""',"''",'none','None','null','Null', '']
    # Si es str

    if isinstance(data_set, str):

        parts = [p.strip() for p in data_set.replace(',', ' ').split() if p.strip()]
        parts = [part if part not in no_valid_entries else '' for part in parts]
      

        files.extend(parts)
    # Si es list
    elif isinstance(data_set, list):
        
        for item in data_set:
            if isinstance(item, str):
                parts = [p.strip() for p in item.replace(',', ' ').split() if p.strip()]
                parts = [part if part not in no_valid_entries else '' for part in parts]

                
                if parts:
                    for part in parts: 
                        if part:
                            files.append(part)
                        else:
                            files.append('')
                else:
                    files.append('')
            elif item is None:
                files.append("")
            else:
                files.append(str(item).strip())

    else:
        raise ValueError(
            f"Not valid format for the set '{id}': {data_set} (type {type(data_set)})"
        )
    
    # Validaciones comunes
    if not files:
        raise ValueError(f"No files were provided in the set: '{id}'")

    # Limitar a 3 elementos máximo
    files = files[:3]  
    while len(files) < 3:
        files.append("")

    if not files[0]:
        raise ValueError(f"The data file cannot be empty at input '{id}'")

    expanded_files = []
    for file_path in files:
        if file_path and file_path != "":  # Solo expandir si no está vacío
            expanded_files.append(os.path.expanduser(file_path))
        else:
            expanded_files.append(file_path)
    
    return expanded_files
    


def validate_fits_files(data_set_list, id_list):
    """
    Checks that the files are not empty and are .fits. Return the same 
    list with each element converted to a Path object.
    """
    data_set_list_path = []
    for id, data_set in zip(id_list, data_set_list):
        new_dataset = []
        for file in data_set:
            if file:  
                # Asegurarse de que la ruta está expandida
                expanded_file = os.path.expanduser(file) if isinstance(file, str) else file
                
                if not str(expanded_file).endswith(".fits"):
                    raise ValueError(
                        f"Input file '{expanded_file}' is not a FITS file. "
                    )
                elif not os.path.isfile(expanded_file):
                    raise FileNotFoundError(
                        f"Input file '{expanded_file}' not found. Dataset: {id}"
                    )
                else:
                    new_dataset.append(Path(expanded_file))
            else:
                new_dataset.append("") 

        data_set_list_path.append(tuple(new_dataset))
       
    return data_set_list_path


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

        #Check the parameter from the config.yaml
        self.check_config_par()

        #Check the logic for the input parameters
        self.input_logic()


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
                
       
    def check_config_par(self):
        """
        Validate the attributes for the Config class readed from the configuration file.

        """
        # Parameters and values allowed
        expected_types = {
            'html_report': bool,
            'verbose': bool,
            'num_cores': int | None,
            'input_data_set': str | list | dict | None,
            'input_file': str | None,
            'clear_logs': bool,
            'log_file': str,
            'enable_tap_service': bool,
            'download_par_file': str | None,
            'enable_sofia': bool,
            'run_mode': str,
            'use_pb': bool,
            'use_mask': bool,
            'abs_flag_cube': bool,
            'auto_setup': bool,
            'sofia_abs_file': str | None,
            'sofia_emi_file': str | None,
            'enable_sip': bool,
            'sip_par_file': str | None,
            'enable_group': bool | None,
            'overlap_mode': str | None,
            'overlap_threshold': float | None
        }

        # Required parameters, up to date
        required_params = list(expected_types.keys())

        # Check the required parameters
        missing_params = [param for param in required_params if not hasattr(self, param)]
        if missing_params:
            param_list = ", ".join(missing_params)
            plural = "s are" if len(missing_params) > 1 else " is"
            raise ValueError(
                f"The following required parameter{plural} missing in "
                f"'{self.config_path.name}': {param_list}"
            )

        # Check the (type)
        for param, expected_type in expected_types.items():
            if hasattr(self, param):
                value = getattr(self, param)
                if not isinstance(value, expected_type):
                    print(type(value), value)
                    raise ValueError(
                        f"The parameter '{param}' in the config.yaml file must be of "
                        f"type {expected_type}, but is of type {type(value)}."
                    )


        # Check for 'overlap_threshold'
        if hasattr(self, 'overlap_threshold') and self.overlap_threshold is not None:
            if not (0 <= self.overlap_threshold <= 1):
                raise ValueError(
                    f"The parameter 'overlap_threshold' must be a float between 0 and 1. "
                    f"Value provided: {self.overlap_threshold}."
                )    
                     
        # Check for 'run_mode' y 'overlap_mode'. 
        # Allowed values for this parameters 
        valid_values = {
            'run_mode': ['emission', 'absorption', 'both'],
            'overlap_mode': ['flux', 'absflux', 'area'],
        }
        for param, valid_values_list in valid_values.items():
            if hasattr(self, param):
                value = getattr(self, param)
                
                if value not in valid_values_list:
                    raise ValueError(
                        f"The parameter '{param}' must have one of the following values: {valid_values_list}. "
                        f"Value provided: '{value}'."
                    )
                
        # Detect and manage of the unexpected parameters
        internal_attributes = ['config_path'] # Parameters created inside the class
        all_params = set(self.__dict__.keys())  # All the atributes in the instance
        allowed_params = set(expected_types.keys())  # Expected parameters
        allowed_params.update(internal_attributes)
        unexpected_params = all_params - allowed_params  # Unexpected parameters

        for param in unexpected_params:
            raise ValueError(
                f"Unexpected parameter '{param}' found in config.yaml. It will be ignored."
            )
            #delattr(self, param)         


    def input_logic(self):

        """
        Validate the logic for the parameters readed from the configuration file.

        """ 
        
        if self.enable_tap_service and self.input_data_set and self.input_file:

            raise ValueError(
                "Error in 'config.yaml': 'enable_tap_service', 'input_data_set' and 'input_file'"
                "cannot be set simultaneously. Set 'enable_tap_service' to False or leave either"
                "'input_data_set' or 'input_file' blank."
            )
        
        elif self.enable_tap_service and self.input_data_set:

            raise ValueError(
                "Error in 'config.yaml': 'enable_tap_service' and 'input_data_set' "
                "cannot be set simultaneously. Set 'enable_tap_service' to False or leave"
                "'input_data_set' blank."
            )
        
        elif self.enable_tap_service and self.input_file:

            raise ValueError(
                "Error in 'config.yaml': 'enable_tap_service' and 'input_file' "
                "cannot be set simultaneously. Set 'enable_tap_service' to False or leave"
                "'input_file' blank."
            )
        
        elif not self.enable_tap_service and not self.input_data_set and not self.input_file:

            raise ValueError(
                "Error in 'config.yaml': None of the parameters 'enable_tap_service', "
                "'input_data_set' or 'input_file' has been set. At least one must be set."
            )
            
        elif not self.enable_tap_service: 

            if self.input_data_set and self.input_file:
                raise ValueError(
                    "Error in 'config.yaml': 'input_data_set' and 'input_file'"
                    "cannot be set simultaneously. Leave 'input_data_set' or 'input_file'"
                    " blank"
                )
            
            elif not self.input_file:
                self.parse_input_data_set()
            
            elif not self.input_data_set:
                self.parse_input_file()
        
        if not self.enable_sofia and self.enable_group:

            raise ValueError(
                    "Error in 'config.yaml': 'enable_group' can only be executed if 'enable_sofia' is True"
                )
            

    def parse_input_data_set(self):
        
        data_type = type(self.input_data_set).__name__
        data_set_list = []

        # Caso 1: Dict. Manejo los mismo que con list o str pero multiples veces
        if data_type == "dict":
            for id, data_set in self.input_data_set.items():
                parsed_files = parse_single_dataset(data_set, id=id)
                data_set_list.append(parsed_files)
                
            self.input_data_set = validate_fits_files(data_set_list, self.input_data_set.keys())

        # Caso 2: list o str
        elif data_type in ["list", "str"]:
            parsed_files = parse_single_dataset(self.input_data_set, id="0")
            data_set_list.append(parsed_files)
            
            self.input_data_set = validate_fits_files(data_set_list, id_list="0")

        else:
            raise ValueError(
                f"Not valid format: {self.input_data_set} (type {type(data_type)})"
            )
  
    
    def parse_input_file(self):
        
        input_file_path = Path(self.input_file)

        if input_file_path.suffix.lower() not in [".txt", ".lst", ".dat"]:
            raise ValueError(
                f"The input file must be text (.txt, .lst, .dat)"
            )
        
        if not input_file_path.exists():
            raise FileNotFoundError(
                f"Input file '{input_file_path}' not found"
            )
        
        #Para comprobar si hay permisos de lectura o no
        try:
            with open(input_file_path, "r") as f:
                pass  # Solo verificar que se puede abrir
        except IOError as e:
            raise IOError(
                f"Cannot read input file '{input_file_path}': {str(e)}"
            )
        
        data_set_dict = {}
        
        with open(input_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Ignoro líneas vacías y comentarios
                if not line or line.startswith('#'):
                    continue
                    
                if ':' not in line:
                    raise ValueError(
                        f"Invalid format on line: {line}.The format must be key : files" 
                    )
                    
                key_part, value_part = line.split(':', 1)
                key = key_part.strip()
                value = value_part.strip()
                
                try:
                    parsed_files = parse_single_dataset(value, id=key)
                    data_set_dict[key] = parsed_files
                except ValueError as e:
                    raise ValueError(
                        f"Error on line '{line}': {str(e)}"
                    )
        
        data_set_list = list(data_set_dict.values())
        id_list = list(data_set_dict.keys())
    
        self.input_data_set = validate_fits_files(data_set_list, id_list)
            

