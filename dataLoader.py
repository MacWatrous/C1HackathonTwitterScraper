import psycopg2
import csv
import os
from textblob import TextBlob
import re

try:
    conn = psycopg2.connect("dbname='' user='' host='' password='' sslmode='require'")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w +:\ / \ / \S +)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

textStore = []

#this is iterating by day
for fn in os.listdir('/Users/ap'):
    x = 0
    ptweets = []
    ntweets = []
    neuttweets = []
    tweets = []
    if os.path.isfile(fn):
        fileName = fn.split(".")
        if fileName[1] == "csv":
            textStore = []
            fileReader = csv.reader(open("/Users/ap/"+fn), delimiter=",")
            date = fileName[0]
            header1 = fileReader.next()  # header
            for row in fileReader:

                index = find_nth(row[0], ';', 4)
                rowExtract = row[0][index+1:]
                for x in range(1,len(row)):
                    rowExtract += row[x]
                index2 = find_nth(rowExtract, ';', 1)
                tweetText = rowExtract[1:index2 - 1]
                #print(rowExtract[1:index2-1])

                index = find_nth(row[0], ';', 2)
                rowExtract = row[0][index+1:]
                index2 = find_nth(rowExtract, ';', 1)
                retweets = rowExtract[:index2]

                textStore.append([tweetText, retweets])
                #print(textStore[x])
                x += 1
            tweets = []
            for store in textStore:
                parsed_tweet = {}
                parsed_tweet['text'] = store[0]
                parsed_tweet['sentiment'] = get_tweet_sentiment(store[0])

                if store[1] > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
            ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
            neuttweets = len(tweets) - len(ntweets) - len(ptweets)
            #print(date,len(ptweets),len(ntweets),neuttweets,totalTweets)
            totalTweets = neuttweets + len(ntweets) + len(ptweets)
            ptweetsLen = len(ptweets)
            ntweetslen = len(ntweets)
            #print("""INSERT INTO main VALUES ('""" + str(date) + """', """ + str(ptweetsLen) + """, """ + str(ntweetslen) + """, """ + str(neuttweets) + """, """ + str(totalTweets) + """);""")
            try:
                cur.execute("""INSERT INTO main VALUES ('""" + str(date) + """', """ + str(ptweetsLen) + """, """ + str(ntweetslen) + """, """ + str(neuttweets) + """, """ + str(totalTweets) + """);""")
                conn.commit()
            except:
                print "failed to store data"

                #row[0] = row[0].replace(';', '*;*')
                #rowParts = row[0].split(';')
                #print rowParts[5]
    #launch day off to DB at this scope



cur.close()
conn.close()
