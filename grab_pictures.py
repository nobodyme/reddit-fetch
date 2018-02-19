#!/usr/bin/python3

import json
import argparse
import requests
import os

parser = argparse.ArgumentParser(description='Fetch images from a subreddit')
parser.add_argument('-n', '--number', type=int, metavar='', default=50, help='Number of images to be downloaded (default=50)')
parser.add_argument('-s', '--subreddit', type=str, metavar='', required=True, help='Exact name of the subreddit')
args = parser.parse_args()

url = 'https://www.reddit.com/r/'
url = url + args.subreddit + '/top/.json?&limit=' + str(args.number)
response = requests.get(url, headers = {'User-agent':'firefox'})
    
if not response.ok:
    print("Error check the name of the subreddit", response.status_code)
    exit(response.status_code)

if not os.path.exists(args.subreddit):
    os.mkdir(args.subreddit)

count = 0

data = response.json()['data']['children']
for i in range(len(data)):
    current_post = data[i]['data']
    image_url = current_post['url']
    if '.png' in image_url:
        extension = '.png'
    elif '.jpg' or '.jpeg' in image_url:
        extension = '.jpeg'
    elif 'imgur' in image_url:
        image_url = image_url+'.jpeg'
    else:
        continue

    image = requests.get(image_url, allow_redirects=True)
    if(image.ok):
        output_filehandle = open(args.subreddit+ '/' + current_post['title'] + extension,
                                mode = 'wb')
        output_filehandle.write(image.content)
        count+=1

print('Total photos fetched' + str(count))
print('Unable to fetch' + str(len(data)-count))