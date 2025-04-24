import re
import numpy as np
import gzip
import shutil
import re
import os
import sys
import pandas as pd
from pathlib import Path
import yaml

# astropy
from astropy.coordinates import Angle
from astropy.coordinates import get_icrs_coordinates
from astropy.coordinates import name_resolve
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy import constants as const
import io
from contextlib import redirect_stdout

# Astroquery is required
from astroquery.alma import Alma

# Python Virtual Observatory
import pyvo
from pyvo.dal import tap

# Logger:
from adplib.logger import Logger
logger = Logger.get_logger()


VALID_KEYWORDS_STR = ('obs_publisher_did', 'obs_collection', 'facility_name', 'instrument_name', 
                      'obs_id', 'dataproduct_type', 'target_name', 's_region', 'pol_states', 'o_ucd',
                      'band_list', 'authors', 'pub_abstract', 'proposal_abstract', 'schedblock_name',
                      'proposal_authors', 'group_ous_uid', 'member_ous_uid', 'asdm_uid', 'obs_title',
                      'type', 'scan_intent', 'science_observation', 'antenna_arrays', 'is_mosaic',  
                      'obs_release_date', 'frequency_support', 'obs_creator_name', 'pub_title',
                      'first_author', 'qa2_passed', 'bib_reference', 'science_keyword', 
                      'scientific_category', 'lastModified', 'access_url', 'access_format',
                      'proposal_id', 'data_rights')


def capture_output(input):
    
    f = io.StringIO()  
    with redirect_stdout(f):  
        input
    output = f.getvalue()
    Logger.raw(output)

def get_segment(path):
    # Busca 'spw' + dígitos + punto literal (\.)
    match = re.search(r'spw\d+\.', path)
    return path[:match.end()] if match else ''


class datap(dict): 

    def __init__(self, **kwargs):
        """
        Reads the tap_parameters file and creates a datap object.
        
        Parameters
        ----------
        config_path: str, default None
            Path to the configuration file. If None, it will display an error.

        Returns
        -------
        self

        Attributes
        ----------
        Different parameters such as database, path, log format, server
        for data download from remote sources, etc.
        """

        #CHANGE. This is not needs in this class. This would be if additional par=val 
        # beyond the path is required, e.g datap('path', condition=True, const=1). These extra par
        #will be storage as a attr as well. 
        super(datap, self).__init__(**kwargs)
        #This line set the keys of the previous key=val pair introduce through **kwargs as 
        # attributes of the class as well.
        self.__dict__ = self 
        self.configure(**kwargs)

        #Check the parameter for the query type before continue:
        self.check_query_par()
        #Chech the parameter in download_par expect query_type:
        self.check_download_par()

        #Initialize Alma() instance. <Attribute>
        self.alma = Alma()

        
        if self.credentials:

            print("Introduce your ALMA credentials: ")
            username = input("- Username: ")
    
            try:
                self.alma.login(username, store_password=self.stored_credentials)
            
            except Exception as e:
                print(f"Error en la autenticación: {e}")

        #Initialize the archive service to use for the download
        self.alma.archive_url = self.server_address

        #This may become a function. FUNCTION
        self._service = tap.TAPService(f"{self.server_address}/tap")


    def configure(self, download_path=None, **kwargs):

        #Esta condición nunca se considera. La clase no se inicializa si el parámetro -d no se usa 
        # (None por defecto). Si es not None pasa a las siguiente, por lo que es código que no 
        # se usa. REMOVE

        if download_path is None:
            
            script_dir = Path(__file__).parent
            download_path = script_dir / "download_par.yaml"
            self.download_path = download_path

            if not download_path.exists():
                raise FileNotFoundError(
                    f"Download file '{download_path}' not found. Checked if the "
                    "'tap/download_par.yaml' has been deleted or the structure has changed. "
                    "See README for further details."
                )
            else:
                logger.info(f"The file in '{download_path}' have been loaded successfully")

        else:
            download_path = Path(os.path.expanduser(download_path))
            self.download_path = download_path

            if not download_path.exists():
                raise FileNotFoundError(f"Download file '{download_path}' not found.")
            else:
                logger.info(f"The file in '{download_path}' have been loaded successfully")

            
        with open(download_path, 'r') as f:
            download_dict = yaml.safe_load(f)
        
        for k, v in download_dict.items():
            setattr(self, k, v)


    def _get_metadata(self):

        """
        Retrieve metadata from the TAP service and return it as a pandas DataFrame.
        """
    
        metadata_query = (
            "SELECT column_name, datatype, unit, ucd, utype, description "
            "FROM TAP_SCHEMA.columns"
        )       
        TAP_metadata = self._service.search(metadata_query)

        return pd.DataFrame(TAP_metadata).set_index('column_name')


    def _format_bytes(self, size):
        """
        Convert the size of the dota to be downloaded in human-readable format.
        """

        power = 1000
        n = 0
        power_labels = {0 : 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB', 5: 'PB', 6: 'EB'}
        while size > power:
            size /= power
            n += 1
        return size, power_labels[n]


    def download_data(self, observations):
        """
        Download ALMA data from the archive to a given directory.

        Parameters
        ----------
        observations : pandas.DataFrame
                This is likely the output of e.g. 'conesearch', 'target', 'catalog', & 'keysearch' 
                functions.

        fitsonly : bool, optional
            (Default value = False)
            Download individual fits files only (fitsonly=True). This option will not download the 
            raw data (e.g. 'asdm' files), weblogs, or README files.

        dryrun : bool, optional
            (Default value = False)
            Allow the user to do a test run to check the size and number of files to download without
            actually downloading the data (dryrun=True). To download the data, set testrun=False.

        print_urls : bool, optional
            (Default value = False)
            Write the list of urls to be downloaded from the archive to the terminal.

        filename_must_include : list of str, optional
            (Default value = '')
            A list of strings the user wants to be contained in the url filename. This is useful 
            to restrict the download further, for example, to data that have been primary beam 
            corrected ('.pbcor') or that have the science target or calibrators (by including 
            their names). The choice is largely dependent on the cycle and type of reduction that
            was performed and data products that exist on the archive as a result. In most recent 
            cycles, the science target can be filtered out with the flag '_sci' or its ALMA target 
            name.

        data_path : str, optional
            (Default value = ./archive_data)
            The directory where the downloaded data should be placed.
        """

        Logger.raw("================================")
        #CHANGE. Definir asi el directorio puede provocar problemas
        default_location = './archive_data'
    
        
        #Check the input Dataframe
        
        #case where the DataFrame is empty.
        try:
            if any(observations['data_rights'] == 'Proprietary'):
                logger.warning("Some of the data you are trying to download are still in the "
                               "proprietary period and are not publicly available yet.")
                observations = observations[observations['data_rights'] == 'Public']

            uids_list = observations['member_ous_uid'].unique()
            # when len(uids_list) == 0, it's because the DataFrame included only proprietary 
            # data and we removed them in the above if statement, so the DataFrame is now empty

            if len(uids_list) == 0:
                logger.error("No data to download. Check the input DataFrame. It is likely that "
                             "your query results include only proprietary data which cannot be "
                             "freely downloaded.")
                sys.exit(-1)
            
        # this is the case where the query had no results to begin with.
        except TypeError:
            logger.error("No data to download. Check the input DataFrame.")
            sys.exit(-1)

        if self.download_par['data_dir'] is None:
            #La función alma.cache_location ya crea el directorio con el nombre en cuestión. 
            self.alma.cache_location = default_location
        else:
            if not os.path.exists(Path(self.download_par['data_dir'])):
                self.alma.cache_location = self.download_par['data_dir']
            else:
                logger.warning(f"The directory '{self.download_par['data_dir']}' already exits."
                               " The data from the archive wiil be storaged in this directory.")
                self.alma.cache_location = self.download_par['data_dir']
        
    
        #Fits only and phrase within the file to download
        if self.download_par['fitsonly']:
            
            data_table = self.alma.get_data_info(uids_list, expand_tarfiles=True)
            
            # filter the data_table and keep only rows with "fits" in 'access_url' and the strings 
            # provided by user in 'filename_must_include' parameter
            
            if self.download_par['include_pb']:
                dl_table = data_table[
                    [i for i, v in enumerate(data_table['access_url'])
                    if ((v.endswith(".fits") or ".pb." in v) and
                        all(fmi in v for fmi in self.download_par['filename_must_include']))]
                ]
            else:
                dl_table = data_table[
                    [i for i, v in enumerate(data_table['access_url'])
                    if (v.endswith(".fits") and
                        all(fmi in v for fmi in self.download_par['filename_must_include']))]
                ]

        else:
            data_table = self.alma.get_data_info(uids_list, expand_tarfiles=False)
            # filter the data_table and keep only rows with "fits" in 'access_url' and the strings 
            # provided by user in 'filename_must_include' parameter
            if self.download_par['include_pb']:
                dl_table = data_table[
                    [i for i, v in enumerate(data_table['access_url'])
                    if (".pb." in v) and
                    all(fmi in v for fmi in self.download_par['filename_must_include'])]
                ]
            else:
                dl_table = data_table[
                    [i for i, v in enumerate(data_table['access_url'])
                    if all(fmi in v for fmi in self.download_par['filename_must_include'])]
                ]
        
        dl_df = dl_table.to_pandas()
        # remove empty elements in the access_url column
        dl_df = dl_df.loc[dl_df.access_url != '']
        dl_link_list = list(dl_df['access_url'].unique())
        # keep track of the download size and number of files to download
        dl_size = dl_df['content_length'].sum()
        dl_files = len(dl_df['access_url'].unique())
        dl_uid_list = list(dl_df['ID'].unique())


        if self.download_par['dryrun']:
            logger.info("This is a dryrun. To begin download, set dryrun=False.")
            Logger.raw("================================")
            

        else:
            logger.info("Starting download. Please wait...")
            Logger.raw("================================")


            try:
                self.alma.download_files(dl_link_list, cache=True)

            except ValueError as e:
                logger.error(e)


        if dl_files > 0:
            logger.info("Download location = {}".format(self.alma.cache_location))
            logger.info("Total number of Member OUSs to download = {}".format(len(dl_uid_list)))
            logger.info("Selected Member OUSs: {}".format(dl_uid_list))
            logger.info("Number of files to download = {}".format(dl_files))
            dl_size_fmt, dl_format = self._format_bytes(dl_size)
            logger.info("Needed disk space = {:.1f} {}".format(dl_size_fmt, dl_format))

            
            if self.download_par['print_urls']:
                logger.info("File URLs to download: ")
                for url in dl_link_list:
                    Logger.raw(f"{url}") 
                
        else:
            logger.warning("Nothing to download.")
            print(
                "Note: often only a subset of the observations (e.g. the representative window)" 
                "is ingested into the archive. In such cases, you may need to download the raw "
                "dataset, reproduce the calibrated measurement set, and image the observations "
                "of interest. It is also possible to request calibrated  measurement sets through"
                " a Helpdesk ticket to the European ARC (see "
                "https://almascience.eso.org/local-news/requesting-calibrated-measurement-sets-in-europe)."
                "Alternatively, check the filename_must_include parameter, there is probably a "
                "syntax error or very restrictive conditions."
                )
            sys.exit(-1)
        
        
        
        if self.download_par['dryrun']:
            sys.exit(-1)

        #Set Attr data locations of the just downloaded data
        self.get_downloaded_file_path(Path(self.alma.cache_location), dl_link_list)
        Logger.raw("================================")
        logger.info("Data download ended.")
        Logger.raw("================================")


    def download_mask(self, observations):
        """
        Download mask files for the given observations from the ALMA archive.

        This method filters the provided observations to include only public data (if any 
        proprietary data is present, it is excluded). It retrieves the unique `member_ous_uid` 
        identifiers, queries the ALMA archive for available mask files, and downloads them. 
        The downloaded files are stored in the cache location specified by the ALMA service.

        Parameters:
        ----------
        observations (pandas.DataFrame): A DataFrame containing observation metadata, including 
                                        a `data_rights` column to filter public data and a 
                                        `member_ous_uid` column to identify unique datasets.

        Returns:
        ----------
        None

        Raises:
        ----------
        SystemExit: If an internal error occurs while processing the observations or querying 
                    the archive.
        ValueError: If an error occurs during the file download process.
        """

        try:
            if any(observations['data_rights'] == 'Proprietary'):
                #logger.warning("Some of the data you are trying to download are still in the 
                # proprietary period and are not publicly available yet.")
                observations = observations[observations['data_rights'] == 'Public']

            uids_list = observations['member_ous_uid'].unique()
            # when len(uids_list) == 0, it's because the DataFrame included only proprietary 
            # data and we removed them in the above if statement, so the DataFrame is now empty

            
        # this is the case where the query had no results to begin with.
        except TypeError:
            logger.critical(
                "Internal error. Something went wrong trying to download mask from "
                "the archive. Fatal error. Please open an issue on GitLab "
                "https://gitlab.com/adp-group1/adp-alma-pipeline with your specific case."
            )
            sys.exit(-1)
        
        #self.alma.cache_location

        data_table = self.alma.get_data_info(uids_list, expand_tarfiles=True)
        dl_table = data_table[
                        [i for i, v in enumerate(data_table['access_url']) 
                         if (".cube.I.mask." in v and 
                             all(fmi in v for fmi in self.download_par['filename_must_include']))]
                             ]
        dl_df = dl_table.to_pandas()
        # remove empty elements in the access_url column
        dl_df = dl_df.loc[dl_df.access_url != '']
        dl_link_list = list(dl_df['access_url'].unique())

        try:
            Logger.raw("================================")
            logger.info("Starting download masks. Please wait...")
            Logger.raw("================================")
            self.alma.download_files(dl_link_list, cache=True)
            
        except ValueError as e:
            logger.error(e)

        self.get_downloaded_mask_path(Path(self.alma.cache_location), dl_link_list)
        Logger.raw("================================")
        logger.info("Mask download ended.")
        Logger.raw("================================")

    
    def run_query(self, query_str):
        """
        Run the TAP query through PyVO service.

        Parameters
        ----------
        query_str : str
            ADQL query to send to the PyVO TAP service
        tap_service : str, optional
            (Default value = 'ESO')
            The TAP service to use. Options are:
            'ESO' for Europe (https://almascience.eso.org/tap),
            'NRAO' for North America (https://almascience.nrao.edu/tap), or
            'NAOJ' for East Asia (https://almascience.nao.ac.jp/tap)
        Returns
        -------
        pandas.DataFrame containing the query results

        """
        # Run query
        # for large queries add maxrec=1000000
        pyvo_TAP_results = self._service.search(query_str, maxrec=1000000)  

        # transform output into astropy table first, then to a pandas DataFrame
        TAP_df = pyvo_TAP_results.to_table().to_pandas()

        # the column publication_year must be in 'object' type because it contains numbers and NaNs
        TAP_df['publication_year'] = TAP_df['publication_year'].astype('object')


        return TAP_df


    def get_downloaded_file_path(self, download_dir, dl_link_list):
        """
        Process and retrieve paths to the most recent data cube and primary beam files in a given 
        directory.

        Parameters:
        ----------
            base_dir (Path): The base directory where the downloaded files are located.

        Returns:
        ----------
            None

        Raises:
        ----------
            SystemExit: If no valid data cube files are found in the specified directory.
        """
        
        data_files = [Path(url).name for url in dl_link_list 
                      if "cube.I.pbcor" in Path(url).name]
        # Excluye los archivos .pb. Solo por si acaso
        data_files = [download_dir / Path(f) for f in data_files if ".pb." not in Path(f).name]       
        

        if data_files:
            self.data_list = data_files
        else:
            logger.error(f"It appears that no files containing a data cube have been downloaded." 
                         "Files with data from ALMA cycle 2 must contain the string 'cube.I.pbcor'" 
                         "in their names. If the file you want to download is older please open an "
                         "issue on GitLab https://gitlab.com/adp-group1/adp-alma-pipeline with the "
                         "specific case. You can still use the Alma Pipeline ADP if you download "
                         "the file yourself and run it locally.")
            logger.info("Exiting pipeline")
            sys.exit(-1)
            

        if self.download_par['include_pb']:
                
            pb_files_aux = [download_dir / Path(Path(url).name) for url in dl_link_list 
                            if "cube.I.pb." in Path(url).name]
            
            pb_files = []
            for data_path in self.data_list:
                data_segment = get_segment(str(data_path))  
                matched = False
                for pb_path in pb_files_aux:
                    if data_segment == get_segment(str(pb_path)):
                        pb_files.append(pb_path)  
                        matched = True
                        break  
                if not matched:
                    pb_files.append("") 

            if  all(mask == "" for mask in pb_files):

                logger.warning(
                    "No primary beam was found in the downloaded dataset. Either it"
                    " is not available in the archive, or the strings included in the "
                    "'filename_must_include' parameter have been so restrictive that "
                    "they exclude the primary beam file from the download. Avoid "
                    "full names if you want to download the primary beam."
                )
                logger.warning(
                    "Continued without taking into account any primary beams"
                )
                self.pb_list = pb_files
                return
            

            decompressed_pb_files = []  

            for file in pb_files:
                if file == "":  # Ignoro entradas vacías
                    decompressed_pb_files.append("")
                    continue

                if file.suffix == ".gz":
                    extracted_file_path = file.with_suffix('')  

                    # Compruebo si el archivo descomprimido ya existe
                    if extracted_file_path.exists():
                        logger.info(
                            "The unzipped primary beam file already exists: "
                            f"{extracted_file_path}"
                        )
                        decompressed_pb_files.append(extracted_file_path)

                        if self.download_par['remove_uncompress_file']:
                            file.unlink()
                            logger.info(f"Compressed file deleted: {file}")
                    else:
                        # Intento descomprimir el archivo
                        try:
                            with gzip.open(file, 'rb') as gz_in:
                                with open(extracted_file_path, 'wb') as extracted_out:
                                    shutil.copyfileobj(gz_in, extracted_out)
                            logger.info(
                                f"Unzipped primary beam file: {extracted_file_path}"
                            )

                            if self.download_par['remove_uncompress_file']:
                                file.unlink()
                                logger.info(f"Compressed file deleted: {file}")

                            decompressed_pb_files.append(extracted_file_path)
                        except Exception as e:
                            logger.error(f"Error trying to unzip {file}: {e}")
                else:
                    # Si no es un archivo comprimido (.gz), lo agrego a la lista
                    decompressed_pb_files.append(file)
    
            if decompressed_pb_files:
                self.pb_list = decompressed_pb_files
            else:
                logger.critical(
                "No valid primary beam files were successfully processed. Fatal error. "
                "Please open an issue on GitLab "
                "https://gitlab.com/adp-group1/adp-alma-pipeline with your specific case."
                )
                sys.exit(-1)

        else:
            self.pb_list = ["" for _ in dl_link_list]


    def get_downloaded_mask_path(self, download_dir, dl_link_list):

        """
        Process and retrieve the most recent mask file from a given directory.

        This method searches for mask files in the specified directory (`base_dir`) that match 
        the pattern `*cube.I.mask*`. It handles compressed `.gz` files by decompressing them 
        if necessary and optionally deleting the original compressed files based on the 
        `self.download_par['remove_uncompress_file']` setting. The most recently modified mask 
        file is selected and stored as an attribute (`self.data_loc_mask`).

        Args:
            base_dir (Path): The directory where the downloaded mask files are located.

        Returns:
            None
        """

        #Cuidado con buscar de esta manera, habría que ser más específico
        mask_files_aux = [download_dir / Path(Path(url).name) for url in dl_link_list 
                      if "cube.I.mask." in Path(url).name]
        
        mask_files = []
        for data_path in self.data_list:
            data_segment = get_segment(str(data_path))  
            matched = False
            for mask_path in mask_files_aux:
                if data_segment == get_segment(str(mask_path)):
                    mask_files.append(mask_path)  
                    matched = True
                    break  
            if not matched:
                mask_files.append("") 
        
        if all(mask == "" for mask in mask_files):
            logger.warning("No mask files found in the download data set selected.")
            self.mask_list = mask_files
            return

        decompressed_mask_files = []  #Almaceno archivos descomprimidos o existentes

        for file in mask_files:

            if file == "":  # Ignoro entradas vacías
                decompressed_mask_files.append("")
                continue
            # Compruebo si esta comprimido (.gz)
            if file.suffix == ".gz":
                extracted_file_path = file.with_suffix('') 

                # Compruebo si el archivo descomprimido ya existe
                if extracted_file_path.exists():
                    logger.info(f"The unzipped file already exists: {extracted_file_path}")
                    decompressed_mask_files.append(extracted_file_path)

                    if self.download_par['remove_uncompress_file']:
                        file.unlink()
                        logger.info(f"Compressed file deleted: {file}")
                else:
                    try:
                        with gzip.open(file, 'rb') as gz_in:
                            with open(extracted_file_path, 'wb') as extracted_out:
                                shutil.copyfileobj(gz_in, extracted_out)
                        logger.info(f"Unzipped file: {extracted_file_path}")

                        if self.download_par['remove_uncompress_file']:
                            file.unlink()
                            logger.info(f"Compressed file deleted: {file}")

                        decompressed_mask_files.append(extracted_file_path)
                    except Exception as e:
                        logger.error(f"Error trying to unzip {file}: {e}")
            else:
                decompressed_mask_files.append(file)

        # Selecciona el archivo más reciente basado en su fecha de modificación
        if decompressed_mask_files:
            self.mask_list = decompressed_mask_files
            #logger.info(f"Most recent file selected: {most_recent_maskfile}")
        else:
            logger.critical(
                "No valid mask files were successfully processed. Fatal error. Please open an"
                " issue on GitLab https://gitlab.com/adp-group1/adp-alma-pipeline with "
                "your specific case."
            )
            sys.exit(-1)



    # Type of querys available     

    def proposal_id(self):
        """
        Query the ALMA archive for a given proposal ID.

        Parameters
        ----------
        Self: All the required parameters are part of the attributes of the class itself. 
        The attiributes are defined in the download_par.yaml, see README for further details

        Returns
        -------
        'TAP_df' pandas.DataFrame containing the query results

        """

        
        query = (
            "SELECT *  FROM ivoa.obscore WHERE obs_publisher_did like "
            f"'%{self.query_par['proposal_id']}%'"
        )

        if self.query_par['public']:
            query = "{} AND data_rights LIKE '%Public%'".format(query)

        elif not self.query_par['public'] and self.query_par['public'] is not None:
            query = "{} AND data_rights LIKE '%Proprietary%'".format(query)

        if self.query_par['print_query']:
            logger.info("Your query is: {}".format(query))

        
        TAP_df = self.run_query(query)

        #CHANGE. Aquí 'filter_results' es una función que si bien he revisado, hace llamadas 
        #a otras muchas funciones que no quiero incluir, al menos por ahora. Asi que ignoro 
        #esta parte    
        '''if TAP_df is not None:
            if self.query_par['published']:  # case of self.query_par['published'] = True
                TAP_df = TAP_df[TAP_df['publication_year'].notnull()]

            # case of self.query_par['published'] = False
            elif not self.query_par['published'] and self.query_par['published'] is not None:  
                
                TAP_df = TAP_df[TAP_df['publication_year'].isnull()]

            filtered_df = self.filter_results(TAP_df)
            return filtered_df'''
        
        return TAP_df
        

    def conesearch(self):
        """
        Query the ALMA archive for a given position and radius around it.

        Parameters
        ----------
        ra : float
            Right ascension in degrees (ICRS).
        dec : float
            Declination in degrees (ICRS).
        search_radius : float, optional
            (Default value = 1. arcmin)
            Search radius (in arcmin) around the source coordinates.

        Returns
        -------
        'TAP_df' pandas.DataFrame containing the query results

        """

        search_radius = self.query_par['search_radius'] * u.arcmin
        if self.query_par['point']:
            query = (
                "SELECT * FROM ivoa.ObsCore WHERE 1 = CONTAINS(POINT('ICRS',"
                f"{self.query_par['ra']},{self.query_par['dec']}), s_region)"
            )

        else:
            query = (
                "SELECT * FROM ivoa.ObsCore "
                f"WHERE (1 = INTERSECTS(CIRCLE('ICRS', {self.query_par['ra']}, "
                f"{self.query_par['dec']}, {search_radius.to(u.deg).value}), s_region) "
                f"OR 1 = CONTAINS(POINT('ICRS', {self.query_par['ra']}, "
                f"{self.query_par['dec']}), s_region))"
            )

        if self.query_par['public']:
            query = f"{query} AND data_rights LIKE '%Public%'"
        elif not self.query_par['public'] and self.query_par['public'] is not None:
            query = f"{query} AND data_rights LIKE '%Proprietary%'"

        if self.query_par['print_query']:
            logger.info("Your query is: {}".format(query))

        TAP_df = self.run_query(query)

        #CHANGE. Aquí 'filter_results' es una función que si bien he revisado, hace llamadas a otras 
        # muchas funciones que no quiero incluir, al menos por ahora. Asi que ignoro esta parte 
        '''
        if TAP_df is not None:
            if self.query_par['published']:  # case of self.query_par['published'] = True
                TAP_df = TAP_df[TAP_df['publication_year'].notnull()]

            # case of self.query_par['published'] = False
            elif not self.query_par['published'] and self.query_par['published'] is not None:  
                TAP_df = TAP_df[TAP_df['publication_year'].isnull()]

            filtered_df = self.filter_results(TAP_df)
            return filtered_df
        '''

        return TAP_df


    def self_conesearch(self, ra, dec, search_radius):
        """
        Query the ALMA archive for a given position and radius around it.

        Parameters
        ----------
        ra : float
            Right ascension in degrees (ICRS).
        dec : float
            Declination in degrees (ICRS).
        search_radius : float, optional
            (Default value = 1. arcmin)
            Search radius (in arcmin) around the source coordinates.

        Returns
        -------
        'TAP_df' pandas.DataFrame containing the query results

        """

        search_radius = search_radius * u.arcmin
        if self.query_par['point']:
            query = (
                "SELECT * FROM ivoa.ObsCore "
                f"WHERE 1 = CONTAINS(POINT('ICRS',{ra},{dec}), s_region)"
            )
        else:
            query = ("SELECT * FROM ivoa.ObsCore "
                     f"WHERE (1 = INTERSECTS(CIRCLE('ICRS',{ra},{dec},{search_radius.to(u.deg).value})"
                     f", s_region) OR 1 = CONTAINS(POINT('ICRS',{ra},{dec}), s_region))"
            )

        if self.query_par['public']:
            query = "{} AND data_rights LIKE '%Public%'".format(query)
        elif not self.query_par['public'] and self.query_par['public'] is not None:
            query = "{} AND data_rights LIKE '%Proprietary%'".format(query)

        if self.query_par['print_query']:
            logger.info("Your query is: {}".format(query))

        TAP_df = self.run_query(query)

        #CHANGE. Aquí 'filter_results' es una función que si bien he revisado, hace llamadas 
        # a otras muchas funciones que no quiero incluir, al menos por ahora. Asi que ignoro 
        # esta parte 
        '''
        if TAP_df is not None:
            if self.query_par['published']:  # case of self.query_par['published'] = True
                TAP_df = TAP_df[TAP_df['publication_year'].notnull()]

            elif not self.query_par['published'] and self.query_par['published'] is not None:  # case of self.query_par['published'] = False
                TAP_df = TAP_df[TAP_df['publication_year'].isnull()]

            filtered_df = self.filter_results(TAP_df)
            return filtered_df
        '''

        return TAP_df
    

    def target(self):
        """
        Query targets by name.

        This is done by using the astropy SESAME resolver to get the target's coordinates and 
        then the ALMA archive is queried for those coordinates and a search_radius around them. 
        The SESAME resolver searches multiple databases (Simbad, NED, VizieR) to parse names 
        commonly found throughout literature and returns their coordinates. If the target is 
        not resolved in any of these databases, consider using the 'keysearch' function and query 
        the archive using the 'target_name' keyword (e.g. keysearch({'target_name': sources})).

        Parameters
        ----------
        sources : str or list of str
            list of sources by name.
            (IMPORTANT: source names must be identified by at least one of Simbad, NED, or Vizier)
        search_radius : float, optional
            (Default value = 1. arcmin)
            Search radius (in arcmin) around the source coordinates.


        Returns
        -------
        'obs' pandas.DataFrame containing the query results.

        See Also
        --------
        keysearch : Query the ALMA archive for any (string-type) keywords defined in ALMA TAP system.

        """
        """if isinstance(self.query_par['sources'], str):
            sources = [self.query_par['sources']]"""
        
        print("================================")
        print("adpalmap.target results ")
        print("================================")
        complete_results = []
        # go through list of sources provided by user and add query results to a list
        for s in self.query_par['sources']:
            print("Target = {}".format(s))
            try:
                # Get source coodinates from astropy SESAME resolver querying multiple databases 
                # (SIMBAD, NED, Vizier)
                source_pos = get_icrs_coordinates(s)
                TAP_df = self.self_conesearch(
                    ra=source_pos.ra.deg, dec=source_pos.dec.deg, 
                    search_radius=self.query_par['search_radius']
                    )
                if TAP_df is not None:
                    complete_results.append(TAP_df)
            # source coords not found in SESAME resolver
            except name_resolve.NameResolveError as err:  
                logger.error(err)
                print(f"Try keysearch function instead: keysearch({{'target_name':['{s}']}}).")
                print("--------------------------------")
                pass
        # if the list of query results is not empty, concatenate them together into one DataFrame
        if complete_results:
            obs = pd.concat(complete_results)
            # need to reset the index of DataFrame so the indices in the final DataFrame are 
            # consecutive
            obs = obs.reset_index(drop=True)
            return obs
        else:
            logger.warning("No observations found for any sources in this list.")
            print("--------------------------------")   


    def keysearch(self):
        """
        Query the ALMA archive for any (string-type) keywords defined in ALMA TAP system.

        Parameters
        ----------
        search_dict : dict[str, list of str]
            Dictionary of keywords in the ALMA archive and their values. Values must be formatted 
            as a list. A list of valid keywords are stored in VALID_KEYWORDS_STR variable.


        Returns
        -------
        pandas.DataFrame containing the query results.

        Notes
        -----
        The power of this function is in combining keywords. When multiple keywords are provided, 
        they are queried using 'AND' logic, but when multiple values are provided for a given 
        keyword, they are queried using 'OR' logic. If a given value contains spaces, its 
        constituents are queried using 'AND' logic. Words encapsulated in quotation marks (either '
        or ") are queried as phrases. Values for the 'target_name' keyword are queried with 'OR'
        logic.

        Examples
        --------
        keysearch({"proposal_abstract": ["high-mass star formation outflow disk"]})
            will query the archive for projects with the words
            "high-mass" AND "star" AND "formation" AND "outflow" AND "disk" in their proposal
            abstracts.

        keysearch({"proposal_abstract": ["high-mass", "star", "formation", "outflow", "disk"]})
            will query the archive for projects with the words
            "high-mass" OR "star" OR "formation" OR "outflow" OR "disk" in their proposal abstracts.

        keysearch({"proposal_abstract": ["'high-mass star formation' outflow disk"]})
            will query the archive for projects with the phrase
            "high-mass star formation" AND the words "outflow" AND "disk" in their proposal abstracts.

        keysearch({"proposal_abstract": ["'star formation'"], "scientific_category":['Galaxies']})
            will query the archive for projects with the phrase
            "star formation" in their proposal abstracts AND
            projects that are within the scientific_category of 'Galaxies'.

        """

        print("================================")
        print("Keysearch results ")
        print("================================")

        # Add keyword to the query dictionary for the data rights (Public, Proprietary, or both)
        if self.query_par['public']:
            self.query_par['search_dict']['data_rights'] = ['Public']
        elif not self.query_par['public'] and self.query_par['public'] is not None:
            self.query_par['search_dict']['data_rights'] = ['Proprietary']
        # Add scan intent keyword to the query dictionary to be the science target by default
        self.query_par['search_dict']['scan_intent'] = ['TARGET']

        # Compile a list of queries based on all keywords provided
        full_query_list = []
        for keyword, values in self.query_par['search_dict'].items():
            # Catch if a wrong keyword is used and give appropriate error
            assert keyword in VALID_KEYWORDS_STR, (
                f"Invalid keyword, must be one of: {VALID_KEYWORDS_STR}"
            )
            # Convert underscores and spaces in the target name to wildcard
            # target_name is always queried with OR logic
            if keyword == 'target_name':
                values = [v.replace('_', '%') for v in values]
                values = [v.replace(' ', '%') for v in values]
                # Create queries for a given keyword using 'OR' logic between different values 
                # and accounting for
                # the case-sensitivity
                current_query = ["LOWER({}) LIKE '%{}%'".format(keyword, v.lower()) for v in values]
                full_query_list.append("({})".format(" OR ".join(current_query)))
            # Account for AND/OR logic for keywords that are not target_name

            else:
                keyword_query_list = []
                for v in values:
                    # If there are quotations in the values of a given keyword, split them out and 
                    # query them as phrases If there are remaining keywords separated by spaces, 
                    # split them out and query them with AND logic
                    if re.search(r"\s", v):
                        split_values = re.findall(r"['\"].*['\"]|\d+\.\d+|[\w-]+", v)
                        current_query = [
                            "LOWER({}) LIKE '%{}%'".format(keyword, re.sub("['\"]", '', s.lower())) 
                            for s in split_values
                        ]

                        keyword_query_list.append("({})".format(" AND ".join(current_query)))
                    # If separate words are provided as values, query them with OR logic
                    else:
                        keyword_query_list.append("LOWER({}) LIKE '%{}%'".format(keyword, v.lower()))
                full_query_list.append("({})".format(" OR ".join(keyword_query_list)))
                

        # Put together the entire query with 'AND' logic between different keywords
        full_query = (
            f"SELECT * FROM ivoa.obscore WHERE {' AND '.join(full_query_list)}" 
            "ORDER BY proposal_id"
        )
        if self.query_par['print_query']:
            logger.info("Your query is: {}".format(full_query))
        TAP_df = self.run_query(full_query)
        # Filter whether the user wants published data, unpublished data, or both (default)
        if self.query_par['published']:  # case pf published = True
            TAP_df = TAP_df[TAP_df['publication_year'].notnull()]
        # case pf published = False
        elif not self.query_par['published'] and self.query_par['published'] is not None:  
            TAP_df = TAP_df[TAP_df['publication_year'].isnull()]
        
        #CHANGE. filter_result, esta función esta pero aún no esta implementada. 
        return TAP_df


    def free(self):

        TAP_df = self.run_query(self.query_par['query_str'])

        return TAP_df


    def check_query_par(self):
        """
        Validate the query parameters (`query_par`) for the specified query type (`query_type`).


        Raises:
        ----------
        ValueError: If `query_type` is undefined or invalid, required parameters are missing, 
                    extra parameters are found, or parameter types are incorrect.
        """

        if not self.query_type:
            raise ValueError(f"The attribute 'query_type' is not defined in the YAML file.")

        # Expected parameters for each query
        expected_params = {
            'proposal':   ['proposal_id'],
            'conesearch': ['ra', 'dec', 'search_radius'],
            'target':     ['sources', 'search_radius'],
            'keysearch':  ['search_dict'],
            'free':       ['query_str'],
        }

        # Expected types for specific parameters
        expected_types = {
            'proposal_id': str,
            'ra': (int, float),
            'dec': (int, float),
            'search_radius': (int, float),
            'sources': list,
            'search_dict': dict,
            'query_str': str,
        }

        # Common parameters to ignore during validation
        common_params = ['point', 'public', 'published', 'print_targets', 'print_query']

        # Get the valid parameters for the current query type
        valid_params = expected_params.get(self.query_type, None)

        if not valid_params:
            raise ValueError(f"The query type '{self.query_type}' is not valid. "
                             "Choose among the available options.")

        # Filter active parameters, excluding common ones
        active_params = {
            k: v for k, v in self.query_par.items() 
            if v is not None 
            and k not in common_params
        }

        # Check missing params
        missing_params = [param for param in valid_params if param not in active_params]
        if missing_params:
            raise ValueError("The next required 'query_par' for 'query_type' ="
                             f" {self.query_type} are missing: {missing_params}")

        # Check extra params
        extra_params = [param for param in active_params if param not in valid_params]
        if extra_params:
            raise ValueError("Invalid parameters found for 'query_type = "
                             f"{self.query_type}': {extra_params}.")

        # Check that the number of parameters matches exactly
        if len(active_params) != len(valid_params):
            raise ValueError(
                "The number of active parameters does not match the expected ones for 'query_type"
                f" = {self.query_type}'. Expected: {valid_params}, Active: "
                f"{list(active_params.keys())}."
            )

        # Validate types for active parameters
        for param, value in active_params.items():
            expected_type = expected_types.get(param)
            if expected_type and not isinstance(value, expected_type):
                raise ValueError(
                    f"The parameter '{param}' must be of type {expected_type}, but got '{value}'"
                    f"({type(value).__name__})."
                )

        logger.info(f"Validation successful: all parameters for 'query_type = {self.query_type}'"
                    " are correct.")


    def check_download_par(self):
        """
        Validates the types of parameters in the class instance, excluding 'query_par'.
        
        Raises:
            ValueError: If any attribute does not match its expected type.
        """
        
        expected_types = {
            'server_address': str,
            'credentials': bool,
            'stored_credentials': bool,
            'download_par': dict,  # Se espera que sea un diccionario para validación más profunda
        }

        for param, expected_type in expected_types.items():
            if hasattr(self, param):
                value = getattr(self, param)
                if not isinstance(value, expected_type):
                    raise ValueError(
                        f"Parameter '{param}' must be of type {expected_type.__name__}, "
                        f"but got {type(value).__name__}, '{value}'."
                    )

        # Validar subparámetros en download_par si está presente
        if hasattr(self, 'download_par') and isinstance(self.download_par, dict):
            download_par_expected_types = {
                'fitsonly': bool,
                'include_pb': bool,
                'remove_uncompress_file': bool,
                'dryrun': bool,
                'print_urls': bool,
                'filename_must_include': list,
                'data_dir': str | None
                }
            

            for key, expected_type in download_par_expected_types.items():
                if key in self.download_par:
                    value = self.download_par[key]
                    if not isinstance(value, expected_type):
                        raise ValueError(
                            f"Parameter 'download_par.{key}' must be of type {expected_type.__name__}"
                            f",  but got {type(value).__name__}, '{value}'."
                        )

        #print("All parameters are valid.")

        

    ''' FUNCTIONS TO BE PONTENTIALLY ADDED. Se entrelazan entre ellas'''
    '''
    def filter_results(self, TAP_df):
        """
        Add a few new useful columns to the pandas.DataFrame with the query results from the PyVO TAP service and
        return the full query DataFrame and optionally a summary of the results.

        Parameters
        ----------
        TAP_df : pandas.DataFrame
            This is likely the output of 'run_query' function.
        print_targets : bool, optional
            (Default value = True)
            Print a list of targets with ALMA data (ALMA source names) to the terminal.

        Returns
        -------
        pandas.DataFrame containing the query results.

        """
        # add new columns to the DataFrame
        TAP_COLUMNS = TAP_df.columns.tolist()
        data = TAP_df.reindex(NEW_COLUMNS + TAP_COLUMNS, axis=1)
        data = data.astype(COLUMN_TYPES)
        data = data.reset_index(drop=True)  # needed to renumber the index of the rows for looping over below
        if not data.empty:
            # calculate the relevant variables
            data['min_freq_GHz'] = [(em_max * u.m).to(u.GHz, equivalencies=u.spectral()).value for em_max in data['em_max']]
            data['max_freq_GHz'] = [(em_min * u.m).to(u.GHz, equivalencies=u.spectral()).value for em_min in data['em_min']]
            data['central_freq_GHz'] = data[['min_freq_GHz', 'max_freq_GHz']].mean(axis=1)
            data['bandwidth_GHz'] = data['max_freq_GHz'] - data['min_freq_GHz']
            data['line_sens_10kms'] = data['sensitivity_10kms'] * 1000.0  # in uJy/beam
            data['cont_sens_bandwidth'] = data['cont_sensitivity_bandwidth'] * 1000.0  # in uJy/beam

            # parse the 'frequency_support' string to determine the frequency_resolution EXACTLY
            data['freq_res_kHz'] = [self._get_freq_res(fs, data['min_freq_GHz'][i], data['max_freq_GHz'][i],
                                                data['em_res_power'][i])
                                    for i, fs in enumerate(data['frequency_support'])]

            nchan = data['bandwidth_GHz'] * 1000000.0 / data['freq_res_kHz']
            data['vel_res_kms'] = const.c.to(u.km / u.s).value / data['em_res_power']
            data['line_sens_native'] = data['line_sens_10kms'] * np.sqrt(10.0 / data['vel_res_kms'] / nchan)

            # add values to the table in desired precision
            data['Obs'] = [i+1 for i in np.arange(data.shape[0])]
            data['project_code'] = data['proposal_id']
            data['ALMA_source_name'] = data['target_name']
            data['RAJ2000'] = data['s_ra']
            data['DEJ2000'] = data['s_dec']
            data['ang_res_arcsec'] = data['s_resolution'].round(decimals=3)
            data['min_freq_GHz'] = data['min_freq_GHz'].round(decimals=2)
            data['max_freq_GHz'] = data['max_freq_GHz'].round(decimals=2)
            data['central_freq_GHz'] = data['central_freq_GHz'].round(decimals=2)
            data['bandwidth_GHz'] = data['bandwidth_GHz'].round(decimals=3)
            data['freq_res_kHz'] = data['freq_res_kHz'].round(decimals=2)
            data['vel_res_kms'] = data['vel_res_kms'].round(decimals=3)
            data['LAS_arcsec'] = data['spatial_scale_max'].round(decimals=3)
            data['FoV_arcsec'] = (data['s_fov'] * 3600.).round(decimals=3)
            data['cont_sens_bandwidth'] = data['cont_sens_bandwidth'].round(decimals=3)
            data['line_sens_10kms'] = data['line_sens_10kms'].round(decimals=2)
            data['line_sens_native'] = data['line_sens_native'].round(decimals=2)
            data['MOUS_id'] = data['member_ous_uid']
            data = data.drop_duplicates().reset_index(drop=True)

            #Function to print an optional summary of the dataframe. Implemented in Alminer, not included here. FUNCTION
            #summary(data, print_targets=print_targets)

            return data
        else:
            print("--------------------------------")
            logger.warning("No observations found.")
            print("--------------------------------")


    def _get_freq_res(frequency_support, freq_min, freq_max, em_res_power):
        """
        Given the minimum and maximum frequency, parse the 'frequency_support' and extract the frequency resolution.
        """
        for s in frequency_support.split('[')[1:]:
            if s.startswith("{:.2f}..{:.2f}".format(freq_min, freq_max)):
                return float(s.split(',')[1].replace('kHz', ''))
        # if the parsing is not successful, calculate the frequency resolution manually
        return float((freq_max * u.GHz / em_res_power).to(u.kHz).value.round(decimals=2))
    '''

