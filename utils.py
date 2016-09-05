import datetime

def get_log_time():
    return datetime.datetime.now().strftime("[%d/%m/%y - %Hh%M %Ss]")

def convert_string(string):
    string_unicode = u""
    for ca in string:
        char = ord(ca)
        string_unicode += unichr(char)
    return string_unicode
