"""
__doc__ to add in an appropiate way, formatter_class=argparse.RawDescriptionHelpFormatter have been set
Contact: Borja Montoro Molina (borjamomo96@gmail.com)

SOFIA_LOGIC BRANCH
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

def run_sofia(comand, output_dir=None):

    """
    .
    """


    #Create a directory on the used data location
    output_dir = f"{output_dir.parent}"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        logger.warning(f"The {output_dir} directory already exists. The SoFia outputs will be stored in this directory unless otherwise specified")
    

    try:
        #It is being assumend that SoFia can be run in any dir location in the device. CHANGES if needed.
        result = subprocess.run(comand, cwd=output_dir, capture_output=True, text=True, check=True)
        
    except subprocess.CalledProcessError as e:
        # In case of error this show the message and exit code of SoFia
        logger.error(f"Error running SoFia: {e}")
        print(e.returncode)
        print(e.stdout)
        print(e.stderr)

def key_par_sofia(sofia_par, par_name=''):

    """
    This fuctions check key --sofia-parameters arguments input.data and output.directory. If the later is specified the output.directory will 
    set to this value prevail over the default or the specified in the sofia.par file.

    Parameter: 

    - sofia_par: --sofia-parameters like object

    Return: return output_loc with the output.direcory value if specified. 
    """

    dict_sofia_par = {k: v for k, v in sofia_par}

    for k, v in dict_sofia_par:
        if k=='input.data': 
            logger.warning('The input.data from --sofia-parameters will prevail over the input-fits or the input.data parameter within the sofia.par file')
        if k=='output.directory': 
            logger.info(f'The output directory {v} will be used to stored SoFia outputs')
            output_loc = v
            return v


def sofia_conditions(input_fits, download_data, sofia_file, sofia_par):

    match (input_fits, download_data, sofia_file, sofia_par):

        case (True, False, True, True): 
            scomand = f"sofia {Path(args.sofia_file).resolve()} input.data={data_loc} {' '.join(args.sofia_par)}"
            logger.info(f"-f=not None -d=None and -s=not None SoFia will be run using {args.sofia_file} and {data_loc}")
            run_sofia(scomand.split(), data_loc)
        
        case (True, False, True, False):
            scomand = f"sofia {Path(args.sofia_file).resolve()} input.data={data_loc} --special"
            logger.info(f"-f=not None -d=None and -s=None, special case with {data_loc}")
            run_sofia(scomand.split(), data_loc)
        
        case (True, False, False, True):
            scomand = f"sofia {Path(args.sofia_file).resolve()} input.data={data_loc} {' '.join(args.sofia_par)} --mode=advanced"
            logger.info(f"-f=None -d=None, advanced mode with {data_loc}")
            run_sofia(scomand.split(), data_loc)
        
        case (True, False, False, False):
            scomand = f"sofia {Path(args.sofia_file).resolve()} input.data={data_loc} {' '.join(args.sofia_par)} --mode=advanced"
            logger.info(f"-f=None -d=None, advanced mode with {data_loc}")
            run_sofia(scomand.split(), data_loc)


def main():

    # Parse args:

    parser = argparse.ArgumentParser(
                    prog='adpalmap',
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    description='The ALMA advance data product pipeline',
                    epilog= __doc__) 

    parser.add_argument('--config-file', dest='config_file', default=None,
                        help='<Optional> Path to the config file to use. By default, APDALMAP will try to use (in order) the file config.yaml, or the example config file.')
    parser.add_argument('-f', '--input-fits', dest='input_fits', nargs='+', default=None, 
                        help='<Optional> Path to the data cube/s.')
    parser.add_argument('-d', '--download-file', dest='download_file', default=None, 
                        help='<Optional> Path to the file with the parameters to download the data.')
    parser.add_argument('-s', '--sofia-file', dest='sofia_file', default=None,
                        help='<Optional> Path to the file with the parameters for SoFia. By default ADPAlmap will use, ~/.adpalmap.sofia.sofia_default.par')
    parser.add_argument('--sofia-parameters', dest='sofia_par', nargs='+', default=None,
                        help='<Optional> List of the parameters following the instruction of SoFia2 cookbook')
    


    args = parser.parse_args()


    #Check args is not empty
    
    #...


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
        logger.info('Skipping data download')


    #--------------------------------------------------------------------------------------------#


    #--------------------------------------------------------------------------------------------#
    #Run SoFia

    if args.sofia_file:
        from sofia.sopar import SoPar

        sopar = SoPar(sofia_file_path=args.sofia_file) #All the parameters in the SoFia parameters file are set as attr within SoPar class



    # Llamar a la función con las condiciones
    ejecutar_condicion(A, B, C, D, args, data_loc)


    
    #--------------------------------------------------------------------------------------------#


    logger.info("ADPALMAP end point")

    

# Run the main functions
if __name__ == '__main__':
    main()

