'''
Created on 11/09/2016
@author: kiarie ndegwa
Better way to parse .sgml format
'''
import re
import os
import collections
import string
import itertools

from copy import deepcopy
from nltk.tokenize import sent_tokenize
import nltk

class BSoupExtract(object):
    '''
    Experiment with Beautiful Soup html, .sgml parser, which was shit, so had to write my own parser
    '''
    def __init__(self, filename, foldername):
        '''
        Constructor: Takes in nucleDict Object
        extracts text between tags
        '''
        self.fileName= filename 
        self.extracted = self.extractSentences()
        self.foldername = foldername
        
    def extractSentences(self):
        extract = {}
        cleanExtract = {}
        with open(self.fileName) as fileobject: 
            tagCount = False
            DocId = ""
            for line in fileobject:
                if "<DOC" in line.split():
                    DocId = re.findall(r'"(.*?)"', line)[0]
                    tagCount = True
                    extract[DocId] = [] 
                if tagCount == True:
                    extract[DocId].append(line)
                if "</DOC>" in line.split():
                    tagCount = False
        #Merge all strings within each 
        for dociD, txtList in extract.iteritems():
            str = ''
            for lin in txtList:
                str = str+lin
            cleanExtract[dociD] = str

        return cleanExtract
    
    def extractMistakesAndCorrection(self, docId):
        '''output ==> {(DocId, ParId): [{(DocId, ParId): {(docId, start, end): (correction, type)}}]'''
        #Return dict of mistakes
        text = self.extracted[docId]
        tag = "<MISTAKE(.*?)\n</MISTAKE>"
        
        mistList = re.findall(tag, text, re.DOTALL)
        mistDict ={}

        for i in mistList:
            #Make sure item in list needs to be corrected, if not skip

            parId = re.findall("start_par=\"(.*?)\"", i).pop()
            typeE = re.findall("<TYPE>(.*?)</TYPE>", i).pop()
           
           
            start_corr = re.findall("start_off=\"(.*?)\"", i)[0]
            end_corr = re.findall("end_off=\"(.*?)\"", i)[0]

            if len(re.findall("<CORRECTION>(.*?)</CORRECTION>", i)) ==0:
                correction = ""
            else:
                correction = re.findall("<CORRECTION>(.*?)</CORRECTION>", i)[0]
            
            
            corrDict ={}
            corrDict[(docId, start_corr, end_corr)] = (correction, typeE)

            if (docId, parId) not in mistDict.keys():
                mistDict[(docId, parId)] = []
                mistDict[(docId, parId)].append(corrDict)
            else:
                mistDict[(docId, parId)].append(corrDict)
            #print mistDict 
        return mistDict
    
    def extractParagraph(self, docId):
        '''output ==> {(DocId, ParId): list(Paragraph)}
        Why nucle2014 so terrible? 
        '''
        text = self.extracted[docId]
        tag = "<P>\n(.*?)\n</P>"
          
        noR = text.split("<REFERENCE>")
        dataClean = re.sub("<REFERENCE>.*?</REFERENCE>", "", text, flags = re.DOTALL)
        dataClean = re.sub("\-\-.*?", "", text, flags = re.DOTALL)
        dataClean = re.sub("\[.*?\]", "", dataClean, flags = re.DOTALL)
        dataClean = re.sub("\(.*?\)", "", dataClean, flags = re.DOTALL)
        dataClean = re.sub("http*?", "", dataClean, flags = re.DOTALL)
        dataClean = re.sub("www*?", "", dataClean, flags = re.DOTALL)
        dataClean = re.sub("/\/\*?", "", dataClean, flags = re.DOTALL)
        dataClean = re.sub("/{*?/}", "", dataClean, flags = re.DOTALL)
        dataClean = re.sub("p:.*?", "", dataClean, flags = re.DOTALL)
        dataClean = re.sub("Retrieved.*?", "", dataClean, flags = re.DOTALL)
        dataClean = re.sub("<{.*?}>", "", dataClean, flags = re.DOTALL)
        dataClean = re.sub("www.*?.com|www.*?.org", "", dataClean, flags = re.DOTALL)
        
        noR = dataClean.split("Reference")
        if len(noR) >=1:
            SHIT = noR[0]
            shitty = SHIT.split("Reference")
            if len(shitty)!=0:
                listPar = re.findall(tag, shitty[0], re.DOTALL)
            else:
                listPar = re.findall(tag, SHIT, re.DOTALL)
        else:
            listPar = re.findall(tag, text, re.DOTALL)
            
        ParDict = {}
        
        for i in range(0, len(listPar)):
            #print listPar[i]
            ParDict[docId, str(i)] = listPar[i]
        return ParDict
    
    def genCorrections(self, docId, typeEr):
        #Generates fully corrected corpus
        corrections = self.extractMistakesAndCorrection(docId)
        origPar = self.extractParagraph(docId)
       
        genSentences = deepcopy(origPar)

        finalCorr = {}
        for i, v in corrections.iteritems():
            #If the paragraphs has sentences that need to be corrected
            if i in genSentences:
                sToBeCorr = deepcopy(genSentences[i]) 
                for l in v:
                    start = int(l.keys()[0][1])
                    end = int(l.keys()[0][2])
                    
                    #print "the start {}, the end {}".format(start, end)
                    cphrase = l.values()[0][0]+origPar[i][end:end+10]
                    ctype = l.values()[0][1]
               
                    if  ctype != typeEr:
                        #generate corrected sentence
                        sToBeCorr = sToBeCorr.replace(origPar[i][start:end+10], cphrase, 1)
                    else:
                        #Ignore collocation error
                        continue
                finalCorr[i] = sToBeCorr
                finalCorr = collections.OrderedDict(sorted(finalCorr.items()))
            #Else if the paragraphs have no incorrect parts
        return finalCorr
    
    def preSave(self):
        CorrectedEssays = {}
        UncorrectedEssays = {}
        DocIDs = self.extractSentences().keys()
        #Pass doc Ids through paragraph correction
        print "Presave in progress"
       
        #This is meant to generate error exceptions
        for i in DocIDs:
            for k, v in self.extractParagraph(i).iteritems():    
                UncorrectedEssays[k] = v 
            for k, v in self.genCorrections(i, 'Null Value').iteritems():                
                CorrectedEssays[k] = v 
                #print v
        #Sort Corrected essays by keys
        CorrectedEssays = collections.OrderedDict(sorted(CorrectedEssays.items()))
        UncorrectedEssays = collections.OrderedDict(sorted(UncorrectedEssays.items()))
        
        for k, v in UncorrectedEssays.iteritems():
            if k not in CorrectedEssays.keys():
                CorrectedEssays[k] = v
      
        return UncorrectedEssays, CorrectedEssays
    
    #Save original and corrected sentences
    def savetoFile(self, par, newFilename, sorting, *evalu):
        '''Save list of sentences to text file'''
        foldername = "../"+self.foldername
        
        if not os.path.exists(foldername):
            os.makedirs(foldername)
                #Add text files to the folder
        path = os.path.join(foldername, newFilename)
        
        with open(path, 'w') as f:
            #Separate line for each sentence
            if sorting == None:
                for s in par:
                    s = s.replace('!', ' !')
                    s = s.replace('.', ' .')
                    s = s.replace(',', ' ,')
                    s = s.replace('?', ' ?')

                    if evalu[0] == True: 
                        f.write(s.lstrip()) 
                    elif evalu[0] == False:                                                      
                        f.write(s.lstrip()+"\n")   
                print newFilename+"dict/eval  file saved"  
            elif sorting !=None:
                for line in sorting:
                    h =  par[line]
                    eh = re.sub(r'[^\x00-\x7F]+',' ', h)
                    inline =  sent_tokenize(eh)
                    for s in inline:
                        s = s.replace('!', ' !')
                        s = s.replace('.', ' .')
                        s = s.replace(',', ' ,')
                        s = s.replace('?', ' ?')                                                       
                        f.write(s.lstrip()+"\n")
        print newFilename+" file saved"    
    
    #Deprecated function replaced with length checked eval
    def evalGen(self, inputtxtfile, src_or_targ):
        '''This takes in the input and splits it into the train, test and eval sets for training
        '''
        inputtxtfile = "../"+self.foldername+"/"+inputtxtfile
        num_linesInput = sum(1 for line in open(inputtxtfile))
        train = int(round(0.7*num_linesInput))
        evalD =  int(round(0.2*num_linesInput))
        
        trainList = []
        evalList = []
        testList = []
        
        count = 0
        with open(inputtxtfile) as fileobject:
            for i in fileobject:
                if(count <= train):
                    trainList.append(i) 
                elif(count > train):
                    evalList.append(i)  
                elif(count > train+evalD):
                    testList.append(i)
                count = count +1   
                
        #Generate training data and save to file
        self.savetoFile(filter(None, trainList), src_or_targ+"-train.txt", None, True)
        #Generate validation data and Save to file
        self.savetoFile(filter(None, evalList), src_or_targ+"-val.txt", None, True)     
        #Generate test data and Save to file
        self.savetoFile(filter(None, testList), src_or_targ+"-test.txt", None, True)     
    
    def LengthCheckedEval(self):
        #Strip all paragraphs with different numbers of sentences
        src, trg = self.preSave()
        keysEval = src.keys()
        
        fin_src = []
        fin_tar = []

        for i in keysEval:
            h =  trg[i]
            eh = re.sub(r'[^\x00-\x7F]+',' ', h)
            
            h1 =  src[i]
            eh1 = re.sub(r'[^\x00-\x7F]+',' ', h1)
            if len(sent_tokenize(eh1)) == len(sent_tokenize(eh)):
                fin_src.append(sent_tokenize(eh1))
                fin_tar.append(sent_tokenize(eh))
        
        finS = list(itertools.chain.from_iterable(fin_src))
        finT = list(itertools.chain.from_iterable(fin_tar))
        
        #Generate train, eval and test sets
        num_linesInput = len(finS)
        train = int(round(0.7*num_linesInput))
        evalD =  int(round(0.3*num_linesInput))
        
        #fin lists
        #Source
        src_trainList = []
        src_evalList = []
        
        #Train
        trg_trainList = []
        trg_evalList = []
        #Final lists
        count  = 0
        
        for i, j in zip(finS, finT):
            if(count <= train):
                src_trainList.append(i) 
                trg_trainList.append(j) 
            elif(count > train):
                src_evalList.append(i) 
                trg_evalList.append(j)
            count = count +1    
        
        #Source text
        #Generate training data and save to file
        self.savetoFile(src_trainList,"src-train.txt", None, False)
        #Generate test data and Save to file
        self.savetoFile(src_evalList, "src-val.txt", None, False)
       
        #target text
        #Generate training data and save to file
        self.savetoFile(trg_trainList,"targ-train.txt", None, False)
        #Generate test data and Save to file
        self.savetoFile(trg_evalList, "targ-val.txt", None, False)
       
    @staticmethod
    def collapseDict(genEntry):
        outputList = []
        for _, v in genEntry.iteritems():
            outputList.append(v)
        return outputList
    
    
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