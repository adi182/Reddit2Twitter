import praw
import json
import requests
import tweepy
import time

def setupConnection(subreddit):
	print "[r2t] setting up connection with Reddit"
	r = praw.Reddit('zakagan and yasoob_python reddit to twitter poster'
				'monitoring %s' %(subreddit)) 
	subreddit = r.get_subreddit(subreddit)
	return subreddit

def collectPosts(subreddit_info):
	print "[r2t] Collecting top posts on r/" + config_dict['subreddit_name']
	for index, submission in enumerate(subreddit_info.get_hot(limit=25)):
		found = duplicateCheck(submission.id)
		if found == 0:
			print "[r2t] Post #%d selected:" %(index+1)
			return submission
		else:
			print "[r2t] Post #%d: ID already collected" %(index+1)

def tweetComposer(post):
	char_remaining=140
	content_dict={'score':"", 'nsfw_warning':"", 'title':"", 'author':"", 'num_comments':"",'link':""}
	num_content=config_dict['include_karma'] + config_dict['include_nsfw_check'] + config_dict['include_title'] \
		+ config_dict['include_author'] + config_dict['include_num_comments'] + config_dict['include_link']
	index=0

	if config_dict['include_karma']==1:
		score=("%d" %(post.score)+u"\u2B06" + ":").encode("utf-8")+getSeperationStr(index,num_content)
		if char_remaining-len(score) >= 0:
			content_dict['score']=score
			char_remaining-=len(score)-2
		del score	
		index+=1

	if config_dict['include_nsfw_check']==1 and post.over_18==True:
		nsfw_warning="[NSFW]"+getSeperationStr(index,num_content)
		if char_remaining-len(nsfw_warning) >= 0:
			content_dict['nsfw_warning']=nsfw_warning
			char_remaining-=len(nsfw_warning)
		del nsfw_warning	
		index+=1
	elif config_dict['include_nsfw_check']==1:
		index+=1

	if config_dict['include_title']==1:
		title=(post.title).encode("utf-8")
		content_dict['title']=title
		title_index=index
		# the post title's length is updated last	
		del title
		index+=1

	if config_dict['include_author']==1:
		author="- u/" + post.author.name.encode("utf-8") + getSeperationStr(index,num_content)
		if char_remaining-len(author) >= 0:			
			content_dict['author']=author
			char_remaining-=len(author)
		del author			
		index+=1

	if config_dict['include_num_comments']==1:
		num_comments=str(post.num_comments)+" comments"+ getSeperationStr(index,num_content)
		if char_remaining-len(num_comments) >= 0:					
			content_dict['num_comments']=num_comments
			char_remaining-=len(num_comments)		
		del num_comments					
		index+=1

	if config_dict['include_link']==1:
		if config_dict['use_permalink_url']==1:
			post_link=post.permalink				
		else:
			post_link=post.url

		if config_dict['use_google_shortener']==1:
			post_link=googleShortener(post_link)+ getSeperationStr(index,num_content)
			shortened_link_len=len(post_link)
		else:		#using Twitter's shortening method
			shortened_link_len=24+len(getSeperationStr(index,num_content))
		
		if char_remaining-shortened_link_len >=0:
			content_dict['link']=post_link.encode("utf-8")
			char_remaining-=shortened_link_len		
		index+=1

	if config_dict['include_title']==1:	 #The post title is revisted to see if it must be truncated
		title=content_dict['title']
		char_remaining-= len(getSeperationStr(title_index,num_content))
		if config_dict['use_quotes_around_title']==1:
			char_remaining-=2	
		if char_remaining-len(title) < 0 and char_remaining >= 3:
			title=title[:char_remaining-len(title)-3]+ '...'

		if char_remaining-len(title) >= 0 and char_remaining >=3:
			if config_dict['use_quotes_around_title']==1:
				title="\""+title+"\""
			title+= getSeperationStr(title_index,num_content)
		else:
			title=""			
		content_dict['title']=title
		del title
	
	tweet_content= content_dict['score'] + content_dict['nsfw_warning'] + content_dict['title'] \
		+ content_dict['author']+ content_dict['num_comments'] + content_dict['link']

	print tweet_content
	return tweet_content

def getSeperationStr(index, max_len):
		if index < max_len-1:
			return" "
		else:
			return""	

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
			print "[r2t] Unfamiler error"	

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
	config_dict={}
	with open("r2t_config.txt") as f:
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
	main()