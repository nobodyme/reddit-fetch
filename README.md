# reddit-fetch

## fetch-comments

A simple program to fetch the top level comments of a reddit post

Useful when you have threads like,
  - What are some of best resources that helped you with python?
  - What's your favorite album?
 
This then gives the list of just the names of everything that you can save.

### Run

  - Clone the repository: `git clone https://github.com/nobodyme/reddit-fetch.git` or download
  - cd into the directory: `cd reddit-fetch`
  - pip3 install -r requirements.txt
  - Run the script with: `python3 fetch_comments.py -l *your-post-link* -loc *directory path(optional, defaults to current one)*`</br>
  eg: `python3 fetch_comments.py -l https://www.reddit.com/r/AskReddit/comments/75goki/whats_a_movie_to_watch_when_you_want_a_good_cry/`
  - Check for help with `python3 fetch_comments.py -h`
  
 <img src="https://user-images.githubusercontent.com/15857119/34459416-e68be8d0-ee15-11e7-872a-71f3b11647d7.png">
  
## grab-pictures

A python program to fetch the pictures of a given subreddit, wrote it when I was looking for some wallpapers to download. It grabs the pictures and puts them in a folder under the name of the supplied subreddit.
You can find the related [medium article here](https://medium.com/@naveenkumarspa/using-python-for-your-desktop-wallpaper-collection-focused-on-beginners-a66451d25660).

### Run

  - Clone the repository: `git clone https://github.com/nobodyme/reddit-fetch.git` or download
  - cd into the directory: `cd reddit-fetch`
  - pip3 install -r requirements.txt
  - Run the script with: `python3 grab_pictures.py -s *name-of-the-subreddits* -n *number-of-photos(optional)* -t *top posts of [day, week, month, year, all](optional)* -loc *directory-path(optional, defauts to current one)*`</br>
  eg: `python3 grab_pictures.py -s itookapicture CozyPlaces -n 100 -t all`
  - Check for help with `python3 grab_pictures.py -h`
