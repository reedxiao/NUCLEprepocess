'''
Created on 23/08/2016
@author: Kiarie Ndegwa
'''
import re
import string

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
    @staticmethod
    def collapseDict(dictEntry):
        outputList = []
        for _, v in dictEntry.iteritems():
            for _, nv in v.iteritems():
                outputList.append(nv)
        return outputList
        
    def savetoFile(self, sent, newFilename):
        '''Save dictionary values to text file'''
        with open(newFilename, 'w') as f:
            #Separate line for each sentence
            for line in sent:
                inline = line.split(".")
                for s in inline:
                    if s != "\n": 
                        f.write(s.lstrip()+".\n")
        
    def generateCorr(self):
        '''This saves the silly NUCLE corpus into a data structure that can be used to generate corrected essays'''
        #To do: Make this come out in the same order as the orig text, it has to be a parallel corpus
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
    
    def generateCorEssays(self):
        '''This def uses the stored sentence corrections from generateCorr'''
        MistakeLoc = self.generateCorr()
        incorrData = self.generateOrig()
        finalData = []
        for DocId, _ in incorrData.iteritems():   
            for parId, listOfCor in MistakeLoc[DocId].iteritems():
                #Holder for corrected sentence
                incorrSent = incorrData[DocId][int(parId)]
                correctedMofo = deepcopy(incorrSent)
                for i in range(0, len(listOfCor)-1):
                    if isinstance(listOfCor[i], str):
                        startCor = int(listOfCor[i-1]['startCor'])
                        endCor = int(listOfCor[i-1]['EndCor'])
                        tempCorrWord = listOfCor[i]
                        corrWord = re.sub(' +',' ',tempCorrWord+" "+incorrSent[endCor:endCor+3])
                        
                        replace = incorrSent[startCor:endCor+3]
                        correctedMofo = correctedMofo.replace(replace, corrWord, 1)
                        #print "correct word==>"+corrWord
                        #print "word to be corrected==>"+replace
                        #print correctedMofo
                finalData.append(correctedMofo)
        return finalData
    
    def dictGen(self, TextList):
        '''This takes the generated corpus and turns it into a training dictionary'''
        OutSym = ["<blank> 1", "<unk> 2", "<s> 3","</s> 4"]
        setOf = set(TextList)
        count = 5
        for lex in setOf:
            entry = lex+" "+str(count)
            OutSym.append(entry)
            count = count+1
        return OutSym
        
    def evalGen(self, input, target):
        '''This takes in the input and target inputs and splits into the train, test and eval sets for training
        '''
        num_linesInput = sum(1 for line in open(input))
        num_linesTarget = sum(1 for line in open(input))
        
        
    if __name__ == '__main__':
        pass