#!/usr/bin/python3

import argparse, colorama, os, requests

from utils import get_valid_filename, erase_previous_line, get_userAgent


def get_comments(url, ua):
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
    parser = argparse.ArgumentParser(
        description='Fetch top level comments from a reddit post (eg: python3 fetch_comments.py -l https://www.reddit.com/r/AskReddit/comments/75goki/whats_a_movie_to_watch_when_you_want_a_good_cry/)')
    parser.add_argument('-l', '--link', type=str, metavar='',
                        required=True, help='Link of the post')
    parser.add_argument('-s', '--sort', type=str, metavar='', choices=[
                        'best', 'top', 'new'], default='confidence', help='Optionally specify order of sort [best or top or new]')
    parser.add_argument('-loc', '--location', type=str, metavar='', default=os.getcwd() + '/comments',
                        help='Optionally specify the directory/location to be downloaded')
    args = parser.parse_args()

    # initializing userAgent
    ua = get_userAgent()

    print('Connecting to reddit..')
    url = args.link + '.json?sort='
    if args.sort == 'best':
        args.sort = 'confidence'

    top_level_comments = get_comments(
        url + args.sort, ua)

    filename = get_valid_filename(top_level_comments[0]) + "_comments.txt"

    if not os.path.exists(args.location):
        os.makedirs(args.location)

    location = os.path.join(args.location, filename)
    output_filehandle = open(location, mode='w', encoding='utf8')
    output_text = '\n'.join(top_level_comments)
    output_filehandle.write(output_text)
    output_filehandle.write('\n')
    erase_previous_line()
    print('Downloaded comments')


if __name__ == '__main__':
    main()
