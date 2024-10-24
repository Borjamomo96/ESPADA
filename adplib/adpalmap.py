"""
__doc__ to add in an appropiate way, formatter_class=argparse.RawDescriptionHelpFormatter have been set
Contact: Borja Montoro Molina (borjamomo96@gmail.com)
"""

import os
import sys
import argparse
import numpy as np

import pyvo

#logging
import logging
logger = logging.getLogger(__name__)


# Functions 
def step_1(input_data):
    """."""
    logger.info("1")
    return 

def main():

    # Parse args:

    parser = argparse.ArgumentParser(
                    prog='adpalmap',
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    description='The ALMA advance data product pipeline',
                    epilog= __doc__) 

    parser.add_argument('-c', '--config-file', dest='config_file', default=None,
                        help='<Optional> Path to the config file to use. By default, APDALMAP will try to use (in order) the file config.yaml, or the example config file.')
    parser.add_argument('-d', '--download-file', dest='download_file', default=None, 
                        help='<Optional> Path to the file with the parameters to download the date.')
    args = parser.parse_args()


    #Check args is not empty
    
    #...


    #Logging configuration 
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger.info("ADPALMAP start point")


    # Configuration:

    #global adpalmap_conf
    from config import Config
    
    adpalmap_config = Config(config_path=args.config_file) 

    #print(adpalmap_config)
    #print(adpalmap_config.prueba['par1'])


    # Data query || Se puede crear una función en este mismo archivo para que haga todo esto y poder escribirlo en una línea.
    
    #CHANGE. La logica de esto hay que repensarla. Si corro directamente la pipeline sin argumentos por defecto -d será 'tap/dowload_par.yaml' 
    # si lo cambio a None, es False y se salta la descarga.
    if args.download_file:
        from tap.datap import datap

        adpalmap_datap = datap(download_path=args.download_file)
        query = adpalmap_datap.proposal_id()
        logger.info('La query se obtenido')

        adpalmap_datap.download_data(query)
        
    else:
        logger.info('Skipping data download')
    

    

    logger.info("ADPALMAP end point")

    

# Ejecutar la función principal con los argumentos proporcionados
if __name__ == '__main__':
    main()

