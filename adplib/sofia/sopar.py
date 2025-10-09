import os
import sys
import subprocess
#import tempfile 
import numpy as np
from pathlib import Path
from astropy.io import fits
import matplotlib.pyplot as plt
from adplib.exceptions import RecoverableError, RecoverableValueError, RecoverableFileNotFoundError


# Logger:
import logging
from adplib.logger import Logger
logger= Logger.get_logger()


SOFIA_PARAMETER = [
    "pipeline.verbose",
    "pipeline.pedantic",
    "pipeline.threads",
    "input.data",
    "input.primaryBeam",
    "input.region",
    "input.gain",
    "input.noise",
    "input.weights",
    "input.mask",
    "input.invert",
    "flag.region",
    "flag.catalog",
    "flag.radius",
    "flag.auto",
    "flag.threshold",
    "flag.log",
    "flag.cube",
    "contsub.enable",
    "contsub.order",
    "contsub.threshold",
    "contsub.shift",
    "contsub.padding",
    "scaleNoise.enable",
    "scaleNoise.mode",
    "scaleNoise.statistic",
    "scaleNoise.fluxRange",
    "scaleNoise.windowXY",
    "scaleNoise.windowZ",
    "scaleNoise.gridXY",
    "scaleNoise.gridZ",
    "scaleNoise.interpolate",
    "scaleNoise.scfind",
    "rippleFilter.enable",
    "rippleFilter.statistic",
    "rippleFilter.windowXY",
    "rippleFilter.windowZ",
    "rippleFilter.gridXY",
    "rippleFilter.gridZ",
    "rippleFilter.interpolate",
    "scfind.enable",
    "scfind.kernelsXY",
    "scfind.kernelsZ",
    "scfind.threshold",
    "scfind.replacement",
    "scfind.statistic",
    "scfind.fluxRange",
    "threshold.enable",
    "threshold.threshold",
    "threshold.mode",
    "threshold.statistic",
    "threshold.fluxRange",
    "linker.enable",
    "linker.radiusXY",
    "linker.radiusZ",
    "linker.minSizeXY",
    "linker.minSizeZ",
    "linker.maxSizeXY",
    "linker.maxSizeZ",
    "linker.minPixels",
    "linker.maxPixels",
    "linker.minFill",
    "linker.maxFill",
    "linker.positivity",
    "linker.keepNegative",
    "reliability.enable",
    "reliability.parameters",
    "reliability.threshold",
    "reliability.scaleKernel",
    "reliability.minSNR",
    "reliability.minPixels",
    "reliability.autoKernel",
    "reliability.iterations",
    "reliability.tolerance",
    "reliability.catalog",
    "reliability.plot",
    "reliability.plotExtra",
    "reliability.debug",
    "dilation.enable",
    "dilation.iterationsXY",
    "dilation.iterationsZ",
    "dilation.threshold",
    "parameter.enable",
    "parameter.wcs",
    "parameter.physical",
    "parameter.prefix",
    "parameter.offset",
    "output.directory",
    "output.file"
]


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
            " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
            "case."
        )
        raise

    fits_path = Path(adpalmap_sopar.input_data)

    if not fits_path.exists():
        logger.critical(
            f"File FITS '{fits_path}' does not exist. Fatal error. Please open an"
            " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
            "case.")
        raise

    with fits.open(fits_path) as hdul:
        data_cube = hdul[0].data

    if data_cube is None:
        error_msg = (
            f"The FITS file '{data_cube}' does not contain data in the primary HDU." 
            "Quality assement aborted."
        )
        logger.error(error_msg)
        raise RecoverableValueError(error_msg)

    if data_cube.ndim == 4:
        data_cube = np.squeeze(data_cube, axis=0)
    elif data_cube.ndim > 4:
        error_msg = (
            "ADP Alma pipeline is not designed to handle data files with more than 4 dimensions. "
            "Quality assesment aborted. "
            "Please open an issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git" 
            "with your specific case.")
        logger.error(error_msg)
        raise RecoverableValueError(error_msg)

    #Ahora el PrimaryBeam
    if hasattr(adpalmap_sopar, "input_primaryBeam") and adpalmap_sopar.input_primaryBeam:

        pb_path = Path(adpalmap_sopar.input_primaryBeam)

        if not pb_path.exists():
            logger.critical(
                f"File FITS '{pb_path}' does not exist. Fatal error. Please open an"
                " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your" 
                "specific case.")
            raise

        with fits.open(pb_path) as hdul:
            
            pb_cube = hdul[0].data

        if pb_cube is None:
            error_msg = (
                f"The FITS file '{pb_cube}' does not contain data in the primary HDU." 
                "Quality assement aborted."
            )
            logger.error(error_msg)
            raise RecoverableValueError(error_msg)
        
        if pb_cube.ndim == 4:
            pb_cube = np.squeeze(pb_cube, axis=0)
        elif pb_cube.ndim > 4:
            error_msg = (
                "ADP Alma pipeline is not designed to handle data files with more than 4 dimensions. "
                " Quality assesment aborted. "
                "Please open an issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git" 
                "with your specific case.")
            logger.error(error_msg)
            raise RecoverableValueError(error_msg)

        final_data_cube = data_cube * pb_cube
                
    else:
        logger.warning(
            "No data cube has been specified with Primary Beam information."
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


def parse_parfile(file_path):
    config = {}
    with open(file_path, 'r') as f:
        for line in f:     
            line = line.strip() 
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = map(str.strip, line.split('=', 1))
                config[key] = value
    return config


def compare_parfiles(file_path, temp_file_path):

    original = parse_parfile(file_path)
    modified = parse_parfile(temp_file_path)

    changes = {}
    for key, new_value in modified.items():
        old_value = original.get(key)
        if old_value != new_value:
            changes[key] = new_value

    return changes


def mask_float2int(file_path):

    file_path = Path(file_path)
    new_file_path = file_path.with_name(file_path.stem + '_int' + file_path.suffix)
    
    if new_file_path.exists():
        logger.info(f"Found cached mask integer file '{new_file_path}'")
        return new_file_path

    try:
        with fits.open(file_path) as hdul:
            data = hdul[0].data
            header = hdul[0].header

            if data.dtype.kind == 'f':
                int_data = np.round(data).astype(np.int16)
                header['BITPIX'] = 16
                new_hdu = fits.PrimaryHDU(data=int_data, header=header)
                new_hdu.writeto(new_file_path, overwrite=True)
                logger.info(
                    f"Integer-type version of the mask '{file_path}' has been created: "
                    f"{new_file_path}"
                )
                return new_file_path
            else:
                return file_path
            
    except Exception as e:
        logger.error(f"Mask conversion to integer failed. File: {file_path}. Error: {e}")
        return ""


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
            self.sofia_file_path = sofia_file_path

            if Path(sofia_file_path).exists():
                self.read_sofia_par_file(sofia_file_path)
                self.sofia_file_path = Path(sofia_file_path)

            else:
                error_msg = (
                    f"Download file {Path(sofia_file_path)} not found."
                    "No SoFiA parameter file was provided and the default parameter file "
                    f"{sofia_file_path} could not be found. Provide a valid SoFiA parameter "
                    "file or check if you have deleted or moved the default file."
                    )
                Logger.log_to_file(logging.ERROR, error_msg)
                raise FileNotFoundError(error_msg)
            
        else:
            sofia_file_path = Path(os.path.expanduser(sofia_file_path))
            self.sofia_file_path = sofia_file_path

            if not sofia_file_path.exists():
                error_msg = f"Parameter file '{sofia_file_path}' not found."
                Logger.log_to_file(logging.ERROR, error_msg)
                raise FileNotFoundError(error_msg)
            else:
                logger.info(f"The file in '{sofia_file_path}' have been loaded successfully")

            self.read_sofia_par_file(sofia_file_path)

    
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
                        
                    except: #CHANGE. Check is ValueError cover all the posibilities.
                        error_msg = (
                            f"The line '{line}' has not a valid format "
                                     "(module.parameter = value)."
                        )
                        Logger.log_to_file(logging.ERROR, error_msg)
                        raise ValueError(error_msg)


    def update_input_parameters(
            self, sop_par, 
            input_data, primary_beam=None, mask=None,
            mode=None, tap=None, run=-1, sofia_threads=1
        ):
        """
        Updates the attributes of the SoPar object with the values provided in sop_params.
        Manages input.data, output.directory, input.invert and input.primaryBeam priority 
        based on adpalmap_main, adpalmap_datap, sop_par and the attributes on self.

        Parameters:
        ----------
        sop_par (dict): Dictionary with parameters provided via -sop.



        Returns:
        ----------
        None: Updates the attributes of the SoPar object directly.
        """
        
        logger.info(f"Reading parameters. Mode: {self.sopar_mode}.")
        
        #----------------------input.data--------------------------#
        # The parameter 'imput.data' is managed in the main function.
        # No require action is needeed here
        if hasattr(self, 'input_data') and getattr(self, 'input_data') is not None:
            logger.warning(
                f"Ignoring parameter 'input.data' provided in the parameter file " 
                f"{self.sofia_file_path}. If you want to "
                "change this, specify it in the input_data_set or input_data_file parameter in "
                "the configuration file."
            )
        self.input_data = input_data
        #----------------------------------------------------------#
        
        #--------------------pipeline.threads----------------------#
        if (sop_par and "pipeline_threads" in sop_par) or self.pipeline_threads:
            logger.warning(
                "The parameter 'self.pipeline_threads' indicated in the terminal or in the "
                f" {self.sofia_file_path} will be ignored, this pipeline controls the flow "
                "of threds used with the parameter 'num_cores' and estimated the optimal"
                "use of these based on the number of cores and RAM available and the size "
                "of the files"
            )
        
        self.pipeline_threads = sofia_threads
        #----------------------------------------------------------#

        #--------------------output.directory----------------------#
        if sop_par and "output.directory" in sop_par: 
            self.output_directory = Path(sop_par["output.directory"])
        elif hasattr(self, "output_directory") and self.output_directory:  
            self.output_directory = Path(self.output_directory)
        else:
            self.output_directory = f"{Path.cwd().resolve()}/adpalmap_{input_data.stem}"
    
        self.base_output_directory = self.output_directory
        #----------------------------------------------------------#

        #----------------------input.invert------------------------#
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
        #----------------------------------------------------------#

        #--------------------input.primaryBeam---------------------#
        if primary_beam:      
            if (sop_par is not None 
                    and 'input.primaryBeam' in sop_par 
                    and sop_par['input.primaryBeam'] is not None):
                logger.warning(
                    f"Ignoring value '{sop_par['input.primaryBeam']}' for the 'input.primaryBeam' "
                    "parameter provided in vía '-sop' comand."
                )
            if(hasattr(self, "input_primaryBeam") and getattr(self, "input_primaryBeam") 
               is not None and self.input_primaryBeam != ""
            ):
                logger.warning(
                    f"Ignoring value '{self.input_primaryBeam}' provided in {self.sofia_file_path}."
                )
                       
            self.input_primaryBeam = primary_beam

        else:
            if (sop_par is not None 
                    and 'input.primaryBeam' in sop_par 
                    and sop_par['input.primaryBeam'] is not None
            ):
                #self.input_primaryBeam = sop_par['input.primaryBeam']
                logger.warning(
                    f"Ignoring value '{sop_par['input.primaryBeam']}' for the 'input.primaryBeam' "
                    "parameter provided vía '-sop' comand."
                )

            if(hasattr(self, "input_primaryBeam") and getattr(self, "input_primaryBeam") 
               is not None and self.input_primaryBeam != ""
            ):
                logger.warning(
                    f"Ignoring value '{self.input_primaryBeam}' provided in {self.sofia_file_path}."
                )
        #----------------------------------------------------------#

        #-----------------------input.mask-------------------------#
        if mask:      
            if (sop_par is not None 
                    and 'input.mask' in sop_par 
                    and sop_par['input.mask'] is not None):
                logger.warning(
                    f"Ignoring value '{sop_par['input.mask']}' for the 'input.mask' "
                    "parameter provided in vía '-sop' comand."
                )
            if(hasattr(self, "input_mask") and getattr(self, "input_mask") 
               is not None and self.input_mask != ""
            ):
                logger.warning(
                    f"Ignoring value '{self.input_mask}' provided in {self.sofia_file_path}."
                )
            
            #Comprueba si la máscara es descargada o no. Si no compruebo que sea tipo int()
            if tap:
                self.input_mask = mask
            else:
                self.input_mask = mask_float2int(mask)

        else:
            if (sop_par is not None 
                    and 'input.mask' in sop_par 
                    and sop_par['input.mask'] is not None
            ):
                #self.input_mask = sop_par['input.mask']
                logger.warning(
                    f"Ignoring value '{sop_par['input.mask']}' for the 'input.mask "
                    "parameter provided in vía '-sop' comand."
                )

            if(hasattr(self, "input_mask") and getattr(self, "input_mask") 
               is not None and self.input_mask != ""
            ):
                logger.warning(
                    f"Ignoring value '{self.input_mask}' provided in {self.sofia_file_path}."
                )

        #----------------------------------------------------------#

        #----------------------scfind.enable ----------------------#
        if mask:
            if (sop_par is not None 
                    and 'scfind.enable' in sop_par 
                    and sop_par['scfind.enable'] is not None
            ):
                logger.warning(
                    f"Ignoring value '{sop_par['scfind.enable']}' for the 'scfind.enable' "
                    "parameter provided in vía '-sop' comand."
                )
            self.scfind_enable = 'false'

        #----------------------------------------------------------#

        if sop_par is not None:

            for key, value in sop_par.items():
                normalized_key = key.replace('.', '_')

                if key in {"input.data"}:
                    logger.warning(
                        f"Ignoring parameter '{key}={value}' provided via -sop. If you "
                        "want to change this, specify it in the input_data_set or " \
                        "input_datafile parameter in the configuration file."
                    )
                    continue
                if key in {"output.directory", "input.invert"}: continue

                # Actualizar o añadir parámetros
                if hasattr(self, normalized_key):
                    setattr(self, normalized_key, value)
                else:
                    # Añadir como nuevo atributo si no existe
                    setattr(self, normalized_key, value)
                    logger.warning(f"Added new parameter '{key}' with value '{value}'.")

        logger.info(f"Parameters ready. Mode: {self.sopar_mode}.")


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

        logger.info(f"Auto-setup start. Mode: {self.sopar_mode}")

        if not hasattr(self, "input_data") or not self.input_data:
            logger.critical(
                "Attribute 'input_data' is not defined or is None. Fatal error. Please open an"
                " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
                "case."
            )
            raise

        fits_path = Path(self.input_data)


        if not fits_path.exists():
            logger.critical(
                f"File FITS '{fits_path}' does not exist. Fatal error. Please open an"
                " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
                "case.")
            raise

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
            logger.info(
                "The 'self.scfind_kernelsXY' parameter has been update to: "
                f"{self.scfind_kernelsXY}"
            )
            logger.info(
                "The 'self.linker_minSizeXY' parameter has been update to: "
                f"{self.linker_minSizeXY}"
            )

        # reliability.minSNR
        if "BMAJ" in header and "BMIN" in header:
            self.reliability_minSNR = 3.0 
            logger.info(
                "The 'self.reliability_minSNR' parameter has been update to: "
                f"{self.reliability_minSNR}"
            ) 

        else:            
            a = 3
            b = 3
            x = (3 / 2) * np.sqrt((np.pi * a * b) / np.log(2))
            self.reliability_minSNR = x
            logger.info(
                "The 'self.reliability_minSNR' parameter has been update to: "
                f"{self.reliability_minSNR}"
            )
                

        # Otros parámetros pueden ser añadidos según las reglas específicas...
        logger.info(f"Auto-setup DONE. Mode: {self.sopar_mode}")


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
        
        os.makedirs(self.output_directory, exist_ok=True)
        self.output_directory = Path(self.output_directory)

        if (mode is not None and mode=='absorption'):
            
            if self.output_filename:
                self.output_filename = f"absorption_{self.output_filename}"
            else:
                self.output_filename = f"absorption_{self.input_data.stem}"

            sopar_log_name = f"absorption_{Path(self.input_data).stem}_logfile.log"
            sopar_report = {
                "software_id" :'SoFiA-2',
                "PID": self.pid,
                "input_name": self.input_data.stem,
                "mode": self.sopar_mode,  
                "log_path": self.output_directory / sopar_log_name,
                "sofia_parfile" : self.sofia_file_path,
                "outputs" : {'images' : [], 'files': []}
            }

            if  sopar_report["log_path"].exists():
                try:
                    sopar_report["log_path"].unlink()
                except:
                    logger.warning(
                        "Error trying to delete existing log file. The new log "
                        "entries will be appended to it."
                    )

            
            temp_file_path = self.create_tempfile()
            sopar_report.update(
                {'sofia_par_changes' : compare_parfiles(self.sofia_file_path, temp_file_path)}
            )
            error = ''
            try:
                self.log_parameters()
                Logger.raw("================================")
                logger.info(
                    f"SoFia start. Mode: {self.sopar_mode}. Input data: "
                    f"{Path(self.input_data).stem}"
                )
                Logger.raw("================================")

                cmd = ["sofia", f"{temp_file_path}"]
                subprocess.run(
                    cmd,
                    text=True,
                    check=True,
                    capture_output=not adpalmap_config.verbose
                )
                Logger.raw("================================")
                logger.info(f"SoFia finished. Mode: {self.sopar_mode}")
                Logger.raw("================================")

                if self.adpalmap_config.html_report:
                    try:
                        self.report_outputs(sopar_report)  
                    except Exception as e:
                        logger.warning(f"Error adding outputs for the html report (non-critical): {e}")

            except subprocess.CalledProcessError as e:
                error = str(e)
                logger.error(f"Error running SoFia. Mode: {self.sopar_mode}. Error: {e}")
                logger.info(f"SoFia execution aborted. Mode: {self.sopar_mode}.")
                sys.exit(-1)

            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

                sopar_report.update({"error": e})
                return sopar_report


        elif (mode is not None and mode=='emission'):

            if self.output_filename:
                self.output_filename = f"emission_{self.output_filename}"
            else:
                self.output_filename = f"emission_{self.input_data.stem}"

            
            sopar_log_name = f"emission_{self.input_data.stem}_logfile.log"
            sopar_report = {
                "software_id" :'SoFiA-2',
                "PID": self.pid,
                "input_name": self.input_data.stem,
                "mode": self.sopar_mode,  
                "log_path": self.output_directory / sopar_log_name,
                "sofia_parfile" : self.sofia_file_path,
                "outputs" : {'images' : [], 'files': []}
            }

            if  sopar_report["log_path"].exists():
                try:
                    sopar_report["log_path"].unlink()
                except:
                    logger.warning(
                        "Error trying to delete existing log file. The new log "
                        "entries will be appended to it."
                    )

            temp_file_path = self.create_tempfile()
            sopar_report.update(
                {'sofia_par_changes' : compare_parfiles(self.sofia_file_path, temp_file_path)}
            )
            error = ''
            try:
                self.log_parameters()
                Logger.raw("================================")
                logger.info(
                    f"SoFia start. Mode: {self.sopar_mode}. Input data: "
                    f"{Path(self.input_data).stem}"
                )
                Logger.raw("================================")
                print("AQUIIII", self.output_filename)
                cmd = ["sofia", f"{temp_file_path}"]
                subprocess.run(
                    cmd, 
                    text=True, 
                    check=True, 
                    capture_output=not adpalmap_config.verbose
                ) 

                Logger.raw("================================")
                logger.info(f"SoFia finished. Mode: {self.sopar_mode}")
                Logger.raw("================================")
                
                if adpalmap_config.html_report:
                    try:
                        self.report_outputs(sopar_report)  
                    except Exception as e:
                        logger.warning(f"Error adding outputs for the html report (non-critical): {e}")

            except subprocess.CalledProcessError as e:
                error = str(e)
                logger.error(f"Error running SoFia. Mode: {self.sopar_mode}. Error: {e}")
                logger.info(f"SoFia execution aborted. Mode: {self.sopar_mode}.")
                sys.exit(-1)
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                sopar_report.update({"error": error})
                return sopar_report    
                    
        
        elif (mode is not None and mode==mode == 'both'):
            if run!=0:
                
                if self.output_filename:
                    self.output_filename = f"absorption_{self.output_filename}"
                else:
                    self.output_filename = f"absorption_{self.input_data.stem}"

                sopar_log_name = f"absorption_{Path(self.input_data).stem}_logfile.log"
                sopar_report = {
                    "software_id" :'SoFiA-2',
                    "PID": self.pid,
                    "input_name": self.input_data.stem,
                    "mode": self.sopar_mode,  
                    "log_path": self.output_directory / sopar_log_name,
                    "sofia_parfile" : self.sofia_file_path,
                    "outputs" : {'images' : [], 'files': []}
                }

                if  sopar_report["log_path"].exists():
                    try:
                        sopar_report["log_path"].unlink()
                    except:
                        logger.warning(
                            "Error trying to delete existing log file. The new log "
                            "entries will be appended to it."
                        )

                temp_file_path = self.create_tempfile()
                sopar_report.update(
                    {'sofia_par_changes' : compare_parfiles(self.sofia_file_path, temp_file_path)}
                )
                error = ''
                try:
                    self.log_parameters()
                    Logger.raw("================================")
                    logger.info(
                        f"SoFia start. Mode: {self.sopar_mode}. Input data: "
                        f"{Path(self.input_data).stem}"
                    )
                    Logger.raw("================================")

                    cmd = ["sofia", f"{temp_file_path}"]
                    subprocess.run(
                        cmd, 
                        text=True, 
                        check=True, 
                        capture_output=not adpalmap_config.verbose
                        ) 

                    Logger.raw("================================")
                    logger.info(f"SoFia finished. Mode: {self.sopar_mode}")
                    Logger.raw("================================")
                    try:
                        self.report_outputs(sopar_report)  
                    except Exception as e:
                        logger.warning(f"Error adding outputs for the html report (non-critical): {e}")

                except subprocess.CalledProcessError as e:
                    error = str(e)
                    logger.error(f"Error running SoFia. Mode: {self.sopar_mode}. Error: {e}")
                    logger.info(f"SoFiA will try to run again in mode: emission.")
                finally:
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                    sopar_report.update({"error": error})
                    return sopar_report 

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
                        logger.warning("There is no mask available from the absorption run. "
                                       "The parameter 'flag_cube' will not be used")
                else:
                    logger.info("The mask from the absorption run will not be used as "
                                "a 'flag_cube'. "
                                f"Mode: {self.sopar_mode}.")

                if self.output_filename:
                    self.output_filename = f"emission_{self.output_filename}"
                else:
                    self.output_filename = f"emission_{self.input_data.stem}"
                
                sopar_log_name = f"emission_{Path(self.input_data).stem}_logfile.log"
                sopar_report = {
                    "software_id" :'SoFiA-2',
                    "PID": self.pid,
                    "input_name": self.input_data.stem,
                    "mode": self.sopar_mode,  
                    "log_path": self.output_directory / sopar_log_name,
                    "sofia_parfile" : self.sofia_file_path,
                    "outputs" : {'images' : [], 'files': []}
                }

                if  sopar_report["log_path"].exists():
                    try:
                        sopar_report["log_path"].unlink()
                    except:
                        logger.warning(
                            "Error trying to delete existing log file. The new log "
                            "entries will be appended to it."
                        )

                temp_file_path = self.create_tempfile()
                sopar_report.update(
                    {'sofia_par_changes' : compare_parfiles(self.sofia_file_path, temp_file_path)}
                )
                error = ''
                try:
                    self.log_parameters()
                    Logger.raw("================================")
                    logger.info(
                        f"SoFia start. Mode: {self.sopar_mode}. Input data: "
                        f"{Path(self.input_data).stem}"
                    )
                    Logger.raw("================================")

                    cmd = ["sofia", f"{temp_file_path}"]
                    subprocess.run(
                        cmd, 
                        text=True, 
                        check=True, 
                        capture_output=not adpalmap_config.verbose
                        ) 

                    Logger.raw("================================")
                    logger.info(f"SoFia finished. Mode: {self.sopar_mode}")
                    Logger.raw("================================")  
                    try:
                        self.report_outputs(sopar_report)  
                    except Exception as e:
                        logger.warning(f"Error adding outputs for the html report (non-critical): {e}")

                except subprocess.CalledProcessError as e:
                    error = str(e)
                    logger.error(f"Error running SoFia. Mode: {self.sopar_mode}. Error: {e}")
                    logger.info(f"SoFia execution aborted. Mode: {self.sopar_mode}.")
                    sys.exit(-1)
                finally:
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                    sopar_report.update({"error": error})
                    return sopar_report 
                

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

        original_path = Path.cwd()     
        temp_file_name = (
            self.sofia_file_path.stem + "_tmp_PID" + str(self.pid) + self.sofia_file_path.suffix
        )
        temp_file_path = original_path / temp_file_name


        with open(temp_file_path, 'w') as tf:
            for key, value in self.__dict__.items():
                # Excluye estos atributos
                if key not in {
                    "sofia_file_path", 
                    "path", 
                    "base_output_directory", 
                    "sopar_mode", 
                    "pid"
                }:
                    key_transformed = key.replace("_", ".")
                    tf.write(f"{key_transformed}={value}\n")

        logger.info(
            "Creating temporary SoFiA parameter file based on the parameter file "
            f"{self.sofia_file_path}."
            )
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

        for par in SOFIA_PARAMETER:
            par_underscore = par.replace(".", "_") 
            
            if hasattr(self, par_underscore):
                Logger.raw_file(f"[{self.pid}]{par}={getattr(self, par_underscore)}")
            else:
                Logger.raw_file(f"[{self.pid}]{par}= ")


    def report_outputs(self, sopar_report):
        
        mode = sopar_report["mode"]

        sopar_report['outputs']['images'].append({
            "type": "rel",
            "path": self.output_directory / f"{mode}_{self.input_data.stem }_rel.eps",
            "description": "Realibiliy Plot",
            "software-id": "sofia"
        })
        sopar_report['outputs']['images'].append({
            "type": "skellman",
            "path": self.output_directory / f"{mode}_{self.input_data.stem}_skellam.eps",
            "description": "Skellman Plot",
            "software-id": "sofia"
        })
        sopar_report['outputs']['files'].append({
            "type": "par_file",
            "path": self.sofia_file_path,
            "format": ".par",
            "software-id": "sofia"
        })    
        sopar_report['outputs']['files'].append({
            "type": "catalog_txt",
            "path": self.output_directory / f"{mode}_{self.input_data.stem}_cat.txt",
            "format": "txt",
            "software-id": "sofia"
        })
        sopar_report['outputs']['files'].append({
            "type": "catalog_xml",
            "path": self.output_directory / f"{mode}_{self.input_data.stem}_xlm.txt",
            "format": "xlm",
            "software-id": "sofia"
        })


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

        logger.info(f"Quality assesment start. Mode: {self.sopar_mode}.")

        # At the moment there is just one singles images but do it in this way allows add
        # additional images easly in the future
        qa_report = {
                "software_id" :'QA',
                "PID": self.pid,
                "input_name": self.input_data.stem,
                "mode": self.sopar_mode,  
                "log_path": "",
                "outputs" : {'images' : [], 'files': []}
            }

        #Momento 8 del cubo inicial (input.data en config.yaml o descargado)
        mom8_ima = moment8_ima(self)

        #Máscara de lo obtenido por SoFiA
        sofia_output_dir = Path(self.output_directory)
        input_file_name = Path(self.input_data).stem
        file_2d_mask = sofia_output_dir / f"{self.sopar_mode}_{input_file_name}_mask-2d.fits"
        
        if file_2d_mask.exists():
            pass
        else:
            logger.warning(
                f"2D-Mask file from SoFia not found in {self.output_directory}."            
            )
            logger.info("Quality assesment aborted.")
            return qa_report
        
        if mask_file:
            with fits.open(mask_file) as hdul:
                mask_archive = np.any(hdul[0].data, axis=0).astype(int)
        
            if mask_archive.ndim == 4:
                mask_archive = np.squeeze(mask_archive, axis=0)
            elif mask_archive.ndim > 4:
                logger.critical(
                    "ADP Alma pipeline is not designed to handle data files with "
                    "more than 4 dimensions. Please open an issue on "
                    "https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
                    "case."
                )
            mask_archive_proj = np.any(mask_archive == 1, axis=0).astype(int)

    
        
        with fits.open(file_2d_mask) as hdul:
            sofia_2d_mask = hdul[0].data

        if mask_file:
            fig, axs = plt.subplots(1, 3, figsize=(15, 6))
        else:
            fig, axs = plt.subplots(1, 2, figsize=(15, 6))
        
        ax = axs[0]
        ax.set_title("Moment 8 Image")
        ax.imshow(mom8_ima, cmap='viridis', origin='lower')
        #ax.colorbar(label="Intensity")

        ax = axs[1]
        ax.set_title("Sofia 2D mask")
        ax.imshow(sofia_2d_mask, cmap='viridis', origin='lower')
        #ax.colorbar(label="Intensity")

        if mask_file:
            ax = axs[2]
            ax.set_title("Mask ALMA archive")
            ax.imshow(mask_archive_proj, cmap='viridis', origin='lower')

        qa_output_dir = Path(self.output_directory) / "quality_assesment_products"
        qa_output_dir.mkdir(parents=True, exist_ok=True)  
        qa_output_file = Path(f"{qa_output_dir / Path(self.input_data).stem}_QA.png")


        try:
            plt.savefig(qa_output_file, bbox_inches='tight')
            logger.info(
                f"QA file saved in {qa_output_dir}. Quality assesment completed "
                f"successfully. Mode: {self.sopar_mode}"
                )
            
            qa_report['outputs']['images'].append({
            "type": "mom8",
            "path": qa_output_file,
            "description": "Moment 8 image",
            "software-id": "qa"
            })
            return qa_report
        except Exception as e:
            logger.warning(f"Something went wrong while saving QA file: {e}")
            logger.info(f"Quality assement aborted . Mode: {self.sopar_mode}")
            return qa_report
            


'''
    def add_outputs(self, sopar_report):
    
        """Añade outputs al reporte, manejando archivos faltantes."""
        expected_outputs = {
            "images": [
                {
                    "type": "rel",
                    "path": self.output_directory / f"{self.input_data.stem}_rel.eps",
                    "description": "Reliability Plot"
                },
                {
                    "type": "skellam",
                    "path": self.output_directory / f"{self.input_data.stem}_skellam.eps",
                    "description": "Skellam Plot"
                }
            ],
            "files": [
                {
                    "type": "catalog_txt",
                    "path": self.output_directory / f"{self.input_data.stem}_cat.txt",
                    "format": "txt"
                },
                {
                    "type": "catalog_xml",
                    "path": self.output_directory / f"{self.input_data.stem}_cat.xml",
                    "format": "xml"
                }
            ]
        }

        registered_outputs = {"images": [], "files": []}
        
        for category, items in expected_outputs.items():
            for item in items:
                try:
                    if item["path"].exists():
                        registered_outputs[category].append(item)
                    else:
                        logger.debug(f"Output file not found: {item['path']}")
                except Exception as e:
                    logger.warning(f"Error checking output {item['path']}: {str(e)}")
        
        sopar_report["outputs"] = registered_outputs
'''

        
        

    