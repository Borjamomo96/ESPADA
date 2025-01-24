# ADP ALMA Pipeline



## Requirements

Este código ha sido desarrollado y testeado (no aún) con Python 3.10.15. 

Esta Pipeline hace uso de los programas externos Source Finding Application (SoFiA) y SoFiA Image Pipeline (SIP). Por tanto, se requiere tener instalados ambos software previamente en el equipo. Para poder instalar ambos software recomendamos encarecidamente leer su documentación correspondiente en los repositorios:

(https://gitlab.com/SoFiA-Admin/SoFiA-2)
(https://github.com/kmhess/SoFiA-image-pipeline)

Adicionalmente se ha usado parte del código del software ALMA Archive Mining & Visualization Toolkit (ALMINER) y se ha adaptado convenientemente. Dado que este software hace uso del paquete Astropy, es necesario tenerlo instalado previamente.  


## Configuration master file

La pipeline se corre usando un archivo de configuración 'config.yaml' que se encuentra por defecto en este repositorio y contiene los parámetros esenciales para que funcione. Estos son: 

- [ ]  GENERAL:
    - quality_assesment: Si True, se realizará un rápido y sencillo quality assement de los datos obtenidos con SoFiA. Tipo <bool>
    - capture_outputs: Si True, capturará todos los outputs provenientes de los programas externos SoFiA y SIP. Tipo <bool>. Se recomienda en general dejarlo como False.

- [ ]  INPUT DATA:
    - input_data: Ruta (con el nombre del archivo incluido) al cubo de datos en el que correr la pipeline. Tipo <str>.
    - input_data_list: NO IMPLEMENTADO AÚN. Esto quiere decir que por el momento si se desean descargar más de un cubo de datos a la vez del archivo de ALMA, la pipeline solo cogerá el más 
    reciente. Ver descripción más adelante 

- [ ]  LOGGER:
    - log_file: Nombre del archivo en que se desean se guarden los mensajes del logger. Tipo <str>. Ejemplo: "adpalmap.log".
    - clear_logs: Si True, limpia el archivo en el que se van a escribir todas las entradas del logger. Esto solo funciona si el nombre del archivo seleccionado coincide con el nombre del archivo 
    en runs anteriores. Tipo <bool>

- [ ]  TAP SERVICE:
    - enable_tap_service: Si True, permite que se ejecute el módulo datap.py, el cual se encarga de descargar datos del archivo de ALMA según las parámetros seleccionados en el archivo 'dowload_par_file'. Tipo <bool>.
    - download_par_file: Ruta (con el nombre del archivo incluido) al archivo que contiene los parámetros deseados para descargar datos del archivo de ALMA. Este archivo se encuentra por defecto
    en este repositorio bajo el nombre 'download_par.yaml'. Tipo <str>. Los parámetros que encontramos dentro de este archivo esta explicados en la sección Download parameter file. ACLARACIÓN, si se elije descargar archivos el programa por defecto usará los archivos descargados e ignorará los archivos seleccionados en INPUT DATA.
         
- [ ]  SOFIA:
    - enable_sofia : If True, permite que se ejecute el módulo sofia.py, en el cual se utiliza el software externo SoFiA. Tipo <bool>. 
    - run_mode: Indica el tipo de emisión que debe buscar SoFiA en el cubo de datos seleccionado. Tiene tres modos disponibles 'emission' 'absoprtion' y 'both'. Si se selecciona 'both' SoFiA se ejecutará primero trantando de buscar absorciones y un segunda vez pero buscando emisiones. Ver descripción del parámetros 'abs_flag_cube' para más detalles. Tipo <str>. 
    - abs_flag_cube: Si True, se usará la máscara obtenida en el primer run de SoFiA del modo 'both', es decir, las absorciones, como una flag mask para la búsqueda de emisiones. Tipo <bool>.
    - auto_setup: Si True,  se ajustarán ciertos parámetros de SoFiA según ciertas palabras clave que se encuentran en el header de los cubos de datos. Tipo <bool>.
    - sofia_abs_file : Ruta (con el nombre del archivo incluido) al archivo que contiene los parámetros necesarios para ejecutar SoFiA buscando absorciones.  Tipo <str>.
    - sofia_emi_file : Ruta (con el nombre del archivo incluido) al archivo que contiene los parámetros necesarios para ejecutar SoFiA buscando emisiones.  Tipo <str>.

    NOTA: Existen ciertos parámetros especificos de SoFiA que chocan con el flujo de ADPAlmaP. Estos son: 
        - 'input.data': Se ignorará en cualquier caso dentro de los parámetros de SoFiA. Se usarán el seleccionado en 'config.yaml' o los descargados según 'download_par.yaml'. en caso de que se mantega en el archivo, simplemente saltará una advertencia indicando que se va a ignorar. 
        - 'input.invert': Se ignorará y se mostrarán advertencias si hay un conflicto entre el modo seleccionado y el valor seleccionado ya sea en el archivo de parámetros o por terminal. 
        - 'input.primaryBeam': Se ignorará solo en el caso de que si activa el módulo para descargar archivos, en tal caso, se usará el archivo descargado siempre y cuando se haya seleccionado su descarga en el archivo 'download_par.yaml'.
    NOTA: Los archivos de parametros tanto de absorcion como de emisión disponibles en el reposiotorio están "optimizados" para funcionar en la mayoría de los cubos de datos de ALMA en la banda 3.
    NOTA: Si se desea se pueden cambiar parámetros a través de la terminal usando el comando "-sop|--sofia-parameters <parameter>=<value>" de igual manera que se haría corriendo SoFiA de manera aislada. Como se ha mencionado, los 3 parámetros anteriores seguirán la lógica explicada y se ignorarán según corresponda. 

- [ ]  SIP:
    - enable_sip : If True, permite que se ejecute el módulo sipar.py, en el cual se utiliza el software externo SIP. Tipo <bool>.
    - sip_par_file : Ruta (con el nombre del archivo incluido) al archivo que contiene los parámetros necesarios para ejecutar SIP. Type <str>. 

    NOTA: La implementación de un archivo de parametros para SIP se ha elegido para comodidad del usuario y para continuar la lógica modular de ADPAlmaP. Si se desea se pueden especificar los argumentos a través de la terminal usando el comando 'sarg|--sip-arguments <- comando value>'. Ejemplo: -sarg -c catalog.xml -i 0.15 -m
    NOTA: El argumento '-c|--catalog' solo se será necesario en el caso de que el módulo encargado de correr SoFiA este deshabilitado, de lo contrario el parámetro se ignorará y usará el catálogo recién obtenido a través de SoFiA. 


## Download parameter file

################
#    SERVER    #
################

#The archive service to use. By default the server address is set to 'ESO'

server_address: 'https://almascience.eso.org' #<str> URL of the server website to query the data.

#Options are:
#'ESO' Europe ('https://almascience.eso.org'),
#'NRAO' North America ('https://almascience.nrao.edu'), or
#'NAOJ' East Asia ('https://almascience.nao.ac.jp')


#The ALMA TAP service allow you to log in using your crendencials. By default is set to False
#Setting True will give you priority in the server queu that allow a faster download

credentials:  False # <bool> 
stored_credentials: False # <bool>

###############
#    QUERY    #
###############

#( By default the query type is set to 'Proposal ID')
#THIS PART MAY SUFFER FUTURE STRUCTE CHANGES. 

query_type: 'proposal'

#The query type options available are:
# 'conesearch' 
# 'target'
# 'keysearch'
# 'free'

##Specific parameters for the query indicated in 'query_type':
query_par:
#-----------------query type = proposal---------------------#
  proposal_id: '2018.1.01852.S' 
#----------------query type = conesearch--------------------#
  #ra: 1
  #dec: 1
  #search_radius: 1.
#------------------query type = target----------------------#
  #sources: None
  #search_radius: 2.
#-----------------query type = keysearch--------------------#
  #search_dict: {"proposal_abstract": ["high-mass star formation outflow disk"]}
#-------------------query type = free-----------------------#
  #query_str: "SELECT * FROM ivoa.obscore WHERE ((LOWER(proposal_abstract) LIKE '%planet-forming disk%')) AND (spatial_resolution < 0.5) AND (LOWER(data_rights) LIKE '%public%') AND (LOWER(scan_intent) LIKE '%target%') ORDER BY proposal_id"

#Common parameters for the query
  point: False 
  public: True
  published: None
  print_targets: True 
  print_query: True



## Parameters for data download

download_par:
  fitsonly : True                                    # <bool> (Default value = True) Download individual fits files only. This option will not download the raw data
  include_pb: True                                  # <bool> (Default value = True). Download all the .pb. files (i.e. all the primary beam cubes) with no distinction among the science cubes. 
  remove_uncompress_file: False                      # <bool> (Default value = True). Remove uncompress_files. This is the case for primary beams cubes in the ALMA archive. 
  dryrun : False                                     # <bool> (Default value = False) Allow the user to do a test run to check the size and number of files to download without actually
                                                      # downloading the data (dryrun=True). To download the data, set testrun=False.
  print_urls : True                                 # bool, optional (Default value = False) Write the list of urls to be downloaded from the archive to the terminal.
  filename_must_include : ['A001_X133d_X4226.COSMOS-1189669_sci.spw25.cube']  #<list of str> A list of strings the user wants to be contained in the url filename. This is useful to restrict the
                                                      # download further, for example, to data that have been primary beam corrected ('.pbcor') or that have
                                                      #the science target or calibrators (by including their names). The choice is largely dependent on the
                                                      #cycle and type of reduction that was performed and data products that exist on the archive as a result.
                                                      #In most recent cycles, the science target can be filtered out with the flag '_sci' or its ALMA target name.
  data_dir :                          #<str> The path of the directory where the downloaded data should be placed.



## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
