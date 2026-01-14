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


def get_template_path():
    
    try:
        import adpweb
        adpweb_dir = Path(adpweb.__file__).parent
        template_path = adpweb_dir / "templates" / "report.html"
        
        if template_path.exists():
            return template_path
    except ImportError:
        pass
    
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    
    posibles = [
        project_root / "adpweb" / "templates" / "report.html",  
        project_root.parent / "adpweb" / "templates" / "report.html",
        Path.cwd() / "adpweb" / "templates" / "report.html",  
    ]
    
    for path in posibles:
        if path.exists():
            return path

    raise FileNotFoundError("No 'report.html' template could be found.")

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

    aux_logger = Initial_Logger.get_initial_logger()
    
    try:
        
    ##############################################################################################

        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        pid_groups = {}
        main_pid = None
        main_final = []
        final_block = False
        # Diccionario para trackear qué PIDs ya pasaron por group
        pid_group_flags = {}

        # Worker from SoFiA-2 - SIP - Group
        sopar_workers = [worker[0] for worker in worker_results]
        sip_workers = [worker[1] for worker in worker_results]
        group_workers = [worker[3] for worker in worker_results]

        
        #Captura [PID:XXXX] y [XXXX]
        pid_pattern = re.compile(r'\[(?:PID:)?(\d+)\]')  

        sofia_start_pattern = re.compile(
            r"\[PID:(\d+)\].*SoFia start\. Mode: (\w+)\. Input data: ([\w\-\.]+)"
        )

        sip_start_pattern = re.compile(
            r"\[PID:(\d+)\].*SIP start\. Mode: (\w+)\. Input data: ([\w\-\.]+)"
        )
        
        group_start_pattern = re.compile(
            r"\[PID:(\d+)\].*Source Grouping start\. Mode: (\w+)\. Input data: ([\w\-\.]+)"
        )

    ##############################################################################################

        for i, line in enumerate(lines):
            
            pid_match = (pid_pattern.search(line))

            # For lines without PID ([PID]). There are a few
            if pid_match is None:
                continue

            current_pid = pid_match.group(1)
            if current_pid not in pid_groups:
                if not main_pid:
                    main_pid = current_pid
                pid_groups[current_pid] = []
                # Iniciate the flag for this PID (False = before group)
                pid_group_flags[current_pid] = False

            if "ADPALMAP successfully ended" in line:
                main_final.append(line)
                final_block = True
            else:    
                if final_block == False:

                    pid_groups[current_pid].append(line)
                    sofia_match = sofia_start_pattern.search(line)
                    sip_match = sip_start_pattern.search(line)
                    group_match = group_start_pattern.search(line)
        
    ##############################################################################################
     
                    if sofia_match:
                        pid, mode, input_name = sofia_match.groups()
                        log_found = False
                        
                        if not pid_group_flags[pid]:  # Before group - find regular ones
                            
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
                                            pid_groups[current_pid].append(
                                                f"    [INCLUDING SOFIA LOG: {log_path_sofia}]\n"
                                            )
                                            pid_groups[current_pid].extend(
                                                [f"    {l}" for l in sofia_lines]
                                            )
                                            log_found = True
                                            break
                                        else:
                                            aux_logger.warning(
                                                "Error reorganizing the final logfile. "
                                                f"The SoFiA-2 logfile '{log_path_sofia}' "
                                                "does not exits."
                                            )
                                if log_found:
                                    break
                        else:  # After group - find in group
                            for worker in group_workers:
                                for run in worker:
                                    if (str(run['PID']) == pid and
                                        run.get('mode') == mode and
                                        run.get('input_name') == input_name and
                                        run.get('software_id') == 'SoFiA-2'):
                                        log_path_sofia = run['log_path']

                                        if log_path_sofia and Path(log_path_sofia).exists():
                                            pid_groups[current_pid].append(
                                                f"\n    === Group SoFiA-2 Execution "
                                                f"(Mode: {mode}) ===\n")
                                            with open(
                                                log_path_sofia, 'r', encoding='utf-8'
                                                ) as sofia_log:
                                                sofia_lines = sofia_log.readlines()
                                            pid_groups[current_pid].append(
                                                    f"    [INCLUDING SOFIA LOG: {log_path_sofia}]\n"
                                                )
                                            pid_groups[current_pid].extend(
                                                [f"        {l}" for l in sofia_lines]
                                            )
                                            log_found = True
                                            break
                                        else:
                                            aux_logger.warning(
                                                "Error reorganizing the final logfile. "
                                                f"The group SoFiA-2 logfile '{log_path_sofia}' "
                                                "does not exits."
                                            )

    ##############################################################################################
    
                    elif sip_match:
                        pid, mode, input_name = sip_match.groups()
                        log_found = False
                        
                        if not pid_group_flags[pid]:  
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
                                            pid_groups[current_pid].append(
                                                f"    [INCLUDING SIP LOG: {log_path_sip}]\n"
                                            )
                                            pid_groups[current_pid].extend(
                                                [f"    {l}" for l in sip_lines]
                                            )
                                            log_found = True
                                            break
                                        else:
                                            aux_logger.warning(
                                                "Error reorganizing the final logfile. "
                                                f"The SIP logfile '{log_path_sip}' "
                                                "does not exits."
                                            )
                                if log_found:
                                    break
                        else:  
                            for worker in group_workers:
                                for run in worker:
                                    if (str(run['PID']) == pid and
                                        run.get('mode') == mode and
                                        run.get('input_name') == input_name and
                                        run.get('software_id') == 'SIP'):
                                        log_path_sip = run['log_path']

                                        if log_path_sip and Path(log_path_sip).exists():
                                            pid_groups[current_pid].append(
                                                f"\n    === Group SIP Execution (Mode: {mode}) ===\n")
                                            with open(
                                                log_path_sip, 'r', encoding='utf-8'
                                                ) as sip_log:
                                                sip_lines = sip_log.readlines()
                                            pid_groups[current_pid].append(
                                                    f"    [INCLUDING SIP LOG: {log_path_sip}]\n"
                                                )
                                            pid_groups[current_pid].extend(
                                                [f"        {l}" for l in sip_lines]
                                            )
                                            log_found = True
                                            break
                                        else:
                                            aux_logger.warning(
                                                "Error reorganizing the final logfile. "
                                                f"The group SIP logfile '{log_path_sip}' "
                                                "does not exits."
                                            )

    ##############################################################################################

                    elif group_match:
                        pid, mode, input_name = group_match.groups()
                        # Mark that this specific PID has already been through the group
                        pid_group_flags[pid] = True

                else:
                    main_final.append(line)

    ##############################################################################################
    
        sorted_lines = []

        # Mensajes iniciales del main
        sorted_lines.extend(pid_groups.pop(main_pid))

        # Subprocesos ordenados numéricamente
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
        
        return sorted_log_path
    
    ##############################################################################################
            
    except Exception as e:
        print(f"Fatal error reorganizing {log_path}. Error: {e}")
        Logger.raw(format_exc())

        sorted_log = log_path.name.replace("raw_", "", 1)
        sorted_log_path = log_path.with_name(sorted_log)
        with open(sorted_log_path, 'w', encoding='utf-8') as f:
            f.writelines(f"Fatal error reorganizing {log_path}. Error: {e}")
        
        return sorted_log_path


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


def process_data(id_number,
                 input_data, 
                 primary_beam, 
                 mask, 
                 ancillary_data,
                 adpalmap_config, 
                 args, 
                 sofia_threads, 
                 number_list,
                 logger
    ):
    
    pid = os.getpid()

    ##############################################################################################
    #Run SoFia
    from adplib.sofia.sopar import SoPar

    if adpalmap_config.enable_sofia == True:

        sofia_report = []
        qa_report = []

        if adpalmap_config.run_mode == 'emission':
            
            # 'mode' variable has only 'emission' or 'absorption' while adpalmap_config.run_mode
            # has also 'both' which has no sense for logs. The 'mode' variable is needed.
            adpalmap_sopar_emi = SoPar(
                sofia_file_path=adpalmap_config.sofia_emi_file, 
                adpalmap_config=adpalmap_config,
                mode='emission', 
                pid= pid,
                sofia_threads=sofia_threads
                )
            
            adpalmap_sopar_emi.update_input_parameters(args.sofia_par, 
                                                       input_data=input_data, 
                                                       primary_beam=primary_beam, 
                                                       mask=mask
                                                       )  
            if adpalmap_config.auto_setup == True:
                adpalmap_sopar_emi.auto_setup()

            emi_sofia_report = adpalmap_sopar_emi.run_sofia()

            sofia_report.append(emi_sofia_report)

            if adpalmap_config.enable_tap_service == True:
                if mask:
                    emi_qa_report = adpalmap_sopar_emi.quality_assesment(mask)
                    qa_report.append(emi_qa_report)
                else:
                    logger.warning("No ALMA file mask available. Reduced QA image.")
                    emi_qa_report = adpalmap_sopar_emi.quality_assesment()
                    qa_report.append(emi_qa_report)
            else:
                logger.warning(
                    f"'enable_tap_service' is set to False. All checks in the QA will not be "
                    "performed."
                )
                emi_qa_report = adpalmap_sopar_emi.quality_assesment()
                qa_report.append(emi_qa_report)


        elif adpalmap_config.run_mode == 'absorption':

            adpalmap_sopar_abs = SoPar(
                sofia_file_path=adpalmap_config.sofia_abs_file, 
                adpalmap_config=adpalmap_config,
                mode='absorption',
                pid = pid,
                sofia_threads=sofia_threads
                )
            #Update sofia abs file with the -sop parameters
            adpalmap_sopar_abs.update_input_parameters(args.sofia_par, 
                                                       input_data=input_data, 
                                                       primary_beam=primary_beam, 
                                                       mask=mask
                                                       )  
            if adpalmap_config.auto_setup == True:
                adpalmap_sopar_abs.auto_setup()

            abs_sofia_report = adpalmap_sopar_abs.run_sofia()

            sofia_report.append(abs_sofia_report)

            if adpalmap_config.enable_tap_service == True:
                if mask:
                    abs_qa_report = adpalmap_sopar_abs.quality_assesment(mask)
                    qa_report.append(abs_qa_report)
                else:
                    logger.warning("No ALMA file mask available. Reduced QA image.")
                    abs_qa_report = adpalmap_sopar_abs.quality_assesment()
                    qa_report.append(abs_qa_report)
            else:
                logger.warning(
                    f"'enable_tap_service' is set to False. All checks in the QA will not be "
                    "performed."
                )
                abs_qa_report = adpalmap_sopar_emi.quality_assesment()
                qa_report.append(abs_qa_report)


        elif adpalmap_config.run_mode == 'both':

            adpalmap_sopar_abs = SoPar(
                sofia_file_path=adpalmap_config.sofia_abs_file,
                adpalmap_config=adpalmap_config,
                mode='absorption',
                pid = pid,
                sofia_threads=sofia_threads
                )
            adpalmap_sopar_emi = SoPar(
                sofia_file_path=adpalmap_config.sofia_emi_file,
                adpalmap_config=adpalmap_config,
                mode='emission',
                pid = pid,
                sofia_threads=sofia_threads
                )
            #Update sofia abs file with the -sop parameters
            adpalmap_sopar_abs.update_input_parameters(args.sofia_par, 
                                                       input_data=input_data, 
                                                       primary_beam=primary_beam, 
                                                       mask=mask
                                                       )  
            #Update sofia emi file with the -sop parameters
            adpalmap_sopar_emi.update_input_parameters(args.sofia_par, 
                                                       input_data=input_data, 
                                                       primary_beam=primary_beam, 
                                                       mask=mask,
                                                       run=0
                                                       )   
            if adpalmap_config.auto_setup == True:
                adpalmap_sopar_emi.auto_setup()
                adpalmap_sopar_abs.auto_setup()


            abs_sofia_report = adpalmap_sopar_abs.run_sofia()
            sofia_report.append(abs_sofia_report)
            
            if adpalmap_config.enable_tap_service == True:
                if mask:
                    abs_qa_report = adpalmap_sopar_abs.quality_assesment(mask)
                    qa_report.append(abs_qa_report)
                else:
                    logger.warning("No ALMA file mask available. Reduced QA image.")
                    abs_qa_report = adpalmap_sopar_abs.quality_assesment()
                    qa_report.append(abs_qa_report)
            else:
                logger.warning(
                    f"'enable_tap_service' is set to False. No ALMA file mask available. "
                    "Reduced QA image."
                )
                abs_qa_report = adpalmap_sopar_abs.quality_assesment()
                qa_report.append(abs_qa_report)

            emi_sofia_report = adpalmap_sopar_emi.run_sofia(run=0)
            sofia_report.append(emi_sofia_report)

            if adpalmap_config.enable_tap_service == True:
                if mask:
                    emi_qa_report = adpalmap_sopar_emi.quality_assesment(mask)
                    qa_report.append(emi_qa_report)
                else:
                    logger.warning("No ALMA file mask available. Reduced QA image.")
                    emi_qa_report = adpalmap_sopar_emi.quality_assesment()
                    qa_report.append(emi_qa_report)
            else:
                logger.warning(
                    f"'enable_tap_service' is set to False. All checks in the QA will not be "
                    "performed."
                )
                emi_qa_report = adpalmap_sopar_emi.quality_assesment()
                qa_report.append(emi_qa_report)


    else:
        sofia_report = []
        qa_report = []
        logger.info(f"'enable_sofia' set to {adpalmap_config.enable_sofia}. "
                    "Skipping Sofia runs.")


    ##############################################################################################
    #Run SIP
    

    if adpalmap_config.enable_sip == True:

        from adplib.sip.sipargs import SiPar

        sip_report = []
        
        adpalmap_sipar = SiPar(
            sip_file_path = adpalmap_config.sip_par_file, adpalmap_config = adpalmap_config,
            input_data = input_data,  ancillary_data = ancillary_data,
            sargs = args.sip_args,
            number_list = number_list, id_number = id_number, pid = pid
            )
        
        adpalmap_sipar.update_input_parameters()
              
        
        if adpalmap_config.enable_sofia == True:
            
            if adpalmap_config.run_mode == 'emission':         
                sip_report.append(
                    adpalmap_sipar.run_sip(sopar=adpalmap_sopar_emi)
                )

            elif adpalmap_config.run_mode == 'absorption':
                sip_report.append(
                    adpalmap_sipar.run_sip(sopar=adpalmap_sopar_abs)
                )
            elif adpalmap_config.run_mode == 'both':
                sip_report.append(
                    adpalmap_sipar.run_sip(sopar=adpalmap_sopar_abs)
                )
                sip_report.append(
                    adpalmap_sipar.run_sip(sopar=adpalmap_sopar_emi, run=0)
                )
        else: 
            if adpalmap_config.run_mode == 'emission':         
                sip_report.append(
                    adpalmap_sipar.run_sip()
                )
            elif adpalmap_config.run_mode == 'absorption':
                sip_report.append(
                    adpalmap_sipar.run_sip()
                )
            elif adpalmap_config.run_mode == 'both':
                sip_report.append(
                    adpalmap_sipar.run_sip()
                )
                sip_report.append(
                    adpalmap_sipar.run_sip(run=0)
                )


    else:
        sip_report = []
        logger.info(f"'enable_sip' set to {adpalmap_config.enable_sip}. Skipping SIP runs.")
    
    ##############################################################################################

    if adpalmap_config.enable_group:

        from adplib.group import group      

        group_report = []

        adpalmap_group = group(adpalmap_config=adpalmap_config)

        # Check if SoFiA is on, otherwise group is not necessary
        if adpalmap_config.enable_sofia:

            if adpalmap_config.run_mode == 'absorption':
                
                Logger.raw("================================") 
                logger.info(f"Source Grouping start. Mode: absorption. Input data: {input_data.stem}")
                Logger.raw("================================")
                # Find the 3D mask from SoFiA-2
                abs_group_mask = adpalmap_group.find_mask_sofia(
                    sopar=adpalmap_sopar_abs, mode="absorption"
                )

                if abs_group_mask:
                    # Execute group and create a new mask
                    group_mask = adpalmap_group.group_sofia_detections(
                        adpalmap_sopar_abs.input_data, abs_group_mask
                    )
                    Logger.raw("================================")
                    logger.info("Source Grouping finished")
                    Logger.raw("================================")
                    if group_mask is not None:
                        # Update the parameters for execute SoFiA-2 again
                        adpalmap_sopar_abs.update_group_parameters(group_mask)
                        # Execute SoFiA-2 
                        abs_sopar_group_report = adpalmap_sopar_abs.run_sofia()
                        group_report.append(abs_sopar_group_report)
                        # Execute SIP
                        abs_sip_group_report = adpalmap_sipar.run_sip(sopar=adpalmap_sopar_abs)
                        group_report.append(abs_sip_group_report)
                    
            
            if adpalmap_config.run_mode == 'emission':

                Logger.raw("================================") 
                logger.info(f"Source Grouping start. Mode: emission. Input data: {input_data.stem}")
                Logger.raw("================================")
                # Find the 3D mask from SoFiA-2
                emi_group_mask = adpalmap_group.find_mask_sofia(
                    sopar=adpalmap_sopar_emi, mode="emission"
                )
                
                if emi_group_mask:
                    # Execute group and create a new mask
                    group_mask = adpalmap_group.group_sofia_detections(
                        adpalmap_sopar_emi.input_data, emi_group_mask
                    )
                    Logger.raw("================================")
                    logger.info("Source Grouping finished")
                    Logger.raw("================================")
                    if group_mask is not None:
                        # Update the parameters for execute SoFiA-2 again
                        adpalmap_sopar_emi.update_group_parameters(group_mask)
                        # Execute SoFiA-2
                        emi_sopar_group_report = adpalmap_sopar_emi.run_sofia()
                        group_report.append(emi_sopar_group_report)
                        # Execute SIP
                        emi_sip_group_report = adpalmap_sipar.run_sip(sopar=adpalmap_sopar_emi)
                        group_report.append(emi_sip_group_report)


            if adpalmap_config.run_mode == 'both':
                
                Logger.raw("================================") 
                logger.info(f"Source Grouping start. Mode: absorption. Input data: {input_data.stem}")
                Logger.raw("================================")
                # Find the 3D mask from SoFiA-2
                abs_group_mask = adpalmap_group.find_mask_sofia(
                    sopar=adpalmap_sopar_abs, mode="absorption"
                )
                if abs_group_mask:
                    # Execute group and create a new mask
                    group_mask = adpalmap_group.group_sofia_detections(
                        adpalmap_sopar_abs.input_data, abs_group_mask
                    )
                    Logger.raw("================================")
                    logger.info("Source Grouping finished")
                    Logger.raw("================================")
                    if group_mask is not None:
                        # Update the parameters for execute SoFiA-2 again
                        adpalmap_sopar_abs.update_group_parameters(group_mask)
                        # Execute SoFiA-2
                        abs_sopar_group_report = adpalmap_sopar_abs.run_sofia()
                        group_report.append(abs_sopar_group_report)
                        # Execute SIP
                        abs_sip_group_report = adpalmap_sipar.run_sip(sopar=adpalmap_sopar_abs)
                        group_report.append(abs_sip_group_report)

                Logger.raw("================================") 
                logger.info(f"Source Grouping start. Mode: emission. Input data: {input_data.stem}")
                Logger.raw("================================")
                # Find the 3D mask from SoFiA-2
                emi_group_mask = adpalmap_group.find_mask_sofia(
                    sopar=adpalmap_sopar_emi, mode="emission"
                )
                
                if emi_group_mask:
                    # Execute group and create a new mask
                    group_mask = adpalmap_group.group_sofia_detections(
                        adpalmap_sopar_emi.input_data, emi_group_mask
                    )
                    Logger.raw("================================")
                    logger.info("Source Grouping finished")
                    Logger.raw("================================")
                    if group_mask is not None:
                        # Update the parameters for execute SoFiA-2 again
                        adpalmap_sopar_emi.update_group_parameters(group_mask)
                        # Execute SoFiA-2
                        emi_sopar_group_report = adpalmap_sopar_emi.run_sofia(run=0)
                        group_report.append(emi_sopar_group_report)
                        # Execute SIP
                        emi_sip_group_report = adpalmap_sipar.run_sip(
                            sopar=adpalmap_sopar_emi,
                            run=0
                        )
                        group_report.append(emi_sip_group_report)               

        else:
            logger.warning(f"No suitable 2D mask from SoFiA were found. Group execution aborted")        

    else: 
        group_report = []
        f"'enable_sip' set to {adpalmap_config.enable_group}. Skipping grouping."
    

    ##############################################################################################

    return sofia_report, sip_report, qa_report, group_report


def main():

    log_flag = False
    worker_results = []
    worker_exceptions = []
    adpalmap_config = None

    start = 0
    start_date = 0
    finish = 0
    finish_date = 0
    log_path = None
    adp_log = None
    queue_listener = None

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
        start, start_date = time.perf_counter(), datetime.now().isoformat()

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
            elif adpalmap_datap.query_type=='member_ous_id': TAP_df = adpalmap_datap.member_ous_id()
            elif adpalmap_datap.query_type=='conesearch': TAP_df = adpalmap_datap.conesearch()
            elif adpalmap_datap.query_type=='target': TAP_df = adpalmap_datap.target()
            elif adpalmap_datap.query_type=='keysearch': TAP_df = adpalmap_datap.keysearch()
            elif adpalmap_datap.query_type=='free': TAP_df = adpalmap_datap.free()
            else:
                logger.critical(
                    "Oops, you should not have come here, Please open an"
                    " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git " \
                    "with your specific case."
                )

            adpalmap_datap.download_data(TAP_df)
            
        else:
            adpalmap_datap = None
            logger.info(f"'enable_tap_service' set to {adpalmap_config.enable_tap_service}. "
                        "Skipping data download")
        #--------------------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------------------#

        # ALMA archive data
        if adpalmap_config.enable_tap_service == True:
            
            data_pack_list = [
                (data, pb, mask)
                for data, pb, mask in zip(
                    adpalmap_datap.data_list, 
                    adpalmap_datap.pb_list, 
                    adpalmap_datap.mask_list
                )
            ]

            ancillary_pack_list = [(cont) for cont in adpalmap_datap.cont_list]

            if len(data_pack_list) != len(ancillary_pack_list):
                logger.critical(
                    f"Unexpected error: 'data_pack_list' and 'ancillary_pack_list' have diffetent "
                    "length. Please open an issue on GitHub "
                    "https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
                    "case."
                )
                sys.exit(-1)
        # Local Data
        else: 
            data_pack_list = adpalmap_config.input_data_set
            ancillary_pack_list = [""] * len (data_pack_list)

        # Complete dataset list
        complete_pack_list = [
        (data, primary_beam, mask, ancillary) 
        for (data, primary_beam, mask), ancillary in zip(data_pack_list, ancillary_pack_list)
        ]
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
                    id_number, data, primary_beam, mask, ancillary,
                    adpalmap_config,
                    args, sofia_threads, number_list,
                    Logger.setup_child_logger(log_queue)
                    )
                for id_number, (data, primary_beam, mask, ancillary) in enumerate(complete_pack_list)
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
        finish, finish_date = time.perf_counter(), datetime.now().isoformat()
        logger.info(f"Execution time: {round(finish-start, 2)} second(s)") 
        queue_listener.stop()

    finally:
        
        if log_flag:
            log_path = Logger.get_log_filename()
            adp_log = reorganize_log(log_path, worker_results)

        if adpalmap_config is not None and adpalmap_config.make_report:
            from adpweb.report import Report
            
            #base_dir = Path(__file__).parent.parent  
            #template = base_dir / "adpweb" / "templates" / "report.html"

            template = get_template_path()


            # METADATA 
            pipeline_metadata = {
                # Pipeline info
                'pipeline_name': 'ADP-ALMA-Pipeline',
                'pipeline_version': 1.0, # get_pipeline_version() to be developed
                'run_id': f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                
                # Execution time
                'start_time': start_date,
                'end_time': finish_date,
                'duration_seconds': round(finish-start, 2),
                
                # Configuration used
                'config_used': adpalmap_config.__dict__,
                
                # System info
                'environment': {
                    'python_version': sys.version,
                    #'hostname': socket.gethostname(),
                    'username': os.getenv('USER', 'unknown'),
                    'working_directory': str(Path.cwd())
                },
                
                # Resources
                'resource_info': {
                    'cpus_available': os.cpu_count(),
                    # 'memory_available': ,  
                    # 'disk_space':   
                }
            }
            
            # Crear Report con toda la información
            adpalmap_report = Report(
                worker_results=worker_results,  
                template=template,
                adp_log=adp_log,
                pipeline_metadata=pipeline_metadata,
                config=adpalmap_config  
            )
            
            if adpalmap_config.make_report:

                json_path = adpalmap_report.generate_json()

                html_path = adpalmap_report.generate_html()

 
            

# Run the main functions
if __name__ == '__main__':
    main()

