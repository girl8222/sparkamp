import csv
import re

screen_names = 'screen_name.csv'

with open(screen_names, 'r') as f:
  reader = csv.reader(f,delimiter = ',')
  your_list = list(reader)

f.close()

a =re.findall(r"'(.*?)'", str(your_list), re.DOTALL)

import tweepy

consumer_key ="bKO8rFtHXG0lxJhw0ZY6W4uNZ"
consumer_secret = "OdiE7BOuIbWc0q8OGGdSPVloiAla8K52hXfnlJ1nrK07bSknus"

access_token = "1546719252-j0L9csoqdj58AJ9QkIsuWysKf8JY9pBCx8f0meo"
access_token_secret = "TfRL5gITo7BhjUykYAjmJUBg51T3tfI9ef6KCgufr3SVw"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
resultFile = open("outputwhy.csv","w",newline='', encoding ="utf-8")
wr= csv.writer(resultFile, dialect = "excel")

overall_list = []

for i in range(1, len(a)):
    result_row = []
    result_row.append(a[i])
    try:
        tweets = api.user_timeline(screen_name=a[i])
    except Exception:
        overall_list.append("error")
        result_row.append("error")
        wr.writerows([result_row])
        continue

    aList = ""
    for j in range(len(tweets)):    
        b = tweets[j]
        aList = aList + " " + b.text

    aList = re.sub(r"http\S+", "", aList)  
    aList.replace("\n", "")
    overall_list.append(aList)
    result_row.append(repr(aList))
    wr.writerows([result_row])
    
resultFile.close()

import nltk, string
from nltk.stem.wordnet import WordNetLemmatizer
#print(len(twenty_all.data))
processed_twenty_train=[]
for i in range(len(overall_list)):
    words=nltk.word_tokenize(overall_list[i])
    lemmatized=[]
    for j in range(len(words)):
        lemma_noun=WordNetLemmatizer().lemmatize(words[j])
        lemmatized.append(WordNetLemmatizer().lemmatize(lemma_noun, 'v'))
    processed_twenty_train.append(" ".join(w for w in lemmatized if w not in (string.punctuation+'...'+'--')))
#print(len(processed_twenty_all))

from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(min_df=1,stop_words=text.ENGLISH_STOP_WORDS)
X = vectorizer.fit_transform(processed_twenty_train)

from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X)
print (X_train_tfidf.shape)

# find 10 most related words
import numpy
vocab = vectorizer.get_feature_names()

print ("Answer of 10 most related words:")
n_top = 10;
for index in range(0,len(overall_list)):
    result = []
    vec = X_train_tfidf[index].toarray()
    #pop 10 max items
    for i in range(n_top):
        #find current max
        max_term_id = numpy.where(vec == vec.max())[1] 
        max_term_id = max_term_id[0]
        vec[0][max_term_id] = 0
        
        result.append(int(max_term_id))
    print (a[index],":")
    ans = ""
    for i in result :
        ans += vocab[i] + ","
    print ("   ",ans)