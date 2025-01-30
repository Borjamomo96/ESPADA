"""
Contact: Borja Montoro Molina (borjamomo96@gmail.com)
"""
#Configuration
from config import Config

import os
import sys
import time
from pathlib import Path
import subprocess
import argparse
import numpy as np


from logger import Initial_Logger
from logger import Logger



# Functions 
def parse_sofia_par(arg):

    """
    Parses a string in key=value format. Splits the string at the first = and returns a tuple 
    (key, value). Raises argparse.ArgumentTypeError if the format is invalid.

    Parameters:
    ----------
    arg (str): Input string in key=value format.

    Returns:
    ----------
    Tuple (key, value).

    Raises:
    ----------
    argparse.ArgumentTypeError: If arg is not in key=value format.
    """

    try:

        key, value = arg.split("=", 1)
        return key, value
    except ValueError:
        raise argparse.ArgumentTypeError("--sofia-parameters must be in par=val format")


def sipargs_to_dict(args_list):

    """
    Converts a list of SIP-related arguments into a structured dictionary. Arguments starting 
    with '-' are treated as keys, and subsequent items are treated as their values. Supports single 
    values, lists, or boolean flags.

    Parameters:
    ----------
    args_list (list): A list of strings representing SIP arguments.

    Returns:
    ----------
    dict: A dictionary where keys are argument names (starting with '-') and values are either 
          single values, lists, or `True` for flags.
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
                        help="<Optional> Path to the master config file to use. By default, "
                        "APDALMAP will try to use the file config.yaml")
    parser.add_argument('-sop', '--sofia-parameters', dest='sofia_par', nargs='+', 
                        type=parse_sofia_par, default=None,
                        help="<Optional> List of the parameters following the instruction of SoFia2 "
                        "cookbook. Note, the parameter introduce here will overwirte the "
                        "corresponding parameter in all the sofia files used in ADPALMAP")
    parser.add_argument('-sarg','--sip-arguments', dest='sip_args', nargs=argparse.REMAINDER, 
                        type=str, default=None, help="<Optional> Optional arguments for the SoFia "
                        "Imaging Pipeline (SIP). If any other ADPAlmap argument is wanted to be "
                        "introduced after this argument, the separtor '--' must be enter.")
    
    args = parser.parse_args()
    
    if args.sofia_par: args.sofia_par = dict(args.sofia_par)
    if args.sip_args: args.sip_args = sipargs_to_dict(args.sip_args)

    ini_logger = Initial_Logger.get_initial_logger()
      
    if (args.config_file is None):
        ini_logger.warning("No config.yaml file specified, default config.yaml file will be used")
        adpalmap_config = Config()
    else:
        adpalmap_config = Config(config_path=args.config_file)    


    logger = Logger.get_logger(log_path=adpalmap_config.log_file, 
                               clear_logs=adpalmap_config.clear_logs)


    logger.info("ADPALMAP start point")
    #------------------------------------------------------------------------------------------------#
    #Optionally download data from ALMA archive
    from tap.datap import datap

    if adpalmap_config.enable_tap_service == True:

        if adpalmap_config.input_data is not None or adpalmap_config.input_data_list is not None:
            logger.warning(f"The paremeter input_data or input_data_list specified in the "
                           "{args.config_file} will be ignore. This run will use the requested "
                           "download data.")

        adpalmap_datap = datap(download_path=adpalmap_config.download_par_file)
        if adpalmap_datap.query_type=='proposal': TAP_df = adpalmap_datap.proposal_id()
        elif adpalmap_datap.query_type=='conesearch': TAP_df = adpalmap_datap.conesearch()
        elif adpalmap_datap.query_type=='target': TAP_df = adpalmap_datap.target()
        elif adpalmap_datap.query_type=='keysearch': TAP_df = adpalmap_datap.keysearch()
        elif adpalmap_datap.query_type=='free': TAP_df = adpalmap_datap.free()

        adpalmap_datap.download_data(TAP_df)
        
    else:
        adpalmap_datap = None
        logger.info(f"'enable_tap_service' set to {adpalmap_config.enable_tap_service}. "
                    "Skipping data download")
    #--------------------------------------------------------------------------------------------#



    #--------------------------------------------------------------------------------------------#
    #Run SoFia
    from sofia.sopar import SoPar

    if adpalmap_config.enable_sofia == True:

        if adpalmap_config.run_mode == 'emission':

            adpalmap_sopar_emi = SoPar(sofia_file_path=adpalmap_config.sofia_emi_file)
            #Update sofia abs file with the -sop parameters
            adpalmap_sopar_emi.update_input_parameters(args.sofia_par, adpalmap_main=adpalmap_config, 
                                                       adpalmap_datap=adpalmap_datap, 
                                                       mode=adpalmap_config.run_mode)  
            if adpalmap_config.auto_setup == True:
                adpalmap_sopar_emi.auto_setup()
            adpalmap_sopar_emi.run_sofia(adpalmap_config, mode=adpalmap_config.run_mode)

            if adpalmap_config.quality_assesment == True:
                logger.info('Starting the quality assesment...')
                if adpalmap_datap is not None:
                    adpalmap_datap.download_mask(TAP_df)
                    adpalmap_sopar_emi.quality_assesment(adpalmap_datap)
                else:
                    logger.warning(f"'enable_tap_service' is set to False. All checks will not be "
                                   "performed.")
                    adpalmap_sopar_emi.quality_assesment(adpalmap_datap)


        elif adpalmap_config.run_mode == 'absorption':

            adpalmap_sopar_abs = SoPar(sofia_file_path=adpalmap_config.sofia_abs_file)
            #Update sofia abs file with the -sop parameters
            adpalmap_sopar_abs.update_input_parameters(args.sofia_par, adpalmap_main=adpalmap_config, 
                                                       adpalmap_datap=adpalmap_datap, 
                                                       mode=adpalmap_config.run_mode)   
            if adpalmap_config.auto_setup == True:
                adpalmap_sopar_abs.auto_setup()
            adpalmap_sopar_abs.run_sofia(adpalmap_config, mode=adpalmap_config.run_mode)

            if adpalmap_config.quality_assesment == True:
                if adpalmap_datap is not None:
                    adpalmap_datap.download_mask(TAP_df)
                    adpalmap_sopar_abs.quality_assesment(adpalmap_datap)
                else:
                    logger.warning(f"'enable_tap_service' is set to False. All checks in the QA will"
                                   " not be performed.")
                    adpalmap_sopar_abs.quality_assesment(adpalmap_datap)

        elif adpalmap_config.run_mode == 'both':

            adpalmap_sopar_abs = SoPar(sofia_file_path=adpalmap_config.sofia_abs_file)
            adpalmap_sopar_emi = SoPar(sofia_file_path=adpalmap_config.sofia_emi_file)
            #Update sofia abs file with the -sop parameters
            adpalmap_sopar_abs.update_input_parameters(args.sofia_par, adpalmap_main=adpalmap_config, 
                                                       adpalmap_datap=adpalmap_datap, 
                                                       mode=adpalmap_config.run_mode)  
            #Update sofia emi file with the -sop parameters
            adpalmap_sopar_emi.update_input_parameters(args.sofia_par, adpalmap_main=adpalmap_config, 
                                                       adpalmap_datap=adpalmap_datap, 
                                                       mode=adpalmap_config.run_mode, run=0)   
            if adpalmap_config.auto_setup == True:
                adpalmap_sopar_emi.auto_setup()
                adpalmap_sopar_abs.auto_setup()

            adpalmap_sopar_abs.run_sofia(adpalmap_config, mode=adpalmap_config.run_mode)

            if adpalmap_config.quality_assesment == True:
                if adpalmap_datap is not None:
                    adpalmap_datap.download_mask(TAP_df)
                    adpalmap_sopar_abs.quality_assesment(adpalmap_datap)
                else:
                    logger.warning(f"'enable_tap_service' is set to False. All checks will not be "
                                   "performed.")
                    adpalmap_sopar_abs.quality_assesment(adpalmap_datap)

            adpalmap_sopar_emi.run_sofia(adpalmap_config, mode=adpalmap_config.run_mode, run=0)

            if adpalmap_config.quality_assesment == True:
                if adpalmap_datap is not None:
                    adpalmap_datap.download_mask(TAP_df)
                    adpalmap_sopar_emi.quality_assesment(adpalmap_datap)
                else:
                    logger.warning(f"'enable_tap_service' is set to False. All checks will not be "
                                   "performed.")
                    adpalmap_sopar_emi.quality_assesment(adpalmap_datap)

    else:
        logger.info(f"'enable_sofia' set to {adpalmap_config.enable_sofia_service}. "
                    "Skipping Sofia runs.")


    #--------------------------------------------------------------------------------------------#
    #Run SIP
    from sip.sipargs import SiPar

    if adpalmap_config.enable_sip == True:

        adpalmap_sipar = SiPar(sip_file_path=adpalmap_config.sip_par_file)
        print(adpalmap_sipar.__dict__)
        adpalmap_sipar.update_input_parameters(args.sip_args, adpalmap_config)
        print(adpalmap_sipar.__dict__)       

        if adpalmap_config.enable_sofia == True:
            
            if adpalmap_config.run_mode == 'emission':
                
                adpalmap_sipar.run_sip(adpalmap_config, sopar=adpalmap_sopar_emi)

            elif adpalmap_config.run_mode == 'absorption':
                
                adpalmap_sipar.run_sip(adpalmap_config, sopar=adpalmap_sopar_abs)

            elif adpalmap_config == 'both':
                
                adpalmap_sipar.run_sip(adpalmap_config, sopar=adpalmap_sopar_emi)
                adpalmap_sipar.run_sip(adpalmap_config, sopar=adpalmap_sopar_abs)
        
        else:
            adpalmap_sipar.run_sip(adpalmap_config)
            
    else:
        logger.info(f"'enable_sip' set to {adpalmap_config.enable_sip}. Skipping SIP runs.")
    #--------------------------------------------------------------------------------------------#
        
    logger.info("ADPALMAP end point")

    

# Run the main functions
if __name__ == '__main__':
    main()

