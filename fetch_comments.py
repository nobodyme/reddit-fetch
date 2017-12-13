#!/usr/bin/python3
from fake_useragent import UserAgent
import argparse
import sys
import json
import requests
import pprint
		
def get_response():
  url = sys.argv[1]
  ua = UserAgent()
  headers = {'User-agent': ua.random }
  print("Using header: ", headers)
  response = requests.get(url+'.json',headers=headers)
  if not response.ok:
    print ("Error ", response.status_code)
    exit(response.status_code)
  
  post_fetch = list()
  data = response.json()
  # pprint.pprint(data)
  title = data[0]['data']['children'][0]['data']['title']
  post_fetch.append(title+'\n\n')
  for i in range(0,len(data[1]['data']['children'])):
    post_fetch.append(data[1]['data']['children'][i]['data']['body']+'\n')
  return post_fetch

def main():

  output_filehandle = open("comments.txt",
                           mode = 'w',
                           encoding = 'utf8')
  top_level_comments = get_response()
  output_text = '\n'.join(top_level_comments)
  output_filehandle.write(output_text)
  output_filehandle.write('\n')

if __name__ == '__main__':
  main()
