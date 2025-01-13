import os
import sys
import subprocess
#import tempfile 
import numpy as np
from pathlib import Path
from astropy.io import fits

# Configuration:
from config import Config
config = Config()
logger = config.get_logger()

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

        super(SoPar, self).__init__(**kwargs)
        self.__dict__ = self
        
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
                        
                    except ValueError: #CHANGE. Check is ValueError cover all the posibilities.
                        logger.error(f"The line '{line}' has not a valid format (module.parameter = value).")
                        sys.exit(-1)


    def update_input_parameters(self, sop_par, adpalmap_main=None, adpalmap_datap=None, mode=None, run=-1):
        """
        Updates the attributes of the SoPar object with the values ​​provided in sop_params.
        Manages input.data priority based on adpalmap_main/adpalmap_datap.

        Args:
        sop_params (dict): Dictionary with parameters provided via -sop.
        adpalmap_main: Object with configuration for adpalmap_main mode.
        adpalmap_datap: Object with configuration for adpalmap_datap mode.

        Returns:
        None: Updates the attributes of the SoPar object directly.
        """
        
        #-------------------input.data logic--------------------#
        #REMOVE. Si Pongo una condición en el main para este caso, aquí no hace falta definirlo. 
        if adpalmap_main and adpalmap_datap: #Ambos definidos
            #raise ValueError("Both adpalmap_main and adpalmap_datap are defined. Only one is allowed.")
            logger.warning(f"Ignoring 'input_data={adpalmap_main.input_data}' specified in the config.yaml file. The parameter 'enable_tap_service' has set 'True' so ADPALMAP will use the downloaded data as 'input_data'")
            self.input_data = adpalmap_datap.data_loc_fits
        elif adpalmap_main:
            if self.input_data is not None:
                logger.warning(f"Ignoring parameter 'input.data={self.input_data}' provided in {self.sofia_file_path}. If you want to change this, specify it in the input_data parameter in the config.yaml file.")
            self.input_data = adpalmap_main.input_data
        elif adpalmap_datap:
            if self.input_data is not None:
                logger.warning(f"Ignoring parameter 'input.data={self.input_data}' provided in {self.sofia_file_path}.")
            self.input_data = adpalmap_datap.data_loc_fits
        else: #Ambos None
            raise ValueError("No valid source for input.data. Define it in either adpalmap_main or adpalmap_datap.")
        
        #---------------output.directory logic-------------------#
        if sop_par and "output.directory" in sop_par: 
            self.output_directory = sop_par["output.directory"]
        elif hasattr(self, "output_directory") and self.output_directory:  
            pass
        else: 
            self.output_directory = str(f"{Path(self.input_data).parent.resolve()}/sofia_outputs")
        
        #Guardo el directorio de salida final en un nuevo atributo
        self.base_output_directory = self.output_directory

        #-----------------input.invert logic---------------------#
        if sop_par is not None:
            invert_value_sopar = sop_par.get("input.invert", getattr(self, "input_invert", False))
        else:
            invert_value_sopar = None
        
        if mode == 'emission' and (invert_value_sopar=='true' or self.input_invert=='true'):
            logger.warning("Parameter 'input.invert=true' is not allowed in 'emission' mode. Changing 'input.invert' to 'false'.")
            self.input_invert = 'false'
        elif mode == 'absorption' and (invert_value_sopar=='false' or self.input_invert=='false'):
            logger.warning("Parameter 'input.invert=false' is not allowed in 'absorption' mode. Changing 'input.invert' to 'true'.")
            self.input_invert = 'true'
        elif mode == 'both' and run !=0:
            logger.warning("Parameter 'input.invert=false' is not allowed in 'both' mode for the first run. Changing 'input.invert' to 'true'.")
            self.input_invert = 'true'
        elif mode == 'both' and run ==0:
            logger.warning("Parameter 'input.invert=true' is not allowed in 'both' mode for the second run. Changing 'input.invert' to 'false'.")
            self.input_invert = 'false'
        

        if sop_par is not None:
            for key, value in sop_par.items():
                normalized_key = key.replace('.', '_')

                if key in {"input.data"}:
                    logger.warning(f"Ignoring parameter '{key}={value}' provided via -sop. If you want to change this, specify it in the input_data parameter in the config.yaml file.")
                    continue
                if key in {"output.directory", "input.invert"}: continue

                # Actualizar o añadir parámetros
                if hasattr(self, normalized_key):
                    setattr(self, normalized_key, value)
                else:
                    # Añadir como nuevo atributo si no existe
                    setattr(self, normalized_key, value)
                    logger.warning(f"Added new parameter '{key}' with value '{value}'.")

    
    def auto_setup(self):
        """
        Lee el archivo FITS asociado al atributo `input_data` y actualiza los
        atributos de SoPar según los valores del header y las operaciones especificadas.

        Raises:
            FileNotFoundError: Si el archivo FITS no existe.
            KeyError: Si algún keyword necesario no está presente en el header.
        """

        if not hasattr(self, "input_data") or not self.input_data:
            logger.critical("El atributo 'input_data' no está definido o está vacío.")
            sys.exit(-1)

        fits_path = Path(self.input_data)

        if not fits_path.exists():
            logger.critical(f"El archivo FITS '{fits_path}' no existe.")
            sys.exit(-1)

        if not fits_path.exists():
            logger.critical(f"File FITS '{fits_path}' does not exist.")
            sys.exit(-1)

        with fits.open(fits_path) as hdul:
            header = hdul[0].header

        
        # Update attributes based on header and defined operations
        if "BMAJ" in header and "BMIN" in header and "CDELT1" in header:
            bmaj = header["BMAJ"]
            bmin = header["BMIN"]
            cdelt1 = abs(header["CDELT1"])

            # Calculate values ​​for scfind.kernelsXY and linker.minSizeXY
            x = (bmaj + bmin) / (2 * cdelt1)
            self.scfind_kernelsXY = f"0, {x:.2f}, {2*x:.2f}"  # Format "0, x, 2x"
            self.linker_minSizeXY = x  
        

        # reliability.minSNR
        if "BMAJ" in header and "BMIN" in header:
            self.reliability_minSNR = 3.0  

        else:
            naxis1 = header.get("NAXIS1", None)
            naxis2 = header.get("NAXIS2", None)
            naxis3 = header.get("NAXIS3", None)

            if naxis1 is not None and naxis2 is not None and naxis3 is not None:
                a = naxis1 / 2
                b = naxis2 / 2
                x = (3 / 2) * np.sqrt((np.pi * a * b) / np.log(2))
                self.reliability_minSNR = x
            else:
                # Manejo del caso en que falte alguno de los valores
                logger.warning(
                    "NAXIS1, NAXIS2, or NAXIS3 is not defined in the FITS file header."
                    "Cannot calculate 'reliability.minSNR'."
                )
                

        # Otros parámetros pueden ser añadidos según las reglas específicas...
        logger.info("Auto-setup DONE.")


    def run_sofia(self, config, mode=None, run=-1, abs_flag_cube=None):        
        
        if (mode is not None and mode=='absorption'):

            self.output_directory = Path(f'{self.output_directory}_absorption')

            if not os.path.exists(self.output_directory):
                os.makedirs(Path(self.output_directory))
            else:
                logger.warning(f"The {Path(self.output_directory)} directory already exists. The SoFia outputs will be stored in this directory") 
            
            temp_file_path = self.create_tempfile()
            try:
                cmd = ["sofia", f"{temp_file_path}"]
                subprocess.run(cmd, text=True, check=True, capture_output=config.capture_outputs) 
            except subprocess.CalledProcessError as e:
                logger.error(f"Error running SoFia: {e}")
                sys.exit(-1)
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            
        elif (mode is not None and mode=='emission'):

            self.output_directory = Path(f'{self.output_directory}_emission')
            
            if not os.path.exists(Path(self.output_directory)):
                os.makedirs(Path(self.output_directory))
            else:
                logger.warning(f"The {Path(self.output_directory)} directory already exists. The SoFia outputs will be stored in this directory") 

            temp_file_path = self.create_tempfile()
            try:
                cmd = ["sofia", f"{temp_file_path}"]
                subprocess.run(cmd, text=True, check=True, capture_output=config.capture_outputs)
            except subprocess.CalledProcessError as e:
                logger.error(f"Error running SoFia: {e}")
                sys.exit(-1)
            finally:
                '''if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)'''
        
        elif mode == 'both':
            if run!=0:
                #Corre en modo absorción, indicado en el main()
                self.output_directory = Path(f'{self.output_directory}_absorption')
                if not os.path.exists(self.output_directory):
                    os.makedirs(Path(self.output_directory))
                else:
                    logger.warning(f"The {Path(self.output_directory)} directory already exists. The SoFia outputs will be stored in this directory") 

                temp_file_path = self.create_tempfile()
                try:
                    cmd = ["sofia", f"{temp_file_path}"]
                    subprocess.run(cmd, text=True, check=True, capture_output=config.capture_outputs) 
                except subprocess.CalledProcessError as e:
                    logger.warning(f"SoFia has returned non-zero exit status: {e.returncode}, trying you finding absorption. " 
                            "SoFia will run again in the 'emission' mode without considering the absorption mask as a flag.cube.")
                finally:
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                    
            elif run==0:
                
                #Por defecto, el directorio de absorción será el self.output_directory_absorption. Uso el base_output_directory para buscarlo 
                # Lo búsco, si no lo encuentra por fallo o porque no encontró absorciones, se mantiene igual. 
                if config.abs_flag_cube is not None and config.abs_flag_cube==True:
                    absorption_dir = Path(f'{self.base_output_directory}_absorption')
                    #Caso en el que no encuentra absorciones
                    if list(absorption_dir.glob('*_mask.fits')):
                        flag_cube = list(absorption_dir.glob('*_mask.fits'))[0]
                        self.flag_cube = flag_cube
                else:
                    logger.info('Ignoring absorption sources as input for flag.cube in the run trying to find emissions sources.')

                self.output_directory = Path(f'{self.output_directory}_emission')
                if not os.path.exists(Path(self.output_directory)):
                    os.makedirs(Path(self.output_directory))
                else:
                    logger.warning(f"The {Path(self.output_directory)} directory already exists. The SoFia outputs will be stored in this directory") 


                temp_file_path = self.create_tempfile()
                try:
                    cmd = ["sofia", f"{temp_file_path}"]
                    subprocess.run(cmd, text=True, check=True, capture_output=config.capture_outputs)                   
                except subprocess.CalledProcessError as e:
                    logger.error(f"Error running SoFia: {e}")
                    sys.exit(-1)
                finally:
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)


    def create_tempfile(self):

        original_path = self.path if hasattr(self, "path") else Path(".")
        temp_file_path = original_path.with_name(original_path.stem + "_tmp" + original_path.suffix)
        
        with open(temp_file_path, 'w') as tf:
            for key, value in self.__dict__.items():
                if key not in {"sofia_file_path", "path", "base_output_directory"}:  # Excluye estos atributos
                    key_transformed = key.replace("_", ".")
                    tf.write(f"{key_transformed}={value}\n")

        return str(temp_file_path)
                
