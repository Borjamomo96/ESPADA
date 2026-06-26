
# ESPADA: Enhanced Spectral‑line Pipeline for the ALMA Data Archive

ESPADA is an end‑to‑end Python pipeline that automates the downloading of ALMA data from the Science Archive, source finding with SoFiA‑2, parameterisation and visualisation with the SoFiA Imaging Pipeline (SIP), and source grouping. It produces advanced data products with minimal user intervention.

## Requirements

This code has been developed with Python ≥ 3.10 (tested with 3.10.15)

This pipeline makes use of the external programs Source Finding Application (SoFiA) and SoFiA Image Pipeline (SIP). Therefore, it is necessary to have both software installed on your system beforehand. To install these programs, we strongly recommend reading their respective documentation in the repositories:

(https://gitlab.com/SoFiA-Admin/SoFiA-2)  
(https://github.com/kmhess/SoFiA-image-pipeline)

**Warning**: ESPADA makes use of the subprocess module to run external software such as SoFiA and SIP. To run each software, the subprocess module needs to know the command to call each one, which is not possible to know a priori for each device. It is recommended to install both SoFiA and SIP according to the authors' recommendations so that both are executed when called from the terminal as: `sofia` and `sofia_image_pipeline` respectively.

_Alternatively (not recommended option, under user responsibility)_: the corresponding line of code where each software is executed can be changed. To do this:

  - Look for the function `run_sofia` inside the _sopar.py_ module. 
  - Inside each function, look for the lines `cmd = ["sofia", f"{temp_file_path}"]` in each of the if blocks corresponding to each of the usage modes (see below). 
  - Change the (str) _"sofia"_ for the corresponding command used to run SoFiA on the device.

  - Look for the function `generate_command` inside the _sipagrs.py_ module.
  - Look for the line `cmd = ["sofia_image_pipeline"]` 
  - Change the (str) _"sofia_image_pipeline"_ for the corresponding command used to run SIP on the device.

There is an additional dependency on the Ghostscript program. This is simply used to generate the final HTML report and convert some results from SoFiA-2, from .eps format to .png format. The latter has greater compatibility and can be viewed in any browser. To install it, simply use:

```
    $ apt-get install ghostscript
    or 
    $ brew install ghostscript
```

This is not a requirement, but ot is strongly recommend to install ESPADA in an isolated environment to avoid dependency conflicts. If you do not have a compatible version of Python installed, you can use pyenv and pyenv-virtualenv to manage Python versions and virtual environments.
You can install pyenv automatically with:

```
    $ curl https://pyenv.run | bash
```

Follow the instructions that this command outputs to add pyenv to your PATH (or copy the commands from https://github.com/pyenv/pyenv for your shell). Once configured, restart your terminal or reload your shell configuration:
```
    $ source ~/.bashrc
```
Install Python 3.10 and create a virtual environment for ESPADA:
```
    $ pyenv install 3.10
    $ pyenv virtualenv 3.10 adpalmap
    $ pyenv activate adpalmap
```
This will create an isolated virtual environment with the correct Python version.
To exit the virtual environment, run:
```
    $ pyenv deactivate
```

## Standard installation procedure

Installing ESPADA from this GitHub repository is fairly straightforward, the user simply needs to type these commands in the terminal:
```
  $ git clone https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git
  $ cd ADP-ALMA-Pipeline
  $ pip install -e .
```
This will install the pipeline in developer mode, which is recommended but not mandatory, and will download all available files from the repository, not just the Python-related ones. Alternatively, it can be run without the “-e” option, but be aware that some files may be missing which can lead to errors.


## Running ESPADA

The pipeline is initiated from a terminal command line with the command: 
```
$ adpalmap
```
Note that this functionality is only available if the instructions outlined above have been properly followed.  In that case, the pipeline will be installed as a command-line tool. Although the pipeline can still be executed with:

```
$ python adpalmap.py
```
this approach is strongly discouraged, as it may lead to import and environment inconsistencies. From this point onward, it will be assumed that the pipeline is executed using the installed command-line interface.

The `adpalmap` command will automatically search for the included default pipeline configuration file, *config.yaml*. However, the recommended usage is through the argument `"-c|$--$config-file"`:
```
$ adpalmap -c config_example.yaml
```
where *"config\_path.yaml"* is the user-defined configuration file, based on the default template.

## Available command line arguments

In addition to the aforementioned argument `"-c|$--$config-file"`, there are currently 6 other available arguments. These are explained below:

  - `"-cp|$--$config-parameters"`: Allows the user to modify the parameters, except for `input\_data\_set` within the *config.yaml* parameter file directly from the terminal. The required format is: `parameter=value`, with the restriction that no spaces are allowed between them. The parser will interpret any space as a new parameter and may fail. An example:
  ```
    $ adpalmap -c config.yaml -cp enable_tap_service=false input_file=Testing/espada_input_file.txt
    $ adpalmap -c config.yaml -cp num_cores=5
  ```

  - `"-sop|$--$sofia-parameters"`: Allows the user to modify any parameter within the SoFiA parameter file directly from the terminal. The required format is the same as when running SoFiA independently: `parameter=value`, with the restriction that no spaces are allowed between them. The parser will interpret any space as a new parameter and may fail. An example:
  ```
    $ adpalmap -c config.yaml -sop linker.radiusXY=2 pipeline.verbose=true
  ```
  Special care must be taken when using this option. ESPADA can be executed to search for emission, absorption—each with its own optimized parameter file—or both, and any parameter specified via the terminal will be applied to all SoFiA parameter files used during execution, which may lead to unintended effects. 
  Some parameters can not be modified in order to preserve the correct functioning of the pipeline; in such cases, a warning message will indicate that the provided value will be ignored.

  - `"-sarg|$--$sip-arguments"`: Similar to the previous option, this allows the user to modify any argument within the SIP parameter file directly from the terminal, with certain caveats. The general format consists of including the `-sarg` argument followed by the native SIP arguments: `-sarg -argument value`.
  Examples:
  ```
  $ adpalmap -c config.yaml --sip-arguments -i 0.15
  $ adpalmap -c config.yaml -sarg -i 0.15 
  $ adpalmap -c config.yaml -sarg -i 0.15 -m -o datacube.fits
  ```
  It is not possible to maintain the same format for all parameters both in the parameter file and via the terminal. For example, boolean parameters in *sip_args.yaml* accept True|False, whereas in the terminal only the corresponding argument should be included or omitted. Since it can be confusing in some cases, minimal use of this functionality is recommended. 
  One important aspect is that \textbf{other ESPADA arguments must not be used after this one}, as they will either be ignored or, in the worst case, the parser will attempt to parse them as parameters within `-sarg`, which may result in errors.  

  - `"-h|$--$help"`: A standard default argument that displays concise documentation on the pipeline and how to execute it easily. The command for its use is:
  ```
  $ adpalmap -h 
  $ adpalmap --help
  ```

  - `"-i|$--$info"`: Displays an additional layer of information about the configuration files and the individual parameters they contain. The format in this case depends on whether a file or a specific parameter is requested: `-i file=file\_name` or `-i parameter=parameter\_name`, where "file_name" and "parameter_name" can refer to any of the configuration files (using their default names) and any parameter contained within them, respectively. Some examples: 
  ```
  $ adpalmap -i file=config.yaml 
  $ adpalmap -i parameter=filename_must_include
  $ adpalmap --info parameter=make_report
  ```

  - `"$--$debug"`: This argument changes the logging level of the messages displayed both in the terminal and in the log files, enabling additional messages as well as the traceback in case of errors. The command is:
  ```
  $ adpalmap -c config.yaml --debug 
  ```
  It is worth noting that ESPADA includes an additional message logging level, beyond the Python standard, called RAW, which will also be displayed. 



## Configuration main file, 'config.yaml'

The pipeline runs using a configuration file named *config.yaml*, which is included by default in this repository and contains the essential parameters for its operation. These are:

###  **GENERAL**:
  - `quality_assessment`: If `True`, a quick and simple quality assessment of the data obtained with SoFiA will be performed. Type `<bool>`.
  - `verbose`: If `True`, it will capture all outputs from the external programs SoFiA and SIP. Type `<bool>`. It is generally recommended to leave this as `True`.
  - `num_cores`: Number of cores to use when running ADPALMAP. By default, all available cores will be used. If none or more cores than available on the device are specified, the maximum available cores will be used. Type <int>. The cores used in running SoFiA will then be dynamically adjusted based on the number of data sets and the maximum cores specified. See section below.

    #### Core allocation rules
    | Condition                      | Formula                                  |
    |--------------------------------|------------------------------------------|
    | User over-allocates cores      | \( $C_{\mathrm{available}} = C_{\mathrm{total}} $\) |
    | User under-allocates cores     | \( $C_{\mathrm{available}} = U $\)           |
    | Dataset ≤ Available Cores        | \( $W_{\mathrm{max}} = D,\ C_{\mathrm{per\_worker}} = \left\lfloor \frac{C_{\mathrm{available}}}{D} \right\rfloor$ \) |
    | Dataset > Available Cores        | \( $W_{\mathrm{max}} = C_{\mathrm{available}},\ C_{\mathrm{per\_worker}} = 1$ \) |

    $C_{\mathrm{total}}$: total CPU cores available  
    $U$: user-defined core limit  
    $D$: number of dataset to run in parallel  
    $C_{\mathrm{available}}$: adjusted core limit after validation  
    $W_{\mathrm{max}}$: maximum concurrent workers  
    $C_{\mathrm{per\_worker}}$: Cores allocated to each worker   


###  **INPUT DATA**:
  - `input_data_set`: Files Path to the data cube, primary Beam (optional) and mask (optional) where the pipeline will run. Available types are `<list>`, `<str>` or `<dict>`. 
  **Note**: Do not confuse the '||' symbol as part of the input, this is simply a separator in the examples.
    + As a `<list>`:   
      `input_data_set`: [data.fits, pb.fits, mask.fits] || [data.fits, "", mask.fits] || [data.fits, pb.fits] || [data.fits] || [data.fits, "", ""].
    + As a `<str>`:  
     `input_data_set`: data.fits pb.fits mask.fits|| data.fits, pb.fits, mask || data.fits, pb.fits mask || data.fits, "" mask || data.fits, "", mask || data.fits "", mask.fits || data.fits, "" ""
  
    **Be careful**: -data.fits, , mask.fits- is valid but it will be interpreter as: [data.fits, mask.fits, ''].
    + As a `<dict>`, for multiple data sets. All the previous rules are applied.   
    `input_data_set`:  
    1 : [data.fits, pb.fits, mask.fits]  
    2 : [data.fits, "", mask.fits]  
    3 : data.fits pb.fits mask.fits || data.fits, pb.fits, mask.fits || data.fits pb.fits, mask.fits  
    4 : data.fits  
    `input_data_set`: {   
    1 : [data.fits, pb.fits, mask.fits]  
    2 : [data.fits, "", mask.fits]  
    3 : data.fits pb.fits mask.fits || data.fits, pb.fits, mask.fits || data.fits pb.fits, mask.fits  
    4 : data.fits  
    }
    
  As an additional note, it will be assumed that the first, second (if any) and third (if any) files will always correspond to data, primary beam and mask, respectively.

  
  - `input_file`: Path to the text file (.txt, .lst, .dat) that includes all the Paths to each of the data sets on which to run the pipeline.
  Type `<str>`. 

    The required format for each line within the file is the same as for 'input_data_set', with the exception of the use of '[ ]'. The latter is not allowed, since when reading the file, the pipeline will not identify it as a Python 'list' but rather as a character within the filename, which will generate an error. Example of how lines should be entered into the file:

    1 : data.fits pb.fits mask.fits  
    2 : data1.fits pb1.fits mask1.fits  
    3 : data2.fits pb2.fits mask2.fits

###  **LOGGER**:
  - `log_file`: Name of the file where logger messages should be saved. Type `<str>`. Example: "adpalmap.log".
  - `clear_logs`: If `True`, clears the file where all logger entries will be written. This only works if the selected filename matches the name of the file from previous runs. Type `<bool>`.



###  **TAP SERVICE**:
  - `enable_tap_service`: If `True`, allows execution of the module `datap.py`, which downloads data from the ALMA archive based on parameters selected in the 'download_par_file'. Type `<bool>`.
  - `download_par_file`: Path (including filename) to the file containing desired parameters for downloading data from ALMA's archive. This file is included by default in this repository under the name 'download_par.yaml'. Type `<str>`. The parameters within this file are explained in the Download parameter file section. NOTE: If downloading files is chosen, by default, the program will use these downloaded files and ignore those selected in INPUT DATA.

###  **SOFIA**:
  - `enable_sofia`: If `True`, allows execution of the module `sofia.py`, which uses external SoFiA software. Type `<bool>`.
  - `run_mode`: Indicates the type of emission that SoFiA should search for in the selected data cube. Available modes are 'emission', 'absorption', and 'both'. If 'both' is selected, SoFiA will first search for absorptions and then run again to search for emissions. See description of 'abs_flag_cube' parameter for more details. Type `<str>`.
  - `use_pb`: If `True` will use the primary beam file(s) (if any) to run SoFiA. If `False` will NOT use it. No matter if it was indicate in the 'input_dataset' or 'input_file' parameters. Type `<bool>`.
  - `use_mask`: If `True` will use the mask file(s) (if any) to run SoFiA. If `False` will NOT use it. No matter if it was indicate in the 'input_dataset' or 'input_file' parameters. Type `<bool>`.
  - `abs_flag_cube`: If `True`, uses the mask obtained during SoFiA's first run in 'both' mode (i.e., absorption) as a flag mask for emission searches. Type `<bool>`.
  - `auto_setup`: If `True`, adjusts certain SoFiA parameters based on specific keywords found in data cube headers. Type `<bool>`.
  - `sofia_abs_file`: Path (including filename) to a file containing parameters necessary for running SoFiA to search for absorptions. Type `<str>`.
  - `sofia_emi_file`: Path (including filename) to a file containing parameters necessary for running SoFiA to search for emissions. Type `<str>`.

    **NOTE**: If desired, parameters can be changed via the terminal using the command `-sop|--sofia-parameters <parameter>=<value>` in the same way as running SoFiA in isolation. As mentioned, the three parameters above will follow the explained logic and will be ignored as appropriate.

    **NOTE**: During the execution of SoFiA there are multiple steps where various parameters specified in the files specified in sofia_abs_file and sofia_emi_file can potentially be changed. For simplicity and to better track these in the logger, for both files (if applicable) a temporary file is created consisting of: {filename}\_{tmp}\_{PID}.par, where PID indicates the PID of the specific process where SoFiA2 is running.

    **NOTE**: the name set in the 'output.directory' parameter will always be rewritten by adding '_emssion' or 'absorption' depending on the run mode.

    **NOTE**: Certain specific SoFiA parameters conflict with ADPAlmaP's workflow:
    - **'input.data', 'input.primaryBeam' and 'input.mask'**: These parameters are always ignored when specified within the SoFiA parameter files. Instead, the pipeline uses the corresponding values defined in `config.yaml` or those retrieved via `download_par.yaml`. A warning message will notify the user that these parameters are being overridden.
    - **'input.invert'**: This parameter is ignored. If there is a conflict between the selected run mode and the value defined either in the parameter files or provided through the -sop comand in the terminal, a warning will be issued. 

    **NOTE**: The parameter files for both absorption and emission available in the repository are "optimized" to work with most ALMA data cubes in band 3.




###  **SIP**:
  - `'enable_sip'`: If `True`, allows the execution of the `sipar.py` module, which uses the external SIP software. Type `<bool>`.
  - `'sip_par_file'`: Path (including filename) to the file containing the parameters necessary to run SIP. Type `<str>`.

    **NOTE:** The implementation of a parameter file for SIP has been chosen for user convenience and to maintain ADPAlmaP's modular logic. If desired, arguments can be specified via the terminal using the command `-sarg|--sip-arguments <-command value>`. <font color="red">¡Be careful!</font> after the SIP arguments you cannot include SoFiA parameters via -sop, these will be directly ignored.
    Example: `-sarg -c catalog.xml -i 0.15 -m`. 

    **NOTE:** The argument `-c|--catalog` will only be necessary if the module responsible for running SoFiA is disabled; otherwise, this parameter will be ignored, and the newly obtained catalog from SoFiA will be used.
    If we are in the case mentioned and the number of datasets we are going to use is strictly greater than 1, this parameter must contain a list of catalogs, one for each dataset.

###  **GROUP**:

  - `enable_sofia`: If `True`, allows execution of the module `group.py`. This module is responsible for grouping different sources detected in SoFiA that are actually the same. It then runs SoFiA and SIP again in the same selected mode with the newly grouped sources.Type `<bool>`.

  - `overlap_mode`: Indicates the type of overlap that should be performed on the sources found by SoFiA for the selected `run_mode`. Available modes are 'flux', 'absflux' or 'area'. Type `<str>`.

  - `overlap_threshold`: Set the limit applied to the 'overlap_mode' selected. Must be a number between 0 and 1. Type `<float>`.  


## Download Parameter File

### **SERVER**:
- `'server_address'`: The archive service to use. Type `<str>`. By default, the server address is set to 'ESO'. URL options for querying data include:
  - 'ESO' Europe (`https://almascience.eso.org`)
  - 'NRAO' North America (`https://almascience.nrao.edu`)
  - 'NAOJ' East Asia (`https://almascience.nao.ac.jp`)

- `'credentials'`: If set to `True` enable login to ALMA's TAP service using your own credentials. Type `<bool>`.
- `'stored_credentials'`: If set to `True` save credentials in cache memory for subsequent pipeline runs, so re-entering credentials won't be necessary. Type `<bool>`.

---

### **QUERY**:

Requesting data from the archive is done through what is known as a Query, which uses ADQL language. Since we assume this language is not commonly used in the community, we have predefined certain types of queries to simplify its use. To do this, we have extracted part of the external software ALminer and included it within ADPALMAP.

Each query consists of two essential parts: the query type, indicated with the `'query_type'` parameter, and the parameters used for this query, indicated within the `'query_par'` parameter.
Within `query_par`, there are two types of parameters: essential and specific to each query type, which are included and commented out in the default *download_par.yaml* file included in the repository; and the parameters common to all types, which appear below.

- `'query_type'`: The available predefined types are: `'proposal'`, `'conesearch'`, `'target'`, `'keysearch'`, and `'free'`. The specific parameters for each type of query are listed below:
  - `'proposal'`:
    - **proposal_id**: Type `<str>`.
  - `'conesearch'`:
    - **ra**: Type `<float>`.
    - **dec**: Type `<float>`.
    - **search_radius**: Type `<float>`.
  - `'target'`:
    - **sources**. Type `<str>`.
    - **search_radius**: Type `<float>`.
  - `'keysearch'`:
    - **search_dict**: Type `<dict>`.
  - `'free'`:
    - **query_str**: Type `<str>`. This option is for more advanced users familiar with ADQL language who can write their own queries.  

**NOTE**: To use parameters specific to a specific query type, make sure that the other specific parameters are not included. For convenience and to avoid possible future oversights, it is recommended to simply comment them out.

In addition to specific parameters for each query type, certain common parameters are required:
  - `common parameters`:
    - **point**: Type `<bool>`.
    - **public**: Type `<bool>`.
    - **published**: Type `<bool>`.
    - **print_targets**: Type `<bool>`.
    - **print_query**: Type `<bool>`.

Examples:
```yaml
query_type: 'proposal'   
query_par: 
  proposal_id: '2016.1.00778.S'   
  point: False   
  public: True  
  published: None  
  print_targets: True   
  print_query: True  
```

```yaml
query_type: 'target'
query_par:
  sources: ['V605 Aql']
  search_radius: 2.
  point: False   
  public: True  
  published: None  
  print_targets: True   
  print_query: True 
```

```yaml
query_type: 'keysearch'
query_par:
  search_dict: {'target_name':['G31.41'], 'proposal_id': ['2018']}
  point: False   
  public: True  
  published: None  
  print_targets: True   
  print_query: True 
```

```yaml
query_type: 'free'   
query_par: 
  query_str: *"SELECT * FROM ivoa.obscore WHERE ((LOWER(proposal_abstract) LIKE '%planet-forming disk%')) AND (spatial_resolution < 0.5) AND (LOWER(data_rights) LIKE '%public%') AND (LOWER(scan_intent) LIKE '%target%') ORDER BY proposal_id"*
    point: False   
    public: True  
    published: None  
    print_targets: True   
    print_query: True 
```
---

### **PARAMETERS**:
- `'download_par'`:

  - **data_dir**: Path of the directory where downloaded data should be placed. Type `<str>`.
  - **fitsonly**: If `True`, download individual FITS files only. This option will not download raw data. Type `<bool>`.
  - **remove_compressed_file**: If `True`, remove compressed files. This applies to primary beam cubes in the ALMA archive. Type `<bool>`.
  - **remove_archive_mask**: If `True`,  delete the original mask files from the archive with float type values in the cube. This it is done because at some point the mask must be transformed into int value type values to be valid for SoFiA .Type `<bool>`.
  - **dryrun**: If `True`, allows users to perform a test run to check file size and number before downloading data. Type `<bool>`.
  - **print_urls**: If `True`, writes a list of URLs to be downloaded from the archive to the terminal. Type `<bool>`.
  - **filename_must_include**: A list of strings that must be included in the URL filename. Useful for filtering downloads further, such as data corrected for primary beams ('.pbcor') or specific science targets or calibrators (by including their names). Choices depend on reduction type and cycle. Example:  *['A001_X133d_X4226.COSMOS-1189669_sci.spw25.cube']*.  
    Type `<list>`.



## Typical errors

- `Old version of python`: It is common for the Python version installed and used by default on your operating system to be 3.8 or older. If it your case and you have not followed the instructions above to created a virtual environment with the minimum required version (3.10), some parts of the code will not work.

## Acknowledgements.

Part of the code from the ALMA Archive Mining & Visualization Toolkit (`alminer`, https://github.com/emerge-erc/ALminer.git) [^1] software has been used and suitably adapted.
[^1]: `alminer` has been developed through a collaboration between Allegro, the ALMA Regional Centre in The Netherlands, and the University of Vienna as part of the EMERGE-StG project. This project has received funding from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (Grant agreement No. 851435).


