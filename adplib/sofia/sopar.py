from pathlib import Path

#Logging
import logging
logger = logging.getLogger(__name__)

class SoPar(dict): 

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

        with open(sofia_file_path, 'r') as file:
                for line in file:
                    
                    # Remove both blank space sides and comment and skip blank lines
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    
                    try:
                        k, v = line.split("=", 1)
                        k = k.strip().replace(".", "_")
                        k = k.strip()
                        v = v.strip()
                        
                        # Convertir valor si es posible a int o float; de lo contrario, queda como string
                        if v.isdigit():
                            v = int(v)
                        else:
                            try:
                                v = float(v)
                            except ValueError:
                                pass
         
                        # Set attributes to the class dinamically
                        setattr(self, k, v)
                        #print(f"Atributo '{k}' ahora tiene valor: '{getattr(self, k)}'")
                        
                        
                    except ValueError:
                        logger.warning(f"The line '{line}' has not a valid format (parameter = value) and it will be ignore.")




