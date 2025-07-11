

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

def calcular_estado_dataset(softwares):
    errors = [sw.get('error', '') for sw in softwares]   
    warnings = [True if sw.get('numero_de_warning', 0) > 4 else False for sw in softwares]

    if errors:
        return 'error'
    elif warnings:
        return 'warning'
    else:
        return 'ok'


current_dir = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(current_dir, 'templates')

env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))
template = env.get_template('report.html')

datasets = [{'input_data': 'archive_data/member.uid___A001_X88f_X6._J100054.83p023126.2__sci.spw21.cube.I.pbcor.fits',
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


for dataset in datasets:
    dataset['estado'] = calcular_estado_dataset(dataset['softwares'])
    

pprint.pprint(datasets)
sys.exit(-1)

html = template.render(datasets=datasets, adp_log=adp_log)

output_file = os.path.join(current_dir, 'report_test.html')
with open(output_file, 'w') as f:
    f.write(html)

webbrowser.open('file://' + output_file)

