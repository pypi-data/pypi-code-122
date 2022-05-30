from pykotor.common.stream import BinaryReader
from pykotor.resource.formats.tlk import TLK, TLKBinaryReader, TLKXMLReader, TLKBinaryWriter
from pykotor.resource.formats.tlk.io_tlk_json import TLKJSONReader, TLKJSONWriter
from pykotor.resource.formats.tlk.io_tlk_xml import TLKXMLWriter
from pykotor.resource.type import SOURCE_TYPES, TARGET_TYPES, ResourceType


def detect_tlk(
        source: SOURCE_TYPES,
        offset: int = 0
) -> ResourceType:
    """
    Returns what format the TLK data is believed to be in. This function performs a basic check and does not guarantee
    accuracy of the result or integrity of the data.

    Args:
        source: Source of the TLK data.
        offset: Offset into the data.

    Raises:
        FileNotFoundError: If the file could not be found.
        IsADirectoryError: If the specified path is a directory (Unix-like systems only).
        PermissionError: If the file could not be accessed.

    Returns:
        The format of the TLK data.
    """

    def check(
            first4
    ):
        if first4 == "TLK ":
            return ResourceType.TLK
        elif "{" in first4:
            return ResourceType.TLK_JSON
        elif "<" in first4:
            return ResourceType.TLK_XML
        else:
            return ResourceType.INVALID

    try:
        if isinstance(source, str):
            with BinaryReader.from_file(source, offset) as reader:
                file_format = check(reader.read_string(4))
        elif isinstance(source, bytes) or isinstance(source, bytearray):
            file_format = check(source[:4].decode('ascii', 'ignore'))
        elif isinstance(source, BinaryReader):
            file_format = check(source.read_string(4))
            source.skip(-4)
        else:
            file_format = ResourceType.INVALID
    except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
        raise e
    except IOError:
        file_format = ResourceType.INVALID

    return file_format


def read_tlk(
        source: SOURCE_TYPES,
        offset: int = 0,
        size: int = None
) -> TLK:
    """
    Returns an TLK instance from the source. The file format (TLK, TLK_XML or TLK_JSON) is automatically determined
    before parsing the data.

    Args:
        source: The source of the data.
        offset: The byte offset of the file inside the data.
        size: Number of bytes to allowed to read from the stream. If not specified, uses the whole stream.

    Raises:
        FileNotFoundError: If the file could not be found.
        IsADirectoryError: If the specified path is a directory (Unix-like systems only).
        PermissionError: If the file could not be accessed.
        ValueError: If the file was corrupted or the format could not be determined.

    Returns:
        An TLK instance.
    """
    file_format = detect_tlk(source, offset)

    if file_format is ResourceType.INVALID:
        raise ValueError("Failed to determine the format of the GFF file.")

    if file_format == ResourceType.TLK:
        return TLKBinaryReader(source, offset, size).load()
    elif file_format == ResourceType.TLK_XML:
        return TLKXMLReader(source, offset, size).load()
    elif file_format == ResourceType.TLK_JSON:
        return TLKJSONReader(source, offset, size).load()


def write_tlk(
        tlk: TLK,
        target: TARGET_TYPES,
        file_format: ResourceType = ResourceType.TLK
) -> None:
    """
    Writes the TLK data to the target location with the specified format (TLK, TLK_XML or TLK_JSON).

    Args:
        tlk: The TLK file being written.
        target: The location to write the data to.
        file_format: The file format.

    Raises:
        IsADirectoryError: If the specified path is a directory (Unix-like systems only).
        PermissionError: If the file could not be written to the specified destination.
        ValueError: If the specified format was unsupported.
    """
    if file_format == ResourceType.TLK:
        TLKBinaryWriter(tlk, target).write()
    elif file_format == ResourceType.TLK_XML:
        TLKXMLWriter(tlk, target).write()
    elif file_format == ResourceType.TLK_JSON:
        TLKJSONWriter(tlk, target).write()
    else:
        raise ValueError("Unsupported format specified; use TLK or TLK_XML.")


def bytes_tlk(
        tlk: TLK,
        file_format: ResourceType = ResourceType.TLK
) -> bytes:
    """
    Returns the TLK data in the specified format (TLK or TLK_XML or TLK_JSON) as a bytes object.

    This is a convience method that wraps the write_tlk() method.

    Args:
        tlk: The target TLK object.
        file_format: The file format.

    Raises:
        ValueError: If the specified format was unsupported.

    Returns:
        The TLK data.
    """
    data = bytearray()
    write_tlk(tlk, data, file_format)
    return data
