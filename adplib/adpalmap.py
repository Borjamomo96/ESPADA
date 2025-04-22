"""
Contact: Borja Montoro Molina (borjamomo96@gmail.com)
"""
#Configuration
from adplib.exceptions import RecoverableError, RecoverableValueError, RecoverableFileNotFoundError
from adplib.config import Config

import os
from datetime import datetime
import re
import time
from pathlib import Path
import argparse
import numpy as np
import psutil

import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from logging.handlers import QueueListener
from multiprocessing import Queue

import logging
from adplib.logger import Initial_Logger
from adplib.logger import Logger
from traceback import format_exc

import sys

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


def reorganize_log(log_path):
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        pid_groups = {}
        main_pid = None
        main_final = []
        final_block = False
        
        #Captura [PID:XXXX] y [XXXX]
        pid_pattern = re.compile(r'\[(?:PID:)?(\d+)\]')  

        for i, line in enumerate(lines):
            
                      
            pid_match = (pid_pattern.search(line))

            if pid_match is None:
                continue

            current_pid = pid_match.group(1)

            if current_pid not in pid_groups:
                if not main_pid:
                    main_pid = current_pid
                pid_groups[current_pid] = []

            if "ADPALMAP successfully ended" in line:
                main_final.append(line)
                final_block = True

            else:    
                if final_block == False:
                    pid_groups[current_pid].append(line)
                else:
                    main_final.append(line)

        sorted_lines = []

        #Mensajes iniciales del main
        sorted_lines.extend(pid_groups.pop(main_pid))

        #Subprocesos ordenados numéricamente
        sub_pids = [pid for pid in pid_groups if pid != main_pid]
        
        for pid in sorted(sub_pids, key=int):
            sorted_lines.append(f"\n=== Subprocess PID: {pid} start ===\n")
            sorted_lines.extend(pid_groups[pid])
            sorted_lines.append(f"===  Subprocess PID: {pid} end  ===\n\n")


        sorted_lines.extend(main_final)

        sorted_log = log_path.name.replace("raw_", "", 1)
        sorted_log_path = log_path.with_name(sorted_log)

        with open(sorted_log_path, 'w', encoding='utf-8') as f:
            f.writelines(sorted_lines)
            
    except Exception as e:
        print(f"Fatal error reorganizing log: {e}")
     

def calculate_workers(data_pack_list, max_cores):
    total_files = len(data_pack_list)
    
    #Estimación de memoria por proceso
    total_size = sum(os.path.getsize(data) for data, _, _ in data_pack_list if data)
    avg_size = (total_size / total_files) if total_files > 0 else 0
    #Memoria disponible en GB
    mem_available = psutil.virtual_memory().available / 1024**3  
    #Heurística:1.5x tamaño + 1GB base
    relative_memory_used_sofia = 2.25
    mem_per_process = (avg_size * relative_memory_used_sofia / 1024**3) + 1  
    
    max_workers_mem = int(mem_available // mem_per_process) if mem_per_process > 0 else max_cores
    max_workers = min(max_cores, max_workers_mem, total_files)
    
    return max_workers


def process_data(number,
                 input_data, 
                 primary_beam, 
                 mask, 
                 adpalmap_config, 
                 args, 
                 sofia_threads, 
                 number_list,
                 logger
    ):
    
    #--------------------------------------------------------------------------------------------#
    #Run SoFia
    from adplib.sofia.sopar import SoPar

    if adpalmap_config.enable_sofia == True:

        if adpalmap_config.run_mode == 'emission':
            
            adpalmap_sopar_emi = SoPar(
                sofia_file_path=adpalmap_config.sofia_emi_file, 
                sopar_mode="emission",
                pid = os.getpid()
                )
            #Update sofia abs file with the -sop parameters
            adpalmap_sopar_emi.update_input_parameters(args.sofia_par, 
                                                       input_data=input_data, 
                                                       primary_beam=primary_beam, 
                                                       mode=adpalmap_config.run_mode,
                                                       sofia_threads=sofia_threads
                                                       )  
            if adpalmap_config.auto_setup == True:
                adpalmap_sopar_emi.auto_setup()

            adpalmap_sopar_emi.run_sofia(adpalmap_config, mode=adpalmap_config.run_mode)

            if adpalmap_config.quality_assesment == True:
                if mask is not None:
                    adpalmap_sopar_emi.quality_assesment(mask)
                else:
                    logger.warning(
                        f"'enable_tap_service' is set to False. All checks in the QA will not be "
                        "performed."
                    )
                    adpalmap_sopar_emi.quality_assesment(mask)


        elif adpalmap_config.run_mode == 'absorption':

            adpalmap_sopar_abs = SoPar(
                sofia_file_path=adpalmap_config.sofia_abs_file, 
                sopar_mode="absorption",
                pid = os.getpid()
                )
            #Update sofia abs file with the -sop parameters
            adpalmap_sopar_abs.update_input_parameters(args.sofia_par, 
                                                       input_data=input_data, 
                                                       primary_beam=primary_beam, 
                                                       mode=adpalmap_config.run_mode,
                                                       sofia_threads=sofia_threads
                                                       )  
            if adpalmap_config.auto_setup == True:
                adpalmap_sopar_abs.auto_setup()

            adpalmap_sopar_abs.run_sofia(adpalmap_config, mode=adpalmap_config.run_mode)

            if adpalmap_config.quality_assesment == True:
                if mask is not None:
                    adpalmap_sopar_abs.quality_assesment(mask)
                else:
                    logger.warning(
                        f"'enable_tap_service' is set to False. All checks in the QA will"
                        " not be performed."
                    )
                    adpalmap_sopar_abs.quality_assesment(mask)

        elif adpalmap_config.run_mode == 'both':

            adpalmap_sopar_abs = SoPar(
                sofia_file_path=adpalmap_config.sofia_abs_file,
                sopar_mode="absorption",
                pid = os.getpid()
                )
            adpalmap_sopar_emi = SoPar(
                sofia_file_path=adpalmap_config.sofia_emi_file,
                sopar_mode="emission",
                pid = os.getpid()
                )
            #Update sofia abs file with the -sop parameters
            adpalmap_sopar_abs.update_input_parameters(args.sofia_par, 
                                                       input_data=input_data, 
                                                       primary_beam=primary_beam, 
                                                       mode=adpalmap_config.run_mode,
                                                       sofia_threads=sofia_threads
                                                       )  
            #Update sofia emi file with the -sop parameters
            adpalmap_sopar_emi.update_input_parameters(args.sofia_par, 
                                                       input_data=input_data, 
                                                       primary_beam=primary_beam, 
                                                       mode=adpalmap_config.run_mode, 
                                                       run=0,
                                                       sofia_threads=sofia_threads
                                                       )   
            if adpalmap_config.auto_setup == True:
                adpalmap_sopar_emi.auto_setup()
                adpalmap_sopar_abs.auto_setup()

            adpalmap_sopar_abs.run_sofia(adpalmap_config, mode=adpalmap_config.run_mode)

            if adpalmap_config.quality_assesment == True:
                if mask is not None:
                    adpalmap_sopar_abs.quality_assesment(mask)
                else:
                    logger.warning(f"'enable_tap_service' is set to False. All checks will not be "
                                   "performed in the QA.")
                    adpalmap_sopar_abs.quality_assesment(mask)

            adpalmap_sopar_emi.run_sofia(adpalmap_config, mode=adpalmap_config.run_mode, run=0)

            if adpalmap_config.quality_assesment == True:
                if mask is not None:
                    adpalmap_sopar_emi.quality_assesment(mask)
                else:
                    logger.warning(f"'enable_tap_service' is set to False. All checks will not be "
                                   "performed in the QA.")
                    adpalmap_sopar_emi.quality_assesment(mask)

    else:
        logger.info(f"'enable_sofia' set to {adpalmap_config.enable_sofia}. "
                    "Skipping Sofia runs.")


    #--------------------------------------------------------------------------------------------#
    #Run SIP
    from adplib.sip.sipargs import SiPar

    if adpalmap_config.enable_sip == True:

        adpalmap_sipar = SiPar(
            sip_file_path = adpalmap_config.sip_par_file,
            adpalmap_config = adpalmap_config,
            input_data = input_data,
            sargs = args.sip_args,
            number_list = number_list,
            number = number
            )
        
        adpalmap_sipar.update_input_parameters(args.sip_args, adpalmap_config)
              
        
        if adpalmap_config.enable_sofia == True:
            
            if adpalmap_config.run_mode == 'emission':         
                adpalmap_sipar.run_sip(adpalmap_config, sopar=adpalmap_sopar_emi)

            elif adpalmap_config.run_mode == 'absorption':
                adpalmap_sipar.run_sip(adpalmap_config, sopar=adpalmap_sopar_abs)

            elif adpalmap_config.run_mode == 'both':
                adpalmap_sipar.run_sip(adpalmap_config, sopar=adpalmap_sopar_abs)
                adpalmap_sipar.run_sip(adpalmap_config, sopar=adpalmap_sopar_emi, run=0)
        
        elif adpalmap_config.enable_sofia == False and adpalmap_config.enable_tap_service == True:
            if adpalmap_config.run_mode == 'emission':         
                adpalmap_sipar.run_sip(adpalmap_config)

            elif adpalmap_config.run_mode == 'absorption':
                adpalmap_sipar.run_sip(adpalmap_config)

            elif adpalmap_config.run_mode == 'both':
                adpalmap_sipar.run_sip(adpalmap_config)
                adpalmap_sipar.run_sip(adpalmap_config, run=0)

        else:
            adpalmap_sipar.run_sip(adpalmap_config)

    else:
        logger.info(f"'enable_sip' set to {adpalmap_config.enable_sip}. Skipping SIP runs.")
    #--------------------------------------------------------------------------------------------#


def main():
    try:
        # Parse args:

        parser = argparse.ArgumentParser(
                        prog='adpalmap',
                        formatter_class=argparse.RawDescriptionHelpFormatter,
                        description='The ALMA advance data product pipeline',
                        epilog= __doc__) 


        parser.add_argument(
            '-c', '--config-file', dest='config_file', default=None,
            help="<Optional> Path to the master config file to use. By default, "
            "APDALMAP will try to use the file 'config.yaml'"
        )
        parser.add_argument(
            '-sop', '--sofia-parameters', dest='sofia_par', nargs='+', 
            type=parse_sofia_par, default=None,
            help="<Optional> List of the parameters following the instructions of SoFia2 "
            "cookbook. Note, the parameter introduced here will overwrite the "
            "corresponding parameter in all the sofia files used in ADPALMAP"
        )
        parser.add_argument(
            '-sarg','--sip-arguments', dest='sip_args', nargs=argparse.REMAINDER, 
            type=str, default=None, help="<Optional> Optional arguments for the SoFia "
            "Imaging Pipeline (SIP). Do not add any other arguments after using -sarg."
            " If you add -sop ... or -c ... they will simply be ignored.."
        )
        
        args = parser.parse_args()
        
        if args.sofia_par: args.sofia_par = dict(args.sofia_par)
        if args.sip_args: args.sip_args = sipargs_to_dict(args.sip_args)

        #--------------------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------------------#

        ini_logger = Initial_Logger.get_initial_logger()
        
        if (args.config_file is None):
            ini_logger.warning("No config.yaml file specified, default config.yaml file will be used")
            adpalmap_config = Config()
        else:
            adpalmap_config = Config(config_path=args.config_file)    
        
        #--------------------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------------------#
        
        log_queue = Queue()  
        queue_listener = QueueListener(log_queue, *logging.getLogger().handlers) 
        queue_listener.start() 

        logger = Logger.get_logger(
            log_path=adpalmap_config.log_file, 
            clear_logs=adpalmap_config.clear_logs,
            queue=log_queue
        )

        #--------------------------------------------------------------------------------------------# 
        logger.info("ADPALMAP start point")
        start = time.perf_counter()
        #--------------------------------------------------------------------------------------------#

        #Optionally download data from ALMA archive
        from adplib.tap.datap import datap

        if adpalmap_config.enable_tap_service == True:

            if adpalmap_config.input_data_set is not None or adpalmap_config.input_file is not None:
                logger.warning("The paremeter input_data or input_file specified in the "
                            f"{args.config_file} will be ignore. This run will use the requested "
                            "download data.")

            adpalmap_datap = datap(download_path=adpalmap_config.download_par_file)
            if adpalmap_datap.query_type=='proposal': TAP_df = adpalmap_datap.proposal_id()
            elif adpalmap_datap.query_type=='conesearch': TAP_df = adpalmap_datap.conesearch()
            elif adpalmap_datap.query_type=='target': TAP_df = adpalmap_datap.target()
            elif adpalmap_datap.query_type=='keysearch': TAP_df = adpalmap_datap.keysearch()
            elif adpalmap_datap.query_type=='free': TAP_df = adpalmap_datap.free()

            adpalmap_datap.download_data(TAP_df)

            if adpalmap_config.quality_assesment == True:
                adpalmap_datap.download_mask(TAP_df)
            
        else:
            adpalmap_datap = None
            logger.info(f"'enable_tap_service' set to {adpalmap_config.enable_tap_service}. "
                        "Skipping data download")
        #--------------------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------------------#

        #Al igual que antes, a este bloque solo entra si input es False y Tap True.
        if adpalmap_config.enable_tap_service == True:
            
            data_pack_list = [
                (data, pb, mask)
                for data, pb, mask in zip(
                    adpalmap_datap.data_list, 
                    adpalmap_datap.pb_list, 
                    adpalmap_datap.mask_list
                )
            ]
        #Datos ya descargados
        else: 
            data_pack_list = adpalmap_config.input_data_set

        number_list = list(range(len(data_pack_list)))
        #--------------------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------------------#

        '''#Número máx de cores dinámico
        cpu_cores = multiprocessing.cpu_count()

        if adpalmap_config.num_cores is not None:

            if adpalmap_config.num_cores > cpu_cores:
                logger.warning(
                    "The number of cores indicated is greater than the number of cores available "
                    f"in the CPU. The number of cores has been assigned as: {cpu_cores}. "
                )
                max_cores = cpu_cores 
            else:
                max_cores = adpalmap_config.num_cores

        else:
            max_cores = cpu_cores

       
        if len(data_pack_list) <= max_cores:
            max_workers = len(data_pack_list)
            s_cores = max(1, max_cores // max_workers)
        else:
            max_workers = max_cores
            s_cores = 1  '''
        
        cpu_cores = multiprocessing.cpu_count()
        
        if adpalmap_config.num_cores is not None:

            if adpalmap_config.num_cores > cpu_cores:
                logger.warning(
                    "The number of cores indicated is greater than the number of cores available "
                    f"in the CPU. The number of cores has been assigned as: {cpu_cores}. "
                )
                max_cores = cpu_cores 
            else:
                max_cores = adpalmap_config.num_cores

        else:
            max_cores = cpu_cores

        reserved_cores = 1
        available_cores = max_cores - reserved_cores 

        max_workers = calculate_workers(data_pack_list, available_cores)

        sofia_threads = max(1, available_cores // max_workers) if max_workers > 0 else 1

        #--------------------------------------------------------------------------------------------#
        sys.exit(-1)
        #--------------------------------------------------------------------------------------------#

        with ProcessPoolExecutor(max_workers=max_workers) as pool:
    
            futures = [
                pool.submit(
                    process_data, 
                    i, data, primary_beam, mask, 
                    adpalmap_config,
                    args, sofia_threads, number_list,
                    Logger.setup_child_logger(log_queue)
                    )
                for i, (data, primary_beam, mask) in enumerate(data_pack_list)
            ]
            
            results = []
            exceptions = []
            for future in as_completed(futures):  
                try:
                    result = future.result()
                    results.append(result)
                #Este primero porque python lee Excepciones de arriba a abajo
                #Errores salvables. El resto de procesos sigue corriendo
                except RecoverableError as e:  
                    exceptions.append(e)
                    #Quitando esta línea eliminamos el traceback
                    Logger.raw(format_exc())
                #Errores criticos
                except (ValueError, FileNotFoundError) as e:
                    exceptions.append(e)
                    raise 
                except SystemExit as e:
                    exceptions.append(e)
                except RuntimeError as e:
                    exceptions.append(e)
                    raise 
                except Exception as e:
                    exceptions.append(e)
                    logger.critical(
                        f"Unexpected error. Please open an issue on GitHub "
                         "https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
                         "case."
                    )
                    raise 
        

        #--------------------------------------------------------------------------------------------#

        logger.info("ADPALMAP successfully ended")
        finish = time.perf_counter()
        logger.info(f"Execution time: {round(finish-start, 2)} second(s)")
        queue_listener.stop() 

    finally:
        log_path = Logger.get_log_filename()
        reorganize_log(log_path)

# Run the main functions
if __name__ == '__main__':
    main()

