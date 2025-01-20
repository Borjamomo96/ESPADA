"""
Contact: Borja Montoro Molina (borjamomo96@gmail.com)
"""


import os
import sys
import time
from pathlib import Path
import subprocess
import argparse
import numpy as np

from sip.sipargs import SiPar
from sofia.sopar import SoPar
from tap.datap import datap


# Configuration:
from config import Config
config = Config()
logger = config.get_logger()


# Functions 

'''def get_relative_path(path, base):
    try:
        return path.relative_to(base)
    except ValueError:
        return path'''

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

 


def main():

    # Parse args:

    parser = argparse.ArgumentParser(
                    prog='adpalmap',
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    description='The ALMA advance data product pipeline',
                    epilog= __doc__) 

    parser.add_argument('-c', '--config-file', dest='config_file', default=None,
                        help='<Optional> Path to the master config file to use. By default, APDALMAP will try to use the file config.yaml')
    parser.add_argument('-sop', '--sofia-parameters', dest='sofia_par', nargs='+', type=parse_sofia_par, default=None,
                        help='<Optional> List of the parameters following the instruction of SoFia2 cookbook. Note, the parameter introduce here will overwirte the corresponding parameter in all the sofia files used in ADPALMAP')
    parser.add_argument('-sarg','--sip-arguments', dest='sip_args', nargs=argparse.REMAINDER, type=str, default=None,
                        help="<Optional> Optional arguments for the SoFia Imaging Pipeline (SIP). If any other ADPAlmap argument is wanted to be introduced after this argument, the separtor '--' must be enter.")
    
    args = parser.parse_args()
    
    if args.sofia_par: args.sofia_par = dict(args.sofia_par)
    if args.sip_args: args.sip_args = sipargs_to_dict(args.sip_args)

    
    #Reconfigure must be True, Config was called on top for run the logger in all functions
    adpalmap_main = Config(reconfigure=True, config_path='config.yaml')


    #Check config file is not empty
    
    if (args.config_file is None):
        logger.error("The argument '-c/--config_file' is mandatory to run ADPALMAP. Use: python adpalmpap.py -c <path_to_configuration_file>")
        sys.exit(-1)       
        
    logger.info("ADPALMAP start point")
    time.sleep(0.5)


    #--------------------------------------------------------------------------------------------#
    #Optionally download data from ALMA archive

    if adpalmap_main.enable_tap_service == True:

        if adpalmap_main.input_data is not None or adpalmap_main.input_data_list is not None:
            logger.warning(f"The paremeter input_data or input_data_list specified in the {args.config_file} will be ignore. This run will use the requested download data.")

        adpalmap_datap = datap(download_path=adpalmap_main.download_par_file)
        if adpalmap_datap.query_type=='proposal': TAP_df = adpalmap_datap.proposal_id()
        elif adpalmap_datap.query_type=='conesearch': TAP_df = adpalmap_datap.conesearch()
        elif adpalmap_datap.query_type=='target': TAP_df = adpalmap_datap.target()
        elif adpalmap_datap.query_type=='keysearch': TAP_df = adpalmap_datap.keysearch()
        elif adpalmap_datap.query_type=='free': TAP_df = adpalmap_datap.free()

        adpalmap_datap.download_data(TAP_df)
        
    else:
        adpalmap_datap = None
        logger.info(f"'enable_tap_service' set to {adpalmap_main.enable_tap_service}. Skipping data download")

    time.sleep(0.5)

    

    #--------------------------------------------------------------------------------------------#


    #--------------------------------------------------------------------------------------------#
    #Run SoFia

    if adpalmap_main.enable_sofia == True:

        if adpalmap_main.run_mode == 'emission':

            adpalmap_sopar_emi = SoPar(sofia_file_path=adpalmap_main.sofia_emi_file)
            adpalmap_sopar_emi.update_input_parameters(args.sofia_par, adpalmap_main=adpalmap_main, adpalmap_datap=adpalmap_datap, mode=adpalmap_main.run_mode)  #Update sofia abs file with the -sop parameters
            if adpalmap_main.auto_setup == True:
                adpalmap_sopar_emi.auto_setup()
            adpalmap_sopar_emi.run_sofia(adpalmap_main, mode=adpalmap_main.run_mode)

            if adpalmap_main.quality_assesment == True:
                logger.info('Starting the quality assesment...')
                if adpalmap_datap is not None:
                    adpalmap_datap.download_mask(TAP_df)
                    adpalmap_sopar_emi.quality_assesment(adpalmap_datap)
                else:
                    logger.warning(f"'enable_tap_service' is set to False. All checks will not be performed.")
                    adpalmap_sopar_emi.quality_assesment(adpalmap_datap)


        elif adpalmap_main.run_mode == 'absorption':

            adpalmap_sopar_abs = SoPar(sofia_file_path=adpalmap_main.sofia_abs_file)
            adpalmap_sopar_abs.update_input_parameters(args.sofia_par, adpalmap_main=adpalmap_main, adpalmap_datap=adpalmap_datap, mode=adpalmap_main.run_mode)   #Update sofia abs file with the -sop parameters
            if adpalmap_main.auto_setup == True:
                adpalmap_sopar_abs.auto_setup()
            adpalmap_sopar_abs.run_sofia(adpalmap_main, mode=adpalmap_main.run_mode)

            if adpalmap_main.quality_assesment == True:
                if adpalmap_datap is not None:
                    adpalmap_sopar_abs.quality_assesment(adpalmap_datap)
                else:
                    logger.warning(f"'enable_tap_service' is set to False. All checks will not be performed.")
                    adpalmap_sopar_abs.quality_assesment(adpalmap_datap)

        elif adpalmap_main.run_mode == 'both':

            adpalmap_sopar_abs = SoPar(sofia_file_path=adpalmap_main.sofia_abs_file)
            adpalmap_sopar_emi = SoPar(sofia_file_path=adpalmap_main.sofia_emi_file)
            adpalmap_sopar_abs.update_input_parameters(args.sofia_par, adpalmap_main=adpalmap_main, adpalmap_datap=adpalmap_datap, mode=adpalmap_main.run_mode)   #Update sofia abs file with the -sop parameters
            adpalmap_sopar_emi.update_input_parameters(args.sofia_par, adpalmap_main=adpalmap_main, adpalmap_datap=adpalmap_datap, mode=adpalmap_main.run_mode, run=0)   #Update sofia emi file with the -sop parameters
            if adpalmap_main.auto_setup == True:
                adpalmap_sopar_emi.auto_setup()
                adpalmap_sopar_abs.auto_setup()

            adpalmap_sopar_abs.run_sofia(adpalmap_main, mode=adpalmap_main.run_mode)

            if adpalmap_main.quality_assesment == True:
                if adpalmap_datap is not None:
                    adpalmap_sopar_abs.quality_assesment(adpalmap_datap)
                else:
                    logger.warning(f"'enable_tap_service' is set to False. All checks will not be performed.")
                    adpalmap_sopar_abs.quality_assesment(adpalmap_datap)

            adpalmap_sopar_emi.run_sofia(adpalmap_main, mode=adpalmap_main.run_mode, run=0)

            if adpalmap_main.quality_assesment == True:
                if adpalmap_datap is not None:
                    adpalmap_sopar_emi.quality_assesment(adpalmap_datap)
                else:
                    logger.warning(f"'enable_tap_service' is set to False. All checks will not be performed.")
                    adpalmap_sopar_emi.quality_assesment(adpalmap_datap)

    else:
        logger.info(f"'enable_sofia' set to {adpalmap_main.enable_tap_service}. Skipping Sofia runs.")


    #--------------------------------------------------------------------------------------------#
    #Run SIP
    if adpalmap_main.enable_sip == True:

        adpalmap_sipar = SiPar(sip_file_path=adpalmap_main.sip_par_file)
        adpalmap_sipar.update_input_parameters(args.sip_args, adpalmap_main)

        if adpalmap_main.enable_sofia == True:

            if adpalmap_main.run_mode == 'emission':
                adpalmap_sipar.run_sip(adpalmap_main, sopar=adpalmap_sopar_emi)

            elif adpalmap_main.run_mode == 'absorption':
                adpalmap_sipar.run_sip(adpalmap_main, sopar=adpalmap_sopar_abs)

            elif adpalmap_main == 'both':
                adpalmap_sipar.run_sip(adpalmap_main, sopar=adpalmap_sopar_emi)
                adpalmap_sipar.run_sip(adpalmap_main, sopar=adpalmap_sopar_abs)
        
        else:
            adpalmap_sipar.run_sip(adpalmap_main)
            
    else:
        logger.info(f"'enable_sip' set to {adpalmap_main.enable_tap_service}. Skipping SIP runs.")
    #--------------------------------------------------------------------------------------------#
        
    logger.info("ADPALMAP end point")

    

# Run the main functions
if __name__ == '__main__':
    main()

