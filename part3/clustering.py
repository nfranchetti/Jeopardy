import pandas as pd
import numpy as np
import nltk
import re
import matplotlib.pyplot as plt
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from sklearn.cluster import KMeans


# here I define a tokenizer and stemmer which returns the set of stems in the text that it is passed

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

def create_clean_columns(df):    
    df['clean_question'] = df['Question'].apply(cleanhtml)
    df['clean_answer'] = df['Answer'].apply(cleanhtml)
    df['clean_category'] = df['Category'].apply(cleanhtml)
    df['everything'] = df['clean_question']+' '+df['clean_answer']+' '+df['clean_category']
    return df

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace('\n', '')
    cleantext = cleantext.replace('-', ' ')
#     cleantext = cleantext.translate(None, string.punctuation)
#     cleantext = cleantext.replace('\'', '')
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    cleantext = regex.sub('', cleantext)
    cleantext = cleantext.lower()
    return cleantext





df = pd.read_csv('../data/JEOPARDY_CSV.csv', encoding='utf-8')

# Remove the dumb spaces
df.columns = ['Show Number', 'Air Date', 'Round', 'Category', 'Value', 'Question', 'Answer']

# Convert to Datetime
df['Air Date'] = pd.to_datetime(df['Air Date'])

# Clean out Value column
df['Value'] = df['Value'].str.replace('$','')
df['Value'] = df['Value'].str.replace(',','')
df['Value'] = df['Value'].apply(lambda x: None if x == 'None' else int(x))

# Drop some useless questions
df = df[df['Question'] != '[audio clue]']
df = df[df['Question'] != '[video clue]']
df = df[df['Question'] != '[filler]']
df = df[df['Question'] != '(audio clue)']

# load nltk's English stopwords as variable called 'stopwords'
stopwords = nltk.corpus.stopwords.words('english')

# load nltk's SnowballStemmer as variabled 'stemmer'
stemmer = SnowballStemmer("english")

questions = df['Question'].values

#use extend so it's a big flat list of vocab
totalvocab_stemmed = []
totalvocab_tokenized = []
for i in questions:
    allwords_stemmed = tokenize_and_stem(i) #for each item in 'synopses', tokenize/stem
    totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
    
    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)


# tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
#                                  min_df=0.2, stop_words='english',
#                                  use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=100000, 
                                 tokenizer=tokenize_and_stem, ngram_range=(1,3))

# %time tfidf_matrix = tfidf_vectorizer.fit_transform(questions)

tfidf_vectorizer.fit(questions)
joblib.dump(tfidf_vectorizer, 'tfidf_test.joblib')

tfidf_vectorizer = joblib.load('tfidf_test.joblib')
tfidf_matrix = tfidf_vectorizer.transform(questions)

terms = tfidf_vectorizer.get_feature_names()

num_clusters = 50

km = KMeans(n_clusters=num_clusters)

km.fit(tfidf_matrix)

clusters = km.labels_.tolist()

joblib.dump(km,  'doc_cluster.pkl')
km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()

df['Cluster'] = clusters

print(df['Cluster'].value_counts())

print("Top terms per cluster:")
print()
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')
    for ind in order_centroids[i, :6]:
        print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
    print()
    print()
    print("Cluster %d categories:" % i, end='')
    for cat in df.ix[i]['Category']:#.values.tolist():
        print(' %s,' % cat, end='')
    print()
    print()