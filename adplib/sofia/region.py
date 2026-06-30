import re

def parse_input_region(region_value, logger=None):
    """
    Parse a SoFiA input.region value as xmin, xmax, ymin, ymax, zmin, zmax.
    """

    if region_value is None:
        return None

    if isinstance(region_value, (list, tuple)):
        if len(region_value) < 6:
            if logger:
                logger.warning(f"Could not parse input.region from value: {region_value}")
            return None
        try:
            return tuple(int(value) for value in region_value[:6])
        except Exception as e:
            if logger:
                logger.warning(f"Could not parse input.region from value {region_value}: {e}")
            return None

    region_text = str(region_value).strip()
    if not region_text:
        return None

    values = [int(value) for value in re.findall(r"[-+]?\d+", region_text)]
    if len(values) < 6:
        if logger:
            logger.warning(f"Could not parse input.region from value: {region_value}")
        return None

    return tuple(values[:6])


def extract_input_region_from_header(header, logger):
    """
    Extract the last valid SoFiA input.region entry from a FITS header HISTORY.

    The expected SoFiA order is:
    xmin, xmax, ymin, ymax, zmin, zmax.
    """

    region = None

    try:
        history_lines = header["HISTORY"] if "HISTORY" in header else []
        if isinstance(history_lines, str):
            history_lines = [history_lines]

        for line in history_lines:
            line = str(line)
            match = re.search(r"\binput\.region\s*=\s*(.*)", line)
            if not match:
                continue

            parsed_region = parse_input_region(match.group(1))
            if parsed_region is not None:
                region = parsed_region

        if region is not None:
            logger.info(f"Found last input.region in HISTORY: {format_input_region(region)}")

    except Exception as e:
        logger.warning(f"Could not parse input.region from header HISTORY: {e}")

    return region


def normalize_input_region(region, data_shape, logger):
    """
    Normalize a SoFiA input.region for a numpy cube shape (nz, ny, nx).

    SoFiA regions are interpreted as xmin, xmax, ymin, ymax, zmin, zmax.
    Upper bounds are inclusive, except that a bound equal to the axis size is
    accepted and normalized to the last valid Python index.
    """

    if region is None:
        return None

    if len(data_shape) != 3:
        logger.warning(f"Cannot apply input.region to non-3D shape: {data_shape}")
        return None

    xmin, xmax, ymin, ymax, zmin, zmax = region
    nz, ny, nx = data_shape

    logger.info(
        (
            f"SoFiA input.region {format_input_region(region)} for cube shape "
            f"z={nz}, y={ny}, x={nx}"
        )
    )

    normalized = [xmin, xmax, ymin, ymax, zmin, zmax]
    axis_info = (
        ("x", 0, 1, nx),
        ("y", 2, 3, ny),
        ("z", 4, 5, nz),
    )

    for axis_name, min_index, max_index, axis_size in axis_info:
        axis_min = normalized[min_index]
        axis_max = normalized[max_index]

        if axis_max == axis_size:
            normalized[max_index] = axis_size - 1
            logger.info(
                (
                    f"Normalized input.region {axis_name} upper bound from "
                    f"{axis_max} to {axis_size - 1}"
                )
            )

        axis_max = normalized[max_index]
        if axis_min < 0 or axis_min >= axis_size:
            logger.warning(
                (
                    f"input.region {axis_name} lower bound {axis_min} is outside "
                    f"valid range [0, {axis_size - 1}]. Using full cube."
                )
            )
            return None

        if axis_max < 0 or axis_max >= axis_size:
            logger.warning(
                (
                    f"input.region {axis_name} upper bound {axis_max} is outside "
                    f"valid range [0, {axis_size - 1}]. Using full cube."
                )
            )
            return None

        if axis_min > axis_max:
            logger.warning(
                (
                    f"input.region {axis_name} lower bound {axis_min} is greater "
                    f"than upper bound {axis_max}. Using full cube."
                )
            )
            return None

    normalized_region = tuple(normalized)
    if normalized_region != tuple(region):
        logger.info(f"Normalized input.region to {format_input_region(normalized_region)}")

    return normalized_region


def apply_input_region_crop(data, region, logger):
    """
    Crop a 3D numpy cube using a SoFiA input.region.
    """

    normalized_region = normalize_input_region(region, data.shape, logger=logger)
    if normalized_region is None:
        return data

    xmin, xmax, ymin, ymax, zmin, zmax = normalized_region
    cropped = data[zmin:zmax + 1, ymin:ymax + 1, xmin:xmax + 1]
    logger.info(f"Cropped data to input.region. New shape: {cropped.shape}")
    return cropped


def format_input_region(region):
    xmin, xmax, ymin, ymax, zmin, zmax = region
    return f"x=[{xmin},{xmax}], y=[{ymin},{ymax}], z=[{zmin},{zmax}]"


def serialize_input_region(region):
    return ", ".join(str(value) for value in region)
