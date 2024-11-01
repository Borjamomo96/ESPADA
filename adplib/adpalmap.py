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
logger = logging.getLogger(__name__)


# Functions 

def parse_key_value(arg):

    """
    .
    """
    try:

        key, value = arg.split("=", 1)
        return key, value
    except ValueError:
        raise argparse.ArgumentTypeError("--sofia-parameters must be in par=val format")


def sofia_conditions(input_fits, adpalmap_datap, sofia_file, sofia_par):

    from sofia.sopar import SoPar
    default_sofia_file = Path('sofia/sofia_default.par').resolve()

    logger.info('AQUI ENTRO')

    match (input_fits is not None, adpalmap_datap is not None, sofia_file is not None, sofia_par is not None):

        case (True, False, True, True): 
            print('1')
            data_loc = Path(input_fits).resolve()
            sopar = SoPar(sofia_file_path=sofia_file) #All the parameters in the SoFia parameters file are set as attr within SoPar class
            if sopar.input_data or sofia_par.get('input_data') is not None:
                logger.warning('The input fits file indicated in sofia parameters file or --sofia-parameters input.data will be ignored. The input-fits will prevail')
            output_dir, makedir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {Path(sofia_file).resolve()} {' '.join([f'{k}={v}' for k, v in sofia_par.items()])} input.data={data_loc.resolve()}"
            logger.info(f"SoFia will be run using {sofia_file} and {data_loc}") 
            run_sofia(scomand.split(), data_loc.resolve(), output_dir, makedir)
        
        case (True, False, True, False):
            print('2')
            data_loc = Path(input_fits).resolve()
            sopar = SoPar(sofia_file_path=sofia_file)
            if sopar.input_data or sofia_par['input_data']: logger.warning('The input fits file indicated in sofia parameters file or --sofia-parameters input.data will be ignored. The input-fits will prevail')
            output_dir, makedir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {Path(sofia_file).resolve()} input.data={data_loc}"
            logger.info(f"SoFia will be run using {sofia_file} and {data_loc}")
            run_sofia(scomand.split(), data_loc.resolve(), output_dir, makedir)
        
        case (True, False, False, True):
            print('3')
            data_loc = Path(input_fits).resolve()
            if sofia_par.get('input_data') is not None: 
                logger.warning('The input fits indicated in --sofia-parameters input.data will be ignored. The input-fits will prevail')
            sopar = SoPar(sofia_file_path=default_sofia_file) 
            output_dir, makedir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {default_sofia_file} {' '.join([f'{k}={v}' for k, v in sofia_par.items()])} input.data={data_loc}" 
            logger.info(f"SoFia will be run using sofia_default.par and {data_loc}")
            run_sofia(scomand.split(), data_loc.resolve(), output_dir, makedir)
        
        case (True, False, False, False):
            print('4')
            data_loc = Path(input_fits).resolve()
            sopar = SoPar(sofia_file_path=default_sofia_file) 
            output_dir, makedir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {default_sofia_file} input.data={data_loc}"
            logger.info(f"SoFia will be run using sofia_default.par and {data_loc}")
            run_sofia(scomand.split(), os.path.dirname(os.path.abspath(data_loc)), output_dir, makedir)


        case (False, True, True, True): 
            print('5')
            data_loc = Path(adpalmap_datap.download_file['data_dir']).resolve()
            sopar = SoPar(sofia_file_path=sofia_file) #All the parameters in the SoFia parameters file are set as attr within SoPar class
            if sopar.input_data or sofia_par.get('input_data') is not None: 
                logger.warning('The input fits file indicated in sofia parameters file or --sofia-parameters input.data will be ignored. The download-fits will prevail')
            output_dir, makedir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {Path(sofia_file).resolve()} {' '.join([f'{k}={v}' for k, v in sofia_par.items()])} input.data={data_loc} "
            logger.info(f"SoFia will be run using {sofia_file} and {data_loc}") 
            run_sofia(scomand.split(), data_loc.resolve(), output_dir, makedir)
        
        case (False, True, True, False):
            print('6')
            data_loc = Path(adpalmap_datap.download_file['data_dir']).resolve()
            sopar = SoPar(sofia_file_path=sofia_file) #All the parameters in the SoFia parameters file are set as attr within SoPar class
            if sopar.input_data or sofia_par.get('input_data') is not None: 
                logger.warning('The input fits file indicated in sofia parameters file or --sofia-parameters input.data will be ignored. The download-fits will prevail')
            output_dir, makedir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {Path(sofia_file).resolve()} input.data={data_loc}"
            logger.info(f"SoFia will be run using {sofia_file} and {data_loc}")
            run_sofia(scomand.split(), data_loc.resolve(), output_dir, makedir)
        
        case (False, True, False, True):
            print('7')
            data_loc = Path(adpalmap_datap.download_file['data_dir']).resolve()
            sopar = SoPar(sofia_file_path=default_sofia_file) 
            if sofia_par.get('input_data') is not None: 
                logger.warning('The input fits indicated in --sofia-parameters input.data will be ignored. The download-fits will prevail')
            output_dir, makedir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {default_sofia_file} {' '.join([f'{k}={v}' for k, v in sofia_par.items()])} input.data={data_loc}" 
            logger.info(f"SoFia will be run using sofia_default.par and {data_loc}")
            run_sofia(scomand.split(), data_loc.resolve(), output_dir, makedir)
        
        case (False, True, False, False):
            print('8')
            data_loc = Path(adpalmap_datap.download_file['data_dir']).resolve()
            sopar = SoPar(sofia_file_path=default_sofia_file) 
            output_dir, makedir = output_dir_conditions(data_loc, sopar, sofia_par)
            scomand = f"sofia {default_sofia_file} input.data={data_loc}"
            logger.info(f"SoFia will be run using sofia_default.par and {data_loc}")
            run_sofia(scomand.split(), data_loc.resolve(), output_dir, makedir)


def output_dir_conditions(data_loc, sopar, sofia_par):
    # Verificar si 'sofia_par' es None antes de acceder a 'output.directory'
    if sopar.output_directory and sofia_par is not None and sofia_par.get('output.directory') is not None:
        print('a')
        return os.path.relpath(data_loc, Path(sofia_par['output.directory']).resolve()), False
    elif sopar.output_directory:
        print('b')
        return os.path.relpath(data_loc, Path(sopar.output_directory).resolve()), False
    elif sofia_par is not None and sofia_par.get('output.directory') is not None:
        print('c')
        print(data_loc, Path(sofia_par['output.directory']))
        return os.path.relpath(data_loc, Path(sofia_par['output.directory']).resolve()), False
    else:
        print('d')  
        return Path(f"{data_loc.parent}/sofia_outputs"), True

    
def run_sofia(comand, data_loc, output_dir, makedir):

    """
    .
    """
    print(makedir)
    if makedir: 
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            comand.append(f"output.directory={output_dir}")
        else:
            logger.warning(f"The {output_dir} directory already exists. The SoFia outputs will be stored in this directory")
            comand.append(f"output.directory={output_dir}")

    try:
        #It is being assumend that SoFia can be run in any dir location in the device. CHANGES if needed.
        result = subprocess.run(comand, capture_output=True, text=True, check=True)
        
        
    except subprocess.CalledProcessError as e:
        # In case of error this show the message and exit code of SoFia
        logger.error(f"Error running SoFia: {e}")
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
    parser.add_argument('--sofia-parameters', dest='sofia_par', nargs='+', type=parse_key_value, default=None,
                        help='<Optional> List of the parameters following the instruction of SoFia2 cookbook')
    


    args = parser.parse_args()
    if args.sofia_par: args.sofia_par = dict(args.sofia_par)

    #Check args is not empty
    
    if (args.input_fits is not None and args.download_file is not None):
        logger.error('Both  -input-fits or download-file have been introduced. Please run again introducing at least one these two parameters"')
        sys.exit(-1)
    elif (args.input_fits is None and args.download_file is None):
        logger.error("Neither -input-fits or download-file have been introduced. Please run again introducing some of these two parameters")
        sys.exit(-1)

    #Logging configuration 
    logging.basicConfig(level=logging.INFO, format='%(levelname)s.%(name)s: %(message)s')

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

    sofia_conditions(args.input_fits, adpalmap_datap, args.sofia_file, args.sofia_par)

    
    #--------------------------------------------------------------------------------------------#


    logger.info("ADPALMAP end point")

    

# Run the main functions
if __name__ == '__main__':
    main()

