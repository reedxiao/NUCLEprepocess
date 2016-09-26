'''
Created on 26/09/2016

@author: kiarie

This code cleans up the brown data set and puts it into a form that can be consumed by
the seq2seq harvard nlp module
'''
import os
import glob
import re
from nltk.tokenize import sent_tokenize
import string 

class BrownCleanUp(object):
 
    def __init__(self, fileDir, fileName):
       self.fileDir = fileDir
       self.fileName = fileName

    def extractText(self):
        '''Generates text file 
           Splits the text file into appropriate train and eval files    
        '''
        path = self.fileDir
        rx_sequence=re.compile(r"^//(.+?) $",re.MULTILINE)
        
        for filename in os.listdir(path):
            filepath1 = self.fileDir+"/"+filename 
            tmp = []
            with open(filepath1, 'r') as o, open(self.fileName, 'w') as f:   
                data=o.read().replace('\n', '')
                dataClean = re.sub("! !", "! ", data, flags = re.M)
                dataClean = re.sub("\? \?", "\? ", dataClean, flags = re.M)
                dataClean = re.sub("[.]+", ". ", dataClean, flags = re.M)
                
                sent = sent_tokenize(dataClean)
                 
                for s in sent:   
                    s = s.replace('!', ' !')
                    s = s.replace('.', ' .' )
                    s = s.replace(',', ' ,')
                    s = s.replace('?', ' ?')
                    s = s.lstrip()
                    tmp.append(s) 
                
                for l in tmp:
                    f.write(l.lstrip()+"\n")
