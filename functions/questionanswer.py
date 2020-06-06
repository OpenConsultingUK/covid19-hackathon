# -*- coding: utf-8 -*-
"""
Created on Fri May 29 19:15:11 2020

@author: Minu Beena Sisupal
"""


def qna(query):
    """
    This function uses NLP technique to give response to user queries.
    """
    from transformers import pipeline
    #mp.freeze_support()
    nlp_qa = pipeline('question-answering',model = 'bert-large-cased-whole-word-masking-finetuned-squad')

    f = open("../data/covidinfo.txt", "r")
    context = f.read() 
    
    response = nlp_qa(context=context, question=query,tokenizer="distilbert-base-cased")
    
    return response['answer']

print(qna('What is Coronaviruses'))