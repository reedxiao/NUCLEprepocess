'''
Created on 13/09/2016

@author: Kiarie Ndegwa

This class uses all the inputs from nucleDict and saves them to a training folder
'''
class CorpusTest(object):
    '''
    Contains a simple save to folder function
    '''
    def __init__(self, f1, f2):
        '''
        full relative path names 
        '''
        self.f1 = f1
        self.f2 = f2
    
    def testCorpus(self):
        list1 = []
        list2 =[]
        print "its working hombre"
        with open(self.f1) as fileobject:
            for i in fileobject:
                list1.append(i)
                
        with open(self.f2) as fileobject:
            for i in fileobject:
                list2.append(i)
        
        for i in range(0, len(list1)):
            if list1[i] == list2[i]:
                continue
            else:
                print "list1"
                print list1[i]
                print "list2"
                print list2[i]
            