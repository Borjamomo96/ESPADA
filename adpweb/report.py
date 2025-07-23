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


    def prepare_images(self):

        #Copia las imágenes a la carpeta del reporte y actualiza rutas
        os.makedirs(self.image_dir, exist_ok=True)
        
        for dataset in self.datasets:
            for img in dataset.get('images', []):
                src = img['path']
                filename = os.path.basename(src)
                dest = self.image_dir / src.name
                
                shutil.copy2(src, dest)
                img['path'] = os.path.join("images", filename)  # Ruta relativa


    def parse_report(self):

        datasets = []
        for dataset_tuple in self.datasets:
            all_software = []
            input_data = None
            images = []
            error_exist = False
            warning_exist = False
            
            for software_list in dataset_tuple:
                for sw in software_list:
                    # Busco input.data. Se puede hacer de otra manera 
                    if not input_data:
                        if 'sofia_par_changes' in sw and 'input.data' in sw['sofia_par_changes']:
                            input_data = sw['sofia_par_changes']['input.data']
                        elif 'input_name' in sw:
                            input_data = sw['input_name']
                    
                    # Determino el 'estado' del software
                    error = sw.get('error', '')
                    warnings = 2 
                    
                    if error:
                        sw_estado = 'error' 
                        error_exist = True
                    elif warnings > 4:
                        sw_estado = 'warning'  
                        warning_exist = True
                    else:
                        sw_estado = 'ok'  
                    
                    # Toda la información de cada software
                    software_info = {
                        'nombre': sw['software_id'],
                        'modo': sw.get('mode', ''),
                        'numero_de_warning': warnings,
                        'log_path': str(sw.get('log_path', '')),
                        'error': error,
                        'sw_estado': sw_estado,
                        'sofia_par_changes': sw.get('sofia_par_changes', {}),
                        'sofia_parfile': ''
                    }
                    all_software.append(software_info)
                    
                    # Imagenes
                    if 'outputs' in sw and 'images' in sw['outputs']:
                        images.extend(sw['outputs']['images'])


            # Reorganizar imágenes por tipo y fuente
            organized_images = {
                'sofia': [],
                'sip': {},
                'qa': []
            }
            
            for img in images:
                if img['software-id'] == 'sofia':
                    organized_images['sofia'].append(img)
                elif img['software-id'] == 'sip':
                    source_id = img.get('source_id', 0)
                    if source_id not in organized_images['sip']:
                        organized_images['sip'][source_id] = []
                    organized_images['sip'][source_id].append(img)
                elif img['software-id'] == 'qa':
                    organized_images['qa'].append(img)


            # Determinar estado general del dataset
            dataset_estado = 'error' if error_exist else 'warning' if warning_exist else 'ok'
            
            datasets.append({
                'input_data': input_data,
                'estado': dataset_estado,
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
            
            self.prepare_images()  
            
            html_content = template.render(
                datasets=self.datasets,
                adp_log=self.adp_log  
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