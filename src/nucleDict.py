'''
Created on 23/08/2016
@author: Kiarie Ndegwa
'''
import re
from copy import deepcopy

class nucleDict(object):
    '''
    This script creates from the 2013 NUCLE CONLL2013 Data set:
    1. the original and target corrected text
    2. target and original text dictionaries needed to train the word2vec model 
    All features are hand crafted and this code is specific to the NUCLE corpus
    '''
    def __init__(self, fileName):
        self.fileName = fileName
        self.uncorrected = self.generateOrig()
        self.corrected = self.generateCorr()
   
    def generateOrig(self):
        '''Generates text from NUCLE .sgml format to plain txt
        .sgml file ==> {DocId: {ParID: Text string}}
        '''
        parDict = {}
        DocId = None
        with open(self.fileName) as fileobject: 
            while(True):
                try:
                    for line in fileobject:
                        if "<DOC" in line.split():
                            DocId = re.findall(r'"(.*?)"', line)[0]
                            parDict[DocId] = []
                        if "<P>" in line.split() and DocId != None:
                            nextSent = fileobject.next()
                            parDict[DocId].append(nextSent)
                    fileobject.next()
                except StopIteration:
                    break

        finalDict = {}
        for i, v in parDict.iteritems():
            par = {}
            for n in range(len(v)):
                par[n] = v[n]
            finalDict[i] = par
        return finalDict
    
    def savetoFile(self, textDict):
        '''Save dictionary values to text file'''
        sent = textDict.value()
        with open(self.fileName, 'w') as f:
            #Separate line for each sentence
            for line in sent:
                inline = line.split(".")
                for s in inline:
                    if s != "\n": 
                        f.write(s.lstrip()+".\n")
        return sent
        
    def generateCorr(self):
        '''This generates the corrected sentences from the corrected NUCLE corpus'''
        Deets= {}
        DocId = None
        parId = None
        corrDeets ={}
        with open(self.fileName) as fileobject: 
            while(True):
                try:
                    for line in fileobject: 
                        if "<DOC" in line.split():
                            DocId = re.findall(r'"(.*?)"', line)[0] 
                            corrDeets.clear()   
                        if "<MISTAKE" in line.split():
                            mist = {}
                            parId =  re.findall(r'"(.*?)"', line)[0]
                            mist["startCor"]= re.findall(r'"(.*?)"', line)[1]
                            mist["EndCor"] = re.findall(r'"(.*?)"', line)[3]
                            if corrDeets.get(parId) == None:
                                corrDeets[parId] = []
                            corrDeets[parId].append(mist)       
                        corrections = re.findall('<CORRECTION>(.*?)</CORRECTION>', line, re.DOTALL) 
                        if len(corrections)!=0:
                            corr = corrections.pop()
                            corrDeets[parId].append(corr)                      
                            Deets[DocId] = deepcopy(corrDeets)  
                    fileobject.next()
                except StopIteration:
                    break  
        return Deets
            
    def dictGen(self):
        '''This takes the generated corrected corpus and turns it into a dictionary'''
    
    def evalGen(self):
        '''This takes in the input and target inputs and splits into the train, test and eval sets for training'''
    
    if __name__ == '__main__':
        pass