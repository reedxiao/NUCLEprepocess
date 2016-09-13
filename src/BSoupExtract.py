'''
Created on 11/09/2016
@author: kiarie ndegwa
Possible better way to parse .sgml format
'''
import re

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
