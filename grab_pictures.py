#!/usr/bin/python3

from fake_useragent import UserAgent
import argparse
import json
import os
import re
import requests


def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

ua = UserAgent()
parser = argparse.ArgumentParser(description='Fetch images from a subreddit')
parser.add_argument('-n', '--number', type=int, metavar='', default=50,
                    help='Number of images to be downloaded (default=50)')
parser.add_argument('-s', '--subreddit', type=str, metavar='',
                    required=True, help='Exact name of the subreddit')
parser.add_argument('-t', '--top', type=str, metavar='', choices=['day', 'week', 'month', 'year', 'all'],
                    default='week', help='optionally specify whether top posts of [day, week, month, year or all]')
args = parser.parse_args()

url = 'https://www.reddit.com/r/'
url = url + args.subreddit + '/top/.json?sort=top&t=' + \
    args.top + '&limit=' + str(args.number)
response = requests.get(url, headers={'User-agent': ua.random})

if not response.ok:
    print("Error check the name of the subreddit", response.status_code)
    exit(response.status_code)

if not os.path.exists(args.subreddit):
    os.mkdir(args.subreddit)

data = response.json()['data']['children']
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

    image = requests.get(image_url, allow_redirects=True)
    if(image.ok):
        output_filehandle = open(
            args.subreddit + '/' + get_valid_filename(current_post['title']) + extension, mode='wb')
        output_filehandle.write(image.content)
