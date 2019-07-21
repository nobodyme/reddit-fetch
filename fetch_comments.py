#!/usr/bin/python3

from fake_useragent import UserAgent
import argparse
import colorama
import json
import re
import requests
import sys
import os


def get_valid_filename(s):
    ''' strips out special characters and replaces spaces with underscores, len 200 to avoid file_name_too_long error '''
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'[^\w.]', '', s)[:200]


def erase_previous_line():
    # cursor up one line
    sys.stdout.write("\033[F")
    # clear to the end of the line
    sys.stdout.write("\033[K")


def get_response(url, ua):
    response = requests.get(url, headers={'User-agent': ua.random})

    if not response.ok:
        print("Error ", response.status_code)
        exit()

    erase_previous_line()
    print('Downloading comments..')

    post_fetch = list()
    data = response.json()
    title = data[0]['data']['children'][0]['data']['title']
    post_fetch.append(title+'\n\n')

    comment = data[1]['data']['children']
    for i in range(len(comment)):
        if 'body' in comment[i]['data'] and comment[i]['data']['body'] != '[deleted]':
            post_fetch.append(str(i+1) + '. ' +
                              comment[i]['data']['body']+'\n')
    return post_fetch


def main():
    colorama.init()
    ua = UserAgent()
    parser = argparse.ArgumentParser(
        description='Fetch top level comments from a reddit post (eg: python3 fetch_comments.py -l https://www.reddit.com/r/AskReddit/comments/75goki/whats_a_movie_to_watch_when_you_want_a_good_cry/)')
    parser.add_argument('-l', '--link', type=str, metavar='',
                        required=True, help='Link of the post')
    parser.add_argument('-s', '--sort', type=str, metavar='', choices=[
                        'best', 'top', 'new'], default='confidence', help='Optionally specify order of sort [best or top or new]')
    parser.add_argument('-loc', '--location', type=str, metavar='', default='',
                        help='Optionally specify the directory/location to be downloaded')
    args = parser.parse_args()

    print('Connecting to reddit..')
    url = args.link + '.json?sort='
    if args.sort == 'best':
        args.sort = 'confidence'

    top_level_comments = get_response(
        url + args.sort, ua)

    filename = get_valid_filename(top_level_comments[0]) + "_comments.txt"

    if args.location:
        if os.path.exists(args.location):
            location = os.path.join(
                args.location, filename)
        else:
            print('Given path does not exist, try without the location parameter to default to the current directory')
            exit(1)
    else:
        location = filename

    output_filehandle = open(location, mode='w', encoding='utf8')
    output_text = '\n'.join(top_level_comments)
    output_filehandle.write(output_text)
    output_filehandle.write('\n')
    erase_previous_line()
    print('Downloaded comments')


if __name__ == '__main__':
    main()
