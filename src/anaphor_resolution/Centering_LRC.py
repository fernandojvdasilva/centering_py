# coding: utf-8 
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
from anaphor_resolution.Centering_Elements import *
from anaphor_resolution.Centering_Algorithm import *
from utils.misc import *

class Centering_LRC(Centering_Algorithm):
    '''
    This class implements the Left Right Centering algorithm for pronoun resolution based on Centering Theory
    
    '''
    def __init__(self, discourse, options):
        Centering_Algorithm.__init__(self, discourse, options)
        self.Cb_candidate = None        
  
    def run(self):        
            
        for i in range(len(self.utterances)):
            self.Cb_candidate = None
            un = self.utterances[i]
            if i > 0:
                un_1 = self.utterances[i-1]
            else:
                un_1 = None
            self.extract_entities(un)
            self.find_referents(un, un_1)
            self.create_CfCb(un, un_1)
            
            
    def extract_entities(self, un):
        for word in un.words:
            re = None            
            if word.properties['tag'] in [Word.PRON, Word.N, Word.PROP]:
                if word.properties['tag'] == Word.PRON and \
                   (word.properties['pron_type'] != 'pers' or \
                    word.properties['text'] == 'se') :
                    continue                    

                # gives a ranking order to the word, following any Cf ranking algorithm...
                # TODO: Implements configuration to choose which Cf order approach to use 
                self.BFP_Order(word) # follows the BFP ranking approach ... 
                re = RE(word)
                un.re_set.append(re) # adds the word to the available Referring expressions                
                
                # if it is a pronoun, for this application, we add it to the list of anaphors as well
                if word.properties['tag'] == Word.PRON :                        
                    un.anaphors.append(re)

    def find_referents(self, un, un_1):        
        for re in un.re_set:            
            if not re.word.properties['tag'] == Word.PRON:
                continue
                         
            ''' Fistly it tries to find a referent intra-sententially, searching from left to right '''
            ref_found = False    
        
            for _re in un.re_set:
                
                if re == _re:
                    break
                
                if _re.word.realizes(re.word) and \
                   (check_binding_constraints(_re.word, re.word) or \
                    not self.options.has_key('bind_const') or \
                    not self.options['bind_const']):
                    
                    re.referent_list.append(_re)
                    ref_found = True
                    break
                
                
            if ref_found:
                continue
            
            if un_1 != None:
                for _re in un_1.centeringSet.Cf:
                    if _re.word.realizes(re.word) and \
                       (check_binding_constraints(_re.word, re.word) or \
                        not self.options.has_key('bind_const') or \
                        not self.options['bind_const']):
                        
                        re.referent_list.append(_re)
                        if self.Cb_candidate == None:
                            self.Cb_candidate = _re
                        break
        
    
    def create_CfCb(self, un, un_1):
        quicksort_bykey(un.re_set, 'rank', 0, len(un.re_set)-1)
        
        ''' The Cf set is simply the re_set ordered ...'''
        un.centeringSet = CenteringSet()
        un.centeringSet.Cf = un.re_set
        
        ''' The Cb is already defined by the Cb_candidate (found when finding references ...)'''
        un.centeringSet.Cb = self.Cb_candidate        

        ''' Sets the center transition type '''
        if un_1 != None:
            un.centeringSet.transition_type = self.center_transition_order(un.centeringSet, un_1.centeringSet)
        
        
    def getCenteringSets_asString(self):
        result = ''
            
        result = ''
        for i in range(len(self.utterances)):
            result = result + self.utterances[i].asString() + '\n'                        
            result = result + self.utterances[i].centeringSet.asString() + '\n'                 
                                    
        return result
