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
    "filter.discardNegative",
    "filter.minSNR",
    "filter.minPixels",
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
    "reliability.enable",
    "reliability.parameters",
    "reliability.threshold",
    "reliability.scaleKernel",
    "reliability.autoKernel",
    "reliability.iterations",
    "reliability.tolerance",
    "reliability.catalog",
    "reliability.plot",
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
    "output.filename",
    "output.dataFormat",
    "output.writeCatASCII",
    "output.writeCatXML",
    "output.writeCatSQL",
    "output.writeDiagnosticPlot"
    "output.writeKarma",
    "output.writeNoise",
    "output.writeFiltered",
    "output.writeMask",
    "output.writeMask2d",
    "output.writeRawMask",
    "output.writeMoments",
    "output.writeCubelets",
    "output.writePV",
    "output.marginAperSpec",
    "output.marginCubeletsXY",
    "output.marginCubeletsZ",
    "output.thresholdMom12",
    "output.overwrite",

]


def moment8_ima(adpalmap_sopar, mode):

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

    # The relevant information about primary beam is on 'primary_beam'
    # the input_primaryBeam parameter is subject to changes
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


    if mode == "absorption":
        logger.info(f"Creating moment 8 image for absorption (minimum along z-axis)")
        projection = np.min(final_data_cube, axis=0)
        projection_viz = -projection  
    else:  
        logger.info(f"Creating moment 8 image for emission (maximum along z-axis)")
        projection = np.max(final_data_cube, axis=0)
        projection_viz = projection

    return projection_viz


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
        self.group = False

        
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
            run=-1,
        ):
        """
        Updates the attributes of the SoPar object with the values provided in sop_params and
        manage some key parameters


        Parameters:
        ----------
        sop_par (dict): Dictionary with parameters provided via -sop.

        Returns:
        ----------
        None: Updates the attributes of the SoPar object directly.
        """
        
        logger.info(
            f"Reading parameters in {self.sofia_file_path}. Mode: {self.mode}."
            )
        
        ##############################################################################################
        if sop_par is not None:

            for key, value in sop_par.items():
                normalized_key = key.replace('.', '_')

                if key in {
                    "input.data",
                    "input.primaryBeam",
                    "input.mask",
                    "pipeline.threads",
                    "output.directory", 
                }: continue

                # Actualizar o añadir parámetros
                if hasattr(self, normalized_key):
                    setattr(self, normalized_key, value)
                else:
                    # Añadir como nuevo atributo si no existe
                    setattr(self, normalized_key, value)
                    logger.warning(f"Added new parameter '{key}' with value '{value}'.")
        ##############################################################################################
        
        ###########################-------------input.data--------------##############################
        # The parameter 'input.data' is managed in the main function.
        if (sop_par is not None 
                    and 'input.data' in sop_par 
                    and sop_par['input.data'] is not None):
                logger.warning(
                    f"Ignoring value '{sop_par['input.data']}' for the 'input_data' parameter "
                    "provided vía '-sop' comand. This must be set in the "
                    "'input_dataset' or 'input_file' parameters in the "
                    f"{self.adpalmap_config.config_path} file"
                )
        if hasattr(self, 'input_data') and getattr(self, 'input_data') is not None:
            logger.warning(
                f"Ignoring value '{self.input_data}' for the 'input.data' parameter provided "
                f"in the parameter file {self.sofia_file_path}.  This must be set in the "
                f"'input_dataset' or 'input_file' parameters in the {self.adpalmap_config.config_path}"
                " file"
            )
                
        self.input_data = input_data
        ##############################################################################################

        #######################-------------input.primaryBeam--------------###########################
             
        if (sop_par is not None 
                and 'input.primaryBeam' in sop_par 
                and sop_par['input.primaryBeam'] is not None):
            logger.warning(
                f"Ignoring value '{sop_par['input.primaryBeam']}' for the 'input.primaryBeam' "
                "parameter provided vía '-sop' comand. This must be set in the 'input_dataset'"
                f" or 'input_file' parameters in the {self.adpalmap_config.config_path} file"
            )
        if(hasattr(self, "input_primaryBeam") and  self.input_primaryBeam):
            logger.warning(
                f"Ignoring value '{self.input_primaryBeam}' for the 'input.primaryBeam' parameter"
                f" provided in {self.sofia_file_path}. This must be set in the 'input_dataset'"
                f" or 'input_file' parameters in the {self.adpalmap_config.config_path} file"
            )
            
        # If exist it will always be used
        if primary_beam: 
            logger.info(f"The primary beam '{primary_beam}' set as 'input.primaryBeam'.")
            self.input_primaryBeam = primary_beam
        else:
            # It should be "" at this point. No changes need it
            pass
        ##############################################################################################

        ###########################-------------input.mask--------------##############################     
        if (sop_par is not None 
                and 'input.mask' in sop_par 
                and sop_par['input.mask'] is not None):
            logger.warning(
                f"Ignoring value '{sop_par['input.mask']}' for the 'input.mask' parameter provided "
                "vía '-sop' comand. This must be set in the 'input_dataset'"
                f" or 'input_file' parameters in the {self.adpalmap_config.config_path} file"
            )
        if(hasattr(self, "input_mask") and self.input_mask):
            logger.warning(
                f"Ignoring value '{self.input_mask}' for the 'input.mask' parameter provided "
                f"in the parameter file {self.sofia_file_path}. This must be set in the "
                "'input_dataset' or 'input_file' parameters in the "
                f"{self.adpalmap_config.config_path} file"
            )
        
        if mask:
            #Comprueba si la máscara es descargada o no. Si no compruebo que sea tipo int()
            if self.adpalmap_config.enable_tap_service:
                if self.adpalmap_config.use_mask:
                    logger.info(f"The mask '{mask}' set as 'input.mask'.")
                    self.input_mask = mask
                else:
                    logger.warning(
                        f"'use_mask' set to False: the mask '{mask}' will no be used as 'input.mask'"
                        )
                    self.input_mask = ""
            else:
                if self.adpalmap_config.use_mask:
                    self.input_mask = mask_float2int(mask)
                else:
                    logger.warning(
                        f"'use_mask' set to False: the mask '{mask}' will no be used as 'input.mask'"
                        )
                    self.input_mask = ""                    
        else:
            pass

        ##############################################################################################

        ##########################-------------input.invert--------------#############################
        if sop_par is not None and "input.invert" in sop_par:
            input_invert_value = sop_par["input.invert"]
        else:
            input_invert_value = getattr(self, "input_invert")

        
        if self.adpalmap_config.run_mode == 'emission':
            if input_invert_value == 'true':
                logger.warning("Parameter 'input.invert=true' is not allowed in 'emission' mode. "
                            "Setting 'input.invert' to 'false'.")
                self.input_invert = 'false'
            else:
                self.input_invert = 'false'   

        elif self.adpalmap_config.run_mode == 'absorption':
            if input_invert_value == 'false':
                logger.warning("Parameter 'input.invert=false' is not allowed in 'absorption' mode. "
                            "Setting 'input.invert' to 'true'.")
                self.input_invert = 'true'
            else:
                self.input_invert = 'true'
          
        elif self.adpalmap_config.run_mode == 'both' and run != 0:
            if input_invert_value == 'false':
                logger.warning("Parameter 'input.invert=false' is not allowed in 'both' mode for "
                            "the first run. Setting 'input.invert' to 'true'.")
                self.input_invert = 'true'
            else:
                self.input_invert = 'true'
                
        elif self.adpalmap_config.run_mode == 'both' and run == 0:
            if input_invert_value == 'true':
                logger.warning("Parameter 'input.invert=true' is not allowed in 'both' mode for "
                            "the second run. Setting 'input.invert' to 'false'.")
                self.input_invert = 'false'
            else:
                self.input_invert = 'false'
                
        else:
            logger.critical("Oops, you should not have come here. Please open an"
                            " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with "
                            "your specific case.")
        
        ##############################################################################################        
        
        #########################-------------scfind.enable--------------#############################
        if (mask and self.adpalmap_config.use_mask):
            logger.info("The 'scfind.enable' parameter has set to 'false'. Setting a mask file in "
                        "'input.mask' and True in 'use_mask' parameter assumes that no further "
                        "sources need to be searched or discarded.")
            logger.info("The 'reliability.enable' parameter has set to 'false'. Setting a mask file in "
                        "'input.mask' and True in 'use_mask' parameter assumes that no further "
                        "sources need to be searched or discarded.")
            logger.warning("Carefully review the parameters set in the linker section")
            self.scfind_enable = 'false'
            self.reliability_enab
            if (sop_par and 'scfind.enable' in sop_par):
                logger.warning(
                    f"Ignoring value '{sop_par['scfind.enable']}' for the 'scfind.enable' "
                    "parameter provided in vía '-sop' comand."
                )
            

        ##############################################################################################

        ########################-------------pipeline.threads--------------###########################
        if (sop_par and "pipeline_threads" in sop_par) or self.pipeline_threads:
            logger.warning(
                "The parameter 'self.pipeline_threads' indicated via -sop or in the "
                f" {self.sofia_file_path} will be ignored. This pipeline manages the threads "
                "used based on the 'num_cores' parameter, the number of datasets, and their size. "
                "Based on this, the optimal thread usage is estimated according to the number of "
                "available cores and RAM."
            )
        
        self.pipeline_threads = self.sofia_threads
        ##############################################################################################

        ########################-------------output.directory--------------########################### 
            
        if sop_par and "output.directory" in sop_par: 
            logger.warning(
                    f"Ignoring value '{sop_par['output.directory']}' for the 'input_data' parameter "
                    "provided vía '-sop' comand. This must be set in the "
                    f"'output.directory' parameter in the {self.adpalmap_config.config_path} file"
            )
        if hasattr(self, "output_directory") and self.output_directory:  
            logger.warning(
                f"Ignoring value '{self.output_directory}' for the 'output.directory' parameter" 
                f" provided in the parameter file {self.sofia_file_path}.  This must be set in " 
                f"the 'output_directory' parameter in the {self.adpalmap_config.config_path}"
                " file"
            )

        self.output_directory = self.adpalmap_config.output_dir / f"espada_{input_data.stem}"
        ##############################################################################################

        ########################--------------output.filename--------------###########################       
        if self.adpalmap_config.run_mode == 'absorption':
            if hasattr(self, "output_filename") and self.output_filename:
                self.output_filename = f"absorption_{self.output_filename}"
                sopar_log_path = f"{self.output_filename}_logfile.log"
            else:
                self.output_filename = f"absorption_{self.input_data.stem}"
                sopar_log_path = f"absorption_{self.input_data.stem}_logfile.log"

        if self.adpalmap_config.run_mode == 'emission':
            if hasattr(self, "output_filename") and self.output_filename:
                self.output_filename = f"emission_{self.output_filename}"
                sopar_log_path = f"{self.output_filename}_logfile.log"
            else:
                self.output_filename = f"emission_{self.input_data.stem}"
                sopar_log_path = f"emission_{self.input_data.stem}_logfile.log"  

        if self.adpalmap_config.run_mode == 'both' and run!=0:
            if hasattr(self, "output_filename") and self.output_filename:
                self.output_filename = f"absorption_{self.output_filename}"
                sopar_log_path = f"{self.output_filename}_logfile.log"
            else:
                self.output_filename = f"absorption_{self.input_data.stem}"
                sopar_log_path = f"absorption_{self.input_data.stem}_logfile.log"

        elif self.adpalmap_config.run_mode == 'both' and run==0:
            if hasattr(self, "output_filename") and self.output_filename:
                # Safe the original 'output.filename' for 'flag.cube'
                self.original_output_filename = self.output_filename
                self.output_filename = f"emission_{self.output_filename}"
                sopar_log_path = f"{self.output_filename}_logfile.log"
            else:
                self.original_output_filename = self.input_data.stem
                self.output_filename = f"emission_{self.input_data.stem}"
                sopar_log_path = f"emission_{self.input_data.stem}_logfile.log" 

        # Safe the logfile and make sure that is Path() object
        self.sopar_logfile = self.output_directory / sopar_log_path
        ##############################################################################################

        ########################--------------output.writeCAT---------------##########################
        if (self.adpalmap_config.enable_sip and 
            self.output_writeCatASCII=='false' and 
            self.output_writeCatXML=='false'):
            logger.warning("Parameter combination not allowed. Either 'self.output_writeCatASCII' or"
                           " 'self.output_writeCatXML' parameters must be set to 'true' if " 
                           "'enable_sip' is set to True. "
                           "By default 'self.output_writeCatASCII' parameter will be set to 'true'")
            
            self.output_writeCatASCII = 'true'

        else:
            pass
        ##############################################################################################


        logger.info(f"Parameters updated. Mode: {self.mode}.")


    def update_group_parameters(self, group_mask):

        """
        Updates the attributes of the SoPar object to being able to Run SoFiA for Groups.

        Parameters:
        ----------
        sop_par (dict): Dictionary with parameters provided via -sop.

        Returns:
        ----------
        None: Updates the attributes of the SoPar object directly.
        """

        logger.info(f"Updating SoFiA parameters. Mode: {self.mode}.")
        
        self.input_mask = group_mask

        if self.mode == "absorption":
            self.input_invert = "true"
        elif self.mode == "emission":
            self.input_invert = "false"

        self.scfind_enable = "false"

        self.linker_enable = "false" 

        self.reliability_enable = "false"

        self.output_filename = f"group_{self.output_filename}"
        
        # '{self.output_filename}' Already contain prefixx 'group_'
        self.sopar_logfile = self.output_directory / f"{self.output_filename}_logfile.log"

        logger.info(f"Parameter ready. Mode: {self.mode}.")


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

        logger.info(f"Auto-setup start. Mode: {self.mode}")

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

        # filter.minSNR
        if "BMAJ" in header and "BMIN" in header:
            self.filter_minSNR = 3.0 
            logger.info(
                "The 'self.filter_minSNR' parameter has been update to: "
                f"{self.filter_minSNR}"
            ) 

        else:            
            a = 3
            b = 3
            x = (3 / 2) * np.sqrt((np.pi * a * b) / np.log(2))
            self.filter_minSNR = x
            logger.info(
                "The 'self.filter_minSNR' parameter has been update to: "
                f"{self.filter_minSNR}"
            )
                

        # Otros parámetros pueden ser añadidos según las reglas específicas...
        logger.info(f"Auto-setup done. Mode: {self.mode}")


    def run_sofia(self, run=-1):        
        """
        Runs the SoFia tool in different modes (absorption, emission, or both) based on 
        the provided configuration.

        This method executes SoFia with the specified mode and handles the creation of 
        output directories, logging, and error handling. It also manages temporary files and 
        ensures proper cleanup.

        Parameters:
        ----------
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
    ##############################################################################################
        # Set source from absorption run as a 'flag_cube' in the emission run in the 'both' mode
        if self.adpalmap_config.run_mode == "both" and run ==0:

            if self.adpalmap_config.abs_flag_cube:                    
                flag_cube = self.output_directory / f"absorption_{self.original_output_filename}_mask.fits"

                if flag_cube.exists():
                    self.flag_cube = flag_cube
                    logger.info("The mask obtained from the absorption run will be used as"
                                " input for the 'flag.cube' parameter")
                else:
                    logger.warning("There is no mask available from the absorption run. "
                                    "The parameter 'flag_cube' will not be used")
            else:
                logger.info("The mask from the absorption run will not be used as "
                            "a 'flag_cube'. "
                            f"Mode: {self.mode}.")
    ##############################################################################################

        # Create a SoFiA-2 report 
        sopar_report = {
                "software_id" :'SoFiA-2',
                "PID": self.pid,
                "input_name": self.input_data.stem,
                "mode": self.mode,  
                "log_path": self.sopar_logfile,
                "sofia_parfile" : self.sofia_file_path,
                "outputs" : {'images' : [], 'files': []}
            }
            
        # Create a temp file with the updated parameters for SoFiA
        temp_file_path = self.create_tempfile()

        # Update the report 
        sopar_report.update(
            {'sofia_par_changes' : compare_parfiles(self.sofia_file_path, temp_file_path)}
        )

        # Remove existing log file
        if  sopar_report["log_path"].exists():
            try:
                sopar_report["log_path"].unlink()
            except:
                logger.warning(
                    "Error trying to delete existing log file. The new log "
                    "entries will be appended to it."
                )

        error = ''

    ##############################################################################################
    
        try:
            # Safe in the log the parameters fotr the run 
            self.log_parameters()
            Logger.raw("================================")
            logger.info(
                f"SoFia start. Mode: {self.mode}. Input data: "
                f"{Path(self.input_data).stem}"
            )
            Logger.raw("================================")

            # Execute SoFiA-2 
            cmd = ["sofia", f"{temp_file_path}"]
            subprocess.run(
                cmd,
                text=True,
                check=True,
                capture_output=not self.adpalmap_config.verbose
            )
            Logger.raw("================================")
            logger.info(f"SoFia finished. Mode: {self.mode}")
            Logger.raw("================================")

            # Safe the 3D-mask for the group module
            if self.adpalmap_config.enable_group:
                self.mask3d = (
                    self.output_directory 
                    / f"{self.mode}_{self.input_data.stem}_mask.fits"
                )

        except subprocess.CalledProcessError as e:
            if self.adpalmap_config.enable_group:
                # If this attribute change from None to any other, find_mask_sofia() in group.py
                # have to be changed as well
                self.mask3d = None
            error = str(e)
            logger.error(
                f"Error running SoFia. Mode: {self.mode}. Error: {e}"
            )
            logger.info(f"SoFia execution aborted")
            
            if self.adpalmap_config.run_mode == 'both' and run!=0:
                # Exits the function without propagating an error to run in 'absorption'
                logger.info(f"SoFiA will try to run again in mode: emission.")

        finally:
            # This step should be here if we want to add outputs from SoFiA-2 no matter if it fails or
            # not. The reliability and diagnostic plot should always be in the report.  
            # Add outputs for the html report
            if self.adpalmap_config.make_report:
                try:
                    self.report_outputs(sopar_report)  
                except Exception as e:
                    logger.warning(f"Error adding outputs for the html report (non-critical): {e}")

            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            sopar_report.update({"error": error})
            return sopar_report
        
        ##############################################################################################
                

    def create_tempfile(self):
        """
        Create a temporary file containing key-value pairs of the object's attributes.

        This method generates a temporary file in the same directory as the object's 
        `path` attribute (or the current directory if `path` is not defined). The file 
        will include all parameters defined in SOFIA_PARAMETER and the values of the 
        corresponding attribute in self.

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

                key_transformed = key.replace("_", ".")
                if key_transformed in SOFIA_PARAMETER:
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
            "type": "diag",
            "path": self.output_directory / f"{mode}_{self.input_data.stem }_diagnostic.eps",
            "description": "Diagnostic Plot",
            "software-id": "sofia"
        })
        sopar_report['outputs']['images'].append({
            "type": "rel",
            "path": self.output_directory / f"{mode}_{self.input_data.stem }_rel.eps",
            "description": "Realibiliy Plot",
            "software-id": "sofia"
        })
        sopar_report['outputs']['images'].append({
            "type": "skellman",
            "path": self.output_directory / f"{mode}_{self.input_data.stem}_skellam.eps",
            "description": "Skellam Plot",
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

        logger.info(f"Quality assesment start. Mode: {self.mode}.")

        # At the moment there is just one singles images but do it in this way allows add
        # additional images easly in the future
        qa_report = {
                "software_id" :'QA',
                "PID": self.pid,
                "input_name": self.input_data.stem,
                "mode": self.mode,  
                "log_path": "",
                "outputs" : {'images' : [], 'files': []}
            }

        #Momento 8 del cubo inicial (input.data en config.yaml o descargado)
        mom8_ima = moment8_ima(self, self.mode)

        #Máscara de lo obtenido por SoFiA
        sofia_output_dir = Path(self.output_directory)
        input_file_name = Path(self.input_data).stem
        file_2d_mask = (
            sofia_output_dir / f"{self.mode}_{input_file_name}_mask-2d.fits"
        )
        
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
        if self.mode == "absorption":
            ax.set_title("Moment 8 Image (Absorption - Min Projection)")
        else:
            ax.set_title("Moment 8 Image (Emission - Max Projection)")
        ax.imshow(mom8_ima, cmap='viridis', origin='lower')
        ax.imshow(mom8_ima, cmap='viridis', origin='lower')
        #ax.colorbar(label="Intensity")

        ax = axs[1]
        ax.set_title("Sofia 2D mask")
        ax.imshow(sofia_2d_mask, cmap='viridis', origin='lower')
        #ax.colorbar(label="Intensity")

        if mask_file:
            ax = axs[2]
            ax.set_title("Mask file")
            ax.imshow(mask_archive_proj, cmap='viridis', origin='lower')

        qa_output_dir = Path(self.output_directory) / "quality_assesment_products"
        qa_output_dir.mkdir(parents=True, exist_ok=True)  
        qa_output_file = Path(f"{qa_output_dir / Path(self.output_filename).stem}_QA.png")


        try:
            plt.savefig(qa_output_file, bbox_inches='tight')
            logger.info(
                f"QA file saved in {qa_output_dir}. Quality assesment completed "
                f"successfully. Mode: {self.mode}"
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
            logger.info(f"Quality assement aborted . Mode: {self.mode}")
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

        
        

    