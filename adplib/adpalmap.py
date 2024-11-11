"""
__doc__ to add in an appropiate way, formatter_class=argparse.RawDescriptionHelpFormatter have been set
Contact: Borja Montoro Molina (borjamomo96@gmail.com)

Main 
"""

import os
import sys
from pathlib import Path
import subprocess
import argparse
import numpy as np

import pyvo


#logging
import logging

class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[34m", #BLUE
        logging.INFO: "\033[32m",  #GREEN
        logging.WARNING: "\033[38;5;214m", #ORANGE 
        logging.ERROR: "\033[31m",  #RED
        logging.CRITICAL: "\033[1;31m",  #BOLD RED
    }
    MODULE_COLOR = "\033[38;5;45m"  # Neon blue

    def format(self, record):
        RESET = "\033[0m"
        color = self.COLORS.get(record.levelno, RESET)

        record.levelname = f"{color}{record.levelname}{RESET}"
        record.module = f"{self.MODULE_COLOR}{record.module}{RESET}"
        format_string = "| %(levelname)s | %(module)s: - %(message)s"
        formatter = logging.Formatter(format_string)

        return formatter.format(record)

logger = logging.getLogger("ColoredLogger")

# Functions 

def parse_sofia_par(arg):

    """
    .
    """
    try:

        key, value = arg.split("=", 1)
        return key, value
    except ValueError:
        raise argparse.ArgumentTypeError("--sofia-parameters must be in par=val format")
    

def sipargs_to_dict(args_list):

    """
    .
    """

    args_dict = {}
    key = None
    
    for item in args_list:
        if item.startswith('-'): 
            key = item
            args_dict[key] = True  
        elif key:
            if args_dict[key] is True:
                args_dict[key] = item  
            elif isinstance(args_dict[key], list):
                args_dict[key].append(item) 
            else:
                args_dict[key] = [args_dict[key], item] 
    
    for k, v in args_dict.items():
        if isinstance(v, list) and len(v) == 1:
            args_dict[k] = v[0]
    
    return args_dict


def sofia_comand_generator(input_fits, adpalmap_datap, sofia_file, sofia_par):

    from sofia.sopar import SoPar
    default_sofia_file = Path('sofia/sofia_default.par').resolve()

    match (input_fits is not None, adpalmap_datap is not None, sofia_file is not None, sofia_par is not None):

        case (True, False, True, True): 
            data_loc = Path(input_fits).resolve()
            sopar = SoPar(sofia_file_path=sofia_file) #All the parameters in the SoFia parameters file are set as attr within SoPar class
            if sopar.input_data or sofia_par.get('input_data') is not None:
                logger.warning('The input fits file indicated in sofia parameters file or --sofia-parameters input.data will be ignored. The input-fits will prevail')
            output_dir = output_dir_conditions(data_loc, sopar, sofia_par)
            #CHANGE. Instead of define sopar_par as dict in the main I could pass the args.sofia_par as in the temrinal ['par=val', 'par1=val1',...] for the comand and here define sofia_par variable
            #dict-like for the conditions
            scomand = f"sofia {Path(sofia_file).resolve()} {' '.join([f'{k}={v}' for k, v in sofia_par.items()])} input.data={data_loc.resolve()}"
            logger.info(f"SoFia will be run using {sofia_file.relative_to(Path.cwd())} and {data_loc.relative_to(Path.cwd())}") 
            return scomand.split(), output_dir, sopar
        
        case (True, False, True, False):
            data_loc = Path(input_fits).resolve()
            sopar = SoPar(sofia_file_path=sofia_file)
            if sopar.input_data or sofia_par['input_data']: logger.warning('The input fits file indicated in sofia parameters file or --sofia-parameters input.data will be ignored. The input-fits will prevail')
            output_dir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {Path(sofia_file).resolve()} input.data={data_loc}"
            logger.info(f"SoFia will be run using {sofia_file.relative_to(Path.cwd())} and {data_loc.relative_to(Path.cwd())}")
            return scomand.split(), output_dir, sopar
        
        case (True, False, False, True):
            data_loc = Path(input_fits).resolve()
            if sofia_par.get('input_data') is not None: 
                logger.warning('The input fits indicated in --sofia-parameters input.data will be ignored. The input-fits will prevail')
            sopar = SoPar(sofia_file_path=default_sofia_file) 
            output_dir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {default_sofia_file} {' '.join([f'{k}={v}' for k, v in sofia_par.items()])} input.data={data_loc}" 
            logger.info(f"SoFia will be run using {default_sofia_file.relative_to(Path.cwd())} and {data_loc.relative_to(Path.cwd())}")
            return scomand.split(), output_dir, sopar
        
        case (True, False, False, False):
            data_loc = Path(input_fits).resolve()
            sopar = SoPar(sofia_file_path=default_sofia_file) 
            output_dir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {default_sofia_file} input.data={data_loc}"
            logger.info(f"SoFia will be run using {default_sofia_file.relative_to(Path.cwd())} and {data_loc.relative_to(Path.cwd())}")
            sys.exit(-1)
            return scomand.split(), output_dir, sopar


        case (False, True, True, True): 
            data_loc = Path(adpalmap_datap.download_file['data_dir']).resolve()
            sopar = SoPar(sofia_file_path=sofia_file) #All the parameters in the SoFia parameters file are set as attr within SoPar class
            if sopar.input_data or sofia_par.get('input_data') is not None: 
                logger.warning('The input fits file indicated in sofia parameters file or --sofia-parameters input.data will be ignored. The download-fits will prevail')
            output_dir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {Path(sofia_file).resolve()} {' '.join([f'{k}={v}' for k, v in sofia_par.items()])} input.data={data_loc} "
            logger.info(f"SoFia will be run using {sofia_file.relative_to(Path.cwd())} and {data_loc.relative_to(Path.cwd())}") 
            return scomand.split(), output_dir, sopar
        
        case (False, True, True, False):
            data_loc = Path(adpalmap_datap.download_file['data_dir']).resolve()
            sopar = SoPar(sofia_file_path=sofia_file) #All the parameters in the SoFia parameters file are set as attr within SoPar class
            if sopar.input_data or sofia_par.get('input_data') is not None: 
                logger.warning('The input fits file indicated in sofia parameters file or --sofia-parameters input.data will be ignored. The download-fits will prevail')
            output_dir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {Path(sofia_file).resolve()} input.data={data_loc}"
            logger.info(f"SoFia will be run using {sofia_file.relative_to(Path.cwd())} and {data_loc.relative_to(Path.cwd())}")
            return scomand.split(), output_dir, sopar
        
        case (False, True, False, True):
            data_loc = Path(adpalmap_datap.download_file['data_dir']).resolve()
            sopar = SoPar(sofia_file_path=default_sofia_file) 
            if sofia_par.get('input_data') is not None: 
                logger.warning('The input fits indicated in --sofia-parameters input.data will be ignored. The download-fits will prevail')
            output_dir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {default_sofia_file} {' '.join([f'{k}={v}' for k, v in sofia_par.items()])} input.data={data_loc}" 
            logger.info(f"SoFia will be run using {default_sofia_file.relative_to(Path.cwd())} and {data_loc.relative_to(Path.cwd())}")
            return scomand.split(), output_dir, sopar 
        
        case (False, True, False, False):
            data_loc = Path(adpalmap_datap.download_file['data_dir']).resolve()
            sopar = SoPar(sofia_file_path=default_sofia_file) 
            output_dir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {default_sofia_file} input.data={data_loc}"
            logger.info(f"SoFia will be run using {default_sofia_file.relative_to(Path.cwd())} and {data_loc.relative_to(Path.cwd())}")
            return scomand.split(), output_dir, sopar


def output_dir_conditions(data_loc, sopar, sofia_par):
    # Verificar si 'sofia_par' es None antes de acceder a 'output.directory'
    if sopar.output_directory and sofia_par is not None and sofia_par.get('output.directory') is not None:
        return Path(sofia_par['output.directory']).resolve()
    elif sopar.output_directory:
        return Path(sopar.output_directory).resolve()
    elif sofia_par is not None and sofia_par.get('output.directory') is not None:
        #print(data_loc, Path(sofia_par['output.directory']), 'Replace: ', os.path.relpath(data_loc, Path(sofia_par['output.directory'])), 'El resolve:', os.path.relpath(data_loc, Path(sofia_par['output.directory']).resolve()) )
        return Path(sofia_par['output.directory']).resolve()
    else:
        return Path(f"{data_loc.parent}/sofia_outputs")

    
def first_run_sofia(comand, output_dir):

    """
    .
    """

    fcomand = comand.copy()
    output_dir = Path(f'{output_dir}_absorption')

    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        logger.warning(f"The {output_dir} directory already exists. The SoFia outputs of the first run will be stored in this directory")     
    fcomand.append(f"output.directory={output_dir}")

    try:
        fcomand.append('input.invert=true')
        subprocess.run(fcomand, capture_output=True, text=True, check=True)
        
    except subprocess.CalledProcessError as e:
        # In case of error this show the message and exit code of SoFia
        logger.error(f"Error running SoFia: {e}")
        print(e.returncode)
        print(e.stdout)
        print(e.stderr)


def second_run_sofia(comand, output_dir):

    """
    .
    """
    fcomand = comand.copy()

    absorption_dir = Path(f'{output_dir}_absorption')

    flag_cube = list(absorption_dir.glob('*_mask.fits'))[0]
    fcomand.append(f'flag.cube={flag_cube}')
    
    output_dir = Path(f'{output_dir}_emission')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        logger.warning(f"The {output_dir} directory already exists. The SoFia outputs of the second run will be stored in this directory")
    fcomand.append(f"output.directory={output_dir}")

    try:
        subprocess.run(fcomand, capture_output=True, text=True, check=True)
        
    except subprocess.CalledProcessError as e:
        # In case of error this show the message and exit code of SoFia
        logger.error(f"Error running SoFia: {e}")
        print(e.returncode)
        print(e.stdout)
        print(e.stderr)


def sip_comand_generator(sip_args, output_dir):

    sip_args_dict = sipargs_to_dict(sip_args) #Por si en el futuro queremos convertirla en dict.
    if '-c' in sip_args_dict: sip_args_dict.pop('-c')
    sip_args_string = ' '.join([f'{k}={v}' for k, v in sip_args_dict.items()])

    absorption_dir = Path(f'{output_dir}_absorption')
    emision_dir = Path(f'{output_dir}_emission')
    sofia_abs_catalog = list(absorption_dir.glob('*_cat.txt'))[0]
    sofia_emi_catalog = list(emision_dir.glob('*_cat.txt'))[0]

    ecomand = f"sofia_image_pipeline -c {sofia_emi_catalog} {sip_args_string}"
    acomand = f"sofia_image_pipeline -c {sofia_abs_catalog} {sip_args_string}"

    return ecomand.split(), acomand.split()


def run_sip(comand):

    try:
        print(comand)
        subprocess.run(comand, capture_output=True, text=True, check=True)
        
    except subprocess.CalledProcessError as e:
        # In case of error this show the message and exit code of SIP
        logger.error(f"Error running SIP: {e}")
        print(e.returncode)
        print(e.stdout)
        print(e.stderr)
        


def main():

    # Parse args:

    parser = argparse.ArgumentParser(
                    prog='adpalmap',
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    description='The ALMA advance data product pipeline',
                    epilog= __doc__) 

    parser.add_argument('--config-file', dest='config_file', default=None,
                        help='<Optional> Path to the config file to use. By default, APDALMAP will try to use (in order) the file config.yaml, or the example config file.')
    parser.add_argument('-f', '--input-fits', dest='input_fits', default=None, 
                        help='<Optional> Path to the data cube.')
    parser.add_argument('-d', '--download-file', dest='download_file', default=None, 
                        help='<Optional> Path to the file with the parameters to download the data.')
    parser.add_argument('-s', '--sofia-file', dest='sofia_file', default=None,
                        help='<Optional> Path to the file with the parameters for SoFia. By default ADPAlmap will use, ~/.adpalmap.sofia.sofia_default.par')
    parser.add_argument('-sop', '--sofia-parameters', dest='sofia_par', nargs='+', type=parse_sofia_par, default=None,
                        help='<Optional> List of the parameters following the instruction of SoFia2 cookbook')
    parser.add_argument('-sarg','--sip-arguments', dest='sip_args', nargs=argparse.REMAINDER, type=str, default=None,
                        help="<Optional> Optional arguments for the SoFia Imaging Pipeline (SIP). If any other ADPAlmap argument is wanted to be introduced after this argument, the separtor '--' must be enter.")
    
    
    args = parser.parse_args()
    if args.sofia_par: args.sofia_par = dict(args.sofia_par)


    print(args.sofia_par)
    print(args.sip_args)

    #Check args is not empty
    
    if (args.input_fits is not None and args.download_file is not None):
        logger.error('Both  -input-fits or download-file have been introduced. Please run again introducing at least one these two parameters"')
        sys.exit(-1)
    elif (args.input_fits is None and args.download_file is None):
        logger.error("Neither -input-fits or download-file have been introduced. Please run again introducing some of these two parameters")
        sys.exit(-1)

    #Logging configuration 
    #logging.basicConfig(level=logging.INFO, format='%(levelname)s.%(name)s: %(message)s')
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)


    logger.info("ADPALMAP start point")


    # Configuration:

    #global adpalmap_conf
    from config import Config
    
    adpalmap_config = Config(config_path=args.config_file) 

    #--------------------------------------------------------------------------------------------#
    #Optionally download data from ALMA archive

    if args.download_file:
        from tap.datap import datap

        adpalmap_datap = datap(download_path=args.download_file)
        query = adpalmap_datap.proposal_id()

        adpalmap_datap.download_data(query)

        
    else:
        adpalmap_datap = None
        logger.info('Skipping data download')


    #--------------------------------------------------------------------------------------------#


    #--------------------------------------------------------------------------------------------#
    #Run SoFia

    sofia_comand, sofia_outputdir, adpalmap_sopar = sofia_comand_generator(args.input_fits, adpalmap_datap, args.sofia_file, args.sofia_par)
    if (adpalmap_sopar.input_invert == 'true'):
        logger.warning("The parameter 'input.invert' has set to 'true' and it will be ignore. By default Sofia will be run twice, first with the cube inverted trying to find absoprion and second trying to find emission.")
    
    first_run_sofia(sofia_comand, sofia_outputdir)
    print(sofia_comand)
    second_run_sofia(sofia_comand, sofia_outputdir)
    
    #--------------------------------------------------------------------------------------------#

    #--------------------------------------------------------------------------------------------#
    #Run SIP
    
    sip_emi_comand, sip_abs_comand = sip_comand_generator(args.sip_args, sofia_outputdir)
    run_sip(sip_emi_comand)
    #run_sip(sip_abs_comand)
    
    #--------------------------------------------------------------------------------------------#

    logger.info("ADPALMAP end point")

    

# Run the main functions
if __name__ == '__main__':
    main()

