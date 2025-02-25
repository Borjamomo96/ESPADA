
# ADP ALMA Pipeline

## Requirements

This code has been developed and tested (not yet) with Python 3.10.15.

This pipeline makes use of the external programs Source Finding Application (SoFiA) and SoFiA Image Pipeline (SIP). Therefore, it is necessary to have both software installed on your system beforehand. To install these programs, we strongly recommend reading their respective documentation in the repositories:

(https://gitlab.com/SoFiA-Admin/SoFiA-2)  
(https://github.com/kmhess/SoFiA-image-pipeline)

Additionally, part of the code from the ALMA Archive Mining & Visualization Toolkit (ALMINER) software has been used and suitably adapted. Since this software uses the Astropy package, it must also be installed beforehand.

---

## Configuration master file, 'config.yaml'

The pipeline runs using a configuration file named *config.yaml*, which is included by default in this repository and contains the essential parameters for its operation. These are:

###  **GENERAL**:
  - `quality_assessment`: If `True`, a quick and simple quality assessment of the data obtained with SoFiA will be performed. Type `<bool>`.
  - `capture_outputs`: If `True`, it will capture all outputs from the external programs SoFiA and SIP. Type `<bool>`. It is generally recommended to leave this as `False`.

###  **INPUT DATA**:
  - `input_data`: Path (including the filename) to the data cube where the pipeline will run. Type `<str>`.
  - `input_data_list`: NOT YET IMPLEMENTED. This means that for now, if you want to download more than one data cube at a time from the ALMA archive, the pipeline will only take the most recent one. See description below.

###  **LOGGER**:
  - `log_file`: Name of the file where logger messages should be saved. Type `<str>`. Example: "adpalmap.log".
  - `clear_logs`: If `True`, clears the file where all logger entries will be written. This only works if the selected filename matches the name of the file from previous runs. Type `<bool>`.

###  **TAP SERVICE**:
  - `enable_tap_service`: If `True`, allows execution of the module `datap.py`, which downloads data from the ALMA archive based on parameters selected in the 'download_par_file'. Type `<bool>`.
  - `download_par_file`: Path (including filename) to the file containing desired parameters for downloading data from ALMA's archive. This file is included by default in this repository under the name 'download_par.yaml'. Type `<str>`. The parameters within this file are explained in the Download parameter file section. NOTE: If downloading files is chosen, by default, the program will use these downloaded files and ignore those selected in INPUT DATA.

###  **SOFIA**:
  - `enable_sofia`: If `True`, allows execution of the module `sofia.py`, which uses external SoFiA software. Type `<bool>`.
  - `run_mode`: Indicates the type of emission that SoFiA should search for in the selected data cube. Available modes are 'emission', 'absorption', and 'both'. If 'both' is selected, SoFiA will first search for absorptions and then run again to search for emissions. See description of 'abs_flag_cube' parameter for more details. Type `<str>`.
  - `abs_flag_cube`: If `True`, uses the mask obtained during SoFiA's first run in 'both' mode (i.e., absorptions) as a flag mask for emission searches. Type `<bool>`.
  - `auto_setup`: If `True`, adjusts certain SoFiA parameters based on specific keywords found in data cube headers. Type `<bool>`.
  - `sofia_abs_file`: Path (including filename) to a file containing parameters necessary for running SoFiA to search for absorptions. Type `<str>`.
  - `sofia_emi_file`: Path (including filename) to a file containing parameters necessary for running SoFiA to search for emissions. Type `<str>`.

    **NOTE**: Certain specific SoFiA parameters conflict with ADPAlmaP's workflow:
    - **'input.data'**: Always ignored within SoFiA's parameters; instead, it uses those selected in *config.yaml* or downloaded via 'download_par.yaml'. A warning will indicate that it is being ignored.
    - **'input.invert'**: Ignored, with warnings displayed if there is a conflict between selected mode and value in parameter files or terminal input.
    - **'input.primaryBeam'**: Ignored only if downloading files via TAP service is enabled; otherwise, downloaded files are used if specified in 'download_par.yaml'. 

    **NOTE**: The parameter files for both absorption and emission available in the repository are "optimized" to work with most ALMA data cubes in band 3.

    **NOTE**: If desired, parameters can be changed via the terminal using the command `-sop|--sofia-parameters <parameter>=<value>` in the same way as running SoFiA in isolation. As mentioned, the three parameters above will follow the explained logic and will be ignored as appropriate.


###  **SIP**:
  - `'enable_sip'`: If `True`, allows the execution of the `sipar.py` module, which uses the external SIP software. Type `<bool>`.
  - `'sip_par_file'`: Path (including filename) to the file containing the parameters necessary to run SIP. Type `<str>`.

    **NOTE:** The implementation of a parameter file for SIP has been chosen for user convenience and to maintain ADPAlmaP's modular logic. If desired, arguments can be specified via the terminal using the command `-sarg|--sip-arguments <-command value>`. <font color="red">¡Be careful!</font> after the SIP arguments you cannot include SoFiA parameters via -sop, these will be directly ignored.
    Example: `-sarg -c catalog.xml -i 0.15 -m`. 

    **NOTE:** The argument `-c|--catalog` will only be necessary if the module responsible for running SoFiA is disabled; otherwise, this parameter will be ignored, and the newly obtained catalog from SoFiA will be used.




## Download Parameter File

### **SERVER**:
- `'server_address'`: The archive service to use. Type `<str>`. By default, the server address is set to 'ESO'. URL options for querying data include:
  - 'ESO' Europe (`https://almascience.eso.org`)
  - 'NRAO' North America (`https://almascience.nrao.edu`)
  - 'NAOJ' East Asia (`https://almascience.nao.ac.jp`)

- `'credentials'`: If `True`, allows you to log in to ALMA's TAP service with your credentials. Type `<bool>`.
- `'stored_credentials'`: If `True`, saves credentials in cache memory for subsequent pipeline runs, so re-entering credentials won't be necessary. Type `<bool>`.

---

### **QUERY**:
- `'query_type'`: Requesting data from the archive is done through what is known as a Query, which uses ADQL language. To simplify usage, there are predefined query types: `'proposal'`, `'conesearch'`, `'target'`, `'keysearch'`, and `'free'`. Each requires specific parameters:
  - `'proposal'`:
    - **proposal_id**. Type `<str>`.
  - `'conesearch'`:
    - **ra**. Type `<float>`.
    - **dec**. Type `<float>`.
    - **search_radius'`. Type `<float>`.
  - `'target'`:
    - **sources**. Type `<str>`.
    - **search_radius**. Type `<float>`.
  - `'keysearch'`:
    - **search_dict**. Type `<dict>`. Example: *{"proposal_abstract": ["high-mass star formation outflow disk"]}*.
  - `'free'`:
    - **query_str**. Type `<str>`. This option is for more advanced users familiar with ADQL language who can write their own queries. Example:  
      *"SELECT * FROM ivoa.obscore WHERE ((LOWER(proposal_abstract) LIKE '%planet-forming disk%')) AND (spatial_resolution < 0.5) AND (LOWER(data_rights) LIKE '%public%') AND (LOWER(scan_intent) LIKE '%target%') ORDER BY proposal_id"*

In addition to specific parameters for each query type, certain common parameters are required:
  - `'point'`. Type `<bool>`.
  - `'public'`. Type `<bool>`.
  - `'published'`. Type `<bool>`.
  - `'print_targets'`. Type `<bool>`.
  - `'print_query'`. Type `<bool>`.

---

### **PARAMETERS**:
- `'download_par'`:
  - **fitsonly**: If `True`, download individual FITS files only. This option will not download raw data. Type `<bool>`.
  - **include_pb**: If `True`, download all `.pb.` files (i.e., all primary beam cubes) without distinction among science cubes. Type `<bool>`.
  - **remove_uncompress_file**: If `True`, removes uncompressed files. This applies to primary beam cubes in the ALMA archive. Type `<bool>`.
  - **dryrun**: If `True`, allows users to perform a test run to check file size and number before downloading data. Type `<bool>`.
  - **print_urls**: If `True`, writes a list of URLs to be downloaded from the archive to the terminal. Type `<bool>`.
  - **filename_must_include**: A list of strings that must be included in the URL filename. Useful for filtering downloads further, such as data corrected for primary beams ('.pbcor') or specific science targets or calibrators (by including their names). Choices depend on reduction type and cycle. Example:  *['A001_X133d_X4226.COSMOS-1189669_sci.spw25.cube']*.  
    Type `<str>`.

  - **data_dir**: Path of the directory where downloaded data should be placed. Type `<str>`.


## Typical errors

- `Old version of python`: It is common to use Python 3.8, however, during the pipeline features that are only available are used, such as using "|" instead of ".union()" to define, for example, several possible types of a variable.




