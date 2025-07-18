

"""# Ruta absoluta a la carpeta de plantillas
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(current_dir, 'templates')

# Configura Jinja2
env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))
template = env.get_template('report1.html')

# Lista de prueba de datasets y tareas
datasets = [
    {
        'nombre': 'ALminer Dataset',
        'tareas': [
            {'nombre': 'Ingest_AT', 'descripcion': 'file=member.uid...'},
            {'nombre': 'CubeStats_AT', 'descripcion': 'robust=medabsdevmed ppp=True'},
            {'nombre': 'CubeSum_AT', 'descripcion': 'numsigma=4.0 sigma=0.00130869 smooth=[]'},
        ]
    },
    {
        'nombre': 'SoFiA-2 Dataset',
        'tareas': [
            {'nombre': 'SFind2D_AT', 'descripcion': 'nsigma=5.0 sigma=0.00375253 region=[hin, 5] smax=35.0 nmax=30'},
            {'nombre': 'CubeSpectrum_AT', 'descripcion': "pos={1896, 1867}, x.im"},
        ]
    },
    {
        'nombre': 'SIP Dataset',
        'tareas': [
            {'nombre': 'LineSegment_AT', 'descripcion': 'numsigma=5.0 minchan=4 maxgap=3 csub=[0,0] iterate=True'},
        ]
    }
]

# Renderiza el HTML
html = template.render(datasets=datasets)

# Guarda el HTML generado
output_file = os.path.join(current_dir, 'report_test.html')
with open(output_file, 'w') as f:
    f.write(html)

print(f"HTML generado correctamente en {output_file}")

# Opcional: abre el archivo HTML en el navegador
webbrowser.open('file://' + output_file)"""
import sys
import pprint
import os
import jinja2
import webbrowser

def get_state(datasets):
    for dataset in datasets:
        hay_error = False
        hay_warning = False

        for sw in dataset['softwares']:
            error = sw.get('error', '')
            warnings = sw.get('numero_de_warning', 0)

            if error:
                sw['sw_estado'] = 'error'
                hay_error = True
            elif warnings > 4:
                sw['sw_estado'] = 'warning'
                hay_warning = True
            else:
                sw['sw_estado'] = 'ok'

        dataset['estado'] = 'error' if hay_error else 'warning' if hay_warning else 'ok'
        
    return datasets

def parse_report(report):
    datasets = []
    for dataset_tuple in report:
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
        
        # Determinar estado general del dataset
        dataset_estado = 'error' if error_exist else 'warning' if warning_exist else 'ok'
        
        datasets.append({
            'input_data': input_data,
            'estado': dataset_estado,
            'softwares': all_software,
            'images': images
        })
    
    return datasets

current_dir = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(current_dir, 'templates')

env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))
template = env.get_template('report.html')

datasets_test = [{'input_data': 'archive_data/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw21.cube.I.pbcor.fits',
  'softwares': [{'nombre': 'SoFiA-2',
    'modo': 'absorption',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw21.cube.I.pbcor_logfile.log',
    'error': "Command '['sofia', '/home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID10369.par']' returned non-zero exit status 8."},
   {'nombre': 'SoFiA-2',
    'modo': 'emission',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw21.cube.I.pbcor_logfile.log',
    'error': "Command '['sofia', '/home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID10369.par']' returned non-zero exit status 8."},
   {'nombre': 'SIP',
    'modo': 'absorption',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw21.cube.I.pbcor_sip.log',
    'error': ''},
   {'nombre': 'SIP',
    'modo': 'emission',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw21.cube.I.pbcor_sip.log',
    'error': ''}]},
 {'input_data': 'archive_data/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw23.cube.I.pbcor.fits',
  'softwares': [{'nombre': 'SoFiA-2',
    'modo': 'absorption',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw23.cube.I.pbcor_logfile.log',
    'error': ''},
   {'nombre': 'SoFiA-2',
    'modo': 'emission',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw23.cube.I.pbcor_logfile.log',
    'error': "Command '['sofia', '/home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID10370.par']' returned non-zero exit status 8."},
   {'nombre': 'SIP',
    'modo': 'absorption',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw23.cube.I.pbcor_sip.log',
    'error': ''},
   {'nombre': 'SIP',
    'modo': 'emission',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw23.cube.I.pbcor_sip.log',
    'error': ''}]},
 {'input_data': 'archive_data/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw19.cube.I.pbcor.fits',
  'softwares': [{'nombre': 'SoFiA-2',
    'modo': 'absorption',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw19.cube.I.pbcor_logfile.log',
    'error': "Command '['sofia', '/home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID10368.par']' returned non-zero exit status 8."},
   {'nombre': 'SoFiA-2',
    'modo': 'emission',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw19.cube.I.pbcor_logfile.log',
    'error': ''},
   {'nombre': 'SIP',
    'modo': 'absorption',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw19.cube.I.pbcor_sip.log',
    'error': ''},
   {'nombre': 'SIP',
    'modo': 'emission',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw19.cube.I.pbcor_sip.log',
    'error': ''}]},
 {'input_data': 'archive_data/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw25.cube.I.pbcor.fits',
  'softwares': [{'nombre': 'SoFiA-2',
    'modo': 'absorption',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw25.cube.I.pbcor_logfile.log',
    'error': "Command '['sofia', '/home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID10369.par']' returned non-zero exit status 8."},
   {'nombre': 'SoFiA-2',
    'modo': 'emission',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw25.cube.I.pbcor_logfile.log',
    'error': ''},
   {'nombre': 'SIP',
    'modo': 'absorption',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw25.cube.I.pbcor_sip.log',
    'error': ''},
   {'nombre': 'SIP',
    'modo': 'emission',
    'numero_de_warning': 2,
    'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw25.cube.I.pbcor_sip.log',
    'error': ''}]}]

"""
datasets = [([{'software_id': 'SoFiA-2', 'PID': 9598, 'input_name': 'sofia_test', 'mode': 'emission', 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_logfile.log', 'outputs': {'images': [{'type': 'rel', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/_rel.eps', 'description': 'Realibiliy Plot'}, {'type': 'skellman', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/_skellman.eps', 'description': 'Skellman Plot'}], 'files': [{'type': 'catalog_txt', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/_cat.txt', 'format': 'txt'}, {'type': 'catalog_xml', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/_xlm.txt', 'format': 'xlm'}]}, 'sofia_par_changes': {'pipeline.threads': '3', 'output.directory': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission', 'input.data': '/home/usuario/0Test_ADP_ALMAPipeline/test_directories/sofia_test.fits'}, 'error': ''}], [{'software_id': 'SIP', 'PID': 9598, 'input_name': 'sofia_test', 'mode': 'emission', 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_sip.log', 'outputs': {'images': [{'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_1_spec.png', 'source_id': 1}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_1_mom0.png', 'source_id': 1}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_1_mom1.png', 'source_id': 1}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_1_mom2.png', 'source_id': 1}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_1_snr.png', 'source_id': 1}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_1_pv.png', 'source_id': 1}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_1_pv_min.png', 'source_id': 1}, {'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_2_spec.png', 'source_id': 2}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_2_mom0.png', 'source_id': 2}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_2_mom1.png', 'source_id': 2}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_2_mom2.png', 'source_id': 2}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_2_snr.png', 'source_id': 2}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_2_pv.png', 'source_id': 2}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_2_pv_min.png', 'source_id': 2}, {'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_3_spec.png', 'source_id': 3}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_3_mom0.png', 'source_id': 3}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_3_mom1.png', 'source_id': 3}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_3_mom2.png', 'source_id': 3}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_3_snr.png', 'source_id': 3}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_3_pv.png', 'source_id': 3}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_3_pv_min.png', 'source_id': 3}, {'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_4_spec.png', 'source_id': 4}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_4_mom0.png', 'source_id': 4}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_4_mom1.png', 'source_id': 4}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_4_mom2.png', 'source_id': 4}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_4_snr.png', 'source_id': 4}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_4_pv.png', 'source_id': 4}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test/source_4_pv_min.png', 'source_id': 4}], 'files': []}, 'comand': ['sofia_image_pipeline', '-c', '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_cat.txt', '-x', 'png', '-i', '0.05', '-s', 'decals', '-line', 'CO', '-log', '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_sip.log'], 'error': ''}]), ([{'software_id': 'SoFiA-2', 'PID': 9600, 'input_name': 'sofia_test_2', 'mode': 'emission', 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2_logfile.log', 'outputs': {'images': [{'type': 'rel', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/_rel.eps', 'description': 'Realibiliy Plot'}, {'type': 'skellman', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/_skellman.eps', 'description': 'Skellman Plot'}], 'files': [{'type': 'catalog_txt', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/_cat.txt', 'format': 'txt'}, {'type': 'catalog_xml', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/_xlm.txt', 'format': 'xlm'}]}, 'sofia_par_changes': {'pipeline.threads': '3', 'output.directory': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission', 'input.data': '/home/usuario/0Test_ADP_ALMAPipeline/test_directories/sofia_test_2.fits'}, 'error': ''}], [{'software_id': 'SIP', 'PID': 9600, 'input_name': 'sofia_test_2', 'mode': 'emission', 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2_sip.log', 'outputs': {'images': [{'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_1_spec.png', 'source_id': 1}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_1_mom0.png', 'source_id': 1}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_1_mom1.png', 'source_id': 1}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_1_mom2.png', 'source_id': 1}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_1_snr.png', 'source_id': 1}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_1_pv.png', 'source_id': 1}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_1_pv_min.png', 'source_id': 1}, {'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_2_spec.png', 'source_id': 2}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_2_mom0.png', 'source_id': 2}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_2_mom1.png', 'source_id': 2}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_2_mom2.png', 'source_id': 2}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_2_snr.png', 'source_id': 2}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_2_pv.png', 'source_id': 2}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_2_pv_min.png', 'source_id': 2}, {'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_3_spec.png', 'source_id': 3}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_3_mom0.png', 'source_id': 3}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_3_mom1.png', 'source_id': 3}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_3_mom2.png', 'source_id': 3}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_3_snr.png', 'source_id': 3}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_3_pv.png', 'source_id': 3}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_3_pv_min.png', 'source_id': 3}, {'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_4_spec.png', 'source_id': 4}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_4_mom0.png', 'source_id': 4}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_4_mom1.png', 'source_id': 4}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_4_mom2.png', 'source_id': 4}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_4_snr.png', 'source_id': 4}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_4_pv.png', 'source_id': 4}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2/source_4_pv_min.png', 'source_id': 4}], 'files': []}, 'comand': ['sofia_image_pipeline', '-c', '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2_cat.txt', '-x', 'png', '-i', '0.05', '-s', 'decals', '-line', 'CO', '-log', '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_2_sip.log'], 'error': ''}]), ([{'software_id': 'SoFiA-2', 'PID': 9599, 'input_name': 'sofia_test_1', 'mode': 'emission', 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1_logfile.log', 'outputs': {'images': [{'type': 'rel', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/_rel.eps', 'description': 'Realibiliy Plot'}, {'type': 'skellman', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/_skellman.eps', 'description': 'Skellman Plot'}], 'files': [{'type': 'catalog_txt', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/_cat.txt', 'format': 'txt'}, {'type': 'catalog_xml', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/_xlm.txt', 'format': 'xlm'}]}, 'sofia_par_changes': {'pipeline.threads': '3', 'output.directory': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission', 'input.data': '/home/usuario/0Test_ADP_ALMAPipeline/test_directories/sofia_test_1.fits'}, 'error': ''}], [{'software_id': 'SIP', 'PID': 9599, 'input_name': 'sofia_test_1', 'mode': 'emission', 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1_sip.log', 'outputs': {'images': [{'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_1_spec.png', 'source_id': 1}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_1_mom0.png', 'source_id': 1}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_1_mom1.png', 'source_id': 1}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_1_mom2.png', 'source_id': 1}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_1_snr.png', 'source_id': 1}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_1_pv.png', 'source_id': 1}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_1_pv_min.png', 'source_id': 1}, {'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_2_spec.png', 'source_id': 2}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_2_mom0.png', 'source_id': 2}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_2_mom1.png', 'source_id': 2}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_2_mom2.png', 'source_id': 2}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_2_snr.png', 'source_id': 2}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_2_pv.png', 'source_id': 2}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_2_pv_min.png', 'source_id': 2}, {'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_3_spec.png', 'source_id': 3}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_3_mom0.png', 'source_id': 3}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_3_mom1.png', 'source_id': 3}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_3_mom2.png', 'source_id': 3}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_3_snr.png', 'source_id': 3}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_3_pv.png', 'source_id': 3}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_3_pv_min.png', 'source_id': 3}, {'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_4_spec.png', 'source_id': 4}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_4_mom0.png', 'source_id': 4}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_4_mom1.png', 'source_id': 4}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_4_mom2.png', 'source_id': 4}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_4_snr.png', 'source_id': 4}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_4_pv.png', 'source_id': 4}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1/source_4_pv_min.png', 'source_id': 4}], 'files': []}, 'comand': ['sofia_image_pipeline', '-c', '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1_cat.txt', '-x', 'png', '-i', '0.05', '-s', 'decals', '-line', 'CO', '-log', '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_1_sip.log'], 'error': ''}]), ([{'software_id': 'SoFiA-2', 'PID': 9601, 'input_name': 'sofia_test_3', 'mode': 'emission', 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3_logfile.log', 'outputs': {'images': [{'type': 'rel', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/_rel.eps', 'description': 'Realibiliy Plot'}, {'type': 'skellman', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/_skellman.eps', 'description': 'Skellman Plot'}], 'files': [{'type': 'catalog_txt', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/_cat.txt', 'format': 'txt'}, {'type': 'catalog_xml', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/_xlm.txt', 'format': 'xlm'}]}, 'sofia_par_changes': {'pipeline.threads': '3', 'output.directory': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission', 'input.data': '/home/usuario/0Test_ADP_ALMAPipeline/test_directories/sofia_test_3.fits'}, 'error': ''}], [{'software_id': 'SIP', 'PID': 9601, 'input_name': 'sofia_test_3', 'mode': 'emission', 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3_sip.log', 'outputs': {'images': [{'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_1_spec.png', 'source_id': 1}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_1_mom0.png', 'source_id': 1}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_1_mom1.png', 'source_id': 1}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_1_mom2.png', 'source_id': 1}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_1_snr.png', 'source_id': 1}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_1_pv.png', 'source_id': 1}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_1_pv_min.png', 'source_id': 1}, {'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_2_spec.png', 'source_id': 2}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_2_mom0.png', 'source_id': 2}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_2_mom1.png', 'source_id': 2}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_2_mom2.png', 'source_id': 2}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_2_snr.png', 'source_id': 2}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_2_pv.png', 'source_id': 2}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_2_pv_min.png', 'source_id': 2}, {'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_3_spec.png', 'source_id': 3}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_3_mom0.png', 'source_id': 3}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_3_mom1.png', 'source_id': 3}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_3_mom2.png', 'source_id': 3}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_3_snr.png', 'source_id': 3}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_3_pv.png', 'source_id': 3}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_3_pv_min.png', 'source_id': 3}, {'type': 'spec', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_4_spec.png', 'source_id': 4}, {'type': 'mom0', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_4_mom0.png', 'source_id': 4}, {'type': 'mom1', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_4_mom1.png', 'source_id': 4}, {'type': 'mom2', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_4_mom2.png', 'source_id': 4}, {'type': 'snr', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_4_snr.png', 'source_id': 4}, {'type': 'pv', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_4_pv.png', 'source_id': 4}, {'type': 'pv_min', 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3/source_4_pv_min.png', 'source_id': 4}], 'files': []}, 'comand': ['sofia_image_pipeline', '-c', '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3_cat.txt', '-x', 'png', '-i', '0.05', '-s', 'decals', '-line', 'CO', '-log', '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/sofia_test_3_sip.log'], 'error': ''}])]

"""


adp_log = """2025-07-02 11:04:36,213 | INFO | [PID:8051] adpalmap: - ADPALMAP start point
2025-07-02 11:04:36,690 | INFO | [PID:8051] adpalmap: - 'enable_tap_service' set to False. Skipping data download
2025-07-02 11:04:36,691 | INFO | [PID:8051] adpalmap: - The worker number has been set to 1

=== Subprocess PID: 8064 start ===
2025-07-02 11:04:36,958 | INFO | [PID:8064] sopar: - The file in '/home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_emi_default.par' have been loaded successfully
2025-07-02 11:04:36,959 | INFO | [PID:8064] sopar: - Reading parameters. Mode: emission.
2025-07-02 11:04:36,960 | INFO | [PID:8064] sopar: - Parameters ready. Mode: emission.
2025-07-02 11:04:36,960 | INFO | [PID:8064] sopar: - Creating temporary SoFiA parameter file based on the parameter file /home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID8064.par.
2025-07-02 11:04:36,961 | INFO | [PID:8064] sopar: - Parameters set for the run: 
[8064]pipeline.verbose=false
[8064]pipeline.pedantic=true
[8064]pipeline.threads=12
[8064]input.data=/home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_test_datacube.fits
[8064]input.primaryBeam= 
[8064]input.region=
[8064]input.gain=
"""


#datasets = get_state(datasets)

datasets = parse_report(datasets)    

html = template.render(datasets=datasets, adp_log=adp_log)

output_file = os.path.join(current_dir, 'report_test_1.html')
with open(output_file, 'w') as f:
    f.write(html)

#webbrowser.open('file://' + output_file)

