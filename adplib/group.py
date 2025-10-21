from astropy.io import fits
import networkx as nx
import numpy as np
from pathlib import Path
import sys
import gc


# Logger:
import logging
from adplib.logger import Logger
logger= Logger.get_logger()

class group(dict): 

    def __init__(self, **kwargs):
        """
          Given a cube and a detection mask with source IDs, this code:
          - Creates a list of overlapping source pairs based on overlap criteria set by the user.
            Basic principle: two sources are deemed to be overlapping if, for both of them, the
            integral of a quantity X over the overlap area exceeds a fraction Xf of the integral
            over the source area. The quantity X is set by "overlap_mode" and can be "area",
            "flux" or "absflux". The threshold Xf is set by "overlap_thr" and is between 0 and 1.
          - Create groups of overlapping sources based on a network analysis. Basic principle: if
            sources A,B are an overlapping pair, and sources B,C are an overlapping pair, then
            A,B,C are a group independent of whether sources A,C are an overlapping pair.
          - Writes a new detection mask including grouped sources only, and where all sources in a
            group have the same ID.
        """

        super(group, self).__init__(**kwargs)
        self.__dict__ = self 


    def find_mask2d_sofia(self, mode=None):

        for single_qa_report in self.qa_report:
            # Verificar que el report sea del modo correcto
            if single_qa_report.get('mode') == mode:
                if 'outputs' in single_qa_report and 'images' in single_qa_report['outputs']:
                    # Buscar la imagen mask2d_sofia en este report específico
                    for image in single_qa_report['outputs']['images']:
                        if image['type'] == 'mask2d_sofia':
                            mask_path = image['path']
                            logger.info(f"Found 2D-mask from SoFiA for mode '{mode}': {mask_path}")
        
                            return mask_path
                        
        #logger.warning("No suitable 2D mask from SoFiA found. Skipping grouping.")
        logger.warning(
          f"No 2D-mask from SoFiA found for mode: '{mode}'. Group execution aborted"
          )
        return None
            

      
    def group_sofia_detections(self, cube_file, mask_file):

        print_all       = True      # prints overlap metrics for all source pairs;
                                    # if False, this info is only given for overlapping pairs
        writemask       = True      # writes new .FITS mask with grouped sources only
        overlap_mode = self.adpalmap_config.overlap_mode
        overlap_threshold = self.adpalmap_config.overlap_threshold

        if not cube_file.exists():
            logger.critical(
                f"The data cube '{cube_file}' does not exist. Fatal error. Please open an"
                " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
                "case.")
            return None
            
        if not mask_file.exists():
            logger.critical(
                f"The mask '{mask_file}' does not exist. Fatal error. Please open an"
                " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
                "case.")
            return None

        logger.info(f"Loading cube '{cube_file}'...")
        with fits.open(cube_file) as f:
            cub = f[0].data
        logger.info(f"Datacube '{cube_file}' opened")

        logger.info(f"Loading mask '{mask_file}'...")
        with fits.open(mask_file) as f:
            msk = f[0].data
            header = f[0].header
        logger.info(f"Mask '{mask_file}' opened")
        logger.info(f"Mask shape: {msk.shape}")
        logger.info(f"Cube shape: {cub.shape}")

        # If mask is 3D, collapse it to 2D by taking max along spectral axis. 
        # This should never happend because we manage the workflow of the pipeline, but just in case..
        if msk.ndim == 3:
            logger.info("Collapsing 3D mask to 2D...")
            msk_2d = msk.max(axis=0)
        else:
            msk_2d = msk

 
        logger.info("Creating integrated flux image from cube...")
        if cub.ndim == 3:
            flux_image = cub.sum(axis=0) 
        else:
            flux_image = cub

        logger.info("Finding unique source IDs...")
        unique_ids = np.unique(msk_2d)
        unique_ids = unique_ids[unique_ids > 0]  
        logger.info(f"Found source IDs: {unique_ids.tolist()}")


        logger.info("Precomputing source properties...")
        source_props = {}
        for source_id in unique_ids:
            
            source_mask = (msk_2d == source_id)
            
            # Calculate properties
            total_area = source_mask.sum()
            total_flux = (flux_image * source_mask).sum()
            total_absflux = np.abs(flux_image * source_mask).sum()
            
            source_props[source_id] = {
                'mask': source_mask,
                'total_area': total_area,
                'total_flux': total_flux,
                'total_absflux': total_absflux
            }

        # Clean up large arrays 
        del msk, msk_2d, flux_image
        gc.collect()

        # Loop over source pairs to find overlaps
        logger.info(f"Looking for source pairs with fractional {overlap_mode} overlap > {overlap_threshold:.2f} ...")
        logger.info(
           f"{'s1':>5s} {'s2':>5s} {'frac_area_1':>14s} {'frac_area_2':>14s} "
           f"{'frac_flux_1':>14s} {'frac_flux_2':>14s} {'frac_absflux_1':>14s} "
           f"{'frac_absflux_2':>14s}"
        )
        pairs = []
        ids = list(source_props.keys())

        for i, ii in enumerate(ids):
            for jj in ids[i+1:]:
                
                mask_ii = source_props[ii]['mask']
                mask_jj = source_props[jj]['mask']
                
                # Calculate overlap area
                overlap_mask = mask_ii & mask_jj
                overlap_area = overlap_mask.sum()
                
                if overlap_area == 0:
                    # No overlap, skip calculations
                    if print_all:
                        logger.info(
                            f"{ii:5d} {jj:5d} {0.0:14.2f} {0.0:14.2f} {0.0:14.2f} "
                            f"{0.0:14.2f} {0.0:14.2f} {0.0:14.2f}"
                        )
                    continue
                
                # Calculate fractional overlaps
                frac_area_ii = overlap_area / source_props[ii]['total_area']
                frac_area_jj = overlap_area / source_props[jj]['total_area']
                
                # For flux calculations, we need the flux image again temporarily
                with fits.open(cube_file) as f:
                    cub_temp = f[0].data
                    if cub_temp.ndim == 3:
                        flux_temp = cub_temp.sum(axis=0)
                    else:
                        flux_temp = cub_temp
                
                frac_flux_ii = (flux_temp * overlap_mask).sum() / source_props[ii]['total_flux'] if source_props[ii]['total_flux'] != 0 else 0
                frac_flux_jj = (flux_temp * overlap_mask).sum() / source_props[jj]['total_flux'] if source_props[jj]['total_flux'] != 0 else 0
                frac_absflux_ii = np.abs(flux_temp * overlap_mask).sum() / source_props[ii]['total_absflux'] if source_props[ii]['total_absflux'] != 0 else 0
                frac_absflux_jj = np.abs(flux_temp * overlap_mask).sum() / source_props[jj]['total_absflux'] if source_props[jj]['total_absflux'] != 0 else 0
                
                del cub_temp, flux_temp
                gc.collect()
                
                # Check overlap criteria
                paired = False
                if overlap_mode == 'area' and frac_area_ii > overlap_threshold and frac_area_jj > overlap_threshold:
                    paired = True
                elif overlap_mode == 'flux' and frac_flux_ii > overlap_threshold and frac_flux_jj > overlap_threshold:
                    paired = True
                elif overlap_mode == 'absflux' and frac_absflux_ii > overlap_threshold and frac_absflux_jj > overlap_threshold:
                    paired = True
                
                if paired:
                    logger.info(
                        f"{ii:5d} {jj:5d} {frac_area_ii:14.2f} {frac_area_jj:14.2f} {frac_flux_ii:14.2f} "
                        f"{frac_flux_jj:14.2f} {frac_absflux_ii:14.2f} {frac_absflux_jj:14.2f} (*)"
                    )
                    pairs.append((ii, jj))
                elif print_all:
                    logger.info(
                        f"{ii:5d} {jj:5d} {frac_area_ii:14.2f} {frac_area_jj:14.2f} {frac_flux_ii:14.2f} "
                        f"{frac_flux_jj:14.2f} {frac_absflux_ii:14.2f} {frac_absflux_jj:14.2f}"
                    )

        logger.info(f"Pairs = {pairs}")

        if pairs:
            groups_nx = nx.from_edgelist(pairs)
            groups = [tuple(gg) for gg in list(nx.connected_components(groups_nx))]
            logger.info(f"Groups = {groups}")
        else:
            groups = []
            logger.info("No overlapping pairs found.")

        if len(groups) and writemask:
            logger.info("Modifying mask in order to group sources and delete un-grouped sources ...")
            
            # Reload the original mask for modification
            with fits.open(mask_file) as f:
                msk_original = f[0].data
                header_original = f[0].header
            
            mask_out = Path(mask_file).parent / f"group_{Path(mask_file).name}"
            
            # Create a copy for output
            msk_new = msk_original.copy()
            
            # Process groups
            remaining_ids = set(ids)
            for gg in groups:
                logger.info(f" group: {gg}")
                group_id = min(gg)
                for source_id in gg:
                    if source_id in remaining_ids:
                        remaining_ids.remove(source_id)
                    if source_id != group_id:
                        logger.info(f"          {source_id} -> {group_id}")
                        if msk_new.ndim == 3:
                            msk_new[msk_new == source_id] = group_id
                        else:
                            msk_new[msk_new == source_id] = group_id
            
            # Remove ungrouped sources
            for source_id in remaining_ids:
                logger.info(f"  source {source_id} deleted")
                if msk_new.ndim == 3:
                    msk_new[msk_new == source_id] = 0
                else:
                    msk_new[msk_new == source_id] = 0
            
            fits.writeto(mask_out, msk_new, header=header_original, overwrite=True)
            logger.info(f"Written mask {mask_out}")

            return Path(mask_out)
        
        else:
            logger.warning("No sources to group")
            return None