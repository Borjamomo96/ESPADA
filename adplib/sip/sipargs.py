from pathlib import Path

#Logging
import logging
logger = logging.getLogger(__name__)

class SiPar(dict): 

    def __init__(self, **kwargs):
        """
        Reads the SIP optional parameters|comand file and creates a SiPar object.
        
        Parameters
        ----------
        config_path: str, default None
            Path to the configuration file. 

        Returns
        -------
        self

        Attributes
        ----------
        All the optional parameters|comand that could be enter into the terminal while running SIP 
        """

        self.configure(**kwargs)


        
    def configure(self, sofia_file_path=None, **kwargs):


        if sofia_file_path is None:
            sofia_file_path='sofia/sofia_default.par'
            if Path(sofia_file_path).exists():
                self.read_sofia_par_file(sofia_file_path)
                self.path = Path('sofia/sofia_default.par')

            else:
                raise FileNotFoundError(f"Download file {Path(sofia_file_path)} not found.")
            
        else:
            self.read_sofia_par_file(sofia_file_path)
            self.path = Path(sofia_file_path)


    def read_sofia_par_file(self, sofia_file_path):


        if download_path is None:
            download_path = Path("tap/download_par.yaml")

            if not download_path.exists():
                raise FileNotFoundError(f"Download file {download_path} not found. Checked if the 'tap/download_par.yaml' have been deleted or the structure have changed. See README for furhter details")
            else:
                logger.info(f"The file in {download_path} have been loaded successfully")

        elif download_path is not None:
            download_path = Path(download_path)

            if not download_path.exists():
                raise FileNotFoundError(f"Download file {download_path} not found.")
            else:
                logger.info(f"The file in {download_path} have been loaded successfully")

        else:
            raise FileNotFoundError(f"Something with the download_path or the download file went wrong")
            
        with open(download_path, 'r') as f:
            download_dict = yaml.safe_load(f)
        
        #Inicializa los datos específicos directos desde el config.yaml. No contempla posibles futuras modificaciones de self (e.g añadiendo nuevos valores dentro del programa) 
        for k, v in download_dict.items():
            setattr(self, k, v)




