'''
Created on 03/11/2009

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
import copy

from corpus.parse_tree.Node import *
from utils.misc import *

class Word(Node):
    '''
    An object of this class holds syntactic information about a single word into a sentence 
    '''
    
    ''' CONSTANTS'''
    
    ''' Gender'''
    M_F = 'm-f' 
    M = 'm'
    F = 'f'

    ''' Number'''
    S = 's' # singular
    P = 'p' # plural
    
    ''' Word Class Tags'''
    N = 'n'
    PROP = 'prop'
    SPEC = 'spec'
    DET = 'det'
    PERS = 'pers'
    PRON = 'pron'
    
    ''' Syntactic Tags'''
    SUBJ = 'subj' # Subject
    ACC = 'acc'   # Direct Object
    DAT = 'dat'   # Indirect Object
    ADVL = 'advl' # Adverbial Adjunct
    V_FIN = 'v_fin' # Finite Verb
    V_INF = 'v_inf' # Infinitive verb
            
    def __init__(self, properties=None):
        '''
        Constructor
        '''
        Node.__init__(self, None)
        if properties != None:
            self.properties = properties
        else:
            self.properties = {'canon':'', 'text':'', 'synt':[], 'gender':Word.M_F, 'person':None, 'number':None, 'tag':None, 'pron_type': None}
        self.rank = 0
        self.sentence = None        
        
    def copy(self, sentence):
        result = Word()
        result.properties = copy.deepcopy(self.properties)
        result.rank = self.rank
        result.sentence = sentence        
        return result
    
    
    ''' returns true if the given word agree in gender, number and person to this word'''
    def agree(self, word):        
        ag_gender = False
        ag_number = False
        ag_person = False
                
        
        ''' EXPERIMENTAL: If this word is a collective, so check if the pronoun agrees with the gender
            of the word whose represents the collective represents the word.
        '''
        collective = isCollective(self.properties['text'])
        if Word.P in word.properties['number'] and collective != None:
            ag_number = True
            ag_gender = (collective['gender'] == Word.M_F) or \
                        (word.properties['gender'] == Word.M_F) or \
                        (collective['gender'] == word.properties['gender'])
            ag_person = True
        else:
        
            ag_gender = (self.properties['gender'] == Word.M_F) or \
                        (word.properties['gender'] == Word.M_F) or \
                        (self.properties['gender'] == word.properties['gender'])                
            
            ag_number = (self.properties['number'] in word.properties['number']) or \
                        (word.properties['number'] in self.properties['number'])
                                  
                        
            ''' If we're dealing with a pronoun, so we should check the person agreement
            to avoid cases like when "Eu" would agree to "carro" '''
            ag_person = True        
                
            if self.properties['tag'] == Word.PRON and word.properties['tag'] == Word.PRON and \
                 self.properties['pron_type'] == 'pers' and word.properties['pron_type'] == 'pers':
                ag_person = self.properties['number'] == word.properties['number']
                
            elif self.properties['tag'] == Word.PRON and self.properties['pron_type'] == 'pers' and \
                word.properties['tag'] in [Word.N , Word.PROP, Word.PRON]:
                ag_person = ('3' in self.properties['number']) and (word.properties['number'] in self.properties['number'])
                
            elif word.properties['tag'] == Word.PRON and word.properties['pron_type'] == 'pers' and \
                self.properties['tag'] in [Word.N , Word.PROP, Word.PRON]:
                ag_person = ('3' in word.properties['number']) and (self.properties['number'] in word.properties['number'])                        
                        
        return (ag_gender and ag_number and ag_person)
    
    
    ''' returns true if the given word can refer to this word '''
    def realizes(self, word):
        
        if word.properties['tag'] == Word.PRON:
            return self.agree(word)
        
        '''if word.properties['tag'] == Word.PRON or\
           self.properties['tag'] == Word.PRON:
            return self.agree(word)'''
        
        
        '''To ensure that Cb is aways a pronoun, we won't consider NPs realized 
         
        if word.properties['tag'] == Word.N and\
            self.properties['tag'] == Word.N:
            return self.agree(word) and (word.properties['text'] == self.properties['text'])
        '''
        
        return False
            
    def __getitem__(self, key):
        if key == 'rank':
            return self.rank
        
    ''' Overrides the nodeAsString method from parse_tree.Node class whose 
        this class inherits from '''        
    def nodeAsString(self, depth):
        result = self.treeIndentation(depth)  
        result += self.form + "(" + self.properties['text'] + ")\n"
        return result
        
    ''' Overrides the getBranchingNode method from parse_tree.Node class whose 
        this class inherits from '''
    def getBranchingNode(self):
        if self.properties['tag'] == Word.N or \
           self.properties['tag'] == Word.PROP:
            return self.parent.getBranchingNode()
        else:
            return self.parent