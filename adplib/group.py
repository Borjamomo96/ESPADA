from astropy.io import fits
from astropy.table import Table
from copy import deepcopy
import networkx as netx
import numpy as np
from pathlib import Path
import sys
import gc
from adplib.sofia.region import (
    extract_input_region_from_header,
    format_input_region,
    normalize_input_region,
    parse_input_region,
)


# Logger:
import logging
from adplib.logger import Logger
logger= Logger.get_logger()


def _unavailable_grouping_summary(summary, message):
    """Keep group membership when final source IDs cannot be established."""
    result = deepcopy(summary)
    result['status'] = 'unavailable'
    result['final_source_count'] = None
    result['warnings'] = [message]
    for entry in result['groups']:
        entry.update(final_source_id=None, final_source_ids=[], status='unavailable')
    return result


def resolve_grouping_summary(
    summary, input_mask_file, output_mask_file, catalog_file, input_region=None,
    original_region=None,
):
    """Match original detections to final SoFiA groups using shared 3D voxels.

    The input is the original emission/absorption mask, not the grouped mask.
    ``input_region`` is the inclusive xyz region used by the grouped SoFiA
    execution. ``original_region`` describes an already cropped original mask;
    when omitted it is read from that mask's HISTORY.
    Splits, merges and missing catalogue IDs never receive an inferred link.
    """
    result = deepcopy(summary)
    if not result['groups']:
        return result

    try:
        catalogue = Table.read(catalog_file, format='votable')
        raw_ids = catalogue['id']
        catalog_ids = {int(value) for value in raw_ids}
        if (len(catalog_ids) != len(raw_ids)
                or any(value <= 0 for value in catalog_ids)
                or any(int(value) != value for value in raw_ids)):
            raise ValueError('The final catalogue contains invalid or duplicate source IDs.')

        label_to_ids = {entry['input_mask_label']: set() for entry in result['groups']}
        source_to_group = {
            int(source_id): entry['input_mask_label']
            for entry in result['groups'] for source_id in entry['original_ids']
        }
        id_to_labels = {}
        output_ids = set()

        with fits.open(input_mask_file, memmap=True) as input_hdul, \
                fits.open(output_mask_file, memmap=True) as output_hdul:
            before = input_hdul[0].data
            after = output_hdul[0].data
            if before.ndim == 4 and before.shape[0] == 1:
                before = before[0]
            if after.ndim == 4 and after.shape[0] == 1:
                after = after[0]
            if before.ndim != 3 or after.ndim != 3:
                raise ValueError('Grouping correspondence requires two 3D masks.')
            if not all(np.issubdtype(array.dtype, np.integer) for array in (before, after)):
                raise ValueError('Grouping correspondence requires integer source masks.')

            region = parse_input_region(input_region)
            if input_region is not None and str(input_region).strip() and region is None:
                raise ValueError('Cannot interpret the grouped SoFiA input.region.')
            if region is None and before.shape != after.shape:
                region = extract_input_region_from_header(output_hdul[0].header, logger)
            source_region = parse_input_region(original_region)
            if source_region is None:
                source_region = extract_input_region_from_header(input_hdul[0].header, logger)
            if source_region is not None:
                sxmin, sxmax, symin, symax, szmin, szmax = source_region
                if before.shape != (szmax - szmin + 1, symax - symin + 1,
                                    sxmax - sxmin + 1):
                    raise ValueError('Original mask shape does not match its input.region.')
                if region is None:
                    region = extract_input_region_from_header(output_hdul[0].header, logger)
                if region is None:
                    region = source_region
                # Translate global cube bounds to the original mask's local grid.
                xmin, xmax, ymin, ymax, zmin, zmax = region
                region = (xmin - sxmin, xmax - sxmin, ymin - symin,
                          ymax - symin, zmin - szmin, zmax - szmin)
            if region is not None:
                region = normalize_input_region(region, before.shape, logger)
                if region is None:
                    raise ValueError('The grouped SoFiA input.region is outside the input mask.')
                xmin, xmax, ymin, ymax, zmin, zmax = region
                before = before[zmin:zmax + 1, ymin:ymax + 1, xmin:xmax + 1]
            if before.shape != after.shape:
                raise ValueError('Input and output grouping masks cannot be aligned.')

            # Compare a plane at a time to avoid allocating another full cube.
            for input_plane, output_plane in zip(before, after):
                output_ids.update(int(value) for value in np.unique(output_plane)
                                  if value > 0)
                shared = (input_plane > 0) & (output_plane > 0)
                if not shared.any():
                    continue
                pairs = np.unique(np.column_stack(
                    (input_plane[shared], output_plane[shared])
                ), axis=0)
                for label, source_id in pairs:
                    label, source_id = int(label), int(source_id)
                    group_label = source_to_group.get(label)
                    if group_label is None:
                        continue  # Ungrouped detections do not define a group.
                    label_to_ids[group_label].add(source_id)
                    id_to_labels.setdefault(source_id, set()).add(group_label)

        result['final_source_count'] = len(catalog_ids)
        result['warnings'] = []
        if output_ids != catalog_ids:
            result['warnings'].append(
                'Final mask and catalogue source IDs differ; only verified matches are linked.'
            )
        unmatched = sorted(catalog_ids - set(id_to_labels))
        if unmatched:
            result['warnings'].append(
                f'Final sources with no overlap with the input groups: {unmatched}.'
            )

        for entry in result['groups']:
            candidates = sorted(label_to_ids[entry['input_mask_label']])
            entry['final_source_id'] = None
            entry['final_source_ids'] = candidates
            if not candidates:
                entry['status'] = 'not_recovered'
                result['warnings'].append(
                    f"Original sources {entry['original_ids']}: no surviving overlap "
                    'in the final mask.'
                )
            elif len(candidates) != 1 or len(id_to_labels[candidates[0]]) != 1:
                entry['status'] = 'ambiguous'
                result['warnings'].append(
                    f"Original sources {entry['original_ids']}: ambiguous final IDs {candidates}."
                )
            elif candidates[0] not in catalog_ids:
                entry['status'] = 'unavailable'
            else:
                entry['status'] = 'matched'
                entry['final_source_id'] = candidates[0]

        result['status'] = 'warning' if result['warnings'] else 'ok'
        return result
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return _unavailable_grouping_summary(
            result, f'Could not verify final grouping IDs: {exc}'
        )


class group(dict): 
    """
    Dictionary-backed helper for grouping overlapping SoFiA detections.
    """

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
        """
        Locate the SoFiA 3D mask for a run mode.

        Parameters
        ----------
        sopar : adplib.sofia.sopar.SoPar, optional
            SoFiA parameter object from the current run.
        mode : str, optional
            Run mode used to select the expected mask name.

        Returns
        -------
        pathlib.Path or None
            Path to the mask file if found.
        """

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
                " issue on https://github.com/Borjamomo96/ESPADA with your specific "
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
        """
        Group overlapping SoFiA detections and write a grouped mask.

        Parameters
        ----------
        cube_file : pathlib.Path
            Input cube used to compute source overlap metrics.
        mask_file : pathlib.Path
            SoFiA detection mask containing source IDs.

        Returns
        -------
        pathlib.Path or None
            Path to the grouped mask, or None when grouping cannot be performed.
        """

        print_all       = True      # prints overlap metrics for all source pairs;
                                    # if False, this info is only given for overlapping pairs
        writemask       = True      # writes new .FITS mask with grouped sources only
        overlap_mode = self.adpalmap_config.overlap_mode
        overlap_threshold = self.adpalmap_config.overlap_threshold
        self.input_region_from_mask = None
        self.normalized_input_region_from_mask = None
        self.grouping_summary = None

        if not cube_file.exists():
            logger.critical(
                f"The data cube '{cube_file}' does not exist. Fatal error. Please open an"
                " issue on https://github.com/Borjamomo96/ESPADA.git with your specific "
                "case.")
            return None
            
        if not mask_file.exists():
            logger.critical(
                f"The mask '{mask_file}' does not exist. Fatal error. Please open an"
                " issue on https://github.com/Borjamomo96/ESPADA.git with your specific "
                "case.")
            return None

        
        
        mask_file_header = fits.Header() # Genetic header to avoid secondary errors

        # Load mask
        logger.info(f"Loading mask '{mask_file}'...")
        with fits.open(mask_file, mmap=True) as f:
            mask = f[0].data
            mask_file_header = f[0].header.copy()
        logger.info(f"Mask '{mask_file}' opened")

        if mask.ndim == 4:
            mask = np.squeeze(mask, axis=0)
        elif mask.ndim > 4:
            logger.error(f"Too many dimensions for the: {mask_file}")
            sys.exit(-1)
        elif mask.ndim != 3:
            logger.error(f"Unexpected cube dimensions: {mask.ndim}. Expected 3D.")
            return None

        # Load cube
        logger.info(f"Loading cube '{cube_file}'...")
        with fits.open(cube_file) as f:
            data = f[0].data
            cube_file_header = f[0].header.copy()
        logger.info(f"Datacube '{cube_file}' opened")

        if data.ndim == 4 and data.shape[0] == 1:
            data = np.squeeze(data, axis=0)
        elif data.ndim > 4:
            logger.error(f"Too many dimensions for the: {cube_file}")
            sys.exit(-1)
        elif data.ndim != 3:
            logger.error(f"Unexpected cube dimensions: {data.ndim}. Expected 3D.")
            return None
        
        full_cube_shape = data.shape

        # Extract region from SoFiA mask header
        region = extract_input_region_from_header(mask_file_header, logger=logger)
        self.input_region_from_mask = region
        normalized_region = None
        
        # Crop the cube according to the SoFiA region, if it exists.
        if region is not None:
            normalized_region = normalize_input_region(region, data.shape, logger=logger)
            self.normalized_input_region_from_mask = normalized_region
            if normalized_region is not None:
                xmin, xmax, ymin, ymax, zmin, zmax = normalized_region
                data = data[zmin:zmax + 1, ymin:ymax + 1, xmin:xmax + 1]
                logger.info(f"Cropped data to input.region. New shape: {data.shape}")


        mask = np.nan_to_num(mask, nan=0.0)
        data = np.nan_to_num(data, nan=0.0)

        
        if data.shape != mask.shape:
            logger.error(
                f"Shape mismatch after cropping: data {data.shape} vs mask {mask.shape}. "
                "Cannot proceed."
            )
            return None

        logger.info(f"Mask shape: {mask.shape}")
        logger.info(f"Cube shape: {data.shape}")

        # Find unique IDs in the mask
        logger.info("Finding unique source IDs...")
        unique_ids = np.unique(mask)
        unique_ids = unique_ids[unique_ids > 0]
        logger.info(f"Found source IDs: {unique_ids.tolist()}")

        # Create dictionary with source information
        logger.info("Precomputing source properties...")
        source_props = {}
        z_offset = normalized_region[4] if normalized_region is not None else 0

        for source_id in unique_ids:
            source_mask = (mask == source_id)
            occupied_channels = np.flatnonzero(source_mask.any(axis=(1, 2)))
            aper_2d = source_mask.sum(axis=0).astype(bool)
            imag_2d = np.nansum(data * source_mask, axis=0)
            source_props[source_id] = {
                'mask': source_mask,
                'z_min': int(occupied_channels[0]) + z_offset,
                'z_max': int(occupied_channels[-1]) + z_offset,
                'aper_2d': aper_2d,
                'imag_2d': imag_2d,
                'total_area': aper_2d.sum(),
                'total_flux': np.nansum(imag_2d),
                'total_absflux': np.nansum(np.abs(imag_2d))
            }

        # Free memory
        del data
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
            groups_nx = netx.from_edgelist(pairs)
            groups = [tuple(gg) for gg in list(netx.connected_components(groups_nx))]
            logger.info(f"Groups = {groups}")
        else:
            groups = []
            logger.warning("No overlapping pairs found.")

        grouped_ids = {int(source_id) for members in groups for source_id in members}
        self.grouping_summary = {
            'input_source_count': len(ids),
            'grouped_source_count': len(grouped_ids),
            'group_count': len(groups),
            'final_source_count': None if groups else 0,
            'ungrouped_source_ids': sorted(int(source_id) for source_id in ids
                                         if int(source_id) not in grouped_ids),
            'overlap_mode': overlap_mode,
            'overlap_threshold': float(overlap_threshold),
            'spectral_coordinates': {
                'axis': 'z', 'index_base': 0, 'bounds': 'inclusive',
                'reference': 'original_cube',
            },
            'status': 'pending' if groups else 'no_groups',
            'warnings': [],
            'groups': [
                {'input_mask_label': int(min(members)),
                 'original_ids': sorted(int(value) for value in members),
                 'members': [
                     {'source_id': int(value),
                      'z_min': source_props[value]['z_min'],
                      'z_max': source_props[value]['z_max']}
                     for value in sorted(members)
                 ],
                 'final_source_id': None, 'final_source_ids': [], 'status': 'pending'}
                for members in sorted(groups, key=min)
            ],
        }

        if len(groups) and writemask:
            logger.info("Modifying mask in order to group sources and delete un-grouped sources...")
            
            # Reuse the in-memory mask instead of reloading the file.
            # SoFiA may overwrite this with its final mask. Correspondence is
            # recovered from the original detections, which remain untouched.
            mask_out = Path(mask_file).parent / f"group_{Path(mask_file).name}"
            msk_new = mask.copy()  
            
            remaining_ids = set(ids)
            for gg in groups:
                logger.info(f"Original sources {sorted(gg)} -> input mask label {min(gg)}")
                group_id = min(gg)
                for source_id in gg:
                    props = source_props[source_id]
                    logger.info(
                        f"Original source {source_id}: channels {props['z_min']}..{props['z_max']} "
                        '(zero-based, inclusive, original cube).'
                    )
                    if source_id in remaining_ids:
                        remaining_ids.remove(source_id)
                    if source_id != group_id:
                        logger.debug(f"Input mask relabel: {source_id} -> {group_id}")
                        msk_new[msk_new == source_id] = group_id
            
            for source_id in remaining_ids:
                logger.info(f"  source {source_id} deleted")
                msk_new[msk_new == source_id] = 0
            
            if np.unique(msk_new[msk_new > 0]).shape[0] > len(groups):
                logger.error("The number of sources in the new mask is larger than the number of groups.")
                sys.exit(-1)

            mask_to_write = msk_new
            mask_header_to_write = mask_file_header

            if normalized_region is not None:
                xmin, xmax, ymin, ymax, zmin, zmax = normalized_region
                region_shape = (
                    zmax - zmin + 1,
                    ymax - ymin + 1,
                    xmax - xmin + 1,
                )

                if msk_new.shape != region_shape:
                    logger.error(
                        (
                            "Cannot expand grouped mask to full cube shape. "
                            f"Grouped mask shape {msk_new.shape} does not match "
                            f"input.region shape {region_shape}."
                        )
                    )
                    return None

                logger.info(
                    (
                        "Expanding grouped mask from input.region "
                        f"{format_input_region(normalized_region)} shape "
                        f"{msk_new.shape} to full cube shape {full_cube_shape}"
                    )
                )
                mask_to_write = np.zeros(full_cube_shape, dtype=msk_new.dtype)
                mask_to_write[zmin:zmax + 1, ymin:ymax + 1, xmin:xmax + 1] = msk_new
                mask_header_to_write = cube_file_header
                mask_header_to_write.add_history(
                    (
                        "ESPADA expanded grouped mask to the original cube shape "
                        f"from input.region {format_input_region(normalized_region)}"
                    )
                )

            fits.writeto(mask_out, mask_to_write, header=mask_header_to_write, overwrite=True)
            logger.info(f"Written mask {mask_out}")
            return Path(mask_out)
        else:
            logger.warning("No sources to group")
            return None


    def resolve_sofia_groups(self, original_mask_file, sopar, sofia_report):
        """Resolve and log a completed grouped run without aborting its products."""
        if self.grouping_summary is None:
            return None
        if sofia_report.get('error') or sofia_report.get('exit_code', 0) != 0:
            resolved = _unavailable_grouping_summary(
                self.grouping_summary,
                'The grouped SoFiA run did not complete; final source IDs are unavailable.',
            )
        else:
            base = Path(sopar.output_directory) / sopar.output_filename
            resolved = resolve_grouping_summary(
                self.grouping_summary, original_mask_file,
                Path(f'{base}_mask.fits'), Path(f'{base}_cat.xml'),
                input_region=getattr(sopar, 'input_region', None),
                original_region=getattr(self, 'normalized_input_region_from_mask', None),
            )
        # Existing worker metadata points to this dictionary. Keep that reference
        # while the same helper may subsequently process the other run mode.
        self.grouping_summary.clear()
        self.grouping_summary.update(resolved)
        for entry in resolved['groups']:
            if entry['status'] == 'matched':
                logger.info(
                    f"Grouped source {entry['final_source_id']} <- original sources "
                    f"{entry['original_ids']} (input mask label {entry['input_mask_label']}). "
                    f"Mode: {sopar.mode}."
                )
        for warning in resolved['warnings']:
            logger.warning(f'Grouping summary ({sopar.mode}): {warning}')
        return resolved


    def summary_report(self, mode):
        """Expose grouping metadata through the existing worker result tuple."""
        return {
            'software_id': 'Grouping',
            'input_path': str(self.input_data),
            'input_name': Path(self.input_data).stem,
            'mode': mode,
            'grouping_summary': self.grouping_summary,
        }
