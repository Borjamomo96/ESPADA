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


    def find_mask_sofia(self, sopar=None, mode=None):
        
        if (hasattr(sopar , 'mask3d') 
        and getattr(sopar, 'mask3d') is not None
        ):
            mask = sopar.mask3d
            if mask.exists():
                logger.info(f"SoFiA mask found for '{mode}' mode: {mask}")
                return mask
            else:
                logger.critical(
                "The mask3d attribute does not exist, something went wrong. Please open an"
                " issue on https://github.com/Borjamomo96/ADP-ALMA-Pipeline.git with your specific "
                "case."
            )
                return None  
            
        else:
            logger.warning(f"SoFiA mask not found for '{mode}' mode in this run")
            logger.info(f"Trying to find a valid mask from previous runs")

            input_data = self.input_data.stem
            mask = (
                self.adpalmap_config.output_dir / f"espada_{input_data}"
                / f"{mode}_{input_data}_mask.fits"
            )
            
            if mask.exists():
                logger.info(f"SoFiA mask found from previous run for '{mode}' mode: {mask}")
                return mask
            else:
                logger.warning(f"SoFiA mask not found for '{mode}' mode from previous run")
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
        
        if cub.ndim == 4:
            cub = np.squeeze(cub, axis=0)
        elif cub.ndim > 4:
            logger.error("Too many dimensions")
            sys.exit(-1)

        logger.info(f"Loading mask '{mask_file}'...")
        with fits.open(mask_file) as f:
            msk_original = f[0].data  
            header = f[0].header
        logger.info(f"Mask '{mask_file}' opened")
        
        if msk_original.ndim == 4:
            msk_original = np.squeeze(msk_original, axis=0)
        elif msk_original.ndim > 4:
            logger.error("Too many dimensions")
            sys.exit(-1)

        msk_original = np.nan_to_num(msk_original, nan=0.0)
        cub = np.nan_to_num(cub, nan=0.0)

        logger.info(f"Mask shape: {msk_original.shape}")
        logger.info(f"Cube shape: {cub.shape}")

        # Find unique IDs in the mask
        logger.info("Finding unique source IDs...")
        unique_ids = np.unique(msk_original)
        unique_ids = unique_ids[unique_ids > 0]
        logger.info(f"Found source IDs: {unique_ids.tolist()}")

        # Create dictionary with source information - CORREGIDO
        logger.info("Precomputing source properties...")
        source_props = {}
        
        for source_id in unique_ids:

            source_mask = (msk_original == source_id)  # ✅ Nombre diferente
            
            # Calculate integrated properties along the spectral axis
            aper_2d = source_mask.sum(axis=0).astype(bool)
            imag_2d = np.nansum(cub * source_mask, axis=0)
            
            source_props[source_id] = {
                'mask': source_mask,      
                'aper_2d': aper_2d,     
                'imag_2d': imag_2d,      
                'total_area': aper_2d.sum(),
                'total_flux': np.nansum(imag_2d),
                'total_absflux': np.nansum(np.abs(imag_2d))
            }

        # Free memory
        del cub
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
                # Use built-in 2D apertures to calculate overlap
                aper_ii = source_props[ii]['aper_2d']
                aper_jj = source_props[jj]['aper_2d']
                imag_ii = source_props[ii]['imag_2d']
                imag_jj = source_props[jj]['imag_2d']

                
                # Calculate overlap area
                overlap = aper_ii & aper_jj
                overlap_area = overlap.sum()
              
                if overlap_area == 0:
                    if print_all:
                        logger.info(
                            f"{ii:5d} {jj:5d} {0.0:14.2f} {0.0:14.2f} {0.0:14.2f} "
                            f"{0.0:14.2f} {0.0:14.2f} {0.0:14.2f}"
                        )
                    continue
                
                # Calculate overlap fractions
                frac_area_ii = overlap_area / source_props[ii]['total_area']
                frac_area_jj = overlap_area / source_props[jj]['total_area']
                frac_flux_ii = (imag_ii * overlap).sum() / source_props[ii]['total_flux'] if source_props[ii]['total_flux'] != 0 else 0
                frac_flux_jj = (imag_jj * overlap).sum() / source_props[jj]['total_flux'] if source_props[jj]['total_flux'] != 0 else 0
                frac_absflux_ii = np.abs(imag_ii * overlap).sum() / source_props[ii]['total_absflux'] if source_props[ii]['total_absflux'] != 0 else 0
                frac_absflux_jj = np.abs(imag_jj * overlap).sum() / source_props[jj]['total_absflux'] if source_props[jj]['total_absflux'] != 0 else 0
                
                # Check overlap criteria
                paired = False
                if overlap_mode == 'area' and frac_area_ii > overlap_threshold and frac_area_jj > overlap_threshold:
                    paired = True
                elif overlap_mode == 'flux' and frac_flux_ii > overlap_threshold and frac_flux_jj > overlap_threshold:
                    paired = True
                elif overlap_mode == 'absflux' and frac_absflux_ii > overlap_threshold and frac_absflux_jj > overlap_threshold:
                    paired = True

                
                if paired:
                    logger.info(f"{ii:5d} {jj:5d} {frac_area_ii:14.2f} {frac_area_jj:14.2f} {frac_flux_ii:14.2f} {frac_flux_jj:14.2f} {frac_absflux_ii:14.2f} {frac_absflux_jj:14.2f} (*)")
                    pairs.append((int(ii), int(jj)))
                elif print_all:
                    logger.info(f"{ii:5d} {jj:5d} {frac_area_ii:14.2f} {frac_area_jj:14.2f} {frac_flux_ii:14.2f} {frac_flux_jj:14.2f} {frac_absflux_ii:14.2f} {frac_absflux_jj:14.2f}")

        logger.info(f"Pairs = {pairs}")

        if pairs:
            groups_nx = nx.from_edgelist(pairs)
            groups = [tuple(gg) for gg in list(nx.connected_components(groups_nx))]
            logger.info(f"Groups = {groups}")
        else:
            groups = []
            logger.warning("No overlapping pairs found.")

        if len(groups) and writemask:
            logger.info("Modifying mask in order to group sources and delete un-grouped sources...")
            
            # Usar msk_original en lugar de recargar el archivo
            mask_out = Path(mask_file).parent / f"group_{Path(mask_file).name}"
            msk_new = msk_original.copy()  
            
            remaining_ids = set(ids)
            for gg in groups:
                logger.info(f" group: {gg}")
                group_id = min(gg)
                for source_id in gg:
                    if source_id in remaining_ids:
                        remaining_ids.remove(source_id)
                    if source_id != group_id:
                        logger.info(f"          {source_id} -> {group_id}")
                        msk_new[msk_new == source_id] = group_id
            
            for source_id in remaining_ids:
                logger.info(f"  source {source_id} deleted")
                msk_new[msk_new == source_id] = 0
            
            if np.unique(msk_new[msk_new > 0]).shape[0] > len(groups):
                logger.error("The number of sources in the new mask is larger than the number of groups.")
                sys.exit(-1)

            fits.writeto(mask_out, msk_new, header=header, overwrite=True)
            logger.info(f"Written mask {mask_out}")
            return Path(mask_out)
        else:
            logger.warning("No sources to group")
            return None