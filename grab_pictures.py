#!/usr/bin/python3
import argparse, colorama, os, requests, sys

from utils import get_valid_filename, erase_previous_line, get_userAgent


def get_pictures_from_subreddit(data, subreddit, dir_path, nsfw, filter_texts, current_downloaded_count, total_count_required):

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
        print(f'downloading pictures from r/{subreddit}.. {str((current_downloaded_count*100)//total_count_required)}%')

        # redirects = False prevents thumbnails denoting removed images from getting in
        image = requests.get(image_url, allow_redirects=False)
        if image.status_code == 200:
            try:
                output_filehandle = open(
                    f'{dir_path}/{get_valid_filename(current_post["title"])}{extension}', mode='bx')
                output_filehandle.write(image.content)
                current_downloaded_count += 1

                if current_downloaded_count >= total_count_required:
                    return current_downloaded_count

            except FileExistsError:
                pass
            except Exception as error:
                print(f'Error downloading images - {error}')
        
    return current_downloaded_count

def main():
    colorama.init()
    parser = argparse.ArgumentParser(
        description='Fetch images from a subreddit (eg: python3 grab_pictures.py -s itookapicture CozyPlaces -n 100 -t all)')
    parser.add_argument('-s', '--subreddits', nargs='+', type=str, metavar='',
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
    after = None
    

    for subreddit in args.subreddits:
        print(f'starting download')
        print(f'Connecting to r/{subreddit}')
        total_pictures_downloaded = 0
        
        while total_pictures_downloaded < args.number:
            
            url = f'https://www.reddit.com/r/{subreddit}/top/.json?sort=top&t={args.top}&limit={str(args.number + 10)}'

            if after:
                url = f'{url}&after={after}'

            response = requests.get(url, headers={'User-agent': ua.random})
            
            if not response.ok:
                print(f'Error connecting to subreddit r/{subreddit}. Please check the name of the subreddit {response.status_code}')
                exit()

            after = response.json()['data']['after']

            dir_path = os.path.join(args.location, subreddit)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            data = response.json()['data']['children']
            total_pictures_downloaded = get_pictures_from_subreddit(data, subreddit, dir_path, args.nsfw, args.filter_texts, total_pictures_downloaded, args.number)

        erase_previous_line()
        erase_previous_line()
        print(f'Downloaded {total_pictures_downloaded} pictures from r/{subreddit}')


if __name__ == '__main__':
    main()
