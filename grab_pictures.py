#!/usr/bin/python3
import argparse, colorama, os, requests, sys

from utils import get_valid_filename, erase_previous_line, get_userAgent


def get_pictures_from_subreddit(data, subreddit, location, nsfw, filter_texts):
    for i in range(len(data)):
        if data[i]['data']['over_18']:
            # if nsfw post and you only want sfw
            if nsfw == 'n':
                continue
        else:
            # if sfw post and you only want nsfw
            if nsfw == 'x':
                continue

        current_post = data[i]['data']
        title = current_post['title'].lower()

        if filter_texts is not None and not any(map(lambda x: x.lower() in title, filter_texts)):
            continue

        image_url = current_post['url']
        if '.png' in image_url:
            extension = '.png'
        elif '.jpg' in image_url or '.jpeg' in image_url:
            extension = '.jpeg'
        elif 'imgur' in image_url:
            image_url += '.jpeg'
            extension = '.jpeg'
        else:
            continue

        erase_previous_line()
        print('downloading pictures from r/' + subreddit +
              '.. ' + str((i*100)//len(data)) + '%')

        # redirects = False prevents thumbnails denoting removed images from getting in
        image = requests.get(image_url, allow_redirects=False)
        if(image.status_code == 200):
            try:
                output_filehandle = open(
                    location + '/' + get_valid_filename(current_post['title']) + extension, mode='bx')
                output_filehandle.write(image.content)
            except:
                pass

def main():
    colorama.init()
    parser = argparse.ArgumentParser(
        description='Fetch images from a subreddit (eg: python3 grab_pictures.py -s itookapicture CozyPlaces -n 100 -t all)')
    parser.add_argument('-s', '--subreddit', nargs='+', type=str, metavar='',
                        required=True, help='Exact name of the subreddits you want to grab pictures')
    parser.add_argument('-n', '--number', type=int, metavar='', default=10,
                        help='Optionally specify number of images to be downloaded (default=10, maximum=1000)')
    parser.add_argument('-t', '--top', type=str, metavar='', choices=['day', 'week', 'month', 'year', 'all'],
                        default='week', help='Optionally specify whether top posts of [day, week, month, year or all] (default=week)')
    parser.add_argument('-loc', '--location', type=str, metavar='', default=os.getcwd() + '/images',
                        help='Optionally specify the directory/location to be downloaded')
    parser.add_argument('-x', '--nsfw', type=str, metavar='', default='y',
                        help='Optionally specify the behavior for handling NSFW content. y=yes download, n=no skip nsfw, x=only download nsfw content')
    parser.add_argument('-f', '--filter-texts', nargs='+', type=str, metavar='',
                        required=False, help='Optionally specify one or more of the given filter texts need to be included in title of the images (e.g. "digital").')
    args = parser.parse_args()

    # initializing userAgent
    ua = get_userAgent()

    global after
    after = ''

    number = args.number // 100

    if number == 0:
        number = 1

    for i in range(0, number):
        for j in range(len(args.subreddit)):

            print('starting download ' + str(i + 1))
            print('Connecting to r/' + args.subreddit[j])

            url = 'https://www.reddit.com/r/' + args.subreddit[j] + '/top/.json?sort=top&t=' + \
                args.top + '&limit=' + str(args.number)

            if after != '' and after != None:
                url = url + '&after=' + after

            response = requests.get(url, headers={'User-agent': ua.random})
            
            if not response.ok:
                print(f'Error connecting to subreddit r/{args.subreddit[j]}. Please check the name of the subreddit {response.status_code}')
                exit()

            after = response.json()['data']['after']

            location = os.path.join(args.location, args.subreddit[j])
            if not os.path.exists(location):
                os.makedirs(location)

            # notify connected and downloading pictures from subreddit
            erase_previous_line()
            print('downloading pictures from r/' + args.subreddit[j] + '..')

            data = response.json()['data']['children']
            get_pictures_from_subreddit(data, args.subreddit[j], location, args.nsfw, args.filter_texts)

            erase_previous_line()
            print('Downloaded pictures from r/' + args.subreddit[j])


if __name__ == '__main__':
    main()
