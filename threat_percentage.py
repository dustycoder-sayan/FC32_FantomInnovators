#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import operator
import seaborn as sns
import text2emotion as te


# ### Defining miniature dataset of positive, negative and neutral words used

# In[2]:


li_pos = ['😀','😁','😂','🤣','😃','😄','😆','😋','😎','🙂','love', 'happy', 'thank', 'mother', 'day', 'good', 'get', 'get', 'go', 'today', 'work', 'twitter', 'really', 'sleep', 'see', 'say', 'night', 'tomorrow']


# In[3]:


li_neut = ['😌','😉','🤗','🙄','🙂','😐','😑','work', 'day', 'one', 'know', 'want', 'find', 'see', 'haha', 'lol', 'make', 'week', 'much', 'need', 'well', 'take', 'wait', 'day', 'back', 'look', 'leave', 'well', 'home', 'still', 'show', 'ye', 'away', 'phone', 'think', 'get', 'I miss you']


# In[4]:


li_neg = ['😠','😒','😡','💢','🗯','👿','kill', 'murder','die', 'you will die', 'will kill you', 'will rape you', 'you will be raped', 'suicide', 'rape', 'kill yourself', 'fuck', 'get', 'miss', 'think', 'sad', 'go', 'sorry', 'today', 'really', 'hate', 'lol', 'sick', 'suck', 'feel']


# ### Syntactic Detection

# In[5]:


with open('full-list-of-bad-words_comma-separated-text-file_2022_05_05.txt', 'r') as foul_words:
    foul = foul_words.read()


# In[6]:


foul_li = foul.split(',')
for word in foul_li:
    word.strip


# In[7]:


def detect_foul(word):
    word.lower()
    if word in foul_li:
        return True
    return False

def foul_density(text):
    cnt=0
    li = text.split()
    li = [word.lower() for word in li]
    length = len(li)
    for word in li:
        if word in foul_li:
            cnt+=1
    return (cnt/length)*100


# In[8]:


def all_upper(word):
    return word.isupper()

def upper_density(text):
    cnt=0
    li = text.split()
    length = len(li)
    for word in li:
        if all_upper(word):
            cnt+=1
    return (cnt/length)*100;


# In[9]:


def badness_of_sentence(text):
    rat = int(foul_density(text))
    up = int(upper_density(text))
    
    if up<50:
        if rat>=70:
            return 0   #High
        elif rat>=30 and rat<70:
            return 30  #Medium
        else:
            return 80  #Low
    else:
        if rat>=50:
            return 0   #High
        else:
            return 80  #Low


# ### String matching

# In[10]:


def lesser(neut, pos, neg):
    least = "Neutral"
    if (neut <= pos) and (neut <= neg):
       least = 'Neutral'
    elif (pos <= neut) and (pos <= neg):
       least = 'Positive'
    else:
       least = 'Negative'
    return least


# In[11]:


def larger(neut, pos, neg):
    largest = "Neutral"
    if (neut >= pos) and (neut >= neg):
       largest = 'Neutral'
    elif (pos >= neut) and (pos >= neg):
       largest = 'Positive'
    else:
       largest = 'Negative'
    return largest


# In[12]:


def get_sentiment(text, cnt_neut=0, cnt_pos=0, cnt_neg=0, index_pos=0, index_neg=0, index_neut=0):
    if '.' in text:
        te = text.split('.')
    else:
        te = text
    for sentence in te:
        words = sentence.split()
        for word in words:
            if word in li_pos:
                index_pos = li_pos.index(word)
            elif word in li_neg:
                index_neg = li_neg.index(word)
            elif word in li_neut:
                index_neut = li_neut.index(word)
            else:
                index_neut = len(li_neut)+1
            least = lesser(index_neut, index_pos, index_neg)
            if least=="Neutral":
                cnt_neut+=1
            elif least=="Positive":
                cnt_pos+=1
            else:
                cnt_neg+=1
    return larger(cnt_neut, cnt_pos, cnt_neg)


# ### threat percentage

# In[13]:


def threat_percentage(text):
    badness = badness_of_sentence(text)
    emotion = get_emotion(text)
    emotion_cnt=0
    sentiment = get_sentiment(text)
    sentiment_cnt=0
    if emotion.lower()=='happy':
        emotion_cnt = 100
    elif emotion.lower()=='sad':
        emotion_cnt = 50
    elif emotion.lower()=='excited':
        emotion_cnt = 70
    elif emotion.lower()=='angry':
        emotion_cnt = 0
        
    if sentiment.lower()=='postive':
        sentiment_cnt = 100
    elif sentiment.lower()=='negative':
        sentiment_cnt = 0
    else:
        sentiment_cnt = 50
    
    return (100 - (badness+emotion_cnt+sentiment_cnt)/3)


# In[14]:


def threshold_percentage(text):
    threshold = 75
    if threat_percentage(text) > 50:
        return True
    else:
        return False

def threshold_percentage_number(num):
    if num>50:
        return True
    else:
        return False


# ### Emotion Analysis

# In[16]:


def get_emotion(text):
    dict = te.get_emotion(text)
    max_key = max(dict, key=dict.get)
    return max_key


# In[17]:




# In[ ]:




