#!/usr/bin/env python
# coding: utf-8

# ## OBJECTIVE
#   
# The objective of this assignment is to extract textual data articles from the given URL and perform text analysis to compute variables that are explained below. 

# ## Data Extraction :
# For each of the articles, given in the input.xlsx file, extract the article text and save the extracted article in a text file with URL_ID as its file name.While extracting text, please make sure your program extracts only the article title and the article text. It should not extract the website header, footer, or anything other than the article text.

# ## Data Analysis :
# For each of the extracted texts from the article, perform textual analysis and compute variables. You need to save the output in CSV format.

# ## Variables :
# <ol>
# <li>POSITIVE SCORE<li\>
# <li>NEGATIVE SCORE<li\>
# <li>POLARITY SCORE<li\>
# <li>SUBJECTIVITY SCORE<li\>
# <li>AVG SENTENCE LENGTH<li\>
# <li>PERCENTAGE OF COMPLEX WORDS<li\>
# <li>FOG INDEX<li\>
# <li>AVG NUMBER OF WORDS PER SENTENCE<li\>
# <li>COMPLEX WORD COUNT<li\>
# <li>WORD COUNT<li\>
# <li>SYLLABLE PER WORD<li\>
# <li>PERSONAL PRONOUNS<li\>
# <li>AVG WORD LENGTH<li\>
# <ol\>

# ### Importing library

# In[ ]:


import requests                  
import pandas as pd              
from bs4 import BeautifulSoup    
from textblob import TextBlob    
import textstat                 
import openpyxl               
import string                  
import spacy                
import re   


# In[2]:


import nltk                
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')


# ### Combined stopwords list

# In[41]:


# joined different stopwords text files
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
stopwords = combine_stopwords(files_and_encodings)


# ### Positive Words Dictionary 

# In[5]:


with open("positive-words.txt","r") as pos:
    poswords = pos.read().split("\n") 


# ### Negative Words Dictionary

# In[ ]:


with open("negative-words.txt","r",encoding = "ISO-8859-1") as neg:
    negwords = neg.read().split("\n")


# ### Python program to fetch link and perform required operation

# In[176]:


import openpyxl

data=[]

def text(): 

    #for fetching data from given input excel sheet #
    w_book = openpyxl.load_workbook('Input.xlsx')  
    w_sheet = w_book['Sheet1']
    
    #fetch the url from sheet into url variable # 
    for i in range (2 , 102):
        url = (w_sheet.cell(row=i, column=2).value)
    
    #We need to pass argument called Headers by passing "User-Agent" to the request to bypass the mod-security error.

        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}     
        response= requests.get(url,headers=headers )
    
    # apply BeautifulSoup to fetch only html parser 
        soup = BeautifulSoup(response.content, 'html.parser')
        
    # fetch title from link
        title_element = soup.find('h1', class_="entry-title")
        article_title = title_element.get_text() if title_element else ""
        #alternate code-article_title = soup.find('title').get_text()

    
    #fetch content from link 
        article_text = soup.findAll(attrs={'class':'td-post-content'})    
        article_text = article_text[0].text.replace('\n'," ") if article_text else ""
        #alternative-code
        #article_text = ""
        #for paragraph in soup.find_all(attrs={'class':'td-post-content'}):
            #article_text += paragraph.get_text() + "\n"
        
    ##Remove punctuation
        article_text= article_text.translate(str.maketrans('', '', string.punctuation)) 
    
    #tokenize the data 
        article_text_tokens = word_tokenize(article_text)
        
    #remove stopwords
        filter_tokens = [word.lower() for word in article_text_tokens if not word.lower() in stopwords]
    
    #positive dictionary 
        pos_count = [w for w in filter_tokens if w in poswords]   
        Positive_score=len(pos_count)
    
    #negative dictionary
        neg_count = [w for w in filter_tokens if w in negwords]   
        Negative_score=len(neg_count)
        
    #join filter data after removing stpowords  
        cleaned_text = ' '.join(filter_tokens)
        
    #words count 
        Word_Count=len(cleaned_text)
        
    #Avg_Sentence_Length  
        Avg_Sentence_Length= sum([len(l) for l in re.split(r'[?!.]', cleaned_text) if l.strip()])/len(re.split(r'[?!.]', cleaned_text))
    
    #calculating fog index using textstat library
        Fog_Index=(textstat.gunning_fog(cleaned_text))
    
    #Avg_Number_of_Words_Per_Sentence
        Avg_no_of_words_per_sentence= (len(cleaned_text.split()))/(len(re.split(r'[?!.]', cleaned_text)))
        
    #function to calculate Syllable Count Per Word excluding word ending with "ed" or "es"
        vowels = "aeiouy"
        count=0
        for word in cleaned_text.split():
            word=re.sub(r'(es|ed)$', '', word )
            for i in range(len(word)):
                if word[i].lower() in vowels:
                    count=count+1
        syllable_count=count
        
        def Syllable_per_word(cleaned_text):
            if len(cleaned_text.split())==0:
                syllable_per_word=0
            else:
                syllable_per_word= syllable_count/len(cleaned_text.split())
            return(syllable_per_word)
        Syllable_Per_Word=Syllable_per_word(cleaned_text)
    
    #function to calculate proper noun in article with help of tagging from nltk lib
        def ProperNounExtractor(text):
            cou = 0
            sentences = nltk.sent_tokenize(text)
            for sentence in sentences:
                words = nltk.word_tokenize(sentence)
                tagged = nltk.pos_tag(words)
                for (word, tag) in tagged:
                    if tag == 'PRP': # If the word is a proper noun
                        cou = cou + 1 
        
            return(cou)
        Personal_Pronouns=ProperNounExtractor(article_text)
    

    #function for sentiment analysis
        def sentiment_analysis(text):
            sentiment = TextBlob(text).sentiment
            return (sentiment.polarity),(sentiment.subjectivity)
    
        polarity, subjectivity=sentiment_analysis(cleaned_text)
    
        #complex words count 
        complex_word=0
        for word in cleaned_text.split():
            count=0
            word=re.sub(r'(es|ed)$', '', word )
            for i in range(len(word)):
                if word[i].lower() in vowels:
                    count+=1
                else:
                    count+=0
            if count > 2:
                complex_word+=1
        Complex_Words=complex_word        
                                 
        
    # calculate average word length
        #total_length=sum(len(word) for word in words)
        def Average_Word_count(cleaned_text):
            total_words=len(cleaned_text.split())
            if total_words==0:
                Average_Word_Length=0
            else:
                Average_Word_Length=len(cleaned_text.replace(' ',''))/total_words
            return(Average_Word_Length)
        
        Average_Word_Length=Average_Word_count(cleaned_text)
        
    # calculate % of complex word
        if Word_Count==0:
            Percentage_of_Complex_Word=0
        else:
            Percentage_of_Complex_Word = Complex_Words / Word_Count * 100
    
        data.insert(i,[url,Positive_score, Negative_score, polarity,subjectivity, Avg_Sentence_Length,Percentage_of_Complex_Word,Fog_Index, Avg_no_of_words_per_sentence , Complex_Words, Word_Count,Syllable_Per_Word,Average_Word_Length, Personal_Pronouns])
        

    
if __name__ == '__main__' :  
    text()
        
df = pd.DataFrame(data,columns=['url','Positive_score','Negative_score','polarity','subjectivity', 'Avg_Sentence_Length', 'Percentage_of_Complex_Word','Fog_Index', 'Avg_no_of_words_per_sentence' , 'Complex_Words', 'Word_Count','Syllable_Per_Word','Average_Word_Length','Personal_Pronouns'])


# ### Dataframe to CSV file

# In[171]:


df.to_csv('All_Url.csv')
df

