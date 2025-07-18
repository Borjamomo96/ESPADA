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

from rich.console import Console
from rich.markdown import Markdown
import yaml

import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from logging.handlers import QueueListener
from multiprocessing import Queue

import logging
from adplib.logger import Initial_Logger
from adplib.logger import Logger
from traceback import format_exc

import sys

DESCRIPTION = """
ADPALMAP: The ALMA Advanced Data Product Pipeline

Overview:
This pipeline automates ALMA data processing, including the SoFiA-2 and SIP softwares.
It allows, download files from the ALMA archive, processing multiple datasets in parallel, performing QA and obtain 
advance data products.

Included programs:
- SoFiA-2: Spectral cube processing (emission/absorption)
- SIP: SoFia Imaging Pipeline
- TAP: Automatic download from ALMA archive borrowing code from ALminer

Main options:
    -c, --config-file Main configuration file (YAML)
    -sop, --sofia-parameters Parameters for SoFia in key=value format
    -sarg, --sip-arguments Arguments for SIP
    -i, --info Information about a file or parameter

For detailed help on a file or parameter, use the command '-i|--info':
adpalmap -i <file|parameter>=<file_name|parameter_name>
"""




# Functions 
def show_info(topic):

    DOC_FILE = Path(__file__).parent / "doc/info_docs.yaml"
    console = Console()

    with open(DOC_FILE, 'r', encoding='utf-8') as f:
        docs = yaml.safe_load(f)

    if topic.startswith('file='):
        file_key = topic.split('=', 1)[1]
        text = docs.get('file', {}).get(file_key)
    elif topic.startswith('parameter='):
        param_key = topic.split('=', 1)[1]
        text = docs.get('parameter', {}).get(param_key)
    else:
        text = "# Invalid topic\nUse `-i file=name` or `-i parameter=name`"

    if text:
        console.print(Markdown(text))
    else:
        console.print(f"[red]No information found for '{topic}'[/red]")


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


def reorganize_log(log_path, worker_results):
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        pid_groups = {}
        main_pid = None
        main_final = []
        final_block = False
        sopar_workers = [worker[0] for worker in worker_results]
        sip_workers = [worker[1] for worker in worker_results]
        
        #Captura [PID:XXXX] y [XXXX]
        pid_pattern = re.compile(r'\[(?:PID:)?(\d+)\]')  

        sofia_start_pattern = re.compile(
            r"\[PID:(\d+)\].*SoFia start\. Mode: (\w+)\. Input data: ([\w\-\.]+)"
        )

        sip_start_pattern = re.compile(
            r"\[PID:(\d+)\].*SIP start\. Mode: (\w+)\. Input data: ([\w\-\.]+)"
        )

        for i, line in enumerate(lines):
            
            pid_match = (pid_pattern.search(line))
            #Es una línea sin PID. Hay algunas
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
                    sofia_match = sofia_start_pattern.search(line)
                    sip_match = sip_start_pattern.search(line)

                    if sofia_match:
                        pid, mode, input_name = sofia_match.groups()
                        # Buscar el log_path correspondiente en sopar_worker_results
                        log_found = False
                        for worker in sopar_workers:
                            for run in worker:
                                if (str(run['PID']) == pid and
                                    run['mode'] == mode and
                                    run['input_name'] == input_name):
                                    log_path_sofia = run['log_path']
                                    if log_path_sofia and Path(log_path_sofia).exists():
                                        with open(
                                            log_path_sofia, 'r', encoding='utf-8'
                                            ) as sofia_log:
                                            sofia_lines = sofia_log.readlines()
                                        # Opcional: indentar o marcar las líneas del log de SoFia
                                        pid_groups[current_pid].extend(
                                            [f"    {l}" for l in sofia_lines]
                                        )
                                        log_found = True
                                        break
                            if log_found:
                                break
                    elif sip_match:
                        pid, mode, input_name = sip_match.groups()
                        log_found = False
                        
                        for worker in sip_workers:
                            for run in worker:
                                if (str(run['PID']) == pid and
                                    run['mode'] == mode and
                                    run['input_name'] == input_name):
                                    log_path_sip = run['log_path']
                                    if log_path_sip and Path(log_path_sip).exists():
                                        
                                        with open(
                                            log_path_sip, 'r', encoding='utf-8'
                                            ) as sip_log:
                                            sip_lines = sip_log.readlines()
                                        # Opcional: indentar o marcar las líneas del log de SIP
                                        pid_groups[current_pid].extend(
                                            [f"    {l}" for l in sip_lines]
                                        )
                                        log_found = True
                                        break
                            if log_found:
                                break
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
        print(f"Fatal error reorganizing {log_path}. Error: {e}")
        Logger.raw(format_exc())
        
     
def calculate_workers(data_pack_list, max_cores):
    total_files = len(data_pack_list)
    
    #Estimación de memoria por proceso
    total_size = sum(os.path.getsize(data) for data, _, _, _ in data_pack_list if data)
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
                 mask_qa,
                 adpalmap_config, 
                 args, 
                 sofia_threads, 
                 number_list,
                 logger
    ):
    
    pid = os.getpid()

    #--------------------------------------------------------------------------------------------#
    #Run SoFia
    from adplib.sofia.sopar import SoPar

    if adpalmap_config.enable_sofia == True:

        sofia_report = []

        if adpalmap_config.run_mode == 'emission':

            adpalmap_sopar_emi = SoPar(
                sofia_file_path=adpalmap_config.sofia_emi_file, 
                sopar_mode=adpalmap_config.run_mode,
                pid = pid
                )
            
            adpalmap_sopar_emi.update_input_parameters(args.sofia_par, 
                                                       input_data=input_data, 
                                                       primary_beam=primary_beam, 
                                                       mask=mask,
                                                       mode=adpalmap_config.run_mode,
                                                       sofia_threads=sofia_threads
                                                       )  
            if adpalmap_config.auto_setup == True:
                adpalmap_sopar_emi.auto_setup()

            emi_dic_report = adpalmap_sopar_emi.run_sofia(adpalmap_config, mode=adpalmap_config.run_mode)

            sofia_report.append(emi_dic_report)

            if adpalmap_config.quality_assesment == True:
                if mask_qa:
                    adpalmap_sopar_emi.quality_assesment(mask_qa)
                else:
                    logger.warning(
                        f"'enable_tap_service' is set to False. All checks in the QA will not be "
                        "performed."
                    )
                    adpalmap_sopar_emi.quality_assesment()


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
                                                       mask=mask,
                                                       mode=adpalmap_config.run_mode,
                                                       sofia_threads=sofia_threads
                                                       )  
            if adpalmap_config.auto_setup == True:
                adpalmap_sopar_abs.auto_setup()

            abs_dic_report = adpalmap_sopar_abs.run_sofia(adpalmap_config, mode=adpalmap_config.run_mode)

            sofia_report.append(abs_dic_report)

            if adpalmap_config.quality_assesment == True:
                if mask_qa:
                    adpalmap_sopar_abs.quality_assesment(mask_qa)
                else:
                    logger.warning(
                        f"'enable_tap_service' is set to False. All checks in the QA will"
                        " not be performed."
                    )
                    adpalmap_sopar_abs.quality_assesment()


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
                                                       mask=mask,
                                                       mode=adpalmap_config.run_mode,
                                                       sofia_threads=sofia_threads
                                                       )  
            #Update sofia emi file with the -sop parameters
            adpalmap_sopar_emi.update_input_parameters(args.sofia_par, 
                                                       input_data=input_data, 
                                                       primary_beam=primary_beam, 
                                                       mask=mask,
                                                       mode=adpalmap_config.run_mode, 
                                                       run=0,
                                                       sofia_threads=sofia_threads
                                                       )   
            if adpalmap_config.auto_setup == True:
                adpalmap_sopar_emi.auto_setup()
                adpalmap_sopar_abs.auto_setup()

            abs_dic_report = adpalmap_sopar_abs.run_sofia(adpalmap_config, mode=adpalmap_config.run_mode)
            sofia_report.append(abs_dic_report)

            if adpalmap_config.quality_assesment == True:
                if mask_qa:
                    adpalmap_sopar_abs.quality_assesment(mask_qa)
                else:
                    logger.warning(f"'enable_tap_service' is set to False. All checks will not be "
                                   "performed in the QA.")
                    adpalmap_sopar_abs.quality_assesment()

            emi_dic_report = adpalmap_sopar_emi.run_sofia(adpalmap_config, mode=adpalmap_config.run_mode, run=0)
            sofia_report.append(emi_dic_report)
            
            if adpalmap_config.quality_assesment == True:
                if mask_qa:
                    adpalmap_sopar_emi.quality_assesment(mask_qa)
                else:
                    logger.warning(f"'enable_tap_service' is set to False. All checks will not be "
                                   "performed in the QA.")
                    adpalmap_sopar_emi.quality_assesment()

    else:
        sofia_report = []
        logger.info(f"'enable_sofia' set to {adpalmap_config.enable_sofia}. "
                    "Skipping Sofia runs.")


    #--------------------------------------------------------------------------------------------#
    #Run SIP
    from adplib.sip.sipargs import SiPar

    if adpalmap_config.enable_sip == True:

        sip_report = []

        adpalmap_sipar = SiPar(
            sip_file_path = adpalmap_config.sip_par_file,
            adpalmap_config = adpalmap_config,
            input_data = input_data,
            sargs = args.sip_args,
            number_list = number_list,
            number = number,
            pid = os.getpid()
            )
        
        adpalmap_sipar.update_input_parameters(args.sip_args, adpalmap_config)
              
        
        if adpalmap_config.enable_sofia == True:
            
            if adpalmap_config.run_mode == 'emission':         
                sip_report.append(
                    adpalmap_sipar.run_sip(adpalmap_config, sopar=adpalmap_sopar_emi)
                )

            elif adpalmap_config.run_mode == 'absorption':
                sip_report.append(
                    adpalmap_sipar.run_sip(adpalmap_config, sopar=adpalmap_sopar_abs)
                )
            elif adpalmap_config.run_mode == 'both':
                sip_report.append(
                    adpalmap_sipar.run_sip(adpalmap_config, sopar=adpalmap_sopar_abs)
                )
                sip_report.append(
                    adpalmap_sipar.run_sip(adpalmap_config, sopar=adpalmap_sopar_emi, run=0)
                )
        elif adpalmap_config.enable_sofia == False and adpalmap_config.enable_tap_service == True:
            if adpalmap_config.run_mode == 'emission':         
                sip_report.append(
                    adpalmap_sipar.run_sip(adpalmap_config)
                )
            elif adpalmap_config.run_mode == 'absorption':
                sip_report.append(
                    adpalmap_sipar.run_sip(adpalmap_config)
                )
            elif adpalmap_config.run_mode == 'both':
                sip_report.append(
                    adpalmap_sipar.run_sip(adpalmap_config)
                )
                sip_report.append(
                    adpalmap_sipar.run_sip(adpalmap_config, run=0)
                )
        else:
            sip_report.append(
                adpalmap_sipar.run_sip(adpalmap_config)
            )
    else:
        sip_report = []
        logger.info(f"'enable_sip' set to {adpalmap_config.enable_sip}. Skipping SIP runs.")
    #--------------------------------------------------------------------------------------------#

    return sofia_report, sip_report  


#Functions html report

def get_html_dataset(dataset_list, html_report):
    
    html_report = [{'inputData_path' : data} for data, pb, mask, _ in dataset_list]

    return html_report


def transformar_report(report):
    datasets = []
    for idx, dataset in enumerate(report):
        # Extraer el nombre del dataset del primer diccionario disponible
        nombre = None
        for sublist in dataset:
            if sublist and isinstance(sublist[0], dict) and 'input_name' in sublist[0]:
                nombre = sublist[0]['input_name']
                break
        if not nombre:
            nombre = f"Dataset {idx+1}"

        softwares = []
        for sublist in dataset:
            for entry in sublist:
                # Extraer nombre del software
                software_nombre = entry.get('software_id', 'Desconocido')
                # Determinar estado según la clave 'error'
                error = entry.get('error', '')
                if error:
                    estado = 'error'
                else:
                    estado = 'ok'
                # Puedes personalizar el log según el software y el error
                log = error if error else f"{software_nombre} ejecutado correctamente."
                # Puedes añadir más campos si lo necesitas
                software_dict = {
                    'nombre': software_nombre,
                    'estado': estado,
                    'log': log
                }
                softwares.append(software_dict)

        # Ejemplo: puedes extraer imágenes si tienes esa información en los diccionarios
        imagenes = []
        for sublist in dataset:
            for entry in sublist:
                # Si tienes paths de imágenes, agrégalas aquí
                if 'imagenes' in entry:
                    for img in entry['imagenes']:
                        imagenes.append({
                            'url': img.get('url', ''),
                            'descripcion': img.get('descripcion', '')
                        })
        # Si no hay imágenes, puedes dejar la lista vacía o poner un ejemplo
        datasets.append({
            'nombre': nombre,
            'softwares': softwares,
            'imagenes': imagenes
        })
    return datasets


def main():

    log_flag = False
    worker_results = []
    worker_exceptions = []
    html_report = []

    try:
        # Parse args:

        parser = argparse.ArgumentParser(
                        prog='adpalmap',
                        formatter_class=argparse.RawDescriptionHelpFormatter,
                        description=DESCRIPTION,
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
        parser.add_argument(
            '-i', '--info', dest='info',  metavar='TOPIC',
            type=str, default=None,
            help="Displays detailed information about a file or parameter. Example: "
            "-i file=config.yaml or -i parameter=fitsonly"
        )

        args = parser.parse_args()
        
        if args.sofia_par: args.sofia_par = dict(args.sofia_par)
        if args.sip_args: args.sip_args = sipargs_to_dict(args.sip_args)
        if args.info:
            show_info(args.info)
            sys.exit(-1)

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

        log_flag = True
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
                print(adpalmap_datap.data_list)
                if not hasattr(adpalmap_datap, 'mask_qa_list'):
                    adpalmap_datap.mask_qa_list = [""] * len(adpalmap_datap.data_list)
            
        else:
            adpalmap_datap = None
            logger.info(f"'enable_tap_service' set to {adpalmap_config.enable_tap_service}. "
                        "Skipping data download")
        #--------------------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------------------#

        #Al igual que antes, a este bloque solo entra si input es False y Tap True.
        if adpalmap_config.enable_tap_service == True:
            
            data_pack_list = [
                (data, pb, mask, mask_qa)
                for data, pb, mask, mask_qa in zip(
                    adpalmap_datap.data_list, 
                    adpalmap_datap.pb_list, 
                    adpalmap_datap.mask_list,
                    adpalmap_datap.mask_qa_list
                )
            ]
        #Datos ya descargados
        else: 
            data_pack_list = [dataset + ('',) for dataset in adpalmap_config.input_data_set]


        number_list = list(range(len(data_pack_list)))

        html_report = get_html_dataset(data_pack_list, html_report)

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

        reserved_cores = 0
        available_cores = max_cores - reserved_cores 

        max_workers = calculate_workers(data_pack_list, available_cores)

        if max_workers < 1:
            logger.warning(
                "The worker number is lower than 1. One or more of the datasets are too large"
                " for the available RAM. The minimum worker count is set to 1, but keep in "
                "mind that unexpected errors may occur."
            )
            max_workers = 1

        sofia_threads = max(1, available_cores // max_workers) if max_workers > 0 else 1

        logger.info(
            f"The worker number has been set to {max_workers}"
        )

        #--------------------------------------------------------------------------------------------#
        
        #--------------------------------------------------------------------------------------------#

        with ProcessPoolExecutor(max_workers=max_workers) as pool:
    
            futures = [
                pool.submit(
                    process_data, 
                    i, data, primary_beam, mask, mask_qa,
                    adpalmap_config,
                    args, sofia_threads, number_list,
                    Logger.setup_child_logger(log_queue)
                    )
                for i, (data, primary_beam, mask, mask_qa) in enumerate(data_pack_list)
            ]
            

            for future in as_completed(futures):  
                try:
                    result = future.result()
                    worker_results.append(result)
                #Este primero porque python lee Excepciones de arriba a abajo
                #Errores salvables. El resto de procesos sigue corriendo
                except RecoverableError as e:  
                    worker_exceptions.append(e)
                    #Quitando esta línea eliminamos el traceback
                    Logger.raw(format_exc())
                #Errores criticos
                except (ValueError, FileNotFoundError) as e:
                    worker_exceptions.append(e)
                    raise 
                except SystemExit as e:
                    worker_exceptions.append(e)
                except RuntimeError as e:
                    worker_exceptions.append(e)
                    raise 
                except Exception as e:
                    worker_exceptions.append(e)
                    logger.critical(
                        f"Unexpected error: {e}. "
                         "Please open an issue on GitHub "
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

        if log_flag:
            log_path = Logger.get_log_filename()
            reorganize_log(log_path, worker_results)

        #if adpalmap_config.html_report:
            


# Run the main functions
if __name__ == '__main__':
    main()

