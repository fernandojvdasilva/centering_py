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

class Centering_Conceptual(Centering_Algorithm):
    '''
    This class implements the BFP algorithm for pronoun resolution based on Centering Theory
    
    '''
    def __init__(self, discourse, options):
        Centering_Algorithm.__init__(self, discourse, options)
  
    def run(self):
        self.construct_anchors() 
        self.choose_Sets()       
  
    ''' It creates the Cf and Cb elements for each Un '''
    def construct_anchors(self):        
                        
        for i in range(len(self.utterances)):
            un = self.utterances[i]
            un.re_set = []
            
            for word in un.words:
                re = None
                # We are discarding pronouns that aren't 3rd person
                if word.properties['tag'] in [Word.PRON, Word.N, Word.PROP]:
                    if word.properties['tag'] == Word.PRON and \
                       (word.properties['pron_type'] != 'pers' or \
                        word.properties['text'] == 'se'):
                        continue                    
                    
                    # It gives a ranking order to the word, following any Cf ranking algorithm...
                    # TODO: Implements configuration to choose which Cf order approach to use 
                    self.BFP_Order(word) # follows the BFP ranking approach ... 
                    re = RE(word)
                    un.re_set.append(re) # adds the word to the available Referring expressions
                    
                    # if it is a pronoun, for this application, we add it to the list of anaphors as well
                    if word.properties['tag'] == Word.PRON :                        
                        un.anaphors.append(re)
                   
            # Sort the referring expressions, following the rank given above 
            quicksort_bykey(un.re_set, 'rank', 0, len(un.re_set)-1)
            
            # Generates all possible Cf and Cb sets for this sentence
            if i > 0:
                ''' Firstly creates a set which there is no Cb for each RE in Un'''                
                un.addCenteringSet(None, un.re_set)
                            
                un_1 = self.utterances[i - 1]
                self.create_possible_CfCb(un, un_1)
            else:
                # If it is the first sentence, then uses re_set as the Cf and let Cb as Null                )                
                #un.addCenteringSet(None, un.re_set)
                if len(un.re_set) > 0:
                    un.addCenteringSet(un.re_set[0], un.re_set)
                else:
                    un.addCenteringSet(None, un.re_set)
                
            un = None
            un_1 = None
            
    
    def choose_Sets(self):
        for i in range(len(self.utterances)):
            un = self.utterances[i]
            if i > 0:
                un_1 = self.utterances[i-1]
            else:
                # TODO: Do something if we have an anaphor in the first sentence (no precedence ...)
                continue
            
            
            # Calculates the transition for the empty set
            for j in range(len(un.centeringSets)):
                un_1_count_anaphors = len(un_1.anaphors)
                                
                transition_type = self.center_transition_order(un.centeringSets[j], \
                                                               un_1.centeringSets[0])
                un.centeringSets[j].transition_type = transition_type
                
                if un_1_count_anaphors > 0:
                    for l in range(un_1_count_anaphors):
                        transition_type = self.center_transition_order(un.centeringSets[j],\
                                                                        un_1.anaphors[l].centeringSet) 
                        if transition_type > un.centeringSets[j].transition_type:
                            un.centeringSets[j].transition_type = transition_type
                
            
            # Calculates the transition for each anaphor
            for j in range(len(un.anaphors)):
                
                choosen_one = {'centeringSet':None, 'transition':0}
                for k in range(len(un.anaphors[j].centeringSets)):
                    
                    un_1_count_anaphors = len(un_1.anaphors)
                    
                    transition_type = self.center_transition_order(un.anaphors[j].centeringSets[k],\
                                                                        un_1.centeringSets[0])                        
                    un.anaphors[j].centeringSets[k].transition_type = transition_type
                            
                    if un_1_count_anaphors > 0:
                        for l in range(un_1_count_anaphors):                            
                            transition_type = self.center_transition_order(un.anaphors[j].centeringSets[k],\
                                                                        un_1.anaphors[l].centeringSet) 
                            if transition_type > un.anaphors[j].centeringSets[k].transition_type:
                                un.anaphors[j].centeringSets[k].transition_type = transition_type
                    
                    if un.anaphors[j].centeringSets[k].transition_type > choosen_one['transition']:
                        choosen_one['centeringSet'] = un.anaphors[j].centeringSets[k]
                        choosen_one['transition'] = un.anaphors[j].centeringSets[k].transition_type
                        
                un.anaphors[j].centeringSet = choosen_one['centeringSet']
                if un.anaphors[j].centeringSet != None:
                    un.anaphors[j].referent_list.append(un.anaphors[j].centeringSet.Cb)                    
            
            
    ''' Generates all possible Cf and Cb sets for this sentence '''
    def create_possible_CfCb(self, un, un_1):
                
        ''' For each RE in Un-1, check if it may be realized in Un. 
        If so, then it becomes a possible Cb and Cf set '''
        for i in range(len(un_1.re_set)):
            for j in range(len(un.anaphors)):
                tmp_re_set = None
                tmp_cb = None
                if un_1.re_set[i].word.realizes(un.anaphors[j].word):
                    # Create a new Cf and Cb Set
                    un.addCenteringSet(un_1.re_set[i], un.re_set, un.anaphors[j])   
                                   