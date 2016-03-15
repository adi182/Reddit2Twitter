Reddit2Twitter
=======

This twitter bot was inspired by Yasoob's [Reddit-Twitter bot](https://github.com/yasoob/Reddit-Twitter-bot). I started making this after reading this [blog post of his](http://pythontips.com/2013/09/14/making-a-reddit-twitter-bot/). Yasoob has some great materials for learning python, so check him out!

Unfortunatelty, due to some changes in how Twitter and Google handling url shortening, Yasoob's bot was no longer funtional. I started making this variation long before I learned about pull requests, and it's expanded further in scope somewhat.

The goal of Reddit2Twitter is to automate the movement of content from a subreddit to a twitter account. This is ideal if you manage a community on twitter, and want to make your subreddit's content immediately availble to an audiance on Twitter. Reddit2Twitter also provides some additional customablity to help facilitate this.

Required libraries
-----------
A few additional libraries must be installed to run this script.

- PRAW
  * Reddit API wrapper for Python
  * install via pip:  ```pip install praw```
- Tweepy
  * Twitter API wrapper for Python
  * install via pip: ```pip install tweepy```
- Requests
  * Python HTTP library
  * install via pip: ```pip install requests```

Getting started: Access tokens, API keys, and the Config file
-----------
Before we start tweeting, we have to take care of some set up in order to properly connect our bot with Twitter. Since this bot only reads posts to reddit and doesn't write (at this time), no reddit account is required.

You can customize how content gathered from reddit gets formatted for twitter my modifying the config file.


