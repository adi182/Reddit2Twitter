import praw
import json
import requests
import tweepy
import time
import sys

def setupConnection(subreddit):
	print "[r2t] setting up connection with Reddit"
	try:
		r = praw.Reddit('zakagan and yasoob_python\'s Reddit2Twitter app, monitoring %s' %(subreddit)) 
	except:
		print  "[r2t] Error accessing subreddit via Praw"
		sys.exit()
	subreddit = r.get_subreddit(subreddit)
	try:
		subreddit.id  #if subreddit doesn't exist, it will have no id on reddit & throw an error
		print "[r2t] Connected to /r/%s" %(subreddit.display_name)
		return subreddit
	except:
		print "[r2t] subreddit could not be found, check name in config file"
		sys.exit()

def collectPosts(subreddit):
	print "[r2t] Collecting current top posts"
	for index, submission in enumerate(subreddit.get_hot(limit=25)):
		found = duplicateCheck(submission.id)
		if found == 0:
			print "[r2t] Post #%d selected" %(index+1)
			return submission
		else:
			print "[r2t] Post #%d: ID already collected" %(index+1)

def tweetComposer(post):
	char_remaining=140
	content_list=[]
	num_content=config_dict['include_karma'] + config_dict['include_nsfw_check'] + config_dict['include_title'] \
		+ config_dict['include_author'] + config_dict['include_num_comments'] + config_dict['include_link']
	char_remaining-=num_content-1

	if config_dict['include_karma']==1:
		score=("%d" %(post.score)+u'\u2B06' + ":").encode("utf-8").decode("utf-8")
		if char_remaining-len(score) >= 0:
			content_list.append(score)
			char_remaining-=len(score)
		del score	

	if config_dict['include_nsfw_check']==1 and post.over_18==True:
		nsfw_warning="[NSFW]"
		if char_remaining-len(nsfw_warning) >= 0:
			content_list.append(nsfw_warning)
			char_remaining-=len(nsfw_warning)
		del nsfw_warning	

	if config_dict['include_title']==1:
		title=post.title
		title_index=len(content_list)		
		content_list.append(title)
		# the post title's length is updated last	
		del title

	if config_dict['include_author']==1:
		author="- u/" + post.author.name.encode("utf-8").decode("utf-8")
		if char_remaining-len(author) >= 0:			
			content_list.append(author)
			char_remaining-=len(author)
		del author			

	if config_dict['include_num_comments']==1:
		num_comments="%d comments" %(post.num_comments)
		if char_remaining-len(num_comments) >= 0:					
			content_list.append(num_comments)
			char_remaining-=len(num_comments)
		del num_comments					

	if config_dict['include_link']==1:
		if config_dict['use_permalink_url']==1:
			post_link=post.permalink				
		else:
			post_link=post.url

		if config_dict['use_google_shortener']==1:
			post_link=googleShortener(post_link)

		shortened_link_len=24		#For now twitter reserves 24 characters for all links and media, this may change
		if char_remaining-shortened_link_len >=0:
			content_list.append(post_link)
			char_remaining-=shortened_link_len
		del post_link, shortened_link_len	

	if config_dict['include_title']==1:	 #The post title is revisted to see if it must be truncated
		title=content_list[title_index]
		if config_dict['use_quotes_around_title']==1:
			char_remaining-=2	
		if char_remaining-len(title) < 0 and char_remaining >0:
			title=(title[:char_remaining-len(title)-1]+ u'\u2026').encode("utf-8").decode("utf-8")

		if char_remaining-len(title) >= 0 and char_remaining >0:
			if config_dict['use_quotes_around_title']==1:
				title="\""+title+"\""
		else:
			title=''			

		content_list[title_index]=title
		if config_dict['use_quotes_around_title']==1:
			char_remaining-=len(title)-2		#in this surrounding quotation marks have been already factored
		else:
			char_remaining-=len(title)
		del title

	tweet_content= " ".join(content_list)
	print tweet_content.encode("utf-8")
	print "Characters remaining = %d" %(char_remaining)
	return tweet_content

def googleShortener(url):
	try:
		headers = {'content-type': 'application/json'}
		payload = {"longUrl": url}
		googl_url = "https://www.googleapis.com/urlshortener/v1/url?key=%s" %(config_dict['google_api_key'])
		r = requests.post(googl_url, data=json.dumps(payload), headers=headers)
		url = json.loads(r.text)['id']
	except:
		print "[r2t] Google shortner could not be accessed, check google api key"
		print "[r2t] Defaulting to twitter's t.co shortner"
	return url

def tweetSender(tweet):
	try:
		auth = tweepy.OAuthHandler(config_dict['consumer_key'], config_dict['consumer_secret'])
		auth.set_access_token(config_dict['access_token'], config_dict['access_token_secret'])
		api = tweepy.API(auth)
		api.update_status(tweet)
		print "[r2t] Tweet sucessfully sent to twitter"
	except Exception, e:	
		print  "[r2t] Error triggered when sending tweet content to twitter:"
		try:
			print "[Twitter] "+ e.args[0][0]['message']
		except:
			print "[r2t] Error outside of communication with Twitter"	
		sys.exit()	

def addPostID(post):
	with open('posted_posts.txt', 'a') as file:
		file.write(str(post.id) + "\n")
	file.close()

def duplicateCheck(post_id):
	found = 0
	with open('posted_posts.txt', 'r') as file:
		for line in file:
			if post_id in line:
				found = 1
	return found

def main():
	while True:
		subreddit = setupConnection(config_dict['subreddit_name'])
		reddit_post = collectPosts(subreddit)
		tweet_content = tweetComposer(reddit_post)	
		tweetSender(tweet_content)
		addPostID(reddit_post)					
		time.sleep(config_dict['tweet_delay']*60)		

if __name__ == '__main__':
	config_dict = {'access_token': "",    #defining what we expect to gt from the config file
		'access_token_secret':"",
		'consumer_key': "",
		'consumer_secret' : "",
		'google_api_key' : "",
		'subreddit_name' : "",
		'include_karma' : 0,               #Note that boolean values will default to 0
		'include_nsfw_check' : 0,
		'include_title' : 0,
		'include_author' : 0,
		'include_num_comments' :0,
		'include_link' : 0,
		'use_permalink_url' : 0,
		'use_google_shortener': 0,
		'use_quotes_around_title': 0,
		'tweet_delay' : 0}
	
	with open("r2t_config.txt") as f:       #Read from config file and save to global dictionary
		for line in f:
			line=line.replace(':', " ")			
			line=line.replace('#', " ")
			line=line.split()
			if len(line) >=2:
				key=line[0]
				val=line[1]
				try:
					val=int(val)
				except:
					pass	
				config_dict[key] = val
	f.close()
	for key in ['include_karma', 'include_nsfw_check', 'include_title', 
		'include_author','include_num_comments', 'include_link', 
		'use_permalink_url', 'use_google_shortener', 
		'use_quotes_around_title', 'tweet_delay']:
		#Check if required int values really are ints
		if isinstance(config_dict[key],int)==False:
			config_dict[key]=0

		if key=='tweet_delay' and config_dict[key]<5:
			config_dict[key]=5	
	main()