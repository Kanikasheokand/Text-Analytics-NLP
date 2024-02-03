#!/usr/bin/env python
# coding: utf-8

# ### Extracting variables for one URl

# In[3]:


import requests
from bs4 import BeautifulSoup
import string
import nltk
from nltk.tokenize import word_tokenize
import textstat
from textblob import TextBlob
import re


# ### Extracting title & text from url

# In[10]:



def extract_text_from_url(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract article title
    title_element = soup.find('h1', class_="entry-title")
    article_title = title_element.get_text() if title_element else ""


    # Extract text from the article
    article_text = ""
    for paragraph in soup.find_all(attrs={'class':'td-post-content'}):
        article_text += paragraph.get_text() + "\n"

    return article_title, article_text
    

url = "https://insights.blackcoffer.com/how-is-login-logout-time-tracking-for-employees-in-office-done-by-ai/"
article_title,article_text  = extract_text_from_url(url)
print(article_title)
print(article_text)


# ### Saving File

# In[11]:


def save_to_text_file(file_name,content):
    with open(file_name, 'w') as file:
        file.write(content)

url_id = article_title
save_to_text_file(f"{url_id}.txt", article_text)


# ### Remove punctuation from text

# In[12]:


translator = str.maketrans("", "", string.punctuation)
text_without_punctuation = article_text.translate(translator)
text_without_punctuation


# ### tokenization

# In[13]:


nltk.download('punkt')
word_tokens = word_tokenize(text_without_punctuation)
len(word_tokens)
word_tokens


# ### Combined stopwords list

# In[14]:


def read_stopwords_from_file(file_path,encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        stopwords = [line.strip() for line in file]
    return stopwords

def combine_stopwords(files_and_encodings):
    combined_stopwords = set()

    for file_path, encoding in files_and_encodings:
        stopwords = read_stopwords_from_file(file_path, encoding)
        combined_stopwords.update(stopwords)

    return list(combined_stopwords)

# Example: List of files and their corresponding encodings
files_and_encodings = [
    ('StopWords_Auditor.txt', 'ascii'),
    ('StopWords_DatesandNumbers.txt', 'ascii'),
    ('StopWords_Generic.txt','ascii'),
     ('StopWords_GenericLong.txt','ascii'),
      ('StopWords_Geographic.txt','ascii'),
       ('StopWords_Names.txt','ascii'),
        ('StopWords_Currencies.txt','ISO-8859-1')
]


# Combine stopwords from different files with different encodings into one list
combined_stopwords_list = combine_stopwords(files_and_encodings)
print(len(combined_stopwords_list))


# ### Removing stopwords from the tokens

# In[15]:


lowercase_tokens = [token.lower() for token in word_tokens]
filtered_tokens = [token for token in lowercase_tokens if token not in combined_stopwords_list]
len(filtered_tokens)


# ### positive words dictionary

# In[16]:


with open("positive-words.txt","r") as pos:
    poswords = pos.read().split("\n")  


# ### Positive Score

# In[17]:


pos_score =[w for w in filtered_tokens if w in poswords]
#pos_score=pos_score.split(" ")
len(pos_score)


# ### Negative words dictionary

# In[18]:


with open("negative-words.txt","r",errors="replace") as neg:
    negwords = neg.read().split("\n")  


# ### Negative Score

# In[19]:


neg_score = " ".join ([w for w in filtered_tokens if w in negwords])
neg_score=neg_score.split(" ")
len(neg_score)


# ### cleaned_text 

# In[20]:


cleaned_text = ' '.join(filtered_tokens)
cleaned_text


# ### Polarity & Subjectivity 

# In[36]:


def sentiment_analysis(text):
    polarity = TextBlob(text).sentiment.polarity
    subjectivity=TextBlob(text).sentiment.subjectivity
    return polarity, subjectivity
    
Polarity, Subjectivity=sentiment_analysis(cleaned_text)
print("Polarity :",Polarity, "Subjectivity :", Subjectivity)


# ### avg_no_of_words_per_sentence

# In[37]:


avg_no_of_words_per_sentence= len(article_text.split())/len(re.split(r'[?!.]', article_text))
avg_no_of_words_per_sentence


# ### Percentage of Complex words 

# In[52]:


percent_complex=(complex_word/word_count)*100
percent_complex


# ### fog_index

# In[39]:


fog_index=(textstat.gunning_fog(text_without_punctuation))
print(fog_index)


# ### complex_word_count

# In[51]:


#complex_word_count
ctext=text_without_punctuation.split()
complex_word=0
for word in ctext:
    count=0
    word=re.sub(r'(es|ed)$', '', word )
    for i in range(len(word)):
        if word[i].lower() in vowels:
            count+=1
        else:
            count+=0
    if count > 2:
          complex_word+=1

complex_word


# ### word_count

# In[53]:


word_count=len(cleaned_text.split()) #used different formula in extractin all_url file 
word_count


# ### Syllable Count Per Word

# In[62]:


vowels = "aeiouy"
count=0
for word in cleaned_text.split():
    word=re.sub(r'(es|ed)$', '', word )
    for i in range(len(word)):
        if word[i].lower() in vowels:
            count+=1
        
print("Syllable Count:", count)
print("Syllable Count Per Word:", count/word_count)


# ### personal pronouns count

# In[64]:


def ProperNounExtractor(text):
    count = 0
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(words)
        for (word, tag) in tagged:
            if tag == 'PRP': # If the word is a proper noun
                count = count + 1 
        
    return(count)         
Personal_Pronouns=ProperNounExtractor(cleaned_text) 
Personal_Pronouns


# ### Avg word length

# In[63]:


Avg_word_length= len(cleaned_text.replace(' ',''))/len(cleaned_text.split())
print('Word average =',Avg_word_length )

