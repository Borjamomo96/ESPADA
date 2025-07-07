

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

import os
import jinja2
import webbrowser

def calcular_estado_dataset(softwares):
    estados = [sw['estado'] for sw in softwares]
    if 'error' in estados:
        return 'error'
    elif 'warning' in estados:
        return 'warning'
    else:
        return 'ok'

current_dir = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(current_dir, 'templates')

env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))
template = env.get_template('report.html')

datasets = [
    {
        'nombre': 'Dataset 1',
        'softwares': [
            {'nombre': 'ALminer', 'estado': 'ok', 'log': 'ALminer ejecutado correctamente.'},
            {'nombre': 'SoFiA-2', 'estado': 'warning', 'log': 'SoFiA-2: Warning, algunos canales vacíos.'},
            {'nombre': 'SIP', 'estado': 'error', 'log': 'SIP: Error fatal en la lectura del archivo.'}
        ],
        'imagenes': [
            {'url': 'static/img1.png', 'descripcion': 'Mapa de momento 0'},
            {'url': 'static/img2.png', 'descripcion': 'Mapa de momento 1'}
        ]
    },
    {
        'nombre': 'Dataset 2',
        'softwares': [
            {'nombre': 'ALminer', 'estado': 'ok', 'log': 'ALminer ejecutado correctamente.'},
            {'nombre': 'SoFiA-2', 'estado': 'ok', 'log': 'SoFiA-2: Warning, algunos canales vacíos.'},
            {'nombre': 'SIP', 'estado': 'ok', 'log': 'SIP: Error fatal en la lectura del archivo.'}
        ],
        'imagenes': [
            {'url': 'static/img1.png', 'descripcion': 'Mapa de momento 0'},
            {'url': 'static/img2.png', 'descripcion': 'Mapa de momento 1'}
        ]
    }
]

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


html = template.render(datasets=datasets, adp_log=adp_log)

output_file = os.path.join(current_dir, 'report_test.html')
with open(output_file, 'w') as f:
    f.write(html)

webbrowser.open('file://' + output_file)

