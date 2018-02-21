#!/usr/bin/python3

from fake_useragent import UserAgent
import argparse
import sys
import json
import requests



def get_response():

    ua = UserAgent()
    parser = argparse.ArgumentParser(
        description='Fetch top level comments from a reddit post')
    parser.add_argument('-l', '--link', type=str, metavar='',
                        required=True, help='Link of the post')
    parser.add_argument('-s', '--sort', type=str, metavar='', choices=[
                        'best', 'top', 'new'], default='confidence', help='optionally specify order of sort [best or top or new]')
    args = parser.parse_args()

    url = args.link + '.json?sort='
    if args.sort == 'best':
        args.sort = 'confidence'
    response = requests.get(url + args.sort, headers={'User-agent': ua.random})

    if not response.ok:
        print ("Error ", response.status_code)
        exit(response.status_code)

    post_fetch = list()
    data = response.json()
    title = data[0]['data']['children'][0]['data']['title']
    post_fetch.append(title+'\n\n')

    comment = data[1]['data']['children']
    for i in range(0, len(comment)):
        if 'body' in comment[i]['data'] and comment[i]['data']['body'] != '[deleted]':
            post_fetch.append(str(i+1) + '. ' +
                              comment[i]['data']['body']+'\n')
    return post_fetch


def main():

    output_filehandle = open("comments.txt",
                             mode='w',
                             encoding='utf8')
    top_level_comments = get_response()
    output_text = '\n'.join(top_level_comments)
    output_filehandle.write(output_text)
    output_filehandle.write('\n')


if __name__ == '__main__':
    main()
