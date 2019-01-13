from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONProtocol
import json
import sys
from operator import itemgetter
import re
from pymongo import MongoClient

sys.path.append('.')


class MRTwitterSentimentalAnalysis(MRJob):

    INTERNAL_PROTOCOL = JSONProtocol
    client = MongoClient('db',27017)
    db = client.twitterdb

    def mapper_initial_data(self):
        self.english_dictionary = self.load_dictionary()
        self.pattern = re.compile(r"[^\w']")
        self.states = {'ALABAMA':'AL','ALASKA':'AK','ARIZONA':'AZ','ARKANSAS':'AR','CALIFORNIA':'CA','COLORADO':'CO','CONNECTICUT':'CT','DELAWARE':'DE','DISTRITC OF COLUMBIA':'DC','FLORIDA':'FL',
           'GEORGIA':'GA','HAWAII':'HI','IDAHO':'ID','ILLINOIS':'IL','INDIANA':'IN','IOWA':'IA','KANSAS':'KS','KENTUCKY':'KY','LOUISIANA':'LA','MAINE':'ME','MARYLAND':'MD','MASSACHUSETTS':'MA',
           'MICHIGAN':'MI','MINNESOTA':'MN','MISSISSIPPI':'MS','MISSOURI':'MO','MONTANA':'MT','NEBRASKA':'NE','NEVADA':'NV','NEW HAMPSHIRE':'NH','NEW JERSEY':'NJ','NEW MEXICO':'NM',
           'NEW YORK':'NY','NORTH CAROLINA':'NC','NORTH DAKOTA':'ND','OHIO':'OH','OKLAHOMA':'OK','OREGON':'OR','PENNSYLVANIA':'PA','RHODE ISLAND':'RI','SOUTH CAROLINA':'SC',
           'SOUTH DAKOTA':'SD','TENNESSEE':'TN','TEXAS':'TX','UTAH':'UT','VERMONT':'VT','VIRGINIA':'VA','WASHINGTON':'WA','WEST VIRGINIA':'WV','WISCONSIN':'WI','WYOMING':'WY'}
        client = MongoClient('db',27017)
        self.db = client.twitterdb

    def load_dictionary(self):
        my_dictionary = {}
        file = open('AFINN-111.txt','r')
        for line in file:
            word,punctuation = line.split('\t')
            my_dictionary[word] = float(punctuation)
        return my_dictionary

    def tweet_state(self,place):
        states_acronym = self.states.values()
        if len(place) == 1:
            place[0] = place[0].upper().strip()
            if self.states.get(place[0]) != None:
                return self.states.get(place[0])
        elif len(place) == 2:
            place[0] = place[0].upper().strip()
            place[1] = place[1].upper().strip()
            if place[1] == 'USA':
                if self.states.get(place[0]) != None:
                    return self.states.get(place[0])
            else:
                if place[1] in states_acronym:
                    return place[1]

    def tweet_word_punctuation(self,tweet_text,dictionary):
        punctuation = 0
        tweet_words = self.pattern.sub(" ", tweet_text.lower()).split(" ")
        for word in tweet_words:
            if word in dictionary:
                punctuation += dictionary[word]
        return punctuation

    def mapper_tweet_filtering(self,_,line):
        tweet = json.loads(line)
        state_punctuation_hashtag = {'state':None,'punctuation':None,'hashtag':[]}
        if'text' in tweet and 'lang' in tweet and 'place' in tweet: #eliminamos los tweets borrados
           if(tweet['lang']=='en' and tweet['place']!= None): #nos quedamos con los tweets en ingles y que tienen informacion del lugar
                if(tweet['place']['country_code'] == 'US'): #nos quedamos con EEUU y cuyo lugar tenga nombre con , que indica ciudad y estado
                    place = tweet['place']['full_name'].split(',')
                    state_punctuation_hashtag['state']= self.tweet_state(place)

                if state_punctuation_hashtag['state'] != None:
                    if tweet['entities']['hashtags'] != []:
                        for hashtag in tweet['entities']['hashtags']:
                            state_punctuation_hashtag['hashtag'].append(hashtag['text'])
                    punctuation = self.tweet_word_punctuation(tweet['text'], self.english_dictionary)
                    state_punctuation_hashtag['punctuation'] = punctuation
                    yield(state_punctuation_hashtag['state'],state_punctuation_hashtag)

    def reducer_state_punctuation(self,state,datas):
        state_information = {'name': None,'punctuation':0,'hashtags':[]}
        punctuations = 0
        hashtags = []
        state = None
        count = 0
        for tweet in datas:
            count += 1
            if state == None:
                state = tweet['state']
            punctuations += tweet['punctuation']
            if tweet['hashtag'] != []:
                hashtags += tweet['hashtag']
        state_information['name'] = state
        state_information["punctuation"] = punctuations/count
        state_information["hashtags"] = hashtags
        yield (state, state_information)

    def mapper_happiest_state(self,state,data):
        yield(None,(state,data))

    def reducer_happiest_state(self,_,state_data):
        happiest_state = {'state':None,'punctuation':None,'hashtags':[]}
        for state,data in state_data:
            if happiest_state['punctuation'] == None:
                happiest_state['state'] = state
                happiest_state['punctuation'] = data['punctuation']
            elif happiest_state['punctuation'] < data['punctuation']:
                happiest_state['state'] = state
                happiest_state['punctuation'] = data['punctuation']
            if data['hashtags'] != []:
                happiest_state['hashtags'] += data['hashtags']

        for hashtag in happiest_state['hashtags']:
            yield(hashtag,{'state':happiest_state['state'],'punctuation':happiest_state['punctuation'],'count':1})

    def mapper_hashtag_treatment(self,hashtag,data):
        yield(hashtag,data)

    def reducer_hashtag_treatment(self, hashtag, data):
        hashtag_count = 0
        information = {'hashtag':hashtag,'hashtag_count':None,'happiest_state':None,'punctuation':None}
        for i in data:
            hashtag_count += i['count']
            if information['happiest_state'] == None and information['punctuation'] == None:
             information['happiest_state'] = i['state']
             information['punctuation'] = i['punctuation']
        information['hashtag_count'] = int(hashtag_count)
        yield(None,information)

    def reducer_trending_topic(self,_,information):
        trending_topic = []
        result = {'trending_topic':[],'happiest_state':None,'punctuation':None}
        for i in information:
            if result['happiest_state'] == None and result['punctuation'] == None:
                result['happiest_state'] = i['happiest_state']
                result['punctuation'] = i['punctuation']
            if len(trending_topic)<10:
                trending_topic.append((i['hashtag'],i['hashtag_count']))
            else:
                if trending_topic[-1][1] < i['hashtag_count']:
                    trending_topic.remove(trending_topic[-1])
                    trending_topic.append((i['hashtag'],i['hashtag_count']))
            trending_topic = sorted(trending_topic, key=itemgetter(1), reverse=True)
        result['trending_topic'] = trending_topic
        item_db = {
		'trending topic':result['trending_topic'],
		'happiest state':result['happiest_state'],
		'state punctuation':result['punctuation']
	}
	self.db.twitterdb.insert_one(item_db)

    def steps(self):
        return [
            MRStep(mapper_init = self.mapper_initial_data,
                   mapper = self.mapper_tweet_filtering,
                   reducer = self.reducer_state_punctuation),
            MRStep(mapper = self.mapper_happiest_state,
                   reducer= self.reducer_happiest_state),
            MRStep(mapper = self.mapper_hashtag_treatment,
                   reducer = self.reducer_hashtag_treatment),
            MRStep(reducer = self.reducer_trending_topic)
        ]

if __name__ == "__main__":
     MRTwitterSentimentalAnalysis().run()
