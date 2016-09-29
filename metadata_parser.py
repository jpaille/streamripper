import re

class MetadataParser(object):

    def parse(self, metadata):
        """
        Parse stream metadata.

        Args:
            metadata (str)

        Returns:
            A tuple (Artist (str), Title (str)) if found. Returns (None, None) otherwise.
        """
        raise NotImplementedError

class HotmixradioParser(MetadataParser):
    """Parser for hotmix radio style metadata.
       Hotmixradio metadata format is "StreamTitle='title of the song - artist ||'.
    """

    def parse(self, metadata):
        group_dict = re.search(r"^StreamTitle='(?P<title>.+?) - (?P<artist>.+?) \|", metadata).groupdict()
        return (group_dict["artist"], group_dict["title"]) if group_dict else (None, None)

metadata_parsers = {"Hotmixradio" : HotmixradioParser}
