##importing libraries


import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pdfminer.high_level import extract_text
import nltk
import re 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords



def job_application_admitter(folder,skills,en,lenn):
    entries=int(en)
    length=int(lenn)
    input_skills=str(skills)


    #folder: path of resumes
    #length: length of id



    ##step 1: 
    ## pdf to data frame
    x=[os.path.join(r,file) for r,d,f in os.walk(folder) for file in f]
    d=pd.DataFrame()
    d["ID"]=x
    d["Resume"]=None
    for i in d.index:
        data=extract_text(d["ID"][i])
        d["Resume"][i]=data
        a=str(d["ID"][i])[-4-length:-4:1]
        d["ID"][i]=a

    #step 2:
    # skills dataset
    Skills=pd.read_csv("SkillsList.csv",encoding= 'unicode_escape')
    # print(Skills)
    SkillsList=Skills['Skills'].tolist()

    ##step 3:
    ##cleaning resume
    clean = []
    for i in range(d.shape[0]):
        review = re.sub(
            '(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"',
            " ",
            d["Resume"].iloc[i],
        )
        review = review.lower()
        review = review.split()      
        lm = WordNetLemmatizer()
        review = [
            lm.lemmatize(word)
            for word in review
            if not word in set(stopwords.words("english"))
        ]
        review = " ".join(review)
        clean.append(review)
    d["Clean_Resume"] = clean


    ##step 4:
    ##extracting skills
    d["Skills"]=None
    for i in range(d.shape[0]):
        stop_words = set(nltk.corpus.stopwords.words('english'))         
        word_tokens = nltk.tokenize.word_tokenize(d["Clean_Resume"][i])          #to tokenize the word
        # print(word_tokens)
    
        # remove the stop words and punctuation
        filtered_tokens = [w for w in word_tokens if w not in stop_words and w.isalpha()]
    
        # generate bigrams and trigrams (such as artificial intelligence)
        bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))    # return all the bigrams and trigrams from filtered tokens
    
        # set to keep the results in.
        found_skills = set()
        SkillsList=[lm.lemmatize(i) for i in SkillsList]
    
        # search for each token in our skills database
        for token in filtered_tokens:
            if token.lower() in SkillsList:
                found_skills.add(token)
        # search for each bigram and trigram in our skills database
        for ngram in bigrams_trigrams:
            if ngram.lower() in SkillsList:
                found_skills.add(ngram)
        d["Skills"][i]=found_skills


    ## ranking the data
    m=[]
    d["Score"]=None
    skills = input_skills.split(",")
    for i in range(d.shape[0]):
        sc = 0
        for x in skills:
            if x in d["Skills"][i]:
                sc += 1
        match = round((sc / len(skills)) * 100, 1)
        d["Score"][i]=match
    data=d.sort_values(by="Score",ascending=False)
    for i in range(entries):
        if(data["Score"][i]>0.0):
            m.append(data["ID"][i])
    # print(data)
    return m



# length=int(input("Enter the length of ID: "))
# folder=input("Enter the path of resumes: ")
# input_skills=input("Enter the skills you want to have : ")
# entries=int(input("Enter the number of resumes you want to select: "))
# print(job_application_admitter(folder,input_skills,entries,length))

