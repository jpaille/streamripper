import re

from utils import convert_string
from settings import metadata_parser


class MetadataParser():
    @staticmethod
    def parse(metadata):
        """Returns a tuple (artist, title)."""
        if metadata_parser == "HmrParser":
            return HmrParser.parse(metadata)

class HmrParser():
    """Parser for hotmix radio style metadata.

       Metadata :  "StreamTitle='title of the song - artist ||'
    """
    @staticmethod
    def parse(metadata):
        group_dict = re.search(r"^StreamTitle='(?P<title>.+?) - (?P<artist>.+?) \|", metadata).groupdict()
        return (group_dict["artist"], group_dict["title"]) if group_dict else (None, None)
