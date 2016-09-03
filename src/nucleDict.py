'''
Created on 23/08/2016
@author: Kiarie Ndegwa
'''
import re
import nltk
import string
import collections

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
        print "GENERATING ORIGINAL TEXT"
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
        #Sort dictionary, by turning it into a generator 
        finalDict = self.sortdict(finalDict)
        return finalDict
    
    @staticmethod
    def sortdict(d, **opts):
    # **opts so any currently supported sorted() options can be passed
    #Also returns a generator that can be iterated over simply
        for k in sorted(d, **opts):
            yield k, d[k]
    
    @staticmethod
    def collapseDict(genEntry):
        outputList = []
        for _, v in genEntry:
            for _, nv in v.iteritems():
                outputList.append(nv)
        return outputList
        
    def savetoFile(self, sent, newFilename):
        '''Save list of sentences to text file'''
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
        print "GENERATING CORRECT SENTENCES"
        incorrData = {c[0]:c[1] for c in incorrData}
        incorrData = collections.OrderedDict(sorted(incorrData.items()))
        for DocId, _ in incorrData.iteritems(): 
            #Sort items in mistakeLoc
            #for parId, listOfCor in MistakeLoc[DocId].iteritems():
            print DocId
            check = 0
            for parId, listOfCor in collections.OrderedDict(sorted(MistakeLoc[DocId].items())).iteritems():
                
                print "Par id: "+parId
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
        #This takes the generated corpus and turns it into a training dictionary
        OutSym = ["<blank> 1", "<unk> 2", "<s> 3","</s> 4"]
        setOf = set()
        count = 5
        exclude = set(string.punctuation)
        for lex in TextList:
            sentence = nltk.sent_tokenize(lex)
            for words in sentence:
                wordList = nltk.word_tokenize(words)
                for entry in wordList:
                    if entry not in exclude and entry not in setOf and entry.isdigit() == False:
                        dictWord = entry+" "+str(count)
                        setOf.add(entry)
                        OutSym.append(dictWord)
                        count = count+1
        return OutSym
        
    def evalGen(self, inputtxtfile, src_or_targ):
        '''This takes in the input and splits it into the train, test and eval sets for training
        '''
        num_linesInput = sum(1 for line in open(inputtxtfile))
        train = int(round(0.6*num_linesInput))
        evalD =  int(round(0.3*num_linesInput))
        
        trainList = []
        evalList = []
        testList = []
        count = 0
        with open(inputtxtfile) as fileobject:
            for i in fileobject:
                if(count <= train):
                    trainList.append(i)
                elif(count > train and count <=train+evalD):
                    evalList.append(i)
                else:
                    testList.append(i)
                    
                count = count +1
                print count
        #Generate training data and save to file
        self.savetoFile(trainList, src_or_targ+"-train.txt")
        #Generate test data and Save to file
        self.savetoFile(evalList, src_or_targ+"-val.txt")
        #Generate evaluation data and Save to file
        self.savetoFile(testList, src_or_targ+"-test.txt")
        
    if __name__ == '__main__':
        pass