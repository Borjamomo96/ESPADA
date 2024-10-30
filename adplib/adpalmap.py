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
    output_dir = f"{data_loc.parent}"

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
    #CHANGE. This file works for the moments but it has to be change. When adpalmap will be installed in other device by default would be convient to create a adpalmap directory in 
    #~/adpalmap/ with a sofia_default.par
    default_sofia_par = Path('sofia/sofia_default.par').resolve()

    
    if (args.input_fits and args.download_file): logger.warning('Both -f and -d parameters have been introduced the input fits file will prevail above download data from the archive')

    #Check if several input.data have been introduced
    #multiple_par_sofia(args.sofia_par, par='input.data')

    #the argument -f=not None. Case where the user speficy a data cube
    if args.input_fits:
        
        #check if the user input one or more than 1 file. This needs to be implemented. CHANGE
        if(len(args.input_fits)==1): data_loc = Path(args.input_fits[0]).resolve()


        #the sofia.par specify by the user will be used. Case where -f=not None -d=None and -s=not None
        if args.sofia_file:

            if args.sofia_par:
                
                output_dir = key_par_sofia(args.sofia_par)
                #This imply that the input.data parameters is set to the download directory either by default or specified by the user independently whether the user also 
                # specified other location in the terminal. This may display a warning or other possibilities to be disscused. CHANGES
                scomand = f"sofia {Path(args.sofia_file).resolve()} input.data={data_loc} {' '.join(args.sofia_par)}"
                logger.info(f"-f=not None -d=None and -s=not None SoFia will be run using {args.sofia_file}")
                run_sofia(scomand.split(), output_dir=output_dir) 
            
            else:
                scomand = f"sofia {Path(args.sofia_file).resolve()} input.data={data_loc}"
                logger.info(f"-f=not None -d=None and -s=not None SoFia will be run using {args.sofia_file}")
                run_sofia(scomand.split()) 

        #the sofia_defeult.par file will be used instead. Case where -f=not None -d=None and -s=None
        else:

            #Check the if conditions. similar. CHANGE
            if not default_sofia_par.exists():
                raise FileNotFoundError(f"{default_sofia_par} not found in the corresponding directory please. Introduce the correct Path of a valid sofia.par file or include the sofia_default.par file in the sofia directory") 
            
            else:
                if args.sofia_par:
                    output_dir = key_par_sofia(args.sofia_par)
                    scomand = f"sofia {default_sofia_par} input.data={data_loc} {' '.join(args.sofia_par)}"
                    logger.info(f"-f=not None -d=None and -s=None SoFia will be run using {default_sofia_par}")
                    run_sofia(scomand.split(), output_dir=output_dir)

                else:
                    scomand = f"sofia {Path(args.sofia_file).resolve()} input.data={data_loc}"
                    logger.info(f"-f=not None -d=None and -s=None SoFia will be run using {default_sofia_par}")
                    run_sofia(scomand.split()) 
        
    #the argument -f=None. Case where the user do not specify a data cube
    else:

        #download data from the archive have been required. Case where -f=None and -d=not None 
        
        if args.download_file:

            data_loc = Path(adpalmap_datap.download_file['data_dir']).resolve()

            #the sofia.par specify by the user will be used. Case where -f=None -d=not None and -s=not None
            if args.sofia_file:

                if args.sofia_par:
                    output_dir = key_par_sofia(args.sofia_par)
                    #This imply that the input.data parameters is set to the download directory either by default or specified by the user independently whether the user also 
                    # specified other location in the terminal. This may display a warning or other possibilities to be disscused. CHANGES
                    scomand = [f"sofia {Path(args.sofia_file).resolve()} input.data={data_loc} {' '.join(args.sofia_par)}"]
                    logger.info(f"-f=None -d=not None and -s=not None SoFia will be run using {args.sofia_file}")
                    run_sofia(scomand.split(), output_dir=output_dir)
                else:
                    scomand = [f"sofia {Path(args.sofia_file).resolve()} input.data={data_loc}"]
                    logger.info(f"-f=None -d=not None and -s=not None SoFia will be run using {args.sofia_file}")
                    run_sofia(scomand.split())

                    

            #the sofia_defeult.par file will be used instead. Case where -f=None -d=not None and -s=None
            else:

                #Check the if conditions. similar. CHANGE
                if not default_sofia_par.exists():
                    raise FileNotFoundError(f"{default_sofia_par} not found in the corresponding directory please.") 
                
                else:
                    if args.sofia_par:
                        output_dir = key_par_sofia(args.sofia_par)
                        scomand = [f"sofia {default_sofia_par} input.data={data_loc} {' '.join(args.sofia_par)}"]
                        #print('Programar para que busque los archivos descargados y use sofia_default.par')
                        logger.info(f"-f=None -d=not None and -s=None SoFia will be run using {default_sofia_par}")
                        run_sofia(scomand.split(), output_dir=output_dir)
                    else:
                        scomand = [f"sofia {default_sofia_par} input.data={data_loc}"]
                        #print('Programar para que busque los archivos descargados y use sofia_default.par')
                        logger.info(f"-f=None -d=not None and -s=None SoFia will be run using {default_sofia_par}")
                        run_sofia(scomand.split())

        #skipping the download of the data. Case where -f=None and -d=None 
        else:
            logger.error("Neither data cube nor download from the archive have been indicated. Please specified either options with -i or -d || The data_example and sofia_default.par will be used (this options needs to be implemented)" )
        
    
    #--------------------------------------------------------------------------------------------#

    

    logger.info("ADPALMAP end point")

    

# Run the main functions
if __name__ == '__main__':
    main()

