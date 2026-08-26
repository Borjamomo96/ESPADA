import os
import json  
import shutil
import sys
import subprocess
import socket

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

from pprint import pprint

# Logger:
import logging
from adplib.logger import Logger
logger= Logger.get_logger()


SOFIA_NO_SOURCES_EXIT_CODE = 8
NO_SOURCES_STATUS = "no_sources"

REPORT_STATUS_SEVERITY = {
    "ok": "ok",
    "warning": "warning",
    "error": "error",
    "disable": "ok",
    NO_SOURCES_STATUS: "warning",
}

DEFAULT_WARNING_THRESHOLD = 4


def resolve_software_status(sw, error, warnings, exit_code):
    """
    Resolve the report status for one software execution.
    """

    if (
        sw.get('software_id') == 'SoFiA-2'
        and error
        and exit_code == SOFIA_NO_SOURCES_EXIT_CODE
    ):
        return NO_SOURCES_STATUS

    if error:
        return 'error'
    if warnings is not None and warnings > DEFAULT_WARNING_THRESHOLD:
        return 'warning'
    return 'ok'


def update_status_counters(parsed_data, status):
    """
    Update report counters for a resolved software status.
    """

    severity = REPORT_STATUS_SEVERITY.get(status, 'error')

    if severity == 'error':
        parsed_data['execution_info']['total_errors'] += 1
        return True, False
    if severity == 'warning':
        parsed_data['execution_info']['total_warnings'] += 1
        return False, True

    parsed_data['execution_info']['successful_workers'] += 1
    return False, False


class Report:
    """
    Build ESPADA JSON and HTML reports from worker results and execution metadata.
    """

    def __init__(
        self, output_dir, worker_results, template, 
        raw_log_path=None, organized_log_path=None, 
        pipeline_metadata=None, config=None
    ):
        """
        Initialize report paths, cached data, logs, and template resources.

        Parameters
        ----------
        output_dir : pathlib.Path
            Pipeline output directory where the report folder will be created.
        worker_results : list
            Worker result tuples collected after processing datasets.
        template : pathlib.Path
            HTML template used to render the report.
        raw_log_path : pathlib.Path, optional
            Path to the raw execution log.
        organized_log_path : pathlib.Path, optional
            Path to the reorganized execution log.
        pipeline_metadata : dict, optional
            Execution metadata included in the JSON and HTML reports.
        config : adplib.config.Config, optional
            Runtime configuration used by the pipeline.
        """

        self.worker_results = worker_results
        self.template = template
        self.raw_log_path = raw_log_path if raw_log_path else None
        self.organized_log_path = organized_log_path if organized_log_path else None
        self.pipeline_metadata = pipeline_metadata
        self.config = config

        # Log content
        self.raw_log_content = self._read_log_file(self.raw_log_path) if self.raw_log_path else ""
        self.organized_log_content = ""
        if self.organized_log_path:
            self.organized_log_content = self._read_log_file(self.organized_log_path)

        # Directories
        base_dir = output_dir / "report"
        timestamp = datetime.now().strftime("%y%m%d_%H%M%S")

        if base_dir.exists():
            self.report_dir = base_dir.with_name(f"{base_dir.name}_{timestamp}")
        else:
            self.report_dir = base_dir

        self.image_dir = self.report_dir / "images"
        self.resources_dir = self.report_dir / "resources"

        # Cache for parsed data
        self.parsed_data = None

        # Cache for HTML data
        self._html_summary_cache = None

        # Create directory structure 
        self._create_directory_structure()
        self._copy_template_resources()

        # Add additional metadata if missing.
        #self._enrich_pipeline_metadata()
    

    def parse_report(self):
        """
        Parse the worker results into a complete and neutral structure.
        """

        if self.parsed_data is not None:
            return self.parsed_data
        
        ########################################################################################### 
        # COMPLETE STRUCTURE

        parsed_data = {
            # Metadata
            'pipeline_metadata': self.pipeline_metadata.copy(),
            
            'execution_info': {
                'total_workers': len(self.worker_results),
                'successful_workers': 0,
                'failed_workers': 0,
                'total_warnings': 0,
                'total_errors': 0,
                'performance_metrics': {
                    # Can be filled with timing data when available.
                }
            },
            
            # Datasets
            'datasets': [],
            
            # Summary
            'global_summary': {
                'total_datasets': 0,
                'datasets_with_errors': 0,
                'datasets_with_warnings': 0,
                'datasets_successful': 0,
                'total_images_generated': 0,
                'total_files_generated': 0
            }
        }
        
        # This process each dataset
        for dataset_tuple in self.worker_results:
            all_software = []
            input_path = None
            input_name = None
            images = []
            qa_by_mode = {}
            error_exist = False
            warning_exist = False
            no_sources_exist = False
            #######################################################################################    
            # COMPLETE INFORMATION BY SOFTWARE

            for software_list in dataset_tuple:
                for sw in software_list:
                    # Identify input data
                    if not input_path and sw.get('input_path'):
                        input_path = str(sw['input_path'])
                    if not input_name and sw.get('input_name'):
                        input_name = str(sw['input_name'])
                    if not input_name and input_path:
                        input_name = Path(input_path).stem
                    
                    # Group flag
                    is_group = software_list is dataset_tuple[3]
                    
                    
                    if sw['software_id'] == 'QA':
                        mode = sw.get('mode', '')
                        if mode not in qa_by_mode:
                            qa_by_mode[mode] = {
                                'cube_statistics': {},
                                'mask_comparison': {},
                                'images': []
                            }

                        cube_stats = sw.get('cube_statistics', {})
                        mask_comparison = sw.get('mask_comparison', {})

                        if cube_stats:
                            qa_by_mode[mode]['cube_statistics'] = cube_stats
                        if mask_comparison:
                            qa_by_mode[mode]['mask_comparison'] = mask_comparison

                        if 'outputs' in sw and 'images' in sw['outputs']:
                            for img in sw['outputs']['images']:
                                img['is_qa'] = True
                                img['software-id'] = 'qa'
                                img['mode'] = mode
                                qa_by_mode[mode]['images'].append(img)
                                images.append(img)
                            
                        continue
            
                    
                    error = sw.get('error', '')
                    warnings = sw.get('warning_number')
                    exit_code = sw.get('exit_code')
                    if exit_code is None:
                        exit_code = 0 if not error else 1
                    
                    sw_status = resolve_software_status(sw, error, warnings, exit_code)
                    sw_status_severity = REPORT_STATUS_SEVERITY.get(sw_status, 'error')
                    has_error, has_warning = update_status_counters(parsed_data, sw_status)
                    error_exist = error_exist or has_error
                    warning_exist = warning_exist or has_warning
                    no_sources_exist = no_sources_exist or sw_status == NO_SOURCES_STATUS
                   
                    ###############################################################################
                    # COMPLETE SOFTWARE INFORMATION
                    software_info = {
                        # Id
                        'software_id': sw['software_id'],
                        'software_version': '',  # CHANGE. Include the software version.
                        'mode': sw.get('mode', ''), 
                        
                        # execution info
                        'execution_info': {
                            'pid': sw.get('PID'),
                            'start_time': '',  # TODO: Get actual execution times.
                            'end_time': '',
                            'duration_seconds': None,
                            'exit_code': exit_code,
                            #'host': socket.gethostname()
                        },
                        
                        # Status and errors
                        'status_info': {
                            'status': sw_status,
                            'status_severity': sw_status_severity,
                            'error_message': error,
                            'error_type': (
                                'runtime' if error and sw_status_severity == 'error' else None
                            ),
                            'software_exit_message': sw.get('sofia_exit_message', ''),
                            'software_subprocess_error': sw.get('sofia_subprocess_error', ''),
                            'warning_count': warnings,
                            'warnings_list': [],  # CHANGE. Can be removed.
                            'is_group': is_group
                        },
                        
                        # Configuration
                        'configuration': {
                            'parfile_used': str(sw.get('sofia_parfile', '')) if 'sofia_parfile' in sw else '',
                            'parfile_content': self._read_log_file(sw.get('sofia_parfile', '')),
                            'formatted_parfile': self._format_parfile_content(
                                self._read_log_file(sw.get('sofia_parfile', '')),
                                sw.get('sofia_par_changes', {})
                            ) if 'sofia_parfile' in sw else '',
                            'parameters_changed': sw.get('sofia_par_changes', {}),
                            'command_executed': ' '.join(sw.get('command', [])) if 'command' in sw else '',
                            'command_args': sw.get('command', [])
                        },
                        
                        # Logs
                        'logs': {
                            'log_path': str(sw.get('log_path', '')),
                            'log_content': self._read_log_file(sw.get('log_path', '')),
                            'log_size_bytes': os.path.getsize(sw.get('log_path', '')) if sw.get('log_path') and os.path.exists(sw.get('log_path')) else 0
                        },
                        
                        # Outputs
                        'outputs': {
                            'files_generated': sw.get('outputs', {}).get('files', []),
                            'images_generated': [],
                            'quality_metrics': {}  # CHANGE. Quantitative metrics to be added.
                        }
                    }
                    
                    all_software.append(software_info)
                    
                    # Process software images
                    if 'outputs' in sw and 'images' in sw['outputs']:
                        for img in sw['outputs']['images']:
                            img['mode'] = sw.get('mode', None)
                            img['is_qa'] = False
                            img['is_group'] = is_group
                            if sw['software_id'] == 'SoFiA-2':
                                img['software-id'] = 'sofia'
                            elif sw['software_id'] == 'SIP':
                                img['software-id'] = 'sip'
                            elif sw['software_id'] == 'QA':
                                img['software-id'] = 'qa'

                            
                            software_info['outputs']['images_generated'].append({
                                'path': str(img.get('path')),
                                'type': img.get('type'),
                                'description': img.get('description'),
                                'size_bytes': os.path.getsize(img['path']) if img.get('path') and os.path.exists(img['path']) else 0
                            })
                        
                        images.extend(sw['outputs']['images'])

            #######################################################################################

            #######################################################################################
            # COMPLETE STRUCTURE OF THE DATASET 
            dataset_identifier = (
                input_path
                or input_name
                or f"dataset_{len(parsed_data['datasets'])}"
            )
            dataset_status = (
                'error' if error_exist else
                NO_SOURCES_STATUS if no_sources_exist else
                'warning' if warning_exist else
                'ok'
            )
            dataset_complete = {
                # Identification
                'dataset_id': dataset_identifier,
                'input_name': input_name,
                'input_path': input_path,
                # FITS metadata
                'fits_metadata': self._extract_fits_metadata(input_path or input_name),
                # Per-software results with full details
                'software_results': all_software,
                # Images for HTML
                'images': images,
                'images_grouped': self._organize_images_for_html(images),
                # Overall status
                'status': dataset_status,
                'qa_by_mode': qa_by_mode
            }

            #######################################################################################
            
            parsed_data['datasets'].append(dataset_complete)
            
            # Update global counters
            if error_exist:
                parsed_data['global_summary']['datasets_with_errors'] += 1
            elif warning_exist:
                parsed_data['global_summary']['datasets_with_warnings'] += 1
            else:
                parsed_data['global_summary']['datasets_successful'] += 1
            
            parsed_data['global_summary']['total_images_generated'] += len(images)
            parsed_data['global_summary']['total_datasets'] += 1
        
        ###########################################################################################


        # Update failed execution if there are datasets with errors
        parsed_data['execution_info']['failed_workers'] = parsed_data['global_summary']['datasets_with_errors']
        
        # Save to cache
        self.parsed_data = parsed_data

        return parsed_data


    def setup_images(self):
        """
        Copy images to the report folder and update paths.
        Transform unwieldy formats like EPS into web-friendly ones
        """
        os.makedirs(self.image_dir, exist_ok=True)
        
        parsed_data = self.parse_report()
        
        for dataset in parsed_data['datasets']:
            for img in dataset.get('images', []):
                img_path = img.get('path')
                if not img_path:
                    continue
                    
                if isinstance(img_path, str):
                    src = Path(img_path)
                else:
                    src = img_path
                
                if not src.exists():
                    logger.warning(f"Image file does not exist: {src}")
                    continue
                
                filename = src.name
                dest = self.image_dir / filename

                ###################################################################################
                # Detectar y convertir EPS a PNG 

                if src.suffix.lower() == '.eps':
                    png_filename = f"{src.stem}.png"
                    png_dest = self.image_dir / png_filename
                    
                    # Convert EPS to PNG if it does not exist
                    if not png_dest.exists():
                        if self._convert_eps_to_png(src, png_dest):
                            img['path'] = os.path.join("images", png_filename)
                        else:
                            # If the conversion fails, copy the original EPS
                            shutil.copy2(src, dest)
                            img['path'] = os.path.join("images", filename)
                            logger.warning(f"EPS conversion failed, using original: {filename}")
                    else:
                        img['path'] = os.path.join("images", png_filename)
                        logger.debug(f"Image already exists: {png_filename}")
                
                else:
                    try:
                        shutil.copy2(src, dest)
                        img['path'] = os.path.join("images", filename)
                        logger.debug(f"Image copied: {filename}")
                    except Exception as e:
                        logger.error(f"Error copying image {src}: {str(e)}")
                ###################################################################################


    def _create_directory_structure(self):
        """
        Creates the directory structure.
        """  

        try:
            self.report_dir.mkdir(exist_ok=True) 
            self.image_dir.mkdir(exist_ok=True)
            self.resources_dir.mkdir(exist_ok=True)
            logger.info(f"Directory structure created in: {self.report_dir}")
        except Exception as e:
            logger.error(f"Could not create directory structure: {str(e)}")
            raise

    
    def _copy_template_resources(self):
        """
        Copy static report resources from the template package into the report directory.
        """

        try:
            
            base_resources_dir = self.template.parent.parent
            
            # Copy css
            for resource in base_resources_dir.glob('resources/*'):
                if resource.is_file():
                    shutil.copy2(resource, self.resources_dir)
                    logger.debug(f"Copied resource: {resource.name}")
            
            # Copy logo image 
            for img in base_resources_dir.glob('images/*'):
                if img.is_file():
                    shutil.copy2(img, self.image_dir)
                    logger.debug(f"Copied image from template: {img.name}")
            
            logger.info("Template resources copied successfully")

        except Exception as e:
            logger.error(f"Error copying resources from template: {str(e)}")
            raise


    def generate_json(self):
        """
        Generates a complete JSON report with all the information.

        This is the primary format for machines/databases.
        """
        try:
            # Parse data if it is not already parsed
            parsed_data = self.parse_report()

            # Use placeholder if there is no organized_log_content
            if self.organized_log_content:
                organized_log_display = self.organized_log_content
            else:
                organized_log_display = "___ESPADA_ORGANIZED_LOG_PLACEHOLDER___"            
            
            # Add ADP log content
            parsed_data['logs'] = {
                'raw_log': {
                    'path': str(self.raw_log_path) if self.raw_log_path else None,
                    'content': self.raw_log_content
                },
                'organized_log': {
                    'path': str(self.organized_log_path) if self.organized_log_path else None,
                    'content': organized_log_display
                }
            }
            
            # Generate JSON file
            output_path = self.report_dir / "report.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(parsed_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Complete JSON report generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating JSON report: {str(e)}")
            raise


    def generate_html(self):
        """
        Generate an HTML report using a SUBSET of the complete information.
        """
        try:
            parsed_data = self.parse_report()
            
            # Prepare data for HTML (create on-demand summary)
            html_datasets = []
            for dataset in parsed_data['datasets']:
                html_summary = self._create_html_summary(dataset)
                html_datasets.append(html_summary)
            
            # Get formatted configuration for HTML
            html_config = self._format_config_for_html()

            # Configure Jinja environment
            env = Environment(loader=FileSystemLoader(os.path.dirname(self.template)))
            template = env.get_template(os.path.basename(self.template))
            
            # Copy images
            self.setup_images()

            # Use placeholder if there is no organized_log_content
            if self.organized_log_content:
                organized_log_display = self.organized_log_content
            else:
                organized_log_display = "___ESPADA_ORGANIZED_LOG_PLACEHOLDER___"

    
            html_content = template.render(
                datasets=html_datasets,
                raw_log_content=self.raw_log_content,
                organized_log_content=organized_log_display,
                config=html_config
            )

            output_path = self.report_dir / "index.html"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML report generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating HTML report: {str(e)}")
            raise


    def _enrich_pipeline_metadata(self):
        """
        Add additional metadata if it is not in pipeline_metadata.
        """

        if 'pipeline_name' not in self.pipeline_metadata:
            self.pipeline_metadata['pipeline_name'] = 'ESPADA'
        
        if 'run_id' not in self.pipeline_metadata:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.pipeline_metadata['run_id'] = f"run_{timestamp}"
        
        if 'generation_time' not in self.pipeline_metadata:
            self.pipeline_metadata['generation_time'] = datetime.now().isoformat()
        
        # Add basic system info if it is not already there
        if 'environment' not in self.pipeline_metadata:
            self.pipeline_metadata['environment'] = {
                'python_version': sys.version,
                'hostname': socket.gethostname(),
                'working_directory': str(Path.cwd())
            }


    def _extract_fits_metadata(self, input_data):
        """
        Extract metadata from FITS files.
        """
        if input_data is None:
            return {
                'file_path': None,
                'file_exists': False,
                'header_info': {},  
                'observational_parameters': {},
                'telescope_info': {},
                'data_dimensions': {},
                'wcs_info': {}
            }      
        try:
            input_path = Path(input_data) if isinstance(input_data, (str, Path)) else input_data
            
            return {
                'file_path': str(input_path) if input_path else None,
                'file_exists': input_path.exists() if input_path else False,
                'header_info': {},  
                'observational_parameters': {},
                'telescope_info': {},
                'data_dimensions': {},
                'wcs_info': {}
            }
        except Exception as e:
            logger.error(f"Error extracting FITS metadata from {input_data}: {str(e)}")
            return {
                'file_path': str(input_data) if input_data else None,
                'file_exists': False,
                'header_info': {},  
                'observational_parameters': {},
                'telescope_info': {},
                'data_dimensions': {},
                'wcs_info': {}
            }


    def _format_config_for_html(self):
        """
        Format the settings to be displayed in the HTML.
        """
        config_data = self.pipeline_metadata.get('configuration', {})
        if not config_data:
            return None
        
        main_config = config_data.get('main_config', {})
        
        category_names = {
            'general': 'General',
            'logger': 'Logger',
            'input_data': 'Input Data',
            'tap_service': 'TAP Service',
            'sofia': 'SoFiA-2',
            'sip': 'SIP',
            'group': 'Group',
            'other': 'Other'
        }
        
        param_names = {
            'make_report': 'Generate Report',
            'verbose': 'Verbose Output',
            'num_cores': 'Number of Cores',
            'output_dir': 'Output Directory',
            'clear_logs': 'Clear Previous Logs',
            'log_file': 'Log File Path',
            'input_data_set': 'Input Dataset(s)',
            'input_file': 'Input File',
            'enable_tap_service': 'Enable TAP Service',
            'download_par_file': 'Download Parameters File',
            'enable_sofia': 'Enable SoFiA-2',
            'run_mode': 'Run Mode',
            'use_mask': 'Use Mask',
            'abs_flag_cube': 'Absorption Flag Cube',
            'auto_setup': 'Auto Setup',
            'sofia_abs_file': 'SoFiA-2 Absorption Par File',
            'sofia_emi_file': 'SoFiA-2 Emission Par File',
            'enable_sip': 'Enable SIP',
            'sip_par_file': 'SIP Parameters File',
            'enable_group': 'Enable Source Grouping',
            'overlap_mode': 'Overlap Mode',
            'overlap_threshold': 'Overlap Threshold'
        }
        
        formatted_main = {}
        for category, params in main_config.items():
            cat_name = category_names.get(category, category.replace('_', ' ').title())
            formatted_params = {}
            for key, value in params.items():
                display_name = param_names.get(key, key.replace('_', ' ').title())
                if isinstance(value, bool):
                    display_value = '✓' if value else '✗'
                elif value is None:
                    display_value = '—'
                elif isinstance(value, list):
                    display_value = ', '.join(str(v) for v in value) if len(value) <= 5 else f"[{len(value)} items]"
                elif isinstance(value, dict):
                    display_value = f"{{{len(value)} keys}}"
                else:
                    display_value = str(value)
                
                formatted_params[key] = {
                    'name': display_name,
                    'value': display_value,
                    'raw_value': value
                }
            formatted_main[cat_name] = formatted_params
        
        # Download config
        download_config = config_data.get('download_config')
        formatted_download = None
        if download_config:
            formatted_download = {
                'server': download_config.get('server', {}),
                'query': download_config.get('query', {}),
                'download_par': download_config.get('download_par', {}),
                'other': download_config.get('other', {})
            }
        
        return {
            'main_config': formatted_main,
            'download_config': formatted_download,
            'config_file_used': config_data.get('config_file_used', 'Unknown')
        }


    def _convert_eps_to_png(self, eps_path, png_path):
        """
        Convert an EPS file to PNG using Ghostscript.

        Arguments:

        eps_path: Path to the input EPS file
        png_path: Path where to save the output PNG

        Returns:
        bool: True if the conversion was successful
        """
        try:
            # Ghostscript command used to convert EPS to PNG.
            cmd = [
                'gs',
                '-dSAFER',
                '-dBATCH',
                '-dNOPAUSE',
                '-dEPSCrop',
                '-sDEVICE=png16m',
                '-dGraphicsAlphaBits=4',
                '-dTextAlphaBits=4',
                '-r150',  # DPI resolution
                f'-sOutputFile={png_path}',
                str(eps_path)
            ]

            # Run conversion.
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30  # 30-second timeout
            )
            
            if result.returncode == 0: 
                logger.info(f"Converted EPS to PNG: {eps_path.name} -> {png_path.name}") 
                return True 
            else: 
                logger.error(f"EPS conversion error: {result.stderr}") 
                return False 

        except subprocess.TimeoutExpired: 
            logger.error(f"Timeout in EPS conversion: {eps_path.name}") 
            return False 
        except FileNotFoundError: 
            logger.error("Ghostscript not found. Install with: 'apt-get install ghostscript' or 'brew install ghostscript'") 
            return False 
        except Exception as e: 
            logger.error(f"Unexpected error converting EPS: {str(e)}") 
            return False


    def _read_log_file(self, log_path):
        """Read the content of a Log file"""
        if not log_path or not os.path.exists(log_path):
            return f"No log: '{log_path}' for this report"
        
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading log file '{log_path}': {str(e)}")
            return f"Error reading log: '{str(e)}'"


    def _format_parfile_content(self, parfile_content, par_changes):
        """
        Formats the contents of the parameter file, highlighting the changes.

        Args:
        parfile_content (str): Full contents of the parameter file
        par_changes (dict): Dictionary with the modified parameters

        Returns:
        str: Formatted text with the changes highlighted
        """

        lines = parfile_content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.rstrip()  
            
            # Keep lines empty and comments clear
            if not line.strip() or line.strip().startswith('#'):
                formatted_lines.append(line)
                continue
            
            # Process lines with parameters
            if '=' in line:
                parts = line.split('=', 1)
                param_name = parts[0].strip()
                param_value = parts[1].strip() if len(parts) > 1 else ''
                
                # Check if this parameter was modified
                if param_name in par_changes:
                    original_value = par_changes[param_name]
                    formatted_line = f"{param_name} = {param_value}  # → Changed for: {original_value}"
                    formatted_lines.append(formatted_line)
                else:
                    formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    

    def _organize_images_for_html(self, images):
        """
        Organize images for the HTML template (existing method).
        """
        organized_images = {
            'sofia': {
                'regular': {'absorption': [], 'emission': []},
                'group': {'absorption': [], 'emission': []}
            },
            'sip': {
                'regular': {'absorption': {}, 'emission': {}},
                'group': {'absorption': {}, 'emission': {}}
            },
            'qa': []
        }
        
        for img in images:
            mode = img.get('mode', 'absorption')
            is_group = img.get('is_group', False)
            software_id = img.get('software-id', '')
            
            if software_id == 'sofia':
                category = 'group' if is_group else 'regular'
                if mode not in organized_images['sofia'][category]:
                    organized_images['sofia'][category][mode] = []
                organized_images['sofia'][category][mode].append(img)
            elif software_id == 'sip':
                category = 'group' if is_group else 'regular'
                if mode not in organized_images['sip'][category]:
                    organized_images['sip'][category][mode] = {}
                
                source_id = img.get('source_id', 0)
                if source_id not in organized_images['sip'][category][mode]:
                    organized_images['sip'][category][mode][source_id] = []
                
                organized_images['sip'][category][mode][source_id].append(img)
            elif software_id == 'qa':
                organized_images['qa'].append(img)
        
        return organized_images


    def _create_html_summary(self, dataset):
        """
        Create HTML summary from full data. 
        """

        if self._html_summary_cache is None:
            self._html_summary_cache = {}
        
        dataset_id = dataset.get('dataset_id')
        if dataset_id in self._html_summary_cache:
            return self._html_summary_cache[dataset_id]
        
        # Transform software_results to HTML format
        html_softwares = []
        for sw in dataset.get('software_results', []):
            software_exit_message = sw['status_info'].get('software_exit_message', '')
            software_exit_code = (
                sw['execution_info']['exit_code']
                if software_exit_message
                else None
            )
            error_message = sw['status_info']['error_message']
            status_title = (
                software_exit_message
                or error_message
                or sw['status_info']['status']
            )
            html_softwares.append({
                'software_id': sw['software_id'],
                'mode': sw['mode'],
                'warning_number': sw['status_info']['warning_count'],
                'log_path': sw['logs']['log_path'],
                'log_content': sw['logs']['log_content'],
                'error': error_message,
                'sw_status': sw['status_info']['status'],
                'sw_status_severity': sw['status_info'].get('status_severity', ''),
                'exit_code': sw['execution_info']['exit_code'],
                'software_exit_code': software_exit_code,
                'software_exit_message': software_exit_message,
                'software_subprocess_error': sw['status_info'].get(
                    'software_subprocess_error', ''
                ),
                'status_title': status_title,
                'sofia_parfile': sw['configuration']['formatted_parfile'],
                'command': sw['configuration']['command_executed'],
                'is_group': sw['status_info']['is_group']
            })
        
        html_summary = {
            'input_name': dataset.get('input_name'),
            'input_path': dataset.get('input_path') or dataset.get('input_name'),
            'status': dataset['status'],
            'softwares': html_softwares,
            'images': dataset['images'],
            'images_grouped': dataset['images_grouped'],
            'qa_by_mode': dataset.get('qa_by_mode', {}) 
        }
        
        self._html_summary_cache[dataset_id] = html_summary
        return html_summary
    

    def get_parsed_data(self):
        """
        Returns the parsed data (useful for testing or integration).
        """
        if self.parsed_data is None:
            self.parse_report()
        return self.parsed_data


    def inject_organized_log(self, organized_log_path, html_path, json_path):
        """
        Injects the contents of the organized log into a pre-generated HTML file.

        Args:
        organized_log_path: Path to the organized log file (*.log)
        html_path: Path to the HTML file to be modified
        """
        
        try:

            # Read the organized log
            organized_content = self._read_log_file(organized_log_path)
            if not organized_content:
                logger.warning("Organized log content is empty, skipping injection")
                return
        
        ##############################################################################################
        
            # Read existing HTML
            html_path = Path(html_path)
            if not html_path.exists():
                logger.error(f"HTML file not found: {html_path}")
                return
            
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Replace the placeholder
            if "___ESPADA_ORGANIZED_LOG_PLACEHOLDER___" not in html_content:
                logger.warning("Placeholder not found in HTML, organized log not injected")
                return
            
            html_content = html_content.replace(
                "___ESPADA_ORGANIZED_LOG_PLACEHOLDER___",
                organized_content
            )
            
            # Atomic writing
            temp_path = html_path.with_suffix(".tmp")
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            temp_path.replace(html_path)
            
            logger.info(f"Organized log injected into HTML report: {html_path}")

        ##############################################################################################

            # Read existing JSON
            json_path = Path(json_path)
            if not json_path.exists():
                logger.warning(f"JSON file not found: {json_path}")
                return
            
            with open(json_path, 'r', encoding='utf-8') as f:
                json_content = f.read()
            
            if "___ESPADA_ORGANIZED_LOG_PLACEHOLDER___" not in json_content:
                logger.warning("Placeholder not found in JSON, skipping JSON injection")
                return
            
            # Escape content for JSON; json.dumps does this automatically.
            escaped_content = json.dumps(organized_content)[1:-1]  # Remove outer quotes.
            json_content = json_content.replace(
                "___ESPADA_ORGANIZED_LOG_PLACEHOLDER___",
                escaped_content
            )

            temp_json = json_path.with_suffix(".tmp")
            with open(temp_json, 'w', encoding='utf-8') as f:
                f.write(json_content)
            temp_json.replace(json_path)

            logger.info(f"Organized log injected into JSON: {json_path}")
        
        ##############################################################################################

        except Exception as e:
            logger.error(f"Error injecting organized log into HTML: {e}")




        
