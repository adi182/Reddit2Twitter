Reddit2Twitter
=======

This twitter bot was inspired by Yasoob's [Reddit-Twitter bot](https://github.com/yasoob/Reddit-Twitter-bot). I started making this after reading [this blog post of his](http://pythontips.com/2013/09/14/making-a-reddit-twitter-bot/). Yasoob has some great materials for learning python, so check him out!

Unfortunatelty, due to some changes in how Twitter and Google handle url shortening, Yasoob's bot was no longer funtional. Yasoob and I have updated his bot for 2016, but this project allows for even greater flexiblity by adding a config file.

The goal of Reddit2Twitter is to automate the movement of content from a subreddit to a twitter account. This is ideal if you manage a community on twitter, and want to make your subreddit's content immediately available to that audiance. The bot is designed to be flexible but robust, and comes with several options for displaying content.

I currently use Reddit2Twitter to run my [Subreddit Simulator twitter bot](https://twitter.com/subreddit_sim), which composes tweets from popular posts on [/r/SubredditSimulator](https://www.reddit.com/r/SubredditSimulator/). I guess I just like bots taking direction from other bots. Here is an example tweet:



Required libraries
-----------
A few additional libraries must be installed to run this script. If you are not famillar with pip, you should start with [this documentation](https://pypi.python.org/pypi/pip)

- PRAW
  * Reddit API wrapper for Python
  * install via pip:  ```pip install praw```
- Tweepy
  * Twitter API wrapper for Python
  * install via pip: ```pip install tweepy```
- Requests
  * Python HTTP library
  * install via pip: ```pip install requests```

Access tokens and API keys
-----------
Next we have to take care of some set up in order to properly connect our bot with Twitter. Since this bot only reads posts to reddit and doesn't write (at this time), no reddit account is required.

Go to [http://dev.twitter.com/apps](http://dev.twitter.com/apps) and register your app (in this case the app is the Reddit2Twitter bot). You will have to register with the same twitter account that you plan on using your bot with. That means that if you want your bot to tweet with its own account, you will have to set that account up first.

Once you have registered, you will need to access and copy the following 4 security codes:

1. ```Access Token```
2. ```Access Token Secret```
3. ```Consumer Key```
4. ```Consumer Secret```

These securiity codes are used to authenticate your bot when it commenticates with twitter. You will have to add these to the config file before executing the Reddit2Twitter script.

If you want you can also have your bot use Google's URL shortner. Twitter has its own method for automatically shortening links, so generally using Google's shortener as well is not recommended. I will elabroate on this further in the next secton. If you are convicted in your desire to use Google's URL shortner then you must autheticate your bot with as well.

In ordert to acomplish this you will need to get a ```Google API Key```. For details please read this [section of the Google Developers guide](https://developers.google.com/url-shortener/v1/getting_started#OAuth2Authorizing).

If you do not want to use Google url shortener then go to the config file and set the apropriate field to ```0```. If the ```Google API Key``` isn't recognized, the script will default to using Twitter's default t.co method anyway.

The Config File
-----------
This file serves two purposes. First it is where you will store the various secrutity codes needed for the bot to opperate, along with th name of your selected subreddit. Second you can customize how content gathered from reddit gets formatted by modifying a list of values. 

Here is what can be customized, all but one boiling down to a boolean option:

* The post's karma score (```1``` to display it, ```0``` to ommit it)
* The post's title (selected as above)
* The post's author username 
* The current number of comments 
* The post's URL 
* Whether or not to use the post's permalink url vs the submitted link (```1``` to choose the permalink, ```0``` to choose the submitted link)
* Whether or not to use Google's URL shortener
* Whether or not to use quotes around a post's title
* How long to wait between sending out tweets (in minutes)

Automatically Shortening Links
-----------

Many have asked for the integration of Google's URL shortener. However at this point it's a bit redundent for use on twitter.

Twitter will automatically shorten links for all types of media and websites. Twitter's t.co links allow  previews, embedded content, and partial visablity of the original URL. And Twitter uses this on all links within Tweets. No matter what kind of link provided, 23 or 24 characters are allocated to it. For this reason I advise that all links be handled by twitter's default t.co shortener.

To do this just keep the ```use_google_shortener``` to ```0```. However, if you want to use google's shortening method, it is still supported. To do so set ```use_google_shortener``` to ```01```. Regardless of the shortened links length, twitter will still set aside 23 or 24 characters for it. 


