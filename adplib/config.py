
import os, yaml, logging
from pathlib import Path

#Logging
import logging
logger = logging.getLogger(__name__)

class Config(dict):
    r""" Configuration class for ADP ALMA Pipeline.
    
    This class is a singleton, that is, it always returns the same instance of the class.
    """

    # PATH CONFIG
    basedir = Path(__file__).parents[1].absolute()

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
        #Garantiza que cualquier acceso futuro al diccionario o la adición de nuevas claves también se refleje en la estructura de atributos de la instancia.
        self.__dict__ = self # Load config file and set attributes

        if reconfigure or not Config._configured:
            self.configure(**kwargs)


        

    def configure(self, config_path=None, **kwargs):

        if config_path is None:
            config_path = Path("config.yaml")

            if not config_path.exists():
                raise FileNotFoundError(f"Config file {config_path} not found. Checked if the config.yaml example have bee deleted")
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
        
        #Inicializa los datos específicos directos desde el config.yaml. No contempla posibles futuras modificaciones de self (e.g añadiendo nuevos valores dentro del programa) 
        for k, v in config_dict.items():
            setattr(self, k, v)
            

    