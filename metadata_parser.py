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
        metadata = metadata[13:] ## remove StreamTitle string
        limit_end_artist = metadata.find(" - ")
        if limit_end_artist == -1:
            artist = None
            title = None
        else:
            artist = metadata[:limit_end_artist]
            limit_end_title = metadata.find("||")
            title =  metadata[limit_end_artist + 3 : limit_end_title].strip()
            title = convert_string(title)
            artist = convert_string(artist)
        return (artist, title)
    
    
