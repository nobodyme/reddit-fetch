#!/usr/bin/python3

from fake_useragent import UserAgent
import argparse
import json
import os
import re
import requests
import sys


def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def erase_previous_line():
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")


def get_pictures_from_subreddit(data, subreddit):
    for i in range(len(data)):
        current_post = data[i]['data']
        image_url = current_post['url']
        if '.png' in image_url:
            extension = '.png'
        elif('.jpg' or '.jpeg') in image_url:
            extension = '.jpeg'
        elif 'imgur' in image_url:
            image_url = image_url+'.jpeg'
            extension = '.jpeg'
        else:
            continue

        # redirects = False prevents removed images from getting in
        image = requests.get(image_url, allow_redirects=False)
        if(image.status_code == 200):
            output_filehandle = open(
                subreddit + '/' + get_valid_filename(current_post['title']) + extension, mode='wb')
            output_filehandle.write(image.content)


def main():
    ua = UserAgent()
    parser = argparse.ArgumentParser(description='Fetch images from a subreddit')
    parser.add_argument('-s', '--subreddit', nargs='+', type=str, metavar='',
                        required=True, help='Exact name of the subreddits you want to grab pictures')
    parser.add_argument('-n', '--number', type=int, metavar='', default=50,
                        help='Optionally specify number of images to be downloaded (default=50)')
    parser.add_argument('-t', '--top', type=str, metavar='', choices=['day', 'week', 'month', 'year', 'all'],
                        default='week', help='optionally specify whether top posts of [day, week, month, year or all] (default=week)')
    args = parser.parse_args()

    for j in range(len(args.subreddit)):
        print('Connecting to r/' + args.subreddit[j])
        url = 'https://www.reddit.com/r/' + args.subreddit[j] + '/top/.json?sort=top&t=' + \
            args.top + '&limit=' + str(args.number)
        response = requests.get(url, headers={'User-agent': ua.random})

        if not response.ok:
            print("Error check the name of the subreddit", response.status_code)
            exit(response.status_code)

        if not os.path.exists(args.subreddit[j]):
            os.mkdir(args.subreddit[j])
        # notify connected and downloading pictures from subreddit
        erase_previous_line()
        print('downloading pictures from r/' + args.subreddit[j] + '..')

        data = response.json()['data']['children']
        get_pictures_from_subreddit(data,args.subreddit[j])
        erase_previous_line()
        print('Downloaded pictures from r/' + args.subreddit[j])


if __name__ == '__main__':
    main()