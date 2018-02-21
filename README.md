# reddit-fetch

## fetch-comments

A simple program to fetch the top level comments of a reddit post

Useful when you have threads like,
  - What are some of best resources that helped you with python?
  - What's your favorite album?
 
This then gives the list of just the names of everything that you can save.

### Run

  - Then clone the repository: `git clone https://github.com/nobodyme/reddit-fetch.git`
  - cd into the directory: `cd reddit-fetch`
  - Run the script with: `python3 fetch_comments.py -l *your-post-link*`</br>
  eg: `python3 fetch_comments.py -l https://www.reddit.com/r/AskReddit/comments/75goki/whats_a_movie_to_watch_when_you_want_a_good_cry/`
  
 <img src="https://user-images.githubusercontent.com/15857119/34459416-e68be8d0-ee15-11e7-872a-71f3b11647d7.png">
  
## grab-pictures

A python program to fetch the pictures of a given subreddit, wrote it when I was looking for some wallpapers to download.

### Run

  - Then clone the repository: `git clone https://github.com/nobodyme/reddit-fetch.git`
  - cd into the directory: `cd reddit-fetch`
  - Run the script with: `python3 grab_pictures.py -s *name-of-the-subreddit* -n *number-of-photos(optional)* -t *top posts of [day, week, month, year, all](optional)*`</br>
  eg: `python3 fetch_comments.py -s itookapicture -n 100 -t all`
  - Check for help with `python3 grab_pictures.py -h`
