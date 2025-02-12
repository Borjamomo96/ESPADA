import os
import sys
import subprocess
#import tempfile 
import numpy as np
from pathlib import Path
from astropy.io import fits
import matplotlib.pyplot as plt

# Logger:
from adplib.logger import Logger
logger = Logger.get_logger()


def moment8_ima(adpalmap_sopar):

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
    if not hasattr(adpalmap_sopar, "input_data") or not adpalmap_sopar.input_data:
        logger.critical(
            "Attribute 'input_data' is not defined or is None. Fatal error. Please open an"
            " issue on GitLab https://gitlab.com/adp-group1/adp-alma-pipeline with your specific "
            "case."
        )
        sys.exit(-1)

    fits_path = Path(adpalmap_sopar.input_data)

    if not fits_path.exists():
        logger.critical(
            f"File FITS '{fits_path}' does not exist. Fatal error. Please open an"
            " issue on GitLab https://gitlab.com/adp-group1/adp-alma-pipeline with your specific "
            "case.")
        sys.exit(-1)

    with fits.open(fits_path) as hdul:
        data_cube = hdul[0].data

    if data_cube is None:
        raise ValueError("The FITS file does not contain data in the primary HDU.")

    if data_cube.ndim == 4:
        data_cube = np.squeeze(data_cube, axis=0)
    elif data_cube.ndim > 4:
        logger.critical(
            "ADP Alma pipeline is not designed to handle data files with more than 4 dimensions. "
            "Please open an issue on GitLab https://gitlab.com/adp-group1/adp-alma-pipeline" 
            "with your specific case.")

    #Ahora el PrimaryBeam
    if hasattr(adpalmap_sopar, "input_primaryBeam") and adpalmap_sopar.input_primaryBeam:

        pb_path = Path(adpalmap_sopar.input_primaryBeam)

        if not pb_path.exists():
            logger.critical(
                f"File FITS '{pb_path}' does not exist. Fatal error. Please open an"
                " issue on GitLab https://gitlab.com/adp-group1/adp-alma-pipeline with your" 
                "specific case.")
            sys.exit(-1)

        with fits.open(pb_path) as hdul:
            pb_cube = hdul[0].data

        if pb_cube is None:
            raise ValueError("The FITS file does not contain data in the primary HDU.")
        
        if pb_cube.ndim == 4:
            pb_cube = np.squeeze(pb_cube, axis=0)
        elif pb_cube.ndim > 4:
            logger.critical(
                "ADP Alma pipeline is not designed to handle data files with more than 4 "
                "dimensions. Please open an issue on GitLab "
                "https://gitlab.com/adp-group1/adp-alma-pipeline with your specific case."
            )

        final_data_cube = data_cube * pb_cube
                
    else:
        logger.warning(
            "No data cube has been specified with Primary Beam information. "
            "Image at moment 8 cannot have the correction subtracted by the Primary "
            "Beam."
        )
        
        final_data_cube = data_cube


    max_projection = np.max(final_data_cube, axis=0)

    return max_projection


def run_and_log(command):
    output = []  

    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
        for line in process.stdout: 
            print(line, end="")  
            output.append(line)  

        process.wait()  

    Logger.raw_file("".join(output))


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
            
            script_dir = Path(__file__).parent
            sofia_file_path = script_dir/'sofia_default.par'

            if Path(sofia_file_path).exists():
                self.read_sofia_par_file(sofia_file_path)
                self.sofia_file_path = sofia_file_path

            else:
                raise FileNotFoundError(f"Download file {Path(sofia_file_path)} not found.")
            
        else:
            self.read_sofia_par_file(sofia_file_path)
            self.sofia_file_path = sofia_file_path

        

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
                        logger.error(f"The line '{line}' has not a valid format "
                                     "(module.parameter = value).")
                        logger.info(f"Exiting pipeline...")
                        sys.exit(-1)


    def update_input_parameters(self, sop_par, input_data, primary_beam=None, id="", mode=None, run=-1):
        """
        Updates the attributes of the SoPar object with the values provided in sop_params.
        Manages input.data, output.directory, input.invert and input.primaryBeam priority 
        based on adpalmap_main, adpalmap_datap, sop_par and the attributes on self.

        Parameters:
        ----------
        sop_params (dict): Dictionary with parameters provided via -sop.
        adpalmap_main: Config() class object with configuration from the configuration file.
        adpalmap_datap: Datap() class object with parameters from the download parameters file.

        Returns:
        ----------
        None: Updates the attributes of the SoPar object directly.
        """
        
        #El parámetro input.data se gestiona antes en la función principal.
        self.input_data = input_data
        
        
        #---------------output.directory logic-------------------#
        if sop_par and "output.directory" in sop_par: 
            self.output_directory = sop_par["output.directory"]
        elif hasattr(self, "output_directory") and self.output_directory:  
            pass
        else: 
            if not id:
                logger.critical(
                    "All SoFiA products will be stored in the same directory. There is a risk "
                    "of overwriting some of them."
                )
                self.output_directory = str(f"{Path(self.input_data).parent.resolve()}/adpalmap_outputs")
            else:
                self.output_directory = str(f"{Path(self.input_data).parent.resolve()}/adpalmap_outputs_{str(id)}")
        
        #CHANGE. Guardo el directorio de salida final en un nuevo atributo 
        self.base_output_directory = self.output_directory

        #-----------------input.invert logic---------------------#
        if sop_par is not None:
            invert_value_sopar = sop_par.get("input.invert", getattr(self, "input_invert", False))
        else:
            invert_value_sopar = None
        
        if mode == 'emission' and (invert_value_sopar=='true' or self.input_invert=='true'):
            logger.warning("Parameter 'input.invert=true' is not allowed in 'emission' mode. "
                           "Changing 'input.invert' to 'false'.")
            self.input_invert = 'false'
        elif mode == 'absorption':
            if (invert_value_sopar=='false' or self.input_invert=='false'):
                logger.warning("Parameter 'input.invert=false' is not allowed in 'absorption' mode. "
                               "Changing 'input.invert' to 'true'.")
                self.input_invert = 'true'
            elif (self.input_invert !='false' or self.input_invert is None):
                self.input_invert = 'true'
            else: 
                self.input_invert = 'true'
        elif mode == 'both' and run !=0:
            if (invert_value_sopar=='false' or self.input_invert=='false'):
                logger.warning("Parameter 'input.invert=false' is not allowed in 'both' mode for "
                               "the first run. Changing 'input.invert' to 'true'.")
            self.input_invert = 'true'
        elif mode == 'both' and run ==0:
            if (invert_value_sopar=='true' or self.input_invert=='true'):
                logger.warning("Parameter 'input.invert=true' is not allowed in 'both' mode for "
                               "the second run. Changing 'input.invert' to 'false'.")
            self.input_invert = 'false'

        #--------------------input.primaryBeam--------------------#
        if primary_beam is not None:         

            if (sop_par is not None 
                    and 'input.primaryBeam' in sop_par 
                    and sop_par['input.primaryBeam'] is not None):
                logger.warning(
                    f"Ignoring value '{sop_par['input.primaryBeam']}' for the  'input.primaryBeam "
                    "parameter provided in vía '-sop' comand."
                )
            if self.input_primaryBeam is not None:
                logger.warning(
                    f"Ignoring value '{self.input_primaryBeam}' provided in {self.sofia_file_path}."
                )
                       
            self.input_primaryBeam = primary_beam

        else:
            if (sop_par is not None 
                    and 'input.primaryBeam' in sop_par 
                    and sop_par['input.primaryBeam'] is not None):
                self.input_primaryBeam = sop_par['input.primaryBeam']

            if self.input_primaryBeam is not None:
                logger.warning(
                    f"Ignoring value '{self.input_primaryBeam}' provided in {self.sofia_file_path}."
                )
        

        if sop_par is not None:
            for key, value in sop_par.items():
                normalized_key = key.replace('.', '_')

                if key in {"input.data"}:
                    logger.warning(f"Ignoring parameter '{key}={value}' provided via -sop. If you "
                                   "want to change this, specify it in the input_data parameter in"
                                   " the config.yaml file.")
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
        Automatically configures attributes based on the FITS file header information.

        This method reads the FITS file specified in `self.input_data` and updates class attributes
        based on the header values. It calculates and sets parameters such as `scfind_kernelsXY`,
        `linker_minSizeXY`, and `reliability_minSNR` using specific rules derived from the header.

        
        Raises:
        ----------
        SystemExit: If `self.input_data` is not defined, is empty, or the FITS file does not exist.
        """

        if not hasattr(self, "input_data") or not self.input_data:
            logger.critical("El atributo 'input_data' no está definido o está vacío.")
            sys.exit(-1)

        fits_path = Path(self.input_data)


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
            self.scfind_kernelsXY = f"0, {x:.0f}, {2*x:.0f}"  # Format "0, x, 2x"
            self.linker_minSizeXY = round(x)  
        

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


    def run_sofia(self, adpalmap_config, mode=None, run=-1):        
        """
        Runs the SoFia tool in different modes (absorption, emission, or both) based on 
        the provided configuration.

        This method executes SoFia with the specified mode and handles the creation of 
        output directories, logging, and error handling. It also manages temporary files and 
        ensures proper cleanup.

        Parameters:
        ----------
        adpalmap_config: Config() class object with configuration from the configuration file..
        mode (str, optional): Mode to run SoFia in. Can be 'absorption', 'emission', or 'both'.
                              Defaults to None.
        run (int, optional): Indicates the run iteration when mode is 'both'. Used to handle 
                             sequential runs. -1 for single runs, 0 for the second run in 'both' 
                             mode. Defaults to -1.

        Raises:
        ----------
        SystemExit: If SoFia encounters an error during execution.
        """
        
        if (mode is not None and mode=='absorption'):

            self.output_directory = Path(f'{self.output_directory}_absorption')

            if not os.path.exists(self.output_directory):
                os.makedirs(Path(self.output_directory))
            else:
                logger.warning(f"The {Path(self.output_directory)} directory already exists."
                               " The SoFia outputs will be stored in this directory") 
            
            temp_file_path = self.create_tempfile()
            try:
                Logger.raw("================================")
                logger.info("Starting to run SoFia...")
                Logger.raw("================================")
                self.log_parameters()

                cmd = ["sofia", f"{temp_file_path}"]
                subprocess.run(
                    cmd,
                    text=True,
                    check=True,
                    capture_output=adpalmap_config.capture_outputs
                )
                Logger.raw("================================")
                logger.info("SoFia ended...")
                Logger.raw("================================")
            except subprocess.CalledProcessError as e:
                logger.error(f"Error running SoFia: {e}")
                logger.info(f"Exiting pipeline...")
                sys.exit(-1)
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            
        elif (mode is not None and mode=='emission'):

            self.output_directory = Path(f'{self.output_directory}_emission')
            
            if not os.path.exists(Path(self.output_directory)):
                os.makedirs(Path(self.output_directory))
            else:
                logger.warning(f"The {Path(self.output_directory)} directory already exists."
                               " The SoFia outputs will be stored in this directory") 

            temp_file_path = self.create_tempfile()
            try:
                Logger.raw("================================")
                logger.info("Starting to run SoFia...")
                Logger.raw("================================")
                self.log_parameters()
                
                cmd = ["sofia", f"{temp_file_path}"]
                subprocess.run(
                    cmd, 
                    text=True, 
                    check=True, 
                    capture_output=adpalmap_config.capture_outputs
                ) 

                Logger.raw("================================")
                logger.info("SoFia ended...")
                Logger.raw("================================")
            except subprocess.CalledProcessError as e:
                logger.error(f"Error running SoFia: {e}")
                logger.info(f"Exiting pipeline...")
                sys.exit(-1)
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
        
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
                    Logger.raw("================================")
                    logger.info("Starting to run SoFia...")
                    Logger.raw("================================")
                    self.log_parameters()

                    cmd = ["sofia", f"{temp_file_path}"]
                    subprocess.run(
                        cmd, 
                        text=True, 
                        check=True, 
                        capture_output=adpalmap_config.capture_outputs
                        ) 

                    Logger.raw("================================")
                    logger.info("SoFia ended...")
                    Logger.raw("================================")
                except subprocess.CalledProcessError as e:
                    logger.warning(f"SoFia has returned non-zero exit status: {e.returncode}, "
                                   "trying you finding absorption. SoFia will run again in the"
                                   " 'emission' mode without considering the absorption mask as"
                                   " a flag.cube.")
                finally:
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                    
            elif run==0:
                
                #Por defecto, el directorio de absorción será el self.output_directory_absorption. 
                # Uso el base_output_directory para buscarlo. Lo búsco, si no lo encuentra por 
                # fallo o porque no encontró absorciones, se mantiene igual. 
                if adpalmap_config.abs_flag_cube is not None and adpalmap_config.abs_flag_cube==True:
                    absorption_dir = Path(f"{self.base_output_directory}_absorption")
                    input_file_name = Path(self.input_data).stem
                    
                    flag_cube = absorption_dir / f"{input_file_name}_mask.fits"
                    if flag_cube.exists():
                        self.flag_cube = flag_cube
                    else:
                        logger.warning("There is no mask available from the absorption run")
                else:
                    logger.info("Ignoring absorption sources as input for flag.cube in the run"
                                " trying to find emissions sources.")

                self.output_directory = Path(f'{self.output_directory}_emission')
                if not os.path.exists(Path(self.output_directory)):
                    os.makedirs(Path(self.output_directory))
                else:
                    logger.warning(f"The {Path(self.output_directory)} directory already exists."
                                   " The SoFia outputs will be stored in this directory") 


                temp_file_path = self.create_tempfile()
                try:
                    Logger.raw("================================")
                    logger.info("Starting to run SoFia...")
                    Logger.raw("================================")
                    self.log_parameters()

                    cmd = ["sofia", f"{temp_file_path}"]
                    subprocess.run(
                        cmd, 
                        text=True, 
                        check=True, 
                        capture_output=adpalmap_config.capture_outputs
                        ) 

                    Logger.raw("================================")
                    logger.info("SoFia ended...")
                    Logger.raw("================================")            
                except subprocess.CalledProcessError as e:
                    logger.error(f"Error running SoFia: {e}")
                    logger.info(f"Exiting pipeline...")
                    sys.exit(-1)
                finally:
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)


    def create_tempfile(self):
        """
        Create a temporary file containing key-value pairs of the object's attributes.

        This method generates a temporary file in the same directory as the object's 
        `path` attribute (or the current directory if `path` is not defined). The file 
        will include all attributes of the object, except for those explicitly excluded 
        (`sofia_file_path`, `path`, and `base_output_directory`). Attribute names are 
        transformed by replacing underscores with dots.

        Returns:
        ----------
        str: The path to the created temporary file as a string.
        """

        original_path = Path(self.sofia_file_path) if hasattr(self, "sofia_file_path") else Path(".")
        temp_file_path = original_path.with_name(original_path.stem + "_tmp" + original_path.suffix)
        
        with open(temp_file_path, 'w') as tf:
            for key, value in self.__dict__.items():
                # Excluye estos atributos
                if key not in {"sofia_file_path", "path", "base_output_directory"}:
                    key_transformed = key.replace("_", ".")
                    tf.write(f"{key_transformed}={value}\n")

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
        for key, value in self.__dict__.items():
            # Excluye estos atributos
            if key not in {"sofia_file_path", "path", "base_output_directory"}:  
                key_transformed = key.replace("_", ".")
                Logger.raw_file(f"{key_transformed}={value}")


    def quality_assesment(self, mask_file=None):
        """
        Perform a quality assessment by visualizing and comparing masks and moment images.

        This method evaluates the quality of the data by generating visualizations of:
        - The moment 8 image.
        - The Sofia 2D mask (if available).
        - The ALMA archive mask (if provided via `adpalmap_datap`).

        Parameters:
        ----------
        adpalmap_datap: Datap() class object with configuration from the download parameter file.. 
                        If None, the ALMA archive mask will not be included in the assessment.
        output_fits (str, optional): Path to the output FITS file used to generate the 
                                    moment 8 image. Defaults to None.

        Returns:
        ----------
            None

        Raises:
        ----------
            ValueError: If the ALMA archive mask data has more than 4 dimensions, as this is not 
                        supported.
        """
        #Momento 8 del cubo inicial (input.data en config.yaml o descargado)
        mom8_ima = moment8_ima(self)

        #Máscara de lo obtenido por SoFiA
        sofia_output_dir = Path(self.output_directory)
        input_file_name = Path(self.input_data).stem
        file_2d_mask = sofia_output_dir / f"{input_file_name}_mask-2d.fits"
        
        if file_2d_mask.exits():
            pass
        else:
            logger.warning("2D-Mask file from SoFia not found in {self.ouput.directory}."
                           " Aborting the quality assesment"
            )
            return

        if mask_file is not None:
            with fits.open(mask_file) as hdul:
                mask_archive = np.any(hdul[0].data, axis=0).astype(int)
        
            if mask_archive.ndim == 4:
                mask_archive = np.squeeze(mask_archive, axis=0)
            elif mask_archive.ndim > 4:
                logger.critical(
                    "ADP Alma pipeline is not designed to handle data files with "
                    "more than 4 dimensions. Please open an issue on GitLab "
                    "https://gitlab.com/adp-group1/adp-alma-pipeline with your specific "
                    "case."
                )
            mask_archive_proj = np.any(mask_archive == 1, axis=0).astype(int)

    
        
        with fits.open(file_2d_mask) as hdul:
            sofia_2d_mask = hdul[0].data

        if mask_file is not None:
            fig, axs = plt.subplots(1, 3, figsize=(15, 6))
        else:
            fig, axs = plt.subplots(1, 2, figsize=(15, 6))
        
        ax = axs[0]
        ax.set_title("Moment 8 Image")
        ax.imshow(mom8_ima, cmap='gray', origin='lower')
        #ax.colorbar(label="Intensity")

        ax = axs[1]
        ax.set_title("Sofia 2D mask")
        ax.imshow(sofia_2d_mask, cmap='gray', origin='lower')
        #ax.colorbar(label="Intensity")

        if mask_file is not None:
            ax = axs[2]
            ax.set_title("Mask ALMA archive")
            ax.imshow(mask_archive_proj, cmap='gray', origin='lower')

        plt.tight_layout()
        plt.show()

        input("Press any key to continue...")
        

    