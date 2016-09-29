'''
Created on 26/09/2016

@author: Kiarie Ndegwa

This code cleans up the brown data set and puts it into a form that can be consumed by
the seq2seq nlp module

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
        print "Opening final file: {}".format(self.fileName)
        f = open(self.fileName, 'w')

        print "Generating brown corpus"
        for filename in os.listdir(path):
            filepath1 = self.fileDir+"/"+filename 
            tmp = []
            sent = ""
            with open(filepath1, 'r') as o:   
                data=o.read().replace('\n', '')
                dataClean = re.sub("! !", "! ", data, flags = re.M)
                dataClean = re.sub("\? \?", "? ", dataClean, flags = re.M)
                dataClean = re.sub("[.]+", ". ", dataClean, flags = re.M)
                dataClean = re.sub("\'\' ", " ", dataClean, flags = re.M) 
                dataClean = re.sub("\`\` ", " ", dataClean, flags = re.M) 
                dataClean = re.sub("; ;", "; ", dataClean, flags = re.M) 
                dataClean = re.sub("/", " ", dataClean, flags = re.M) 
                
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
                    
        print "Brown corpus generated"