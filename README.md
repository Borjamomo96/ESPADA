
# ADP ALMA Pipeline

ADPAlmaP is a wrapper for the software (ALminer, SoFiA2 and SIP) designed to obtain advanced ALMA data products.

## Requirements

This code has been developed and tested (not yet) with Python 3.10.15.

This pipeline makes use of the external programs Source Finding Application (SoFiA) and SoFiA Image Pipeline (SIP). Therefore, it is necessary to have both software installed on your system beforehand. To install these programs, we strongly recommend reading their respective documentation in the repositories:

(https://gitlab.com/SoFiA-Admin/SoFiA-2)  
(https://github.com/kmhess/SoFiA-image-pipeline)

Additionally, part of the code from the ALMA Archive Mining & Visualization Toolkit (ALMINER, https://github.com/emerge-erc/ALminer.git) software has been used and suitably adapted.

**Warning**: ADPALMAP makes use of the subprocess module to run external software such as SoFiA and SIP. To run each software, the subprocess module needs to know the command to call each one, which is not possible to know a priori. It is recommended to install both SoFiA and SIP according to the authors' recommendations so that both are executed when called from the terminal as: `sofia` and `sofia_image_pipeline` respectively.

_Alternatively (not recommended option, under user responsibility)_: the corresponding line of code where each software is executed can be changed. To do this:

  - Look for the function `run_sofia` inside the _sopar.py_ module. 
  - Inside each function, look for the lines `cmd = ["sofia", f"{temp_file_path}"]` in each of the if blocks corresponding to each of the usage modes. 
  - Change the (str) _"sofia"_ for the corresponding command used to run SoFiA on the device.

  - Look for the function `generate_command` inside the _sipagrs.py_ module.
  - Look for the line `cmd = ["sofia_image_pipeline"]` 
  - Change the (str) _"sofia_image_pipeline"_ for the corresponding command used to run SIP on the device.
---

## Installation

**DISCLAIMER**: The steps provided here are RECOMMENDATION only, there may be other ways to install ADP Alma Pipeline that will also work.

We recommend installing ADP Alma pipeline in an isolated environment as described below. 

ADPALMAP requires Python 3.10 or later, If you don't have Python 3.10 or later, you can install pyenv and pyenv-virtualenv, which will manage python versions for you. You can use the automatic installer pyenv-installer:

```
    $ curl https://pyenv.run | bash
```

Follow the instructions that this command outputs to add pyenv to PATH (or copy the commands from https://github.com/pyenv/pyenv for your shell). Restart your terminal, or source the file (e.g. . ~/.bashrc or . ~/.zshrc) Then, run:

```
    $ pyenv install 3.10
    $ pyenv virtualenv 3.10 adpalmap
    $ pyenv activate adpalmap
```

Now you will have a virtual environment with the right Python version, and you can continue with the next step. To deactivate, just run `pyenv deactivate`.

With the environment activated, download this repository and install ADPALMAP:
```
  $ git clone https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git
  $ cd ADP-ALMA-Pipeline
  $ pip install -e .
```
This will install it in developer mode, alternatively you can simply install it with `pip install .`.

As mentioned, ADPALMAP uses the external software SoFiA2 and SIP, which must be able to run within the newly created environment by issuing the commands `sofia` and `sofia_image_pipeline`, respectively, in the terminal. See "Requirements" for details.


## Running ADPAlmaP

If you have followed the instructions mentioned above, you can now run the pipeline as if it were a module with the command:
```
$ adpalmap
```
If, on the other hand, you have followed an alternative path and it is not yet a module, the pipeline can be run as a script:

```
$ python adpalmap.py
```
From now on, it will be assumed that it will be run as a module.

The pipeline runs using a configuration file named *config.yaml*, which is explained in detail in the next section. Unless otherwise specified, the pipeline will attempt to use the 'config.yaml' file that is found by default when cloning the repository. If this file is moved to another directory or a different one is to be used, an equivalent file must be specified per terminal using the '-c|--config-file' argument:
```
$ adpalmap -c config_example.yaml
```
The pipeline also has two other arguments, '-sop|--sofia-parameters' and '-sarg|--sip-arguments', which are used to enter the SoFiA2|SIP parameters|arguments, just as they would be if they were run in isolation, respectively. The following sections provide more details about their usage. Example:
```
$ adpalmap -sop contsub.threshold=3.0 linker.radiusXY=3 -sarg -i 0.15

```


## Configuration master file, 'config.yaml'

The pipeline runs using a configuration file named *config.yaml*, which is included by default in this repository and contains the essential parameters for its operation. These are:

###  **GENERAL**:
  - `quality_assessment`: If `True`, a quick and simple quality assessment of the data obtained with SoFiA will be performed. Type `<bool>`.
  - `capture_outputs`: If `True`, it will capture all outputs from the external programs SoFiA and SIP. Type `<bool>`. It is generally recommended to leave this as `False`.
  - `num_cores`: Number of cores to use when running ADPALMAP. If none or more cores are specified, all available cores on the device are used. Type <int>. The cores used in running SoFiA will then be dynamically adjusted based on the number of data sets and the maximum cores specified. See section below.

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
  **Note**: Do not confuse the '||' symbol as part of the input, this is simply a separator
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
  - `abs_flag_cube`: If `True`, uses the mask obtained during SoFiA's first run in 'both' mode (i.e., absorptions) as a flag mask for emission searches. Type `<bool>`.
  - `auto_setup`: If `True`, adjusts certain SoFiA parameters based on specific keywords found in data cube headers. Type `<bool>`.
  - `sofia_abs_file`: Path (including filename) to a file containing parameters necessary for running SoFiA to search for absorptions. Type `<str>`.
  - `sofia_emi_file`: Path (including filename) to a file containing parameters necessary for running SoFiA to search for emissions. Type `<str>`.

    **NOTE**: During the execution of SoFiA there are multiple steps where various parameters specified in the files specified in sofia_abs_file and sofia_emi_file can potentially be changed. For simplicity and to better track these in the logger, for both files (if applicable) a temporary file is created consisting of: {filename}\_{tmp}\_{PID}.par, where PID indicates the PID of the specific process where SoFiA2 is running.

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
    If we are in the case mentioned and the number of datasets we are going to use is strictly greater than 1, this parameter must contain a list of catalogs, one for each dataset.




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

- `Old version of python`: It is common for the Python version installed and used by default on your operating system to be 3.8 or older. If it your case and you have not followed the instructions above to created a virtual environment with the minimum required version (3.10), some parts of the code will not work.




