from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sentiment_mod as s





class listener(StreamListener):
	def on_data(self, data):
		all_data = json.loads(data)
		try:
			tweet = all_data["text"]
			sentiment_value, confidence = s.sentiment(tweet)
			print (tweet, sentiment_value, confidence)
			if confidence*100 >=80:
				output = open("twitter-out.txt", "a")
				output.write(sentiment_value)
				output.write('\n')
				output.close()
		except:
			print ("Error tweet")
		return True

	def on_error(self, status):
		print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Trump"])