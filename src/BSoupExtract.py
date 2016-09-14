'''
Created on 11/09/2016
@author: kiarie ndegwa
Possible better way to parse .sgml format
'''
import re
from copy import deepcopy

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
            type = re.findall("<TYPE>(.*?)</TYPE>", i).pop()
            correction = re.findall("<CORRECTION>(.*?)</CORRECTION>", i)[0]
            start_corr = re.findall("start_off=\"(.*?)\"", i)[0]
            end_corr = re.findall("end_off=\"(.*?)\"", i).pop()
            
            corrDict ={}
            corrDict[(docId, start_corr, end_corr)] = (correction, type)
            
            if (docId, parId) not in mistDict.keys():
                mistDict[(docId, parId)] = []
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
        #TO do:
        #Find means of correction sentences/paragraph using replace
        finalCorr = {}
        print corrections[('41', '0')]
        for i, v in corrections.iteritems():
            if i == ('41', '0'):
                
                sToBeCorr = deepcopy(genSentences[i]) 
                for l in v:                
                    start = int(l.keys()[0][1])
                    end = int(l.keys()[0][2])
                    
                    cphrase = l.values()[0][0]+origPar[i][end:end+4]
                    ctype = l.values()[0][1]
                    print cphrase
                    if ctype != typeEr:
                        sToBeCorr = sToBeCorr.replace(origPar[i][start:end+4], cphrase, 1)            
                finalCorr[i] = sToBeCorr
            
        print finalCorr['41', '0']