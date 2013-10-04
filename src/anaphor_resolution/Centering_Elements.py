'''
Created on 10/11/2009

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
from corpus.Word import *
from anaphor_resolution.Centering_Algorithm import *

class Centering_Element:
    '''
        This class contains several attributes and methods
        usefull for many Centering Theory related objects
    '''
    
    def __init__(self):
        '''The linked_objects attribute may store objects which are linked by utility '''
        self.linked_objects = {}
        self.anaphors = []
        self.anaphor = None
        self.referent_list = []
        self.centeringSets = [] # Set of possible Cf's and Cb's for this sentence
        self.centeringSet = None

class Un(Centering_Element):
    '''
    Represents a sentence for centering viewpoint
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        Centering_Element.__init__(self)        
        self.re_set = []                
        self.index = 0        
    
    def addCenteringSet(self, cb, cf, anaphor=None):
        cs = CenteringSet(cb, cf, anaphor)
        
        if anaphor != None:
            anaphor.centeringSets.append(cs)
        else:
            self.centeringSets.append(cs)
            
            
    
class CenteringSet(Centering_Element):
    
    '''
    Represents a possible Forward Looking Center (Cf) set and a possible Backward Looking Center (Cb)
    '''
                
    def __init__(self, cb=None, cf=None, anaphor=None):
        Centering_Element.__init__(self)
        
        # RE's whose represents the Referential Expressions for this possible Cf set
        if cf != None:
            self.Cf = cf
        else:
            self.Cf = []
    
        # Word which represent the Referential Expression for this possible Cb
        self.Cb = cb
        
        # Type of center transition, assuming this Cf
        self.transition_type = None 
        
        # Sets the anaphor which "owns" this centeringSet
        self.anaphor = anaphor
        self.referent_list = []
        if cb != None and anaphor != None:
            self.referent_list.append(cb)
            
        # Mark the filter used by BFP algorithm
        self.filtered = None            
        
    def transition_asString(self):
        if self.transition_type == Centering_Algorithm.CONTINUING:
            return 'CONTINUING'
        
        if self.transition_type == Centering_Algorithm.RETAINING:
            return 'RETAINING'
        
        if self.transition_type == Centering_Algorithm.SMOOTH_SHIFT:
            return 'SMOOTH-SHIFT'
        
        if self.transition_type == Centering_Algorithm.SHIFT:
            return 'SHIFT'
            
        
    def asString(self):
        result = '\t\tCf = {'                 
        for cf in self.Cf:
            if type(cf) is dict:
                result = result + cf['anaphor'].word.properties['text']
                if cf['referent'] != None: 
                    result = result + '=' + cf['referent'].word.properties['text'] 
                result += ', '
            else:
                #result = result + cf.word.properties['text'] + ', '             
                result = result + cf.referents_asString() + ', '
        result = result + '}\n'
        if self.Cb != None:
            result = result + '\t\tCb = ' + self.Cb.word.properties['text'] + '\n'
        else:
            result = result + '\t\tCb = None\n'
        result = result + '\t\tTransition = '+  str(self.transition_asString()) + '\n'
        return result
    
    
    def referents_asString(self):
        result = self.anaphor.word.properties['text']
        if len(self.referent_list) > 0:
            for rf in self.referent_list:
                result = result + '=' + rf.referents_asString()
        return result
    
class RE(Centering_Element):
    
    '''
    Represents an Referring Expression (an word that is a pronoun or a noun phrase 
    or a proper name)
    '''
    
    def __init__(self, word=None, re=None):
        
        Centering_Element.__init__(self)
        # Word which represent this RE
        if word != None:
            self.word = word            
        elif re != None:
            self.word = re.word            
        else:
            self.word = None      
        self.marked = False
        
        # rank information used by SH_Order algorithm   
        self.inf_status = -1
        ''' Represents an utterance index in the following form: 
            1001 for the first entity on the first utterance
            2010 for the 10th entity on the seconde utterance
           10003 for the 3rd entity on the 10th utterance '''
        self.utt = -1     
                        
    def referents_asString(self):
        if self.word.properties['tag'] == Word.PRON and\
            self.centeringSet != None:
            return self.centeringSet.referents_asString()
        else:
            if self.referent_list != None and len(self.referent_list) > 0:
                result = self.word.properties['text'] + '='
                for ref in self.referent_list:
                    result = result + ref.referents_asString()
                return result 
            else:
                return self.word.properties['text']
        
    def get_entity_referent(self):
        if len(self.referent_list) == 0 or self.referent_list[0] == None:
            return None
        elif self.referent_list[0].word.properties['tag'] in [Word.PROP, Word.N]:
            return self.referent_list[0]
        else:
            return self.referent_list[0].get_entity_referent()
         
        
    def __getitem__(self, key):
        if key == 'rank':
            return self.word['rank']
        if key == 'utt':
            return self.utt
        if key == 'word_id':
            return self.word.properties['id']
        
    def has_key(self, key):
        return key in ['rank', 'utt', 'word_id']    
        
    @staticmethod
    def word_set_to_re_set(word_set):
        re_set = []
        for word in word_set:
            re_set.append(RE(word))
        return re_set
    
    @staticmethod
    def re_set_clone(re_set):
        cp_re_set = []
        for re in re_set:            
            cp_re_set.append(RE(None, re))             
        return cp_re_set
        