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


# Funciones de tu pipeline (puedes descomponer las tareas en módulos)
def step_1(input_data):
    """Primer paso de la pipeline: puede ser preprocesamiento, validación de datos, etc."""
    logger.info("Ejecutando el paso 1")
    # Aquí va tu código
    processed_data = input_data  # Ejemplo de procesamiento
    return processed_data


def step_2(processed_data):
    """Segundo paso de la pipeline: podría ser el procesamiento del modelo, análisis, etc."""
    logger.info("Ejecutando el paso 2")
    # Aquí va tu código
    result = processed_data  # Ejemplo de salida
    return result


def main():

    # Parse args:

    parser = argparse.ArgumentParser(
                    prog='adpalmap',
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    description='The ALMA advance data product pipeline',
                    epilog= __doc__) 

    parser.add_argument('-conf', '--config-file', dest='config_file', default=None,
                        help='<Optional> Path to the config file to use. By default, APDALMAP will try to use (in order) the file config.yaml, or the the example config file.')
    
    args = parser.parse_args()


    #Check args is not empty
    
    #...


    #Logging configuration 
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger.info("ADPALMAP start point")


    # Configuration:

    #global adpalmap_conf
    from config import Config
    
    adpalmap_config = Config(config_path=args.config_file, check1=True) 

    # Data query || This needs to be convert into a Class, it would be more efficient 

    service = pyvo.dal.TAPService(adpalmap_config.server_address)

    output = service.search(adpalmap_config.query).to_table().to_pandas()
    final = output.head(5)

    mous_ids = np.unique(output['member_ous_uid'])[0]

    datalink = pyvo.dal.adhoc.DatalinkResults.from_result_url(f"https://almascience.eso.org/datalink/sync?ID={mous_ids}")
    #print(type(datalink))
    #print(datalink)

    for dl in datalink:    
        dl.cachedataset(filename=os.path.basename(dl['access_url']))

    '''sys.exit(1)'''

    logger.info("ADPALMAP end point")

    

# Ejecutar la función principal con los argumentos proporcionados
if __name__ == '__main__':
    main()

