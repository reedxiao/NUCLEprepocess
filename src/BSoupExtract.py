'''
Created on 11/09/2016
@author: kiarie ndegwa
Possible better way to parse .sgml format
'''
import re
import os

from copy import deepcopy
from nltk.tokenize import sent_tokenize

class BSoupExtract(object):
    '''
    Experiment with Beautiful Soup
    '''
    def __init__(self, filename):
        '''
        Constructor: Takes in nucleDict Object
        extracts text between tags
        '''
        self.fileName= filename 
        self.extracted = self.extractSentences()
        
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
    
    def extract(self, docId, tag):
        text = self.extracted[docId]
        tag = "<"+tag+"(.*?)"+"/"+tag+">"
        return re.findall(tag, text, re.DOTALL)
    
    def extractMistakesAndCorrection(self, docId):
        '''output ==> {(DocId, ParId): [{(DocId, ParId): {(docId, start, end): (correction, type)}}]'''
        #Return dict of mista
        text = self.extracted[docId]
        tag = "<MISTAKE(.*?)\n</MISTAKE>"
        
        mistList = re.findall(tag, text, re.DOTALL)
        mistDict ={}

        for i in mistList:

            parId = re.findall("start_par=\"(.*?)\"", i).pop()

            typeE = re.findall("<TYPE>(.*?)</TYPE>", i).pop()
            correction = re.findall("<CORRECTION>(.*?)</CORRECTION>", i)[0]
            start_corr = re.findall("start_off=\"(.*?)\"", i)[0]
            end_corr = re.findall("end_off=\"(.*?)\"", i)[0]
            
            corrDict ={}
            corrDict[(docId, start_corr, end_corr)] = (correction, typeE)

            if (docId, parId) not in mistDict.keys():
                mistDict[(docId, parId)] = []
                mistDict[(docId, parId)].append(corrDict)
            else:
                mistDict[(docId, parId)].append(corrDict) 
        return mistDict
    
    def extractParagraph(self, docId):
        '''output ==> {(DocId, ParId): list(Paragraph)}'''
        text = self.extracted[docId]
        tag = "<P>\n(.*?)\n</P>"
        listPar = re.findall(tag, text, re.DOTALL)
        ParDict = {}
        for i in range(0, len(listPar)):
            ParDict[docId, str(i)] = listPar[i]
        return ParDict
    
    def genCorrections(self, docId, typeEr):
        #Generates fully corrected corpus
        corrections = self.extractMistakesAndCorrection(docId)
        origPar = self.extractParagraph(docId)
        genSentences = deepcopy(origPar)

        finalCorr = {}
        for i, v in corrections.iteritems():
            sToBeCorr = deepcopy(genSentences[i]) 
            for l in v:
                                
                start = int(l.keys()[0][1])
                end = int(l.keys()[0][2])
                
                cphrase = l.values()[0][0]+origPar[i][end:end+10]
                ctype = l.values()[0][1]

                if ctype != typeEr:
                    sToBeCorr = sToBeCorr.replace(origPar[i][start:end+10], cphrase, 1)            
            finalCorr[i] = sToBeCorr
        return finalCorr
    
    def savetoFile(self, sent, newFilename, foldername):
        '''Save list of paragraphs and saves to text file'''
        foldername = "../"+foldername
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
                            f.write(s.lstrip())    
                print newFilename+" file saved"
                                   
            except OSError as exc:
                raise