#!/usr/bin/python3

import argparse
import sys
import json
import requests
		
def get_response():
		
  url = sys.argv[1]
  response = requests.get(url+'.json',headers = {'User-agent':'bot'})
		
  if not response.ok:
    print ("Error ", response.status_code)
    exit(response.status_code)
  
  post_fetch = list()      
  data = response.json()
  title = data[0]['data']['children'][0]['data']['title']
  post_fetch.append(title+'\n\n')
  for i in range(0,50):
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
