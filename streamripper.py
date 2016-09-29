# -*- coding: utf-8 -*-

import argparse
from copy import deepcopy
import sys
from threading import Thread
import requests

from metadata_parser import metadata_parsers
from settings import radio_parser_style
from song import Song
from utils import get_log_time

class NoDataReceivedError(Exception):
    """Exception raised when request.raw.read() returns
       an empty string.
    """
    pass

parser = argparse.ArgumentParser(description='Record radio streams.')
parser.add_argument("url", metavar="URL", help="Radio stream URL.")
parser.add_argument("-d", dest="base_directory", help="Select a different base directory for ripping.", default=".")
parser.add_argument("--cut-begining", type=int, default=0,
                    help="Number of seconds to cut at the begining.")
parser.add_argument("--cut-end", type=int, default=0,
                    help="Number of seconds to cut at the end.")
parser.add_argument("--min-song-duration", type=int, default=60,
                    help="Minimum song duration in seconds.")
parser.add_argument("--record-first-song", action="store_true",
                    help="""You will be probably starting recording at the middle of a song so the first song
                            is usually incomplete. Use this option if you still want to record it.""")
parser.add_argument("-u", dest="user_agent", action="store_true", default="streamripper",
                    help="""Use a different UserAgent than "Streamripper"
                            In the http request, streamripper includes a string that identifies what
                            kind of program is requesting the connection. By default it is the string
                            "Streamripper". Here you can decide to identify yourself as a different
                            agent if you like.""")
args = parser.parse_args()


def save_song(song):
    """Call song.save() asynchronously."""
    old_song = deepcopy(song)
    Thread(target=old_song.save).start()

def build_header():
    """Build a custom header"""
    headers = {"User-Agent": args.user_agent,
               'Icy-MetaData': 1}
    return headers

def get_metadata_length(stream):
    byte_length = stream.raw.read(1)
    if byte_length == "":
        raise NoDataReceivedError
    return ord(byte_length) * 16

def print_stream_info(stream):
    print "stream: {}".format(stream.headers['icy-name'])
    print "server name: {}".format(stream.headers['Server'])
    print "declared bitrate: {}".format(stream.headers['icy-br'])
    print "meta interval: {}".format(stream.headers['icy-metaint'])

if __name__ == "__main__":
    """Main recording loop. For more information on the shoutcast protocol, check this nice
       tutorial http://www.smackfu.com/stuff/programming/shoutcast.html"""

    print "Connecting..."
    stream = requests.get(args.url, stream=True,
                          headers=build_header())
    print_stream_info(stream)

    block_size = int(stream.headers["icy-metaint"])
    byterate = int(stream.headers["icy-br"][:3]) * 1000 / 8
    song = None
    is_first_song = False if args.record_first_song else True

    try:
        while 42:
            mp3_bytes = stream.raw.read(block_size)
            try:
                metadata_length = get_metadata_length(stream)
            except NoDataReceivedError:
                print "{} Request.raw.read returned an empty string. Process end.".format(get_log_time())
                raise RuntimeError
            if metadata_length: ## we receive metadata from stream: a new song is coming.
                if song:
                    save_song(song) ## save the current song.
                    is_first_song = False
                artist, title = metadata_parsers[radio_parser_style]().parse(stream.raw.read(metadata_length))
                song = Song(artist, title,
                            args.cut_begining, args.cut_end, args.min_song_duration,
                            byterate, args.base_directory, is_first_song) ## create a new song.
            song.data += mp3_bytes
    except KeyboardInterrupt:
        sys.exit()
