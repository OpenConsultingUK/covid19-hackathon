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
    nlp_qa = pipeline('question-answering')
    f = open("../data/covidinfo.txt", "r")
    context = f.read() 

    response = nlp_qa(context=context, question=query)
    
    return response['answer']
