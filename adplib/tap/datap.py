#import re
import numpy as np
import os
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


# Astroquery is required
from astroquery.alma import Alma

# Python Virtual Observatory
import pyvo
from pyvo.dal import tap

#Logging
import logging
logger = logging.getLogger(__name__)

class datap(dict): 

    def __init__(self, **kwargs):
        """
        Reads the tap_parameters file and creates an datap object.
        
        Parameters
        ----------
        config_path: str, default None
            Path to the configuration file. If None, it will display an error.

        Returns
        -------
        self

        Attributes
        ----------
        Different configuration parameters such as database path, log format, server
        for data download from remote sources, etc.
        """

        #The dict constructor is used and every key phrase in the .yaml file become an attribute of this class
        super(datap, self).__init__(**kwargs)
        #Garantiza que cualquier acceso futuro al diccionario o la adición de nuevas claves también se refleje en la estructura de atributos de la instancia.
        self.__dict__ = self # Load config file and set attributes
        self.d_configure(**kwargs)

        #Initialize Alma() instance. <Attribute>
        self.alma = Alma()

        
        if self.credentials:

            print("Introduce your ALMA credentials: ")
            username = input("- Usuario: ")
    
            try:
                self.alma.login(username, store_password=self.stored_credentials)
            
            except Exception as e:
                print(f"Error en la autenticación: {e}")

        #Initialize the archive service to use for the download
        self.alma.archive_url = self.server_address

        #This may become a function. FUNCTION
        self._service = tap.TAPService(f"{self.server_address}/tap")


    def d_configure(self, download_path=None, **kwargs):

        #Esta condición nunca se considera. La clase no se inicializa si el parámetro -d no se usa (None por defecto). Si es not None pasa a las siguiente, por lo que es código que no 
        # se usa. REMOVE

        if download_path is None:
            download_path = Path("tap/download_par.yaml")

            if not download_path.exists():
                raise FileNotFoundError(f"Download file {download_path} not found. Checked if the 'tap/download_par.yaml' have been deleted or the structure have changed. See README for furhter details")
            else:
                logger.info(f"The file in {download_path} have been loaded successfully")

        elif download_path is not None:
            download_path = Path(download_path)

            if not download_path.exists():
                raise FileNotFoundError(f"Download file {download_path} not found.")
            else:
                logger.info(f"The file in {download_path} have been loaded successfully")

        else:
            raise FileNotFoundError(f"Something with the download_path or the download file went wrong")
            
        with open(download_path, 'r') as f:
            download_dict = yaml.safe_load(f)
        
        #Inicializa los datos específicos directos desde el config.yaml. No contempla posibles futuras modificaciones de self (e.g añadiendo nuevos valores dentro del programa) 
        for k, v in download_dict.items():
            setattr(self, k, v)


    def _get_metadata(self):
    
        metadata_query = "SELECT column_name, datatype, unit, ucd, utype, description from TAP_SCHEMA.columns"
        TAP_metadata = self._service.search(metadata_query)

        return pd.DataFrame(TAP_metadata).set_index('column_name')


    def _format_bytes(self, size):
            """Convert the size of the dota to be downloaded in human-readable format."""
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
            This is likely the output of e.g. 'conesearch', 'target', 'catalog', & 'keysearch' functions.

        fitsonly : bool, optional
            (Default value = False)
            Download individual fits files only (fitsonly=True). This option will not download the raw data
            (e.g. 'asdm' files), weblogs, or README files.

        dryrun : bool, optional
            (Default value = False)
            Allow the user to do a test run to check the size and number of files to download without actually
            downloading the data (dryrun=True). To download the data, set testrun=False.

        print_urls : bool, optional
            (Default value = False)
            Write the list of urls to be downloaded from the archive to the terminal.

        filename_must_include : list of str, optional
            (Default value = '')
            A list of strings the user wants to be contained in the url filename. This is useful to restrict the
            download further, for example, to data that have been primary beam corrected ('.pbcor') or that have
            the science target or calibrators (by including their names). The choice is largely dependent on the
            cycle and type of reduction that was performed and data products that exist on the archive as a result.
            In most recent cycles, the science target can be filtered out with the flag '_sci' or its ALMA target name.

        data_path : str, optional
            (Default value = ./archive_data)
            The directory where the downloaded data should be placed.

        """


        print("================================")
        
        default_location = './tap/archive_data'
        
        #Check the input Dataframe
        
        #case where the DataFrame is empty.
        try:
            if any(observations['data_rights'] == 'Proprietary'):
                logger.warning("Some of the data you are trying to download are still in the proprietary period and are not publicly available yet.")
                observations = observations[observations['data_rights'] == 'Public']

            uids_list = observations['member_ous_uid'].unique()
            # when len(uids_list) == 0, it's because the DataFrame included only proprietary data and we removed them in the above if statement, so the DataFrame is now empty

            if len(uids_list) == 0:
                logger.critical("No data to download. Check the input DataFrame. It is likely that your query results include only proprietary data which cannot be freely downloaded.")
                return
            
        # this is the case where the query had no results to begin with.
        except TypeError:
            logger.critical("No data to download. Check the input DataFrame.")
            return
        
        # change download location if specified by user, else the location will be a folder called 'data' in the current working directory
        if self.download_par['data_dir'] != default_location:
            if os.path.isdir(self.download_par['data_dir']):
                self.alma.cache_location = self.download_par['data_dir']
            else:
                logger.warning("{} is not a directory. The download location will be set to {}".format(self.download_par['data_dir'], default_location))
                self.alma.cache_location = default_location
        elif (self.download_par['data_dir'] == default_location) and not os.path.isdir(self.download_par['data_dir']):  # create the 'data' subdirectory
            os.makedirs(default_location)
            self.alma.cache_location = default_location

        #Fits only and phrase within the file to download
        if self.download_par['fitsonly']:

            print('ENTROOOO')
            data_table = self.alma.get_data_info(uids_list, expand_tarfiles=True)
            # filter the data_table and keep only rows with "fits" in 'access_url' and the strings provided by user in 'filename_must_include' parameter
            dl_table = data_table[[i for i, v in enumerate(data_table['access_url']) if v.endswith(".fits") and all(fmi in v for fmi in self.download_par['filename_must_include'])]]

        else:
            data_table = self.alma.get_data_info(uids_list, expand_tarfiles=False)
            # filter the data_table and keep only rows with "fits" in 'access_url' and the strings provided by user in 'filename_must_include' parameter
            dl_table = data_table[[i for i, v in enumerate(data_table['access_url']) if all(fmi in v for fmi in self.download_par['filename_must_include'])]]


        dl_df = dl_table.to_pandas()
        # remove empty elements in the access_url column
        dl_df = dl_df.loc[dl_df.access_url != '']
        dl_link_list = list(dl_df['access_url'].unique())
        # keep track of the download size and number of files to download
        dl_size = dl_df['content_length'].sum()
        dl_files = len(dl_df['access_url'].unique())
        dl_uid_list = list(dl_df['ID'].unique())



        #This options will be potentially removed. REMOVE
        if self.download_par['dryrun']:
            logger.info("This is a dryrun. To begin download, set dryrun=False.")
            print("================================")

        else:
            logger.info("Starting download. Please wait...")
            print("================================")

            try:
                self.alma.download_files(dl_link_list, cache=True)

            except ValueError as e:
                print(e)


        if dl_files > 0:
            print("Download location = {}".format(self.alma.cache_location))
            print("Total number of Member OUSs to download = {}".format(len(dl_uid_list)))
            print("Selected Member OUSs: {}".format(dl_uid_list))
            print("Number of files to download = {}".format(dl_files))
            dl_size_fmt, dl_format = self._format_bytes(dl_size)
            print("Needed disk space = {:.1f} {}".format(dl_size_fmt, dl_format))

            #This option will be potentially removed. REMOVE
            if self.download_par['print_urls']:
                print("File URLs to download = {}".format("\n".join(dl_link_list)))
        else:
            print("Nothing to download.")
            print("Note: often only a subset of the observations (e.g. the representative window) is ingested into "
                "the archive. In such cases, you may need to download the raw dataset, reproduce the calibrated "
                "measurement set, and image the observations of interest. It is also possible to request calibrated "
                "measurement sets through a Helpdesk ticket to the European ARC "
                "(see https://almascience.eso.org/local-news/requesting-calibrated-measurement-sets-in-europe).")
        print("--------------------------------")
    

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
        pyvo_TAP_results = self._service.search(query_str, maxrec=1000000)  # for large queries add maxrec=1000000

        # transform output into astropy table first, then to a pandas DataFrame
        TAP_df = pyvo_TAP_results.to_table().to_pandas()

        # the column publication_year must be in 'object' type because it contains numbers and NaNs
        TAP_df['publication_year'] = TAP_df['publication_year'].astype('object')


        return TAP_df


    # Type of querys available     

    def proposal_id(self):
        """
        Query the ALMA archive for a given proposal ID.

        Parameters
        ----------
        Self: All the required parameters are part of the attributes of the class itself. The attiributes are defined in the download_par.yaml, see README for further details

        Returns
        -------
        pandas.DataFrame containing the query results

        """

        query = f"SELECT *  FROM ivoa.obscore WHERE obs_publisher_did like '%{self.query_par['proposal_id']}%'"

        if self.query_par['public']:
            query = "{} AND data_rights LIKE '%Public%'".format(query)

        elif not self.query_par['public'] and self.query_par['public'] is not None:
            query = "{} AND data_rights LIKE '%Proprietary%'".format(query)

        if self.query_par['print_query']:
            print("Your query is: {}".format(query))

        
        TAP_df = self.run_query(query)

        #CAMBIOS. Aquí filter_results es una función que si bien he revisado, hace llamadas a otras muchas funciones que no quiero incluir, al menos por ahora. Asi que ignoro esta parte    
        '''if TAP_df is not None:
            if self.query_par['published']:  # case pf published = True
                TAP_df = TAP_df[TAP_df['publication_year'].notnull()]

            elif not self.query_par['published'] and self.query_par['published'] is not None:  # case of published = False
                TAP_df = TAP_df[TAP_df['publication_year'].isnull()]

            filtered_df = self.filter_results(TAP_df)
            return filtered_df'''
        
        return TAP_df
        


    ''' !!DANGER!! FUNCTIONS TO BE REVISED. NOT IMPLEMENTE PROPERLY YET'''
    '''
    def conesearch(ra, dec, search_radius=1., tap_service='ESO', point=False, public=True, published=None, print_targets=True, print_query=False):
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
        tap_service : str, optional
            (Default value = 'ESO')
            The TAP service to use. Options are:
            'ESO' for Europe (https://almascience.eso.org/tap),
            'NRAO' for North America (https://almascience.nrao.edu/tap), or
            'NAOJ' for East Asia (https://almascience.nao.ac.jp/tap)
        point : bool, optional
            (Default value = True)
            Search whether the specified position (ra, dec) is contained within any ALMA observations (point=True)
            or query all ALMA observations that overlap with a cone centred at the specified position (ra, dec) and
            extending the search_radius (point=False). In the case of point=True, the search_radius parameter is ignored.
        public : bool, optional
            (Default value = True)
            Search for public data (public=True), proprietary data (public=False),
            or both public and proprietary data (public=None).
        published : bool, optional
            (Default value = None)
            Search for published data only (published=True), unpublished data only (published=False),
            or both published and unpublished data (published=None).
        print_query : bool, optional
            (Default value = True)
            Print the ADQL TAP query to the terminal.
        print_targets : bool, optional
            (Default value = False)
            Print a list of targets with ALMA data (ALMA source names) to the terminal.

        Returns
        -------
        pandas.DataFrame containing the query results

        """
        search_radius = search_radius * u.arcmin
        if point:
            query = "SELECT * FROM ivoa.ObsCore WHERE 1 = CONTAINS(POINT('ICRS',{},{}), s_region)".format(ra, dec)
        else:
            query = "SELECT * FROM ivoa.ObsCore WHERE (1 = INTERSECTS(CIRCLE('ICRS',{},{},{}), s_region) OR " \
                    "1 = CONTAINS(POINT('ICRS',{},{}), s_region))".format(ra, dec, search_radius.to(u.deg).value, ra, dec)

        if public:
            query = "{} AND data_rights LIKE '%Public%'".format(query)
        elif not public and public is not None:
            query = "{} AND data_rights LIKE '%Proprietary%'".format(query)

        if print_query:
            print("Your query is: {}".format(query))

        TAP_df = run_query(query, tap_service=tap_service)
        if TAP_df is not None:
            if published:  # case pf published = True
                TAP_df = TAP_df[TAP_df['publication_year'].notnull()]
            elif not published and published is not None:  # case of published = False
                TAP_df = TAP_df[TAP_df['publication_year'].isnull()]
            filtered_df = filter_results(TAP_df, print_targets=print_targets)
            return filtered_df


    def target(sources, search_radius=1., tap_service='ESO', point=False, public=True, published=None, print_query=False, print_targets=True):
        """
        Query targets by name.

        This is done by using the astropy SESAME resolver to get the target's coordinates and then the ALMA archive
        is queried for those coordinates and a search_radius around them. The SESAME resolver searches multiple databases
        (Simbad, NED, VizieR) to parse names commonly found throughout literature and returns their coordinates. If the
        target is not resolved in any of these databases, consider using the 'keysearch' function and query the archive
        using the 'target_name' keyword (e.g. keysearch({'target_name': sources})).

        Parameters
        ----------
        sources : str or list of str
            list of sources by name.
            (IMPORTANT: source names must be identified by at least one of Simbad, NED, or Vizier)
        search_radius : float, optional
            (Default value = 1. arcmin)
            Search radius (in arcmin) around the source coordinates.
        tap_service : str, optional
            (Default value = 'ESO')
            The TAP service to use. Options are:
            'ESO' for Europe (https://almascience.eso.org/tap),
            'NRAO' for North America (https://almascience.nrao.edu/tap), or
            'NAOJ' for East Asia (https://almascience.nao.ac.jp/tap)
        point : bool, optional
            (Default value = True)
            Search whether the specified position (ra, dec) is contained within any ALMA observations (point=True)
            or query all ALMA observations that overlap with a cone centred at the specified position (ra, dec) and
            extending the search_radius (point=False). In the case of point=True, the search_radius parameter is ignored.
        public : bool, optional
            (Default value = True)
            Search for public data (public=True), proprietary data (public=False),
            or both public and proprietary data (public=None).
        published : bool, optional
            (Default value = None)
            Search for published data only (published=True), unpublished data only (published=False),
            or both published and unpublished data (published=None).
        print_query : bool, optional
            (Default value = True)
            Print the ADQL TAP query to the terminal.
        print_targets : bool, optional
            (Default value = False)
            Print a list of targets with ALMA data (ALMA source names) to the terminal.

        Returns
        -------
        pandas.DataFrame containing the query results.

        See Also
        --------
        keysearch : Query the ALMA archive for any (string-type) keywords defined in ALMA TAP system.

        """
        if isinstance(sources, str):
            sources = [sources]
        print("================================")
        print("alminer.target results ")
        print("================================")
        complete_results = []
        # go through list of sources provided by user and add query results to a list
        for s in sources:
            print("Target = {}".format(s))
            try:
                # Get source coodinates from astropy SESAME resolver querying multiple databases (SIMBAD, NED, Vizier)
                source_pos = get_icrs_coordinates(s)
                TAP_df = conesearch(ra=source_pos.ra.deg, dec=source_pos.dec.deg, search_radius=search_radius,
                                    tap_service=tap_service, point=point, public=public, published=published,
                                    print_query=print_query, print_targets=print_targets)
                if TAP_df is not None:
                    complete_results.append(TAP_df)
            except name_resolve.NameResolveError as err:  # source coords not found in SESAME resolver
                print(err)
                print("Try keysearch function instead: keysearch({{'target_name':['{}']}}).".format(s))
                print("--------------------------------")
                pass
        # if the list of query results is not empty, concatenate them together into one DataFrame
        if complete_results:
            obs = pd.concat(complete_results)
            # need to reset the index of DataFrame so the indices in the final DataFrame are consecutive
            obs = obs.reset_index(drop=True)
            return obs
        else:
            print("No observations found for any sources in this list.")
            print("--------------------------------")   


    def catalog(target_df, search_radius=1., tap_service='ESO', point=False, public=True, published=None, print_query=False, print_targets=True):
        """
        Query the ALMA archive for a list of coordinates or a catalog of sources based on their coordinates.

        Parameters
        ----------
        target_df : pandas.DataFrame
            Source names and coordinates.

            Index:
                RangeIndex
            Columns:
                Name: Name, dtype: str, description: target name (can be numbers or dummy names)
                Name: RAJ2000, dtype: float64, description: right ascension in degrees (ICRS)
                Name: DEJ2000, dtype: float64, description: declination in degrees (ICRS)
        search_radius : float, optional
            (Default value = 1. arcmin)
            Search radius (in arcmin) around the source coordinates.
        tap_service : str, optional
            (Default value = 'ESO')
            The TAP service to use. Options are:
            'ESO' for Europe (https://almascience.eso.org/tap),
            'NRAO' for North America (https://almascience.nrao.edu/tap), or
            'NAOJ' for East Asia (https://almascience.nao.ac.jp/tap)
        point : bool, optional
            (Default value = True)
            Search whether the specified position (ra, dec) is contained within any ALMA observations (point=True)
            or query all ALMA observations that overlap with a cone centred at the specified position (ra, dec) and
            extending the search_radius (point=False). In the case of point=True, the search_radius parameter is ignored.
        public : bool, optional
            (Default value = True)
            Search for public data (public=True), proprietary data (public=False),
            or both public and proprietary data (public=None).
        published : bool, optional
            (Default value = None)
            Search for published data only (published=True), unpublished data only (published=False),
            or both published and unpublished data (published=None).
        print_query : bool, optional
            (Default value = True)
            Print the ADQL TAP query to the terminal.
        print_targets : bool, optional
            (Default value = False)
            Print a list of targets with ALMA data (ALMA source names) to the terminal.

        Returns
        -------
        pandas.DataFrame containing the query results.

        """
        print("================================")
        print("alminer.catalog results")
        print("================================")
        complete_results = []
        for p in range(target_df.shape[0]):
            print("Target = {}".format(target_df.Name[p]))
            source_pos = SkyCoord(target_df.RAJ2000[p] * u.deg, target_df.DEJ2000[p] * u.deg, frame='icrs')
            TAP_df = conesearch(ra=source_pos.ra.deg, dec=source_pos.dec.deg, search_radius=search_radius,
                                tap_service=tap_service, point=point, public=public, published=published,
                                print_query=print_query, print_targets=print_targets)
            if TAP_df is not None:
                complete_results.append(TAP_df)
        # if the list of query results is not empty, concatenate them together into one DataFrame
        if complete_results:
            obs = pd.concat(complete_results)
            # need to reset the index of DataFrame so the indices in the final DataFrame are consecutive
            obs = obs.drop_duplicates().reset_index(drop=True)
            return obs
        else:
            print("No observations found for any sources in this catalog.")
            print("--------------------------------")


    def keysearch(search_dict, tap_service='ESO', public=True, published=None, print_query=False, print_targets=True):
        """
        Query the ALMA archive for any (string-type) keywords defined in ALMA TAP system.

        Parameters
        ----------
        search_dict : dict[str, list of str]
            Dictionary of keywords in the ALMA archive and their values. Values must be formatted as a list.
            A list of valid keywords are stored in VALID_KEYWORDS_STR variable.
        tap_service : str, optional
            (Default value = 'ESO')
            The TAP service to use. Options are:
            'ESO' for Europe (https://almascience.eso.org/tap),
            'NRAO' for North America (https://almascience.nrao.edu/tap), or
            'NAOJ' for East Asia (https://almascience.nao.ac.jp/tap)
        public : bool, optional
            (Default value = True)
            Search for public data (public=True), proprietary data (public=False),
            or both public and proprietary data (public=None).
        published : bool, optional
            (Default value = None)
            Search for published data only (published=True), unpublished data only (published=False),
            or both published and unpublished data (published=None).
        print_query : bool, optional
            (Default value = True)
            Print the ADQL TAP query to the terminal.
        print_targets : bool, optional
            (Default value = False)
            Print a list of targets with ALMA data (ALMA source names) to the terminal.

        Returns
        -------
        pandas.DataFrame containing the query results.

        Notes
        -----
        The power of this function is in combining keywords. When multiple keywords are provided, they are
        queried using 'AND' logic, but when multiple values are provided for a given keyword, they are queried using
        'OR' logic. If a given value contains spaces, its constituents are queried using 'AND' logic. Words encapsulated
        in quotation marks (either ' or ") are queried as phrases. Values for the 'target_name' keyword
        are queried with 'OR' logic.

        Examples
        --------
        keysearch({"proposal_abstract": ["high-mass star formation outflow disk"]})
            will query the archive for projects with the words
            "high-mass" AND "star" AND "formation" AND "outflow" AND "disk" in their proposal abstracts.

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
        print("alminer.keysearch results ")
        print("================================")
        # Add keyword to the query dictionary for the data rights (Public, Proprietary, or both)
        if public:
            search_dict['data_rights'] = ['Public']
        elif not public and public is not None:
            search_dict['data_rights'] = ['Proprietary']
        # Add scan intent keyword to the query dictionary to be the science target by default
        search_dict['scan_intent'] = ['TARGET']

        # compile a list of queries based on all keywords provided
        full_query_list = []
        for keyword, values in search_dict.items():
            # Catch if a wrong keyword is used and give appropriate error
            assert keyword in VALID_KEYWORDS_STR, "Invalid keyword, must be one of: {}".format(VALID_KEYWORDS_STR)
            # Convert underscores and spaces in the target name to wildcard
            # target_name is always queried with OR logic
            if keyword == 'target_name':
                values = [v.replace('_', '%') for v in values]
                values = [v.replace(' ', '%') for v in values]
                # Create queries for a given keyword using 'OR' logic between different values and accounting for
                # the case-sensitivity
                current_query = ["LOWER({}) LIKE '%{}%'".format(keyword, v.lower()) for v in values]
                full_query_list.append("({})".format(" OR ".join(current_query)))
            # Account for AND/OR logic for keywords that are not target_name
            else:
                keyword_query_list = []
                for v in values:
                    # If there are quotations in the values of a given keyword, split them out and query them as phrases
                    # If there are remaining keywords separated by spaces, split them out and query them with AND logic
                    if re.search(r"\s", v):
                        split_values = re.findall(r"['\"].*['\"]|\d+\.\d+|[\w-]+", v)
                        current_query = ["LOWER({}) LIKE '%{}%'".format(keyword, re.sub("['\"]", '', s.lower())) for s in
                                        split_values]
                        keyword_query_list.append("({})".format(" AND ".join(current_query)))
                    # If separate words are provided as values, query them with OR logic
                    else:
                        keyword_query_list.append("LOWER({}) LIKE '%{}%'".format(keyword, v.lower()))
                full_query_list.append("({})".format(" OR ".join(keyword_query_list)))
        # Put together the entire query with 'AND' logic between different keywords
        full_query = "SELECT * FROM ivoa.obscore WHERE {} ORDER BY proposal_id".format(" AND ".join(full_query_list))
        if print_query:
            print("Your query is: {}".format(full_query))
        TAP_df = run_query(full_query, tap_service=tap_service)
        # Filter whether the user wants published data, unpublished data, or both (default)
        if published:  # case pf published = True
            TAP_df = TAP_df[TAP_df['publication_year'].notnull()]
        elif not published and published is not None:  # case pf published = False
            TAP_df = TAP_df[TAP_df['publication_year'].isnull()]
        return filter_results(TAP_df, print_targets=print_targets)


    def free(query, service=''):
        return
    '''

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

