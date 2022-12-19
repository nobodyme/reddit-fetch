
import sys, re
from fake_useragent import UserAgent

def get_valid_filename(s):
    ''' strips out special characters and replaces spaces with underscores, len 200 to avoid file_name_too_long error '''
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'[^\w.]', '', s)[:200]

def erase_previous_line():
    # cursor up one line
    # sys.stdout.write("\033[F")
    # # clear to the end of the line
    # sys.stdout.write("\033[K")
    return None

def get_userAgent():
    return UserAgent(fallback='Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11')