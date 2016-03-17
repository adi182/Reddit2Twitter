Reddit2Twitter
=======

This twitter bot was inspired by Yasoob's [Reddit-Twitter bot](https://github.com/yasoob/Reddit-Twitter-bot). I started making this after reading [this blog post of his](http://pythontips.com/2013/09/14/making-a-reddit-twitter-bot/). Yasoob has some great materials for learning python, so check him out!

Unfortunatelty, due to some changes in how Twitter and Google handling url shortening, Yasoob's bot was no longer funtional. I started making this variation long before I learned about pull requests, and it's expanded further in scope somewhat.

The goal of Reddit2Twitter is to automate the movement of content from a subreddit to a twitter account. This is ideal if you manage a community on twitter, and want to make your subreddit's content immediately availble to an audiance on Twitter. Reddit2Twitter also provides some additional customablity to help facilitate this.

Required libraries
-----------
A few additional libraries must be installed to run this script. If you are not famillar with pip, you may start with [this documentation](https://pypi.python.org/pypi/pip)

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

Go to [http://dev.twitter.com/apps](http://dev.twitter.com/apps) and register your app Iin this case the app is the Reddit2Twitter bot). You will have to register on the same twitter account that you plan on using your bot with. That means if you want your bot to tweet with its own account, you will have to set that account up first.

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
You can customize how content gathered from reddit gets formatted for twitter my modifying the config file. 

Please read the sample config file provided. Feel free to make adjustments for your own personal use. I will update this section with more detail on how to adjust your twitter bot's settings soon.

First a note about shortening links. Twitter will shorten links to all types of sites and media automatically. Twitter's t.co links allows for previews, embedded content, and they doesn't completly obsificate the name of the destination site. No matter what kind of link provided, 23 or 24 characters are allocated to it. For this reason I advise that all links be handled by twitter's default t.co shortener.

To do this just keep the ```use_google_shortener``` to ```0```. However, if you want to use google's shortening method it is still supported. To do so, set ```use_google_shortener``` to ```01```. Regardless of the shortened links length, twitter will still set aside 23 or 24 for it. 


