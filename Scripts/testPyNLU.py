'''
Created on May 17, 2017

@author: dexter
'''

from nluModule import  *
from  Models.SentenceModel import Sentence


n = nluModule()

n.loadModel()

r=n.findAction("I want to buy British Sterling ")
print(r)


