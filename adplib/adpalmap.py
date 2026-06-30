"""
Contact: Borja Montoro Molina (borjamomo96@gmail.com)
"""
#Configuration
from adplib.exceptions import RecoverableError, ConfigurationError
from adplib.config import Config

import os
import shutil
import json
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
multiprocessing.set_start_method('spawn', force=True)

from concurrent.futures import ProcessPoolExecutor, as_completed

import logging
from logging.handlers import QueueListener
from logging.handlers import QueueHandler
from queue import Empty
from adplib.logger import Initial_Logger
from adplib.logger import Logger
from traceback import format_exc

import sys

DESCRIPTION = """
ESPADA: Extracting Source Pipeline for Advance Data for ALMA

Overview:
This pipeline automates ALMA data processing, including the SoFiA-2 and SIP softwares.
It allows, download files from the ALMA archive, processing multiple datasets in parallel, 
performing QA and obtain advance data products.

Included programs:
- SoFiA-2: Spectral cube processing (emission/absorption)
- SIP: SoFia Imaging Pipeline
- TAP: Automatic download from ALMA archive borrowing code from ALminer

Main options:
    -c, --config-file Main configuration file (YAML)
    -cp, --config-parameters Parameters for config.yaml in key=value format
    -sop, --sofia-parameters Parameters for SoFia in key=value format
    -sarg, --sip-arguments Arguments for SIP
    -i, --info Information about a file or parameter
    --debug Run ESPARA in debug mode


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

##################################################################################################
# Parser Config and SOFIA parameter from terminal 

def parse_key_value(arg):

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
        raise argparse.ArgumentTypeError(
            "--config-parameter, --download-paramater or --sofia-parameters must be in " 
            "par=val format."
            )


def convert_str2python_value(value_str):
    """
    Convert a string to appropriate Python type (bool, int, float, list, str).
    """
    value_str = value_str.strip()
    
    # Boolean
    if value_str.lower() in ('true', 'yes', 'on'):
        return True
    if value_str.lower() in ('false', 'no', 'off'):
        return False
    
    # Lists with brackets or separated by commas
    if (value_str.startswith('[') and value_str.endswith(']')) or ',' in value_str:
        # Reutilizar parse_sip_value para manejar listas correctamente
        return parse_sip_value(value_str)
    
    # Number
    try:
        if '.' in value_str:
            return float(value_str)
        else:
            return int(value_str)
    except ValueError:
        pass
    
    # String by default
    return value_str

##################################################################################################
# Parser SIP argument from terminal 

def convert_if_number(s):
    """
    Converts strings to int, float, or a list of numbers if possible.
    Handles formats: '5', '5.5', '[1,2,3]', '1,2,3', '1 2 3'
    """

    if isinstance(s, list):
        s = ' '.join(str(item) for item in s)
    s = str(s).replace('[', '').replace(']', '').strip()

    if not s: # Empty 
        return s
    
    # If is a list with empty spaces or comas
    if ',' in s or ' ' in s:
        parts = s.replace(',', ' ').split()
        converted_parts = []
        for part in parts:
            if part: # Ignore empty strings
                try:
                    converted_parts.append(int(part) if '.' not in part else float(part))
                except ValueError:       
                    return s #return original string        
        # If all parts were converted, return list
        return converted_parts if len(converted_parts) > 1 else converted_parts[0]
    
    # Simple string: try to convert to int or float
    try:
        return int(s) if '.' not in s else float(s)
    except ValueError:
        return s


def parse_sip_value(value):
    """
    Converts list-formatted strings to actual string lists.

    Does NOT convert numbers
    """
    if not isinstance(value, str):
        return value
    
    value = value.strip()
    
    # Formato [a, b, c] o [a,b,c]
    if value.startswith('[') and value.endswith(']'):
        content = value[1:-1].strip()
        if not content:
            return []
        
        items = []
        current = []
        in_quotes = False
        quote_char = None
        
        for char in content:
            if char in ['"', "'"] and not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
            elif char == ',' and not in_quotes:
                items.append(''.join(current).strip())
                current = []
            else:
                current.append(char)
        
        if current:
            items.append(''.join(current).strip())
        # Limpiar comillas
        cleaned = []
        for item in items:
            item = item.strip()
            if (item.startswith('"') and item.endswith('"')) or \
               (item.startswith("'") and item.endswith("'")):
                item = item[1:-1]
            cleaned.append(item)
        return cleaned 
    
    # Formato separado por comas (sin corchetes)
    elif ',' in value:
        parts = [p.strip() for p in value.split(',')]
        # Quitar comillas
        parts = [p[1:-1] if (p.startswith('"') and p.endswith('"')) or 
                           (p.startswith("'") and p.endswith("'")) else p for p in parts]
        return parts
    
    # Valor simple
    else:
        return value


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

    if not any(item.startswith('-') for item in args_list):
        raise ValueError(
            "No SIP parameter shortcuts found in -sarg arguments."
        )
    
    for item in args_list:
        if item.startswith('-'): 
            key = item
            args_dict[key] = True  
        elif key:
            processed_value = parse_sip_value(item)   
            
            if args_dict[key] is True:
                args_dict[key] = processed_value
            elif isinstance(args_dict[key], list):
                if isinstance(processed_value, list):
                    args_dict[key].extend(processed_value)
                else:
                    args_dict[key].append(processed_value)
            else:
                if isinstance(processed_value, list):
                    args_dict[key] = [args_dict[key]] + processed_value
                else:
                    args_dict[key] = [args_dict[key], processed_value]
    
    print(processed_value, type(processed_value))
    for k, v in args_dict.items():
        if isinstance(v, (str, list)) and v is not True:
            args_dict[k] = convert_if_number(v)
            print(type(args_dict[k]))
    return args_dict

##################################################################################################

def clean_previous_outputs(adpalmap_config, data_pack_list, logger):
    """
    Remove stale products for the datasets that will be processed in this run.
    """
    sip_patterns = (
        "*_figures",
        "*_sip.log",
        "*_mom0.png",
        "*_mom0.jpg",
        "*_mom0.pdf",
        "*_mom0.svg",
        "*_mom0_*.png",
        "*_mom0_*.jpg",
        "*_mom0_*.pdf",
        "*_mom0_*.svg",
        "*_mom1.png",
        "*_mom1.jpg",
        "*_mom1.pdf",
        "*_mom1.svg",
        "*_mom2.png",
        "*_mom2.jpg",
        "*_mom2.pdf",
        "*_mom2.svg",
        "*_sources.png",
        "*_sources.jpg",
        "*_sources.pdf",
        "*_sources.svg",
    )
    group_patterns = ("group_*",)

    for data, _, _, _ in data_pack_list:
        if not data:
            continue

        dataset_dir = adpalmap_config.output_dir / f"espada_{Path(data).stem}"

        if not dataset_dir.exists():
            logger.debug(f"No previous output directory found for dataset: {dataset_dir}")
            continue

        if adpalmap_config.enable_sofia:
            logger.info(
                "Cleaning previous outputs for dataset "
                f"'{Path(data).stem}': SoFiA enabled, removing {dataset_dir}"
            )
            _remove_path(dataset_dir, adpalmap_config.output_dir, logger)
            continue

        if adpalmap_config.enable_sip:
            logger.info(
                "Cleaning previous SIP outputs for dataset "
                f"'{Path(data).stem}' in {dataset_dir}"
            )
            _remove_matching_outputs(
                dataset_dir, sip_patterns, adpalmap_config.output_dir, logger
            )

            logger.info(
                "Cleaning previous group outputs for dataset "
                f"'{Path(data).stem}' in {dataset_dir}"
            )
            _remove_matching_outputs(
                dataset_dir, group_patterns, adpalmap_config.output_dir, logger
            )
            continue

        if adpalmap_config.enable_group:
            logger.info(
                "Cleaning previous group outputs for dataset "
                f"'{Path(data).stem}' in {dataset_dir}"
            )
            _remove_matching_outputs(
                dataset_dir, group_patterns, adpalmap_config.output_dir, logger
            )


def _remove_matching_outputs(dataset_dir, patterns, output_dir, logger):
    """
    Remove files or folders in a dataset directory that match any of the provided patterns.
    """

    candidates = []
    seen = set()
    for pattern in patterns:
        for candidate in dataset_dir.glob(pattern):
            resolved_candidate = candidate.resolve()
            if resolved_candidate in seen:
                continue
            seen.add(resolved_candidate)
            candidates.append(candidate)

    if not candidates:
        logger.debug(f"No previous outputs matched in {dataset_dir}. Patterns: {patterns}")
        return

    for candidate in candidates:
        _remove_path(candidate, output_dir, logger)


def _remove_path(path, output_dir, logger):
    """
    Remove a file or directory after verifying it is inside output_dir.
    """
    path = Path(path)
    output_dir = Path(output_dir).resolve()

    if not path.exists():
        return

    resolved_path = path.resolve()
    if resolved_path != output_dir and output_dir not in resolved_path.parents:
        logger.warning(f"Skipping cleanup outside output_dir: {path}")
        return

    try:
        if path.is_dir():
            shutil.rmtree(path)
            logger.info(f"Removed previous output directory: {path}")
        else:
            path.unlink()
            logger.info(f"Removed previous output file: {path}")
    except Exception as e:
        logger.warning(f"Could not remove previous output '{path}': {e}")

##################################################################################################

def worker_init(log_queue):
    """
    Required for macOS system.
    Initialize the logger on each worker with QueueHandler.
    """
    RAW_LEVEL = 15
    logger = logging.getLogger("espada_logger")
    logger.setLevel(RAW_LEVEL)
    logger.handlers.clear()             
    logger.addHandler(QueueHandler(log_queue))
    logger.propagate = False
    Logger._logger_instance = logger


def calculate_workers(data_pack_list, max_cores):
    total_files = len(data_pack_list)
    
    #Estimación de memoria por proceso
    total_size = sum(os.path.getsize(data) for data, _, _, _ in data_pack_list if data)
    avg_size = (total_size / total_files) if total_files > 0 else 0
    #Memoria disponible en GB
    mem_available = psutil.virtual_memory().available / 1024**3  
    #Heurística: 2.25 x tamaño + 1GB base
    relative_memory_used_sofia = 2.25
    mem_per_process = (avg_size * relative_memory_used_sofia / 1024**3) + 1  
    max_workers_mem = int(mem_available // mem_per_process) if mem_per_process > 0 else max_cores
    
    max_cores_cpu = max_cores 
    
    max_workers = min(max_cores_cpu, max_workers_mem, total_files)
    
    return max_workers


def calculate_sofia_threads(max_cores, max_workers):

    cores_for_python = max_workers  # 1 core per worker
    #cores_for_system = max(1, max_cores // 10)  # 10% for the system
    
    available_for_sofia = max_cores - cores_for_python #- cores_for_system
    available_for_sofia = max(1, available_for_sofia)
    
    # Threads per worker
    base_threads = max(1, available_for_sofia // max_workers)

    # SoFiA efficiency limit
    MAX_SOFIA_THREADS = 8
    threads = min(base_threads, MAX_SOFIA_THREADS)

    return threads


def reorganize_log(log_path, worker_results):
    
    try:
        
        aux_logger = Initial_Logger()
        _ = worker_results
    ##############################################################################################

        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        pid_groups = {}
        main_pid = None
        main_final = []
        final_block = False

        
        #Captura [PID:XXXX] y [XXXX]
        pid_pattern = re.compile(r'\[(?:PID:)?(\d+)\]')  
        external_log_event_pattern = re.compile(
            r'\[(?:PID:)?(\d+)\]ESPADA_EVENT\s+external_log\s+(\{.*\})'
        )

        def append_external_log(target_lines, event):
            software_id = event.get("software_id", "External software")
            mode = event.get("mode")
            log_path_event = event.get("log_path")
            group_label = "Group " if event.get("is_group") else ""

            heading = f"    === {group_label}{software_id} Execution"
            if mode:
                heading += f" (Mode: {mode})"
            heading += " ===\n"
            target_lines.append(heading)

            if not log_path_event:
                target_lines.append(
                    f"    [NO {group_label}{software_id} LOG PATH PROVIDED]\n"
                )
                return

            external_log_path = Path(log_path_event)
            if not external_log_path.exists():
                target_lines.append(
                    f"    [MISSING {group_label}{software_id} LOG: {external_log_path}]\n"
                )
                aux_logger.warning(
                    "Error reorganizing the final logfile. "
                    f"The {group_label}{software_id} logfile '{external_log_path}' "
                    "does not exist."
                )
                return

            with open(external_log_path, 'r', encoding='utf-8') as external_log:
                external_log_lines = external_log.readlines()

            target_lines.append(
                f"    [INCLUDING {group_label}{software_id} LOG: {external_log_path}]\n"
            )
            target_lines.extend([f"        {line}" for line in external_log_lines])

    ##############################################################################################

        for line in lines:
            pid_match = pid_pattern.search(line)
            if pid_match:
                main_pid = pid_match.group(1)
                break

        if main_pid is None:
            main_pid = "0"

        pid_groups[main_pid] = []

    ##############################################################################################

        for i, line in enumerate(lines):      
            pid_match = (pid_pattern.search(line))

            # For lines without PID ([PID]). There are a few
            if pid_match is None:
                # Asignar al proceso principal
                current_pid = main_pid
                
                if "ESPADA ended" in line:
                    main_final.append(line)
                    final_block = True
                elif not final_block:
                    pid_groups[main_pid].append(line)
                else:
                    main_final.append(line)
                continue

            current_pid = pid_match.group(1)
            if current_pid not in pid_groups:
                pid_groups[current_pid] = []

            if "ESPADA ended" in line:
                main_final.append(line)
                final_block = True
            else:    
                if final_block == False:
                    event_match = external_log_event_pattern.search(line)
                    if event_match:
                        try:
                            append_external_log(
                                pid_groups[current_pid],
                                json.loads(event_match.group(2)),
                            )
                        except Exception as e:
                            pid_groups[current_pid].append(
                                f"    [INVALID ESPADA_EVENT external_log: {e}]\n"
                            )
                            aux_logger.warning(
                                "Error parsing ESPADA_EVENT external_log while "
                                f"reorganizing the final logfile: {e}"
                            )
                        continue

                    pid_groups[current_pid].append(line)

                else:
                    main_final.append(line)

    ##############################################################################################
    
        sorted_lines = []

        # Initial messages from main
        sorted_lines.extend(pid_groups.pop(main_pid))

        # Numerically ordered subprocesses
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


def _build_configuration_dict(adpalmap_config, adpalmap_datap):
    """
    Build a dictionary with the configuration used in the execution.
    """
    def _safe_serialize(obj):
        """
        Converts non-serializable objects to a string or safe representation.
        """
        if isinstance(obj, Path):
            return str(obj)
        elif isinstance(obj, (str, int, float, bool, list, dict, type(None))):
            return obj
        else:
            return str(obj)

    def _dict_from_obj(obj, exclude_prefix='_'):
        """
        Converts an object's attributes to a dictionary, excluding those that begin with a prefix.
        """
        result = {}
        for key, value in obj.__dict__.items():
            if key.startswith(exclude_prefix):
                continue
            result[key] = _safe_serialize(value)
        return result

    
    main_config_raw = _dict_from_obj(adpalmap_config)
    
    
    categories = {
        'general': ['make_report', 'verbose', 'num_cores', 'output_dir'],
        'logger': ['clear_logs', 'log_file'],
        'input_data': ['input_data_set', 'input_file'],
        'tap_service': ['enable_tap_service', 'download_par_file'],
        'sofia': ['enable_sofia', 'run_mode', 'use_mask', 'abs_flag_cube', 
                  'auto_setup', 'sofia_abs_file', 'sofia_emi_file'],
        'sip': ['enable_sip', 'sip_par_file'],
        'group': ['enable_group', 'overlap_mode', 'overlap_threshold']
    }
    
    categorized_main = {}
    for category, keys in categories.items():
        cat_dict = {}
        for key in keys:
            if key in main_config_raw:
                cat_dict[key] = main_config_raw.pop(key)
        if cat_dict:
            categorized_main[category] = cat_dict
    
    # Any remaining parameters (if any) go to 'other'
    if main_config_raw:
        categorized_main['other'] = main_config_raw

    # Configuración de descarga (solo si se usó TAP)
    download_config = None
    if adpalmap_config.enable_tap_service and adpalmap_datap is not None:
        download_config_raw = _dict_from_obj(adpalmap_datap)
        # Organize download_config into subcategories
        server_keys = ['server_address', 'credentials', 'stored_credentials']
        query_keys = ['query_type', 'query_par']
        download_par_keys = ['download_par']
        
        server = {k: download_config_raw.get(k) for k in server_keys if k in download_config_raw}
        query = {k: download_config_raw.get(k) for k in query_keys if k in download_config_raw}
        download_par = download_config_raw.get('download_par', {})
        
        
        other_download = {k: v for k, v in download_config_raw.items() 
                          if k not in server_keys + query_keys + download_par_keys}
        
        download_config = {
            'server': server,
            'query': query,
            'download_par': download_par
        }
        if other_download:
            download_config['other'] = other_download

    return {
        'main_config': categorized_main,
        'download_config': download_config,
        'config_file_used': str(adpalmap_config._config_path) if hasattr(adpalmap_config, '_config_path') else 'config.yaml'
    }


def process_data(id_number,
                 input_data, 
                 primary_beam, 
                 mask, 
                 ancillary_data,
                 adpalmap_config, 
                 args, 
                 sofia_threads, 
                 number_list
    ):

    # This logger instance was initialized in worker_init
    logger = Logger.get_logger()

    pid = os.getpid()

    # Must be defined after define the logger and before Group
    from adplib.sofia.sopar import SoPar, find_previous_qa_reports
    from adplib.sip.sipargs import SiPar
    from adplib.group import group

    
    ##############################################################################################
    # Run SoFia

    if adpalmap_config.enable_sofia == True:

        sofia_report = []
        qa_report = []

        if adpalmap_config.run_mode == 'absorption':

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

            if mask:
                if adpalmap_config.use_mask:
                    logger.info(f"Mask file available but 'use_mask' set to True. "
                                "Reduced QA image.")
                    abs_qa_report = adpalmap_sopar_abs.quality_assesment()
                    qa_report.append(abs_qa_report)
                else:
                    abs_qa_report = adpalmap_sopar_abs.quality_assesment(mask)
                    qa_report.append(abs_qa_report)
            else:
                logger.warning("No mask file available. Reduced QA image.")
                abs_qa_report = adpalmap_sopar_abs.quality_assesment()
                qa_report.append(abs_qa_report)

        elif adpalmap_config.run_mode == 'emission':
            
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

            if mask:
                if adpalmap_config.use_mask:
                    logger.info(f"Mask file available but 'use_mask' set to True. "
                                "Reduced QA image.")
                    emi_qa_report = adpalmap_sopar_emi.quality_assesment()
                    qa_report.append(emi_qa_report)
                else:
                    emi_qa_report = adpalmap_sopar_emi.quality_assesment(mask)
                    qa_report.append(emi_qa_report)
            else:
                logger.warning("No mask file available. Reduced QA image.")
                emi_qa_report = adpalmap_sopar_emi.quality_assesment()
                qa_report.append(emi_qa_report)

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
            
            if mask:
                if adpalmap_config.use_mask:
                    logger.info(f"Mask file available but 'use_mask' set to True. "
                                "Reduced QA image.")
                    abs_qa_report = adpalmap_sopar_abs.quality_assesment()
                    qa_report.append(abs_qa_report)
                else:
                    abs_qa_report = adpalmap_sopar_abs.quality_assesment(mask)
                    qa_report.append(abs_qa_report)
            else:
                logger.warning("No mask file available. Reduced QA image.")
                abs_qa_report = adpalmap_sopar_abs.quality_assesment()
                qa_report.append(abs_qa_report)

            emi_sofia_report = adpalmap_sopar_emi.run_sofia(run=0)
            sofia_report.append(emi_sofia_report)

            if mask:
                if adpalmap_config.use_mask:
                    logger.info(f"Mask file available but 'use_mask' set to True. "
                                "Reduced QA image.")
                    emi_qa_report = adpalmap_sopar_emi.quality_assesment()
                    qa_report.append(emi_qa_report)
                else:
                    emi_qa_report = adpalmap_sopar_emi.quality_assesment(mask)
                    qa_report.append(emi_qa_report)
            else:
                logger.warning("No mask file available. Reduced QA image.")
                emi_qa_report = adpalmap_sopar_emi.quality_assesment()
                qa_report.append(emi_qa_report)

    else:
        sofia_report = []
        qa_report = find_previous_qa_reports(input_data, adpalmap_config, pid, logger)
        logger.info(f"'enable_sofia' set to {adpalmap_config.enable_sofia}. "
                    "SoFiA execution skipped")
    ##############################################################################################
    
    ##############################################################################################
    # Run SIP
    
    if adpalmap_config.enable_sip == True:

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
        logger.info(f"'enable_sip' set to {adpalmap_config.enable_sip}. SIP execution skipped")
    ##############################################################################################
    
    ##############################################################################################
    # Run 
    
    if adpalmap_config.enable_group:
    
        group_report = []
        adpalmap_group = group(adpalmap_config=adpalmap_config, input_data=input_data)

        try:
            if adpalmap_config.run_mode == 'absorption':
                
                do_group = True
                try:
                    adpalmap_sopar_abs
                except NameError:
                    adpalmap_sopar_abs = SoPar(
                    sofia_file_path=adpalmap_config.sofia_abs_file, 
                    adpalmap_config=adpalmap_config,
                    mode='absorption',
                    pid = pid,
                    sofia_threads=sofia_threads
                    )
                    adpalmap_sopar_abs.update_input_parameters(args.sofia_par, 
                                                       input_data=input_data, 
                                                       primary_beam=primary_beam, 
                                                       mask=mask
                                                       ) 

                try:
                    adpalmap_sipar
                except NameError:
                    try:
                        adpalmap_sipar = SiPar(
                            sip_file_path = adpalmap_config.sip_par_file, 
                            adpalmap_config = adpalmap_config,
                            input_data = input_data,  ancillary_data = ancillary_data,
                            sargs = args.sip_args,
                            number_list = number_list, id_number = id_number, pid = pid
                            )   
                    except RecoverableError as e:
                        logger.warning(
                            f"Group execution aborted. Error: {e}"
                        )
                        do_group = False
                    except ValueError as e:
                        raise  
                    except Exception as e:
                        raise     
                
                if do_group:
                    Logger.raw("================================") 
                    logger.info(
                        f"Source Grouping start. Mode: absorption. Input data: {input_data}"
                    )
                    Logger.raw("================================")
                    # Find the 3D mask from SoFiA-2
                    abs_group_mask = adpalmap_group.find_mask_sofia(
                        sopar=adpalmap_sopar_abs, mode="absorption"
                    )

                    if abs_group_mask:
                        # Execute group and create a new mask
                        group_mask = adpalmap_group.group_sofia_detections(
                            input_data, abs_group_mask
                        )
                        Logger.raw("================================")
                        logger.info("Source Grouping finished")
                        Logger.raw("================================")
                        if group_mask is not None:
                            # Update the parameters for execute SoFiA-2 again
                            adpalmap_sopar_abs.update_group_parameters(
                                group_mask,
                                input_region_from_mask=getattr(
                                    adpalmap_group, "input_region_from_mask", None
                                ),
                            )
                            # Execute SoFiA-2 
                            abs_sopar_group_report = adpalmap_sopar_abs.run_sofia()
                            group_report.append(abs_sopar_group_report)
                            # Execute SIP
                            abs_sip_group_report = adpalmap_sipar.run_sip(sopar=adpalmap_sopar_abs)
                            group_report.append(abs_sip_group_report)
                    else:
                        logger.warning(
                            "Group execution aborted. mode: 'absorption'"
                        ) 
           
            elif adpalmap_config.run_mode == 'emission':
                
                do_group = True
                try:
                    adpalmap_sopar_emi
                except NameError:
                    adpalmap_sopar_emi = SoPar(
                    sofia_file_path=adpalmap_config.sofia_emi_file, 
                    adpalmap_config=adpalmap_config,
                    mode='emission',
                    pid = pid,
                    sofia_threads=sofia_threads
                    )
                    adpalmap_sopar_emi.update_input_parameters(args.sofia_par, 
                                                       input_data=input_data, 
                                                       primary_beam=primary_beam, 
                                                       mask=mask
                                                       ) 
                
                try:
                    adpalmap_sipar
                except NameError:
                    try:
                        adpalmap_sipar = SiPar(
                            sip_file_path = adpalmap_config.sip_par_file, 
                            adpalmap_config = adpalmap_config,
                            input_data = input_data,  ancillary_data = ancillary_data,
                            sargs = args.sip_args,
                            number_list = number_list, id_number = id_number, pid = pid
                            )     
                    except RecoverableError as e:
                        logger.warning(
                            f"Group execution aborted. Error: {e}"
                        )
                        do_group = False
                    except ValueError as e:
                        print(e)
                        raise  
                    except Exception as e:
                        print(e)
                        raise     
                
                if do_group:       
                    Logger.raw("================================") 
                    logger.info(
                        f"Source Grouping start. Mode: emission. Input data: {input_data}"
                    )
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
                            adpalmap_sopar_emi.update_group_parameters(
                                group_mask,
                                input_region_from_mask=getattr(
                                    adpalmap_group, "input_region_from_mask", None
                                ),
                            )
                            # Execute SoFiA-2
                            emi_sopar_group_report = adpalmap_sopar_emi.run_sofia()
                            group_report.append(emi_sopar_group_report)
                            # Execute SIP
                            emi_sip_group_report = adpalmap_sipar.run_sip(sopar=adpalmap_sopar_emi)
                            group_report.append(emi_sip_group_report)
                    else:
                        logger.warning(
                            "Group execution aborted. mode: 'emission'"
                        )    

            elif adpalmap_config.run_mode == 'both':
                
                do_group_absorption = True
                try:
                    adpalmap_sopar_abs
                except NameError:
                    adpalmap_sopar_abs= SoPar(
                    sofia_file_path=adpalmap_config.sofia_abs_file, 
                    adpalmap_config=adpalmap_config,
                    mode='absorption',
                    pid = pid,
                    sofia_threads=sofia_threads
                    )
                    adpalmap_sopar_abs.update_input_parameters(
                        args.sofia_par, 
                        input_data=input_data, 
                        primary_beam=primary_beam, 
                        mask=mask
                    ) 

                do_group_emission = True
                try:
                    adpalmap_sopar_emi
                except NameError:
                    adpalmap_sopar_emi = SoPar(
                    sofia_file_path=adpalmap_config.sofia_emi_file, 
                    adpalmap_config=adpalmap_config,
                    mode='emission',
                    pid = pid,
                    sofia_threads=sofia_threads
                    )
                    adpalmap_sopar_emi.update_input_parameters(args.sofia_par, 
                                                       input_data=input_data, 
                                                       primary_beam=primary_beam, 
                                                       mask=mask,
                                                       run=0
                                                       )                 

                try:
                    adpalmap_sipar
                except NameError:
                    try:
                        adpalmap_sipar = SiPar(
                            sip_file_path = adpalmap_config.sip_par_file, 
                            adpalmap_config = adpalmap_config,
                            input_data = input_data,  ancillary_data = ancillary_data,
                            sargs = args.sip_args,
                            number_list = number_list, id_number = id_number, pid = pid
                            )   
                    except RecoverableError as e:
                        logger.warning(
                        f"SIP catalog not available. "
                        f"Absorption group will be skipped. Error: {e}"
                        )
                        do_group_absorption = False
                    except ValueError as e:
                        raise  
                    except Exception as e:
                        raise     
         
                if do_group_absorption:
                    #Logger.raw("================================") 
                    logger.info(
                        f"Source Grouping start. Mode: absorption. Input data: {input_data}"
                    )
                    #Logger.raw("================================")
                    # Find the 3D mask from SoFiA-2
                    abs_group_mask = adpalmap_group.find_mask_sofia(
                        sopar=adpalmap_sopar_abs, mode="absorption"
                    )
                    if abs_group_mask:
                        # Execute group and create a new mask
                        group_mask = adpalmap_group.group_sofia_detections(
                            adpalmap_sopar_abs.input_data, abs_group_mask
                        )
                        #Logger.raw("================================")
                        logger.info("Source Grouping finished")
                        #Logger.raw("================================")
                        if group_mask is not None:
                            # Update the parameters for execute SoFiA-2 again
                            adpalmap_sopar_abs.update_group_parameters(
                                group_mask,
                                input_region_from_mask=getattr(
                                    adpalmap_group, "input_region_from_mask", None
                                ),
                            )
                            # Execute SoFiA-2
                            abs_sopar_group_report = adpalmap_sopar_abs.run_sofia()
                            group_report.append(abs_sopar_group_report)
                            # Execute SIP
                            abs_sip_group_report = adpalmap_sipar.run_sip(sopar=adpalmap_sopar_abs)
                            group_report.append(abs_sip_group_report)

                
                if do_group_emission:
                    #Logger.raw("================================") 
                    logger.info(
                        f"Source Grouping start. Mode: emission. Input data: {input_data}"
                    )
                    #Logger.raw("================================")
                    # Find the 3D mask from SoFiA-2
                    emi_group_mask = adpalmap_group.find_mask_sofia(
                        sopar=adpalmap_sopar_emi, mode="emission"
                    )
                    
                    if emi_group_mask:
                        # Execute group and create a new mask
                        group_mask = adpalmap_group.group_sofia_detections(
                            adpalmap_sopar_emi.input_data, emi_group_mask
                        )
                        #Logger.raw("================================")
                        logger.info("Source Grouping finished")
                        #Logger.raw("================================")
                        if group_mask is not None:
                            # Update the parameters for execute SoFiA-2 again
                            adpalmap_sopar_emi.update_group_parameters(
                                group_mask,
                                input_region_from_mask=getattr(
                                    adpalmap_group, "input_region_from_mask", None
                                ),
                            )
                            # Execute SoFiA-2
                            emi_sopar_group_report = adpalmap_sopar_emi.run_sofia(run=0)
                            group_report.append(emi_sopar_group_report)
                            # Execute SIP
                            emi_sip_group_report = adpalmap_sipar.run_sip(
                                sopar=adpalmap_sopar_emi,
                                run=0
                            )
                            group_report.append(emi_sip_group_report)               

        except Exception as e:    
            logger.error(f"Unexpected error trying to group sources: {e}. Group execution aborted")
            Logger.raw(format_exc())
            pass   

    else: 
        group_report = []
        f"'enable_sip' set to {adpalmap_config.enable_group}. Group execution skipped"
    ##############################################################################################

    if (
        adpalmap_config.enable_sofia == False and 
        adpalmap_config.enable_sip == False and
        adpalmap_config.enable_group == False
    ):

        empty_report = {
            "software_id": "TAP",
            "PID": pid,
            "input_name": input_data.stem if input_data else f"dataset_{id_number}",
            "input_path": str(input_data) if input_data else None,
            "mode": "download_only",
            "log_path": "",
            "error": "",
            "outputs": {"images": [], "files": []}
        }
        return ([empty_report], [], [], [])

    return sofia_report, sip_report, qa_report, group_report


def main():
    
    ilogger = Initial_Logger()
    current_logger = ilogger

    log_flag = False
    worker_results = []
    worker_exceptions = []
    adpalmap_config = None
    adpalmap_datap = None

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
            '-cp', '--config-parameter', dest='config_par', nargs='+',
            type=parse_key_value, default=None,
            help="Override parameters in config.yaml. Format: key=value (multiple allowed)."
        )
        parser.add_argument(
            '-sop', '--sofia-parameters', dest='sofia_par', nargs='+', 
            type=parse_key_value, default=None,
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
        parser.add_argument(
            '--debug', action='store_true', 
                            help="Enable debug mode (shows full tracebacks)"
        )

        args = parser.parse_args()
        
        if args.config_par: 
            args.config_par = dict(args.config_par)
            for k, v in args.config_par.items():
                python_value = convert_str2python_value(v)
                args.config_par[k]=python_value
        if args.sofia_par: args.sofia_par = dict(args.sofia_par)
        if args.sip_args: args.sip_args = sipargs_to_dict(args.sip_args)
        if args.info:
            show_info(args.info)
            sys.exit(-1)
        debug_mode = args.debug
        
    ##############################################################################################

    ##############################################################################################

        if debug_mode:
            ilogger.logger.setLevel(logging.DEBUG)
            ilogger.debug("Debug mode enabled")
        else:
            ilogger.logger.setLevel(logging.INFO)    


        if (args.config_file is None):
            ilogger.warning(
                "No config.yaml file specified, default config.yaml file will be used"
            )
            adpalmap_config = Config(config_par=args.config_par)
        else:
            adpalmap_config = Config(config_path=args.config_file, config_par=args.config_par)    
        
    ##############################################################################################

    ##############################################################################################
        log_queue = multiprocessing.Queue()  

        logger = Logger.get_logger(
            output_dir=adpalmap_config.output_dir,
            log_path=adpalmap_config.log_file, 
            clear_logs=adpalmap_config.clear_logs,
            queue=log_queue,
            debug_mode=debug_mode 
        )

        queue_listener = QueueListener(log_queue, *logger.handlers) 
        queue_listener.start() 

        current_logger = logger
    ############################################################################################## 
        logger.info("ESPADA start point")

        log_flag = True
        start, start_date = time.perf_counter(), datetime.now().isoformat()
    ##############################################################################################

        #Optionally download data from ALMA archive
        if adpalmap_config.enable_tap_service == True:
            from adplib.tap.datap import datap

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
    ##############################################################################################

    ##############################################################################################

        # ALMA archive data
        if adpalmap_config.enable_tap_service == True:
            
            data_pack_list = [
                (data, pb, mask, cont)
                for data, pb, mask, cont in zip(
                    adpalmap_datap.data_list,
                    adpalmap_datap.pb_list,
                    adpalmap_datap.mask_list,
                    adpalmap_datap.cont_list
                )
            ]
        # Local Data
        else: 
            data_pack_list = adpalmap_config.input_data_set

        # Complete dataset list
        complete_pack_list = data_pack_list
        number_list = list(range(len(data_pack_list)))


        if adpalmap_config.enable_tap_service and complete_pack_list:
            input_file_path = adpalmap_config.output_dir / "espada_input_file.txt"
            with open(input_file_path, 'w') as f:
                f.write("# Auto-generated input file from ESPADA run with TAP service\n")
                f.write("# Format: dataset_id: cube_path primary_beam_path mask_path continuum_path\n")
                f.write("# Empty fields are represented as \"\"\n")
                for idx, (cube, pb, mask, continuum) in enumerate(complete_pack_list, start=1):
                    cube_str = str(cube) if cube else '""'
                    pb_str = str(pb) if pb else '""'
                    mask_str = str(mask) if mask else '""'
                    cont_str = str(continuum) if continuum else '""'
                    f.write(f"{idx}: {cube_str} {pb_str} {mask_str} {cont_str}\n")
            logger.info(
                f"Generated input file for future runs (without re-download): {input_file_path}"
            )

        clean_previous_outputs(adpalmap_config, complete_pack_list, logger)

    ##############################################################################################
        
    ##############################################################################################
      
        cpu_cores = multiprocessing.cpu_count()
        
        if adpalmap_config.num_cores is not None:
            if adpalmap_config.num_cores > cpu_cores:
                logger.warning(
                    "The number of cores indicated is greater than the number of cores available "
                    f"in the CPU. The number of cores has been assigned as: {cpu_cores}. "
                )
                max_cores = int(cpu_cores)
            else:
                max_cores = adpalmap_config.num_cores

        else:
            max_cores = cpu_cores

        reserved_cores = 0
        available_cores = max_cores - reserved_cores 

        max_workers = calculate_workers(data_pack_list, available_cores)
        debug_in_process = os.environ.get("ESPADA_DEBUG_IN_PROCESS") == "1"

        if max_workers < 1:
            logger.warning(
                "The worker number is lower than 1. One or more of the datasets are too large"
                " for the available RAM. The minimum worker count is set to 1, but keep in "
                "mind that unexpected errors may occur."
            )
            max_workers = 1
        
        if debug_in_process:
            logger.warning(
                "ESPADA_DEBUG_IN_PROCESS enabled: datasets will run sequentially in the "
                "main process. Use this mode only for debugging."
            )
            max_workers = 1

        sofia_threads = calculate_sofia_threads(max_cores, max_workers)

        logger.info(f"The number of worker has been set to {max_workers}")
        logger.info(f"The number of SoFiA threads has been set to {sofia_threads}")

    ##############################################################################################
        
    ##############################################################################################

        if debug_in_process:
            for id_number, (data, primary_beam, mask, ancillary) in enumerate(complete_pack_list):
                try:
                    result = process_data(
                        id_number, data, primary_beam, mask, ancillary,
                        adpalmap_config,
                        args, sofia_threads, number_list
                    )
                    worker_results.append(result)

                #Este primero porque python lee Excepciones de arriba a abajo
                #Errores salvables. El resto de procesos sigue corriendo
                except RecoverableError as e:  
                    worker_exceptions.append(e)
                #Errores criticos
                except ConfigurationError as e:  
                    worker_exceptions.append(e)
                    logger.error(f"Configuration error: {e}")
                    raise 
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
                         "https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your "
                         "specific case."
                    )
                    raise 
        
        else:
            with ProcessPoolExecutor(
                max_workers=max_workers, initializer=worker_init, initargs=(log_queue,)
            ) as pool:
        
                futures = [
                    pool.submit(
                        process_data, 
                        id_number, data, primary_beam, mask, ancillary,
                        adpalmap_config,
                        args, sofia_threads, number_list
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
                    #Errores criticos
                    except ConfigurationError as e:  
                        worker_exceptions.append(e)
                        logger.error(f"Configuration error: {e}")
                        raise 
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
                             "https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your "
                             "specific case."
                        )
                        raise 

    ##############################################################################################

        logger.info("ESPADA ended")
        if adpalmap_config is not None and adpalmap_config.make_report:
            logger.info(
                "See the final reports for an overview of the results obtained during the "
                "pipeline execution."
            )
        finish, finish_date = time.perf_counter(), datetime.now().isoformat()
        logger.info(f"Execution time: {round(finish-start, 2)} second(s)") 

    ##############################################################################################

    except ConfigurationError as e:
        current_logger.error(f"Pipeline aborted due to configuration error: {e}")
        if debug_mode:
            current_logger.debug(format_exc())
        sys.exit(1)

    except FileNotFoundError as e:
        current_logger.error(f"Required file not found: {e}")
        if debug_mode:
            current_logger.debug(format_exc())
        sys.exit(1)

    except ValueError as e:
        current_logger.error(f"Invalid value encountered: {e}")
        if debug_mode:
            current_logger.debug(format_exc())
        sys.exit(1)

    except RuntimeError as e:
        current_logger.critical(f"Runtime error: {e}")
        if debug_mode:
            current_logger.debug(format_exc())
        sys.exit(1)

    except KeyboardInterrupt:
        current_logger.warning("Pipeline interrupted by user")
        sys.exit(1)

    except Exception as e:
        current_logger.critical(
            f"Unexpected error: {e}. "
                "Please open an issue on GitHub "
                "https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your "
                "specific case."
        )
        if debug_mode:
            current_logger.debug(format_exc())
        sys.exit(1)
    
    ##############################################################################################

    finally:

    ##############################################################################################
        html_path = None
        raw_log_path = Logger.get_log_filename() if log_flag else None

        if adpalmap_config is not None and adpalmap_config.make_report:
            from adpweb.report import Report

            base_dir = Path(__file__).parent.parent  
            template = base_dir / "adpweb" / "templates" / "report.html"


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
                'configuration': _build_configuration_dict(adpalmap_config, adpalmap_datap),
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
                output_dir=adpalmap_config.output_dir,
                worker_results=worker_results,  
                template=template,
                raw_log_path=raw_log_path,
                organized_log_path=None,
                pipeline_metadata=pipeline_metadata,
                config=adpalmap_config  
            )
            
            json_path = adpalmap_report.generate_json()

            html_path = adpalmap_report.generate_html()
    ##############################################################################################

        organized_log_path = None
        if log_flag:
            organized_log_path = reorganize_log(raw_log_path, worker_results)

        if html_path and organized_log_path and adpalmap_report:
            adpalmap_report.inject_organized_log(organized_log_path, html_path, json_path)

    ##############################################################################################
        # Shutdown of the ProcessPoolExecutor if it exists
        try:
            if 'pool' in locals() and pool is not None:
                pool.shutdown(wait=True, cancel_futures=True)
        except Exception as e:
            logger.debug(f"Error shutting down pool: {e}")
        
        # Stop QueueListener before anything else
        if queue_listener is not None:
            try:
                queue_listener.stop()

                # Configuración
                max_wait_seconds = 5
                batch_timeout = 0.5  # Timeout por batch
                start_time = time.time()
                messages_processed = 0

                while not log_queue.empty():
                    if time.time() - start_time > max_wait_seconds:
                        remaining = log_queue.qsize()
                        logger.warning(
                            f"TIMEOUT: Emptying stopped after {max_wait_seconds}s. "
                            f"{remaining} unprocessed messages remain. "
                            f"Processed: {messages_processed}"
                        )
                        break
                    try:
                        record = log_queue.get(timeout=batch_timeout)
                        for handler in logger.handlers:
                            handler.handle(record)
                        messages_processed += 1
                    except Empty:
                        break
                    except Exception:
                        logger.debug(
                            f"Error trying to empty the queue listener before it closes"
                        )
            except Exception as e:
                logger.error(f"Error stopping queue listener: {e}")       
    ##############################################################################################
            

# Run the main functions
if __name__ == '__main__':
    main()
