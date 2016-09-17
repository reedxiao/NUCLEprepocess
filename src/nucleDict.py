'''
Created on 23/08/2016
@author: Kiarie Ndegwa
'''
import re
import nltk
import string
import collections
import BSoupExtract
import os

from nltk.tokenize import sent_tokenize

from copy import deepcopy


class nucleDict(object):
    '''
    This script creates from the 2013 NUCLE CONLL2013 Data set:
    1. the original and target corrected text
    2. target and original text dictionaries needed to train the word2vec model 
    All features are hand crafted and this code is specific to the NUCLE corpus
    '''
    def __init__(self, fileName, foldername):
        self.fileName = fileName
        self.uncorrected = self.generateOrig()
        self.corrected = self.generateCorr()
        self.foldername = foldername
        
    def generateOrig(self):
        '''Generates text from NUCLE .sgml format to plain useable data structure
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
            for n in range(0, len(v)-1):
                par[n] = v[n]
            finalDict[i] = par
        finalDict = collections.OrderedDict(sorted(finalDict.items()))
        return finalDict

    @staticmethod
    def collapseDict(genEntry):
        outputList = []
        for _, v in genEntry.iteritems():
            for _, nv in v.iteritems():
                outputList.append(nv)
        return outputList
        
    def savetoFile(self, sent, newFilename, flag):
        '''Save list of sentences to text file'''
        foldername = "../"+self.foldername
        if not os.path.exists(os.path.dirname(foldername)):
            try:
                os.makedirs(os.path.dirname(foldername))
                #Add text files to the folder
                path = os.path.join(foldername, newFilename)
                with open(path, 'w') as f:
                    #Separate line for each sentence
                    for line in sent:
                        inline =  sent_tokenize(line)
                        for s in inline:
                            s = s.replace('!', ' !')
                            s = s.replace('.', ' .')
                            s = s.replace(',', ' ,')
                            s = s.replace('?', ' ?')
                            #s = s.replace('\n', '')
                            if flag == True:                                      
                                f.write(s.lstrip())
                            else:
                                f.write(s.lstrip())   
                print newFilename+" file saved"           
            except OSError as exc:
                raise
            else:
                path = os.path.join(foldername, newFilename)
                with open(path, 'w') as f:
                    #Separate line for each sentence
                    for line in sent:
                        inline =  sent_tokenize(line)
                        for s in inline:
                            s = s.replace('!', ' !')
                            s = s.replace('.', ' .')
                            s = s.replace(',', ' ,')
                            s = s.replace('?', ' ?')
                            #s = s.replace('\n', '')
                            if flag == True:                                      
                                f.write(s.lstrip())
                            else:
                                f.write(s.lstrip())   
                print newFilename+" file saved"        
                
        
    def generateCorr(self):
        '''This saves the silly NUCLE corpus into a data structure that can be used to generate corrected essays'''
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
                        #to do:
                        #Make sure you do something with the fact that something with the collocation errors
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
        incord = []
        print "incorrData keys"
        print incorrData.itervalues().next()
        
        print "mistakes locations"
        print MistakeLoc.itervalues().next()
        
        #TO DO 
        #What the hell is going on here with regards to the data structures
        #Do the list of corrections and the list of the original texts line up at all?
        for DocId, DictOfParIDs in incorrData.iteritems(): 
            for parId, listOfCor in collections.OrderedDict(sorted(MistakeLoc[DocId].items())).iteritems():
                if int(parId) in [int(i) for i in incorrData[DocId].keys()]:
                    incorrSent = incorrData[DocId][int(parId)]
                    incord.append(incorrSent)
                    correctedMofo = deepcopy(incorrSent)
                    for i in range(0, len(listOfCor)):
                        if isinstance(listOfCor[i], str):
                            startCor = int(listOfCor[i-1]['startCor'])
                            endCor = int(listOfCor[i-1]['EndCor'])
                            tempCorrWord = listOfCor[i]                        
                            corrWord = re.sub(' +',' ',tempCorrWord+" "+incorrSent[endCor:endCor+3])
                            replace = incorrSent[startCor:endCor+3]
                            correctedMofo = correctedMofo.replace(replace, corrWord, 1)
                    finalData.append(correctedMofo)
        return finalData, incord
     
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
                elif(count > train+evalD):
                    testList.append(i)
                count = count +1       
        #Generate training data and save to file
        self.savetoFile(trainList, src_or_targ+"-train.txt", True)
        #Generate test data and Save to file
        self.savetoFile(evalList, src_or_targ+"-val.txt", True)
        #Generate evaluation data and Save to file
        self.savetoFile(testList, src_or_targ+"-test.txt", True)
    
    def Opt1collocationError(self):
        #The target sentence generated only fixes the collocation errors and ignores all else
        #The source corpus is the unchanged 
        dictOrigin = BSoupExtract.BSoupExtract(self.fileName).extractSentences()
        #print dictOrigin.keys()
        docIDs = [int(i) for i in dictOrigin.keys()]	        
        docIDs.sort()

        mistakeTags = []
        for i in docIDs:
            t = (re.findall('<MISTAKE(.*?)</MISTAKE>', dictOrigin[str(i)], re.DOTALL), i)
            mistakeTags.append(t)
        errorCorr = []
        sent = self.uncorrected
        for mistakes in mistakeTags:
            for mistake in mistakes[0]:
                err = re.findall('<TYPE>(Wci)</TYPE>(.*?)<CORRECTION>(.*?)</CORRECTION>', mistake, re.DOTALL)
                #Sentence coordinates
                locStart = re.findall('start_off="(.*?)"', mistake, re.DOTALL)
                locEnd = re.findall('end_off="(.*?)">', mistake, re.DOTALL)
                SentCoord = ("start_id="+locStart[0], "end_id="+locEnd[0])
                #Paragraph coordinates
                SParCoord = re.findall('start_par="(.*?)"', mistake, re.DOTALL)
                EParCoord = re.findall('end_par="(.*?)"', mistake, re.DOTALL)
                ParCoord = ("start_par="+SParCoord[0], "end_par="+EParCoord[0])
                #Get sentence that needs to be corrected?
                if len(err)!=0:
                    fin = []
                    f = re.findall('<TYPE>Wci</TYPE>\n(.*?)<CORRECTION>(.*?)</CORRECTION>', mistake, re.DOTALL)
                    if f[0][1]=='':
                        chop = sent[str(mistakes[1])].get(int(SParCoord[0]))
                        tobeCorr = chop[int(locStart[0]):int(locEnd[0])]
                    chop = sent[str(mistakes[1])].get(int(SParCoord[0]))  
                    tobeCorr =  None
                    if chop !=None:
                        tobeCorr = chop[int(locStart[0]):int(locEnd[0])]
                    fin = (f[0][1], tobeCorr, SentCoord, "Doc id: "+str(mistakes[1]), ParCoord)
            #print fin
    def Opt2collocationError(self, textList):
        #Source corpus has all corrections but the collocation errors
        #Target sentence has isolated collocation sentences
        pass
    
    if __name__ == '__main__':
        pass
