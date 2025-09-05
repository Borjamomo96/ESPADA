import os
import shutil

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

from pprint import pprint

# Logger:
import logging
from adplib.logger import Logger
logger= Logger.get_logger()

class Report:

    def __init__(self, datasets, template, adp_log):
        self.datasets = datasets
        self.template = template
        self.adp_log = adp_log
        self.adp_log_content = self._read_log_file(adp_log)
        self.report_dir = Path.cwd().resolve() / "report"
        self.image_dir = self.report_dir / "images"
        self.resources_dir = self.report_dir / "resources"

        # Creo estructura de directorios al inicializar
        self._create_directory_structure()
        self._copy_template_resources()


    def _create_directory_structure(self):
        
        report_dir_aux = self.report_dir
        timestamp = datetime.now().strftime("%d%m%y_%H%M%S")
        if self.report_dir.exists():
            self.report_dir = report_dir_aux.with_name(f"{report_dir_aux.name}_{timestamp}")
            self.image_dir = self.report_dir / "images"
            self.resources_dir = self.report_dir / "resources"

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
            
            # Copio los css
            for resource in base_resources_dir.glob('resources/*'):
                if resource.is_file():
                    shutil.copy2(resource, self.resources_dir)
                    logger.debug(f"Copied resource: {resource.name}")
            
            # Copio imagen de logo 
            for img in base_resources_dir.glob('images/*'):
                if img.is_file():
                    shutil.copy2(img, self.image_dir)
                    logger.debug(f"Copied image from template: {img.name}")
            
            logger.info("Template resources copied successfully")

        except Exception as e:
            logger.error(f"Error copying resources from template: {str(e)}")
            raise


    def setup_images(self):

        #Copia las imágenes a la carpeta del reporte y actualiza rutas
        os.makedirs(self.image_dir, exist_ok=True)
        
        for dataset in self.datasets:
            for img in dataset.get('images', []):
                src = img['path']
                filename = os.path.basename(src)
                dest = self.image_dir / src.name
                
                shutil.copy2(src, dest)
                img['path'] = os.path.join("images", filename)  # Ruta relativa


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
            
            # Mantener líneas vacías y comentarios
            if not line.strip() or line.strip().startswith('#'):
                formatted_lines.append(line)
                continue
            
            # Procesar líneas con parámetros
            if '=' in line:
                parts = line.split('=', 1)
                param_name = parts[0].strip()
                param_value = parts[1].strip() if len(parts) > 1 else ''
                
                # Verificar si este parámetro fue modificado
                if param_name in par_changes:
                    original_value = par_changes[param_name]
                    formatted_line = f"{param_name} = {param_value}  # → Changed for: {original_value}"
                    formatted_lines.append(formatted_line)
                else:
                    formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    

    def parse_report(self):
        datasets = []
        for dataset_tuple in self.datasets: #Todos los datset disponibles de los diferentes workers

            all_software = []
            input_data = None
            images = []
            error_exist = False
            warning_exist = False
            
            # Los dataset vienen en tuplas de 3: SoFiA, SIP y QA
            for software_list in dataset_tuple: 
                
                for sw in software_list: # En cada tupla puede haber absorcion emision
                    # Busco input.data. Se puede hacer de otra manera 
                    if not input_data:
                        if 'sofia_par_changes' in sw and 'input.data' in sw['sofia_par_changes']:
                            input_data = sw['sofia_par_changes']['input.data']
                        elif 'input_name' in sw:
                            input_data = sw['input_name']

                    # To process just SoFIa and SIP
                    if sw['software_id'] == 'QA':
                        if 'outputs' in sw and 'images' in sw['outputs']:
                            for img in sw['outputs']['images']:
                                img['is_qa'] = True  # Marco como imagen QA
                            images.extend(sw['outputs']['images'])
                        continue
                    
                    # Determino el 'status' del software
                    error = sw.get('error', '')
                    warnings = 2 
                    
                    if error:
                        sw_status = 'error' 
                        error_exist = True
                    elif warnings > 4:
                        sw_status = 'warning'  
                        warning_exist = True
                    else:
                        sw_status = 'ok'  
                    
        
                    # Toda la información de cada software
                    software_info = {
                        'software_id': sw['software_id'],
                        'mode': sw.get('mode', ''),
                        'warning_number': warnings,
                        'log_path': str(sw.get('log_path', '')),
                        'log_content': self._read_log_file(sw.get('log_path', '')),
                        'error': error,
                        'sw_status': sw_status,
                        'sofia_parfile': self._format_parfile_content(
                            self._read_log_file(sw.get('sofia_parfile', '')),
                            sw.get('sofia_par_changes', {})
                        ),
                        'command' : ' '.join(sw.get(('command'), ''))
                    }
                    all_software.append(software_info)
                    
                    # Imagenes
                    # Guardo TODAS las imágenes sin ordenar de todos los softwares y de todos 
                    # los modos
                    if 'outputs' in sw and 'images' in sw['outputs']:
                        for img in sw['outputs']['images']:
                            img['mode'] = sw.get('mode', None)
                            img['is_qa'] = False  # Marco como no QA
                        images.extend(sw['outputs']['images'])


            # Reorganizar imágenes por tipo y fuente
            # Aquí las reorganizo por tipo de software. 
            organized_images = {
                'sofia': {'absorption': [], 'emission': []},
                'sip': {'absorption': {}, 'emission': {}}, #Pueden haber varias fuentes de ahí que sea {} 
                'qa': []
            }
            
            for img in images:
                mode = img.get('mode', 'absorption')

                if img['software-id'] == 'sofia':
                    if mode not in organized_images['sofia']:
                        organized_images['sofia'][mode] = []
                    organized_images['sofia'][mode].append(img)

                elif img['software-id'] == 'sip':
                    if mode not in organized_images['sip']:
                        organized_images['sip'][mode] = {}
                    
                    source_id = img.get('source_id', 0)
                    if source_id not in organized_images['sip'][mode]:
                        organized_images['sip'][mode][source_id] = []
                    
                    organized_images['sip'][mode][source_id].append(img)
                elif img['software-id'] == 'qa':
                    organized_images['qa'].append(img)


            # Determinar status general del dataset
            dataset_status = 'error' if error_exist else 'warning' if warning_exist else 'ok'
            
            datasets.append({
                'input_data': input_data,
                'status': dataset_status,
                'softwares': all_software,
                'images': images,
                'images_grouped': organized_images
            })
        
        return datasets
    
    
    def generate_html(self):

        try:
            self.datasets = self.parse_report()

            env = Environment(loader=FileSystemLoader(os.path.dirname(self.template)))
            template = env.get_template(os.path.basename(self.template))
            
            self.setup_images()  
            
            html_content = template.render(
                datasets=self.datasets,
                adp_log_content=self.adp_log_content  
            )

            from pprint import pformat
            with open("test_print.txt", 'w') as f:
                f.write(pformat(self.datasets))

            output_path = self.report_dir / "index.html"
            with open(output_path, 'w') as f:
                f.write(html_content)
            
            logger.info(f"Report successfully generated in:{output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error generating HTML report: {str(e)}")
            raise