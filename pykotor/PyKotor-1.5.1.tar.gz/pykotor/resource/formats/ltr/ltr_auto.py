from pykotor.resource.formats.ltr.io_ltr import LTRBinaryReader, LTRBinaryWriter
from pykotor.resource.formats.ltr.ltr_data import LTR
from pykotor.resource.type import SOURCE_TYPES, TARGET_TYPES, ResourceType


def read_ltr(
        source: SOURCE_TYPES,
        offset: int = 0,
        size: int = None
) -> LTR:
    """
    Returns an LTR instance from the source.

    Args:
        source: The source of the data.
        offset: The byte offset of the file inside the data.
        size: Number of bytes to allowed to read from the stream. If not specified, uses the whole stream.

    Raises:
        ValueError: If the file was corrupted or in an unsupported format.

    Returns:
        An LTR instance.
    """
    try:
        return LTRBinaryReader(source, offset, size).load()
    except (IOError, ValueError):
        raise ValueError("Tried to load an unsupported or corrupted LTR file.")


def write_ltr(
        ltr: LTR,
        target: TARGET_TYPES,
        file_format: ResourceType = ResourceType.LTR
) -> None:
    """
    Writes the LTR data to the target location with the specified format (LTR only).

    Args:
        ltr: The LTR file being written.
        target: The location to write the data to.
        file_format: The file format.

    Raises:
        ValueError: If an unsupported file format was given.
    """
    if file_format == ResourceType.LTR:
        LTRBinaryWriter(ltr, target).write()
    else:
        raise ValueError("Unsupported format specified; use LTR.")


def bytes_ltr(
        ltr: LTR,
        file_format: ResourceType = ResourceType.LTR
) -> bytes:
    """
    Returns the LTR data in the specified format (LTR only) as a bytes object.

    This is a convience method that wraps the write_ltr() method.

    Args:
        ltr: The target LTR object.
        file_format: The file format.

    Raises:
        ValueError: If an unsupported file format was given.

    Returns:
        The LTR data.
    """
    data = bytearray()
    write_ltr(ltr, data, file_format)
    return data
