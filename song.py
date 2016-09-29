import os

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, error, TPE1, TIT2

from utils import get_log_time

class Song(object):
    artist = None
    title = None
    filename = None
    full_path_song = None
    data = ""

    def __init__(self, artist, title,
                 cut_begining=0, cut_end=0, min_song_duration=60,
                 byterate=1000, base_directory=".",
                 first_song=False):

        self.artist = artist
        self.title = title
        self.cut_begining = cut_begining
        self.cut_end = cut_end
        self.min_song_duration = min_song_duration
        self.byterate = byterate
        self.base_directory = base_directory
        self.first_song = first_song

        if not self.artist and not self.title:
            print u"{} Skipping...".format(get_log_time())
        else:
            self.filename = u"{} - {}.mp3".format(self.artist, self.title)
            self.full_path_song = os.path.join(self.base_directory, self.filename)
            print u"{} Ripping  {}".format(get_log_time(), self.filename)

    def _is_song_valid(self):
        if not self.artist or not self.title:
            return False
        elif os.path.exists(self.full_path_song):
            print u"{} Skip song {} already exist.".format(get_log_time(), self.filename)
            return False
        elif self.first_song:
            print u"{} Skip song {} may be incomplete because it's the first recorded .".format(get_log_time(),
                                                                                                self.filename)
            return False
        elif self.get_length_in_seconds() < self.min_song_duration:
            print u"{} Skip song {} is under {} seconds.".format(get_log_time(), self.filename, self.min_song_duration)
            return False
        return True

    def save(self):
        """ Save song in base_directory.
        Except : - If the song already exist.
                 - If the song has no metadata (title and artist)
                 - If this is the first recorded song, the begining may be skipped.
                 - If the song is inferior to self.min_song_duration seconds.
        """
        if self._is_song_valid():
            with open(self.full_path_song, "w+") as mp3_file:
                print u"{} Song {} successfully saved.".format(get_log_time(), self.filename)
                self.cut_song()
                mp3_file.write(self.data)
            self.add_id3_tags()

    def cut_song(self):
        """Cut begining and end of the song.

        This is used to remove the radio jingle song.
        Use command line parameters to get the cutting limits.
        """
        if self.cut_end == 0:
            self.data = self.data[self.cut_begining * self.byterate:]
        else:
            self.data = self.data[self.cut_begining * self.byterate :-self.cut_end * self.byterate]


    def add_id3_tags(self):
        audio = MP3(self.full_path_song, ID3=ID3)
        try:
            audio.add_tags()
        except error:
            pass
        audio.tags.add(TIT2(encoding=3, text=self.title))
        audio.tags.add(TPE1(encoding=3, text=self.artist))
        audio.save()

    def get_length_in_seconds(self):
        return len(self.data) / self.byterate
