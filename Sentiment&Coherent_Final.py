#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

# read the data from CSV file
# data = pd.read_csv('/Users/mohamedgani/Downloads/Exhibits/combined_file.csv')
data = pd.read_csv('/Users/mohamedgani/Downloads/output_final_htm_file.csv')
data = data.dropna()


# In[2]:


data


# In[3]:


# extract the document titles
titles = data['b title']

# create a bag-of-words representation of the documents
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(titles)

# perform K-means clustering
kmeans = KMeans(n_clusters=9, random_state=0).fit(X)

# add the cluster labels to the data frame
data['cluster'] = kmeans.labels_


# In[4]:


# Set the display options to show all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
data


# In[5]:


# get the list of words in the vocabulary
words = vectorizer.get_feature_names()

# get the centroid of each cluster
centroids = kmeans.cluster_centers_

# print the top words for each cluster
for i in range(kmeans.n_clusters):
    print(f"Cluster {i} words:", end='')
    for ind in centroids[i].argsort()[-10:]:
        print(f" {words[ind]}", end='')
    print()


# In[6]:


# Keep only rows that have the value of 5 in the column 'my_column'
data = data.loc[data['cluster'] == 2]
# Replace all other values with NaN
data['cluster'] = data['cluster'].mask(data['cluster'] != 2, other=pd.np.nan)


# In[7]:


data = data.dropna()
data


# In[8]:


from sklearn.feature_extraction.text import TfidfVectorizer
# extract the document titles
titles = data['b title']

# create a bag-of-words representation of the documents
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(titles)

# perform K-means clustering
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

# add the cluster labels to the data frame
data['cluster_2'] = kmeans.labels_

data


# In[9]:


# get the list of words in the vocabulary
words = vectorizer.get_feature_names()

# get the centroid of each cluster
centroids = kmeans.cluster_centers_

# print the top words for each cluster
for i in range(kmeans.n_clusters):
    print(f"Cluster {i} words:", end='')
    for ind in centroids[i].argsort()[-10:]:
        print(f" {words[ind]}", end='')
    print()


# In[10]:


import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# Preprocess data
def preprocess_text(text):
    # Remove punctuation and double quotes
    text = text.translate(str.maketrans('', '', string.punctuation.replace('"', '')))
    
    # Convert text to lowercase
    text = text.lower()
    
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    
    # Join the words back into a string
    preprocessed_text = ' '.join(words)
    return preprocessed_text

data['corresponding p new text'] = data['corresponding p text'].apply(preprocess_text)

data


# In[11]:


import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon if necessary
nltk.download('vader_lexicon')

# Select the rows where cluster_2 is 0
cluster_2_0 = data[data['cluster_2'] == 0]

# Initialize the VADER sentiment analysis model
sia = SentimentIntensityAnalyzer()

# Define a function to calculate the polarity scores for each review
def get_polarity_scores(review):
    # Calculate the polarity scores using the VADER model
    sentiment_scores = sia.polarity_scores(review)
    
    # Extract the positive, negative, and neutral scores
    pos_score = sentiment_scores['pos']
    neg_score = sentiment_scores['neg']
    neu_score = sentiment_scores['neu']
    
    # Extract the compound polarity score
    polarity_score = sentiment_scores['compound']
    
    # Return the scores as a dictionary
    return {'pos_score': pos_score, 'neg_score': neg_score, 'neu_score': neu_score, 'polarity_score': polarity_score}

# Apply the function to the p_text column of the DataFrame to calculate the polarity scores for each review
polarity_scores_df = cluster_2_0['corresponding p new text'].apply(get_polarity_scores).apply(pd.Series)

# Merge the polarity scores DataFrame with the original DataFrame
cluster_2_0 = pd.concat([cluster_2_0, polarity_scores_df], axis=1)

# Define a function to categorize the polarity scores as positive, negative, or neutral
def get_sentiment_label(row):
    pos_score = row['pos_score']
    neg_score = row['neg_score']
    if pos_score > neg_score:
        return 'positive'
    elif pos_score < neg_score:
        return 'negative'
    else:
        return 'neutral'

# Apply the function to the polarity scores DataFrame to categorize the polarity scores
cluster_2_0['sentiment_label'] = polarity_scores_df.apply(get_sentiment_label, axis=1)
cluster_2_0


# In[ ]:




