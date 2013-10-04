'''
Created on 05/10/2009

@author: Fernando

    Copyright 2009-2013 Fernando J. V. da Silva
    
    This file is part of centering_py.

    centering_py is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    centering_py is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with centering_py.  If not, see <http://www.gnu.org/licenses/>.


'''

import re

class PALAVRAS_Tokenizer:
    '''
    classdocs
    '''

    words = []
    elements = []
    source = None
    

    def __init__(self, source):
        '''
        Constructor
        '''
        tmp_words = source.split('\n')
        for tmp_word in tmp_words:
            self.words.append(Word(tmp_word))
        coverNounPrhares()
        
        
    def coverNounPhrases(self):
        curr_np = None
        for i in range(len(self.words)):
            
            ''' if it wants to attach to a Noun ... '''
            if self.words[i].properties['synt'] == 'N':
                ''' if there isn't any opened Noun Phrase, then starts a new one ... '''
                ''' 
                    if there is a opened Noun Phrase, so there is 2 ways to follow:
                    - if the word wants to attaches to the LAST NP, so it attaches ...
                    - if the word wants to attaches to the NEXT NP, so it closes the current NP, append it to the elements list, start a new 
                    current NP and attaches to it.
                ''' 
                if curr_np == None:
                    curr_np = NP()
                    curr_np.words.append(self.words[i])                                
                else:                                    
                    if self.words[i].attacher == '<':
                        curr_np.words.append(self.words[i])
                    else:
                        self.elements.append(curr_np)                        
                        curr_np = NP()
                        curr_np.words.append()
            
            elif self.words[i].properties['class'] == 'N':
                if curr_np == None:
                    curr_np = NP()
                if curr_np.has_Nclass:
                    self.elements.append(curr_np)                    
                    curr_np = NP()                    
                curr_np.words.append(self.words[i])
                curr_np.synt = self.words[i].properties['synt']
                curr_np.gender = self.words[i].properties['gender']
                curr_np.number = self.words[i].properties['number']
                curr_np.has_Nclass = True
            
            else:
                if curr_np != None:
                    self.elements.append(curr_np)
                    curr_np = NP()
                self.elements.append(self.words[i])
            
            
            
class NP:
    words = []
    gender = None
    number = None       
    synt = None
    has_Nclass = False     
            
        
        
class Word:
    
    ''' tagging constants   '''
    CLASSES = ['N','PROP','SPEC','DET','PERS','ADJ','ADV','V','NUM','KS','KC','IN']
    GENDER = ['M','F','M/F']
    NUMBER = ['S','P','S/P']
    CASE = ['NOM','ACC','DAT','PIV','ACC/DAT','NOM/PIV']
    PERSON = ['1S','1P','2S','2P','3S','3P','1/3S','0/1/3S']
    TENSE = ['PR','IMPF','PS','MQP','FUT','COND']
    MOOD = ['IND','SUBJ','IMP']
    FINITENESS = ['VFIN','INF','PCP','GER']
    
    tokens = []
    properties = {}
    
    attacher = None
    
    def __init__(self, source):
        self.tokens = source.split(' ')
        self.tokenize()
        
    def tokenize(self):
        for i in range(len(self.tokens)):
            self.matchToken(self.tokens[i])
            
    def matchToken(self, token):
                
        ''' match class '''
        if token in self.CLASSES:
            self.properties['class'] = token
            return
        
        ''' match gender '''
        if token in self.GENDER:
            self.properties['gender'] = token
            return
            
        ''' match number '''
        if token in self.NUMBER:
            self.properties['number'] = token
            return
        
        ''' match case '''
        if token in self.CASE:
            self.properties['case'] = token
            return
            
        ''' match person '''
        if token in self.PERSON:
            self.properties['person'] = token
            return
                  
        ''' match tense '''
        if token in self.TENSE:
            self.properties['tense'] = token
            return  
        
        ''' match mood '''
        if token in self.MOOD:
            self.properties['mood'] = token
            return
        
        ''' match finiteness '''
        if token in self.FINITENESS:
            self.properties['fin'] = token
            return
                
        ''' match main '''
        if re.match('\[.+\]$', token):            
            self.properties['main'] = token[1:(len(token)-1)]
            return  
        
        ''' match subclass '''    
        if re.match('<.+>$', token):
            self.properties['subclass'] = token[1:(len(token)-1)]
            return
            
        ''' match syntactic tags '''
        if re.match('@[A-Z><]+$', token):
            if re.search('>', token):
                self.attacher = '>'
            elif re.search('<', token):
                self.attacher = '<'
            token = token.replace('<','')
            token = token.replace('>','')
            token = token.replace('@','')
            self.properties['synt'] = token
            
        
        
        
