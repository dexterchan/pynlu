'''
Created on May 17, 2017

@author: dexter
'''
from google.cloud import language
from  Models.SentenceModel import Sentence
import json
import operator

class nluModule:
    def __init__(self):
        '''
        Constructor
        '''
        # Instantiates a client
        self.language_client = language.Client()
        self.actionMap={}
        self.dataFile="data/configdata.json"
        self.KeyMap={}
        
    def loadModel(self):
        self.actionMap={}
        with open(self.dataFile,'r') as fr:
            self.actionMap = json.load(fr)
        print(self.actionMap)
        
        for key in self.actionMap.keys():
            self.KeyMap[ key ] = Sentence (key)
        
     
        
    def findAction (self, text):
        document = self.language_client.document_from_text(text)
        annotations = document.annotate_text()
        outputEntity=""
        outputVerb=""
        
        #for token in annotations.tokens:
        #    msg = '%11s: %s' % (token.part_of_speech, token.text_content)
        #    print(msg)
    
        if( len (annotations.entities) > 0):
            outputEntity = annotations.entities[0].name
        
        
        for t in reversed(annotations.tokens):
            if(t.part_of_speech == "VERB"):
                outputVerb=t.text_content
                break
        
        outputResponse={}
        outputResponse["entity"]=outputEntity
        outputResponse["verb"] = outputVerb
        
        strAction = outputVerb+","+outputEntity
        
        contest = {}
        for key in self.actionMap.keys():
            contest [key]=self.KeyMap[ key ].calculateJaccardDist(Sentence( strAction ))
            
        sorted_x = sorted(contest.items(), key=operator.itemgetter(1))
        
        sortedResponse=[]
        for s in sorted_x:
            sortedResponse.append( (self.actionMap [ s[0] ],  s[1] )  )
        
        
        return sortedResponse