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

class Report:

    def __init__(self, worker_results, template, adp_log, pipeline_metadata=None, config=None):

        self.worker_results = worker_results
        self.template = template
        self.adp_log = adp_log
        self.pipeline_metadata = {} #pipeline_metadata or
        self.config = config

        # Log content
        self.adp_log_content = self._read_log_file(adp_log)


        # Directories
        base_dir = Path.cwd().resolve() / "report"
        timestamp = datetime.now().strftime("%d%m%y_%H%M%S")

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

        # Add additional etadata if missing
        #self._enrich_pipeline_metadata()
    

    def parse_report(self):
        """
        Parse the worker resuslts into a COMPLETE and NEUTRAL structure.
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
                    # Se puede llenar con info de timing si está disponible
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
            input_data = None
            images = []
            error_exist = False
            warning_exist = False
            #######################################################################################    
            # COMPLETE INFORMATION BY SOFTWARE

            for software_list in dataset_tuple:
                for sw in software_list:
                    # Identify input data
                    if not input_data:
                        if 'sofia_par_changes' in sw and 'input.data' in sw['sofia_par_changes']:
                            input_data = sw['sofia_par_changes']['input.data']
                        elif 'input_name' in sw:
                            input_data = sw['input_name']
                    
                    # Grouo flag
                    is_group = software_list is dataset_tuple[3]
                    
                    # Skip QA processing (this is done in other part)
                    if sw['software_id'] == 'QA':
                        if 'outputs' in sw and 'images' in sw['outputs']:
                            for img in sw['outputs']['images']:
                                img['is_qa'] = True
                                img['software-id'] = 'qa'  
                            images.extend(sw['outputs']['images'])
                        continue
                    
                    
                    error = sw.get('error', '')
                    warnings = sw.get('warning_number', 2)  # CAMBIAR EN UN FUTURO POR EL Nº REAL
                    
                    if error:
                        sw_status = 'error'
                        error_exist = True
                        parsed_data['execution_info']['total_errors'] += 1
                    elif warnings > 4:  # CAMBIAR EL UMBRAL EN UN FUTURO
                        sw_status = 'warning'
                        warning_exist = True
                        parsed_data['execution_info']['total_warnings'] += 1
                    else:
                        sw_status = 'ok'
                        parsed_data['execution_info']['successful_workers'] += 1
                   
                    ###############################################################################
                    # COMPLETE SOFTWARE INFORMATION
                    software_info = {
                        # Id
                        'software_id': sw['software_id'],
                        'software_version': '',  # CAMBIAR. Incluir la versión de software
                        'mode': sw.get('mode', ''), 
                        
                        # execution info
                        'execution_info': {
                            'pid': sw.get('PID'),
                            'start_time': '',  # TODO: Obtener tiempos reales
                            'end_time': '',
                            'duration_seconds': None,
                            'exit_code': 0 if not error else 1,
                            #'host': socket.gethostname()
                        },
                        
                        # Status and errors
                        'status_info': {
                            'status': sw_status,
                            'error_message': error,
                            'error_type': 'runtime' if error else None,
                            'warning_count': warnings,
                            'warnings_list': [],  # CAMBIAR. Se puede quitar
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
                            'quality_metrics': {}  # CAMBIAR. Métricas cuantitativas por añadir
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
            dataset_complete = {
                # Identificación
                'dataset_id': input_data or f"dataset_{len(parsed_data['datasets'])}",
                'input_data': input_data,
                # Metadatos del FITS
                'fits_metadata': self._extract_fits_metadata(input_data),
                # Resultados por software (TODO el detalle)
                'software_results': all_software,
                # Imágenes (para HTML)
                'images': images,
                'images_grouped': self._organize_images_for_html(images),
                # Status general
                'status': 'error' if error_exist else 'warning' if warning_exist else 'ok',
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
                            logger.info(f"Convert EPS to PNG: {filename} -> {png_filename}")
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
            
            # Add ADP log content
            parsed_data['adp_log'] = {
                'log_path': str(self.adp_log) if self.adp_log else None,
                'log_content': self.adp_log_content
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
            
            # Configure Jinja environment
            env = Environment(loader=FileSystemLoader(os.path.dirname(self.template)))
            template = env.get_template(os.path.basename(self.template))
            
            # Copy images
            self.setup_images()
            
    
            html_content = template.render(
                datasets=html_datasets,
                adp_log_content=self.adp_log_content
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
            self.pipeline_metadata['pipeline_name'] = 'ADP-ALMA-Pipeline'
        
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
            # Comando Ghostscript para convertir EPS a PNG
            cmd = [
                'gs',
                '-dSAFER',
                '-dBATCH',
                '-dNOPAUSE',
                '-dEPSCrop',
                '-sDEVICE=png16m',
                '-dGraphicsAlphaBits=4',
                '-dTextAlphaBits=4',
                '-r150',  # Resolución DPI
                f'-sOutputFile={png_path}',
                str(eps_path)
            ]
            
            # Ejecutar conversión
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30  # Timeout de 30 segundos
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
            html_softwares.append({
                'software_id': sw['software_id'],
                'mode': sw['mode'],
                'warning_number': sw['status_info']['warning_count'],
                'log_path': sw['logs']['log_path'],
                'log_content': sw['logs']['log_content'],
                'error': sw['status_info']['error_message'],
                'sw_status': sw['status_info']['status'],
                'sofia_parfile': sw['configuration']['formatted_parfile'],
                'command': sw['configuration']['command_executed'],
                'is_group': sw['status_info']['is_group']
            })
        
        html_summary = {
            'input_data': dataset['input_data'],
            'status': dataset['status'],
            'softwares': html_softwares,
            'images': dataset['images'],
            'images_grouped': dataset['images_grouped']
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






        