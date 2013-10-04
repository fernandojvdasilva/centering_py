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

class Centering_BFP(Centering_Algorithm):
    '''
    This class implements the BFP algorithm for pronoun resolution based on Centering Theory
    
    '''
    def __init__(self, discourse, options):
        Centering_Algorithm.__init__(self, discourse, options)        
  
    def run(self):        
            
        for i in range(len(self.utterances)):
            un = self.utterances[i]
            if i > 0:
                un_1 = self.utterances[i-1]
            else:
                un_1 = None
            self.construct_anchors(un, un_1) 
            if un_1 != None:
                if len(un.centeringSets) > 1:
                    self.filter_Sets(un, un_1)
                self.choose_Sets(un, un_1)
            else:
                un.centeringSet = un.centeringSets[0]       
  
    ''' It creates the Cf and Cb elements for each Un '''
    def construct_anchors(self, un, un_1):                          
        for word in un.words:
            re = None            
            if word.properties['tag'] in [Word.PRON, Word.N, Word.PROP]:
                if word.properties['tag'] == Word.PRON and \
                   (word.properties['pron_type'] != 'pers' or \
                    word.properties['text'] == 'se'):
                        continue                    
                # gives a ranking order to the word, following any Cf ranking algorithm...
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
        if un_1 != None:                           
            #un.addCenteringSet(None, un.re_set)

            self.create_possible_CfCb(un, un_1)
        else:
            # If there it is the first sentence, then uses re_set as the Cf and let Cb as Null                )                
            #un.addCenteringSet(None, un.re_set)
            if len(un.re_set) > 0:
                un.addCenteringSet(un.re_set[0], un.re_set)
            else:
                un.addCenteringSet(None, un.re_set)
                                            
                        
                        
    ''' It generates all possible Cf and Cb sets for this sentence '''
    def create_possible_CfCb(self, un, un_1):
        possible_Cf_Sets = []
        all_expanded = []        
        possible_Cb = []
        for i in range(len(un_1.re_set)):
            possible_Cb.append(un_1.re_set[i])
        ''' Firstly it creates a set which there is no Cb for each RE in Un'''
        possible_Cb.append(None)        
        for i in range(len(un.re_set)):
            expanded_re_set = []            
            expanded_re_set.append({'anaphor':un.re_set[i], 'referent':None})
            if un.re_set[i].word.properties['tag'] == Word.PRON:                
                for j in range(len(un_1.centeringSet.Cf)):                              
                    # TODO: add configuration to allow choose between discourse entity and Un-1 entity
                    if un_1.centeringSet.Cf[j].word.realizes(un.re_set[i].word):
                        #if not (un_1.centeringSet.Cf[j] in possible_Cb): 
                            #possible_Cb.append(un_1.centeringSet.Cf[j])
                        expanded_re_set.append({'anaphor':un.re_set[i], 'referent':un_1.centeringSet.Cf[j]})                            
            all_expanded.append(expanded_re_set)
        
        i = len(all_expanded) - 1
        vect_mult = []                
        
        if 0 == i:
            for en in all_expanded[i]:
                possible_Cf_Sets.append([en])
        elif i > 0:
            if type(all_expanded[i]) is list:
                for el in all_expanded[i]:
                    vect_mult.append(el)
            else:            
                vect_mult.append(all_expanded[i])
            while i > 0:
                i -= 1                
                vect_mult = vector_cartesian_product(all_expanded[i], vect_mult)        
        
        if len(possible_Cf_Sets) == 0:
            possible_Cf_Sets = vect_mult
                    
        for i in range(len(possible_Cb)):
            if len(possible_Cf_Sets) <= 0:
                un.addCenteringSet(possible_Cb[i], [])
            for j in range(len(possible_Cf_Sets)):                            
                un.addCenteringSet(possible_Cb[i], possible_Cf_Sets[j])



    ''' Filter codes '''
    FILTERED_CONTRAINDEXED   = 1    
    FILTERED_CB_NOT_FIRST    = 2
    FILTERED_CB_NOT_REALIZED = 3                
         
    def filter_Sets(self, un, un_1):                   
        for j in range(len(un.centeringSets)):
                
            cb_is_realized = False                        
            for k in range(len(un.centeringSets[j].Cf)):
                
                '''(a) Filter by contraindices'''
                ''' if we proposed the same antecedent for two contraindexed pronouns... '''
                if self.options.has_key('bind_const') and \
                   self.options['bind_const']:
                                    
                    for l in range(k+1, len(un.centeringSets[j].Cf)):
                                                                                    
                        if un.centeringSets[j].Cf[k]['anaphor'].word.properties['tag'] == Word.PRON and \
                           un.centeringSets[j].Cf[l]['anaphor'].word.properties['tag'] == Word.PRON:
                            
                            if (not check_binding_constraints(un.centeringSets[j].Cf[k]['anaphor'].word, \
                                                              un.centeringSets[j].Cf[l]['anaphor'].word)) and \
                               (Centering_BFP.references(un.centeringSets[j].Cf[k]['referent'], \
                                                         un.centeringSets[j].Cf[l]['referent']) or \
                               Centering_BFP.references(un.centeringSets[j].Cf[l]['referent'], \
                                                        un.centeringSets[j].Cf[k]['referent'])):
                                un.centeringSets[j].filtered = Centering_BFP.FILTERED_CONTRAINDEXED
                                break
                            
                    ''' or if we have proposed an antecedent for a pronoun which it is contraindexed with ...'''
                    ''' if un.centeringSets[j].Cf[k]['anaphor'] != None and un.centeringSets[j].Cf[k]['referent'] != None and \ '''
                    if un.centeringSets[j].Cf[k]['referent'] != None and \
                       un.centeringSets[j].Cf[k]['anaphor'].word.properties['tag'] == Word.PRON:
                   
                        if (not check_binding_constraints(un.centeringSets[j].Cf[k]['referent'].word, 
                                                          un.centeringSets[j].Cf[k]['anaphor'].word)):
                            un.centeringSets[j].filtered = Centering_BFP.FILTERED_CONTRAINDEXED
                            break
                                                                
                if un.centeringSets[j].filtered != None:
                    break
                
                ''' (c) If none of the entities realized as pronouns in the proposed Cf
                list equals the proposed Cb then eliminate this anchor '''     
                if not cb_is_realized:
                    cb_is_realized = Centering_BFP.references(un.centeringSets[j].Cf[k]['referent'], 
                                                              un.centeringSets[j].Cb) or \
                                                              (None == un.centeringSets[j].Cf[k]['referent'] and \
                                                               None == un.centeringSets[j].Cb)
                                                                        
                        
            if not cb_is_realized and \
               (len(un.centeringSets[j].Cf) > 0 or \
                    (len(un.centeringSets[j].Cf) <= 0 and un.centeringSets[j].Cb != None) \
                ) and \
               un.centeringSets[j].filtered == None:
                un.centeringSets[j].filtered = Centering_BFP.FILTERED_CB_NOT_REALIZED
                
            if un.centeringSets[j].filtered != None:
                continue
            
            '''(b) Go through Cf(Un-1) keeping (in order) those which appear 
            in the proposed Cf list of the anchor. If the 
            proposed Cb of the anchor does not equal the first ele- 
            ment of this constructed list then eliminate this anchor.  '''
            if len(un.anaphors) <= 0:
                continue                 
            constructed_list = [] 
            for k in range(len(un_1.centeringSet.Cf)):
                 for l in range(len(un.centeringSets[j].Cf)):
                     if un.centeringSets[j].Cf[l]['referent'] == un_1.centeringSet.Cf[k]:
                        constructed_list.append(un_1.centeringSet.Cf[k])
                        break
                                           
            if len(constructed_list) > 0 and un.centeringSets[j].Cb != constructed_list[0]:
                un.centeringSets[j].filtered = Centering_BFP.FILTERED_CB_NOT_FIRST                                                       
                    
                                
    def choose_Sets(self, un, un_1):
        if len(un.re_set) <= 0:
            ''' Finds the first non-filtered set...'''
            for j in range(len(un.centeringSets)):
                if None == un.centeringSets[j].filtered:
                    un.centeringSet = un.centeringSets[j]
                    un.centeringSet.linked_objects['choosen_centering_set'] = un.centeringSets[j]
            return
        
        choosen_one = {'centeringSet':un.centeringSets[0], 'transition':0}
        
        if len(un_1.re_set) > 0:
            for j in range(len(un.centeringSets)):
                if un.centeringSets[j].filtered != None:
                    continue
                un.centeringSets[j].transition_type = self.center_transition_order(un.centeringSets[j], un_1.centeringSet) 
                if un.centeringSets[j].transition_type > choosen_one['transition']:
                    choosen_one['transition'] = un.centeringSets[j].transition_type
                    choosen_one['centeringSet'] = un.centeringSets[j]
        
        un.centeringSet = CenteringSet()
        un.centeringSet.transition_type = choosen_one['transition']
        un.centeringSet.linked_objects['choosen_centering_set'] = choosen_one['centeringSet']
        un.centeringSet.Cb = choosen_one['centeringSet'].Cb
        for j in range(len(choosen_one['centeringSet'].Cf)):
            if choosen_one['centeringSet'].Cf[j]['anaphor'] != None:
                cf = choosen_one['centeringSet'].Cf[j]['anaphor']
                cf.referent_list.append(choosen_one['centeringSet'].Cf[j]['referent'])            
            else:
                cf = choosen_one['centeringSet'].Cf[j]                
            un.centeringSet.Cf.append(cf)                    
    
    def center_transition_order(self, un_centeringSet, un_1_centeringSet):
        if un_centeringSet == None or un_1_centeringSet == None:
            return Centering_Algorithm.SHIFT
        
        equals_Cb = Centering_BFP.references(un_centeringSet.Cb, un_1_centeringSet.Cb)
        Cb_equals_Cp = Centering_BFP.references(un_centeringSet.Cf[0]['referent'], un_centeringSet.Cb)
                
        # Check Continuing
        if equals_Cb and Cb_equals_Cp:
            return Centering_Algorithm.CONTINUING
        
        # Check Retaining
        if equals_Cb and (not Cb_equals_Cp):
            return Centering_Algorithm.RETAINING
        
        # Check Smooth-Shifting
        if (not equals_Cb) and Cb_equals_Cp:
            return Centering_Algorithm.SMOOTH_SHIFT
        
        # Check Shifting
        if (not equals_Cb) and (not Cb_equals_Cp):
            return Centering_Algorithm.SHIFT
        
        return Centering_Algorithm.SHIFT    
    
    
    @staticmethod
    def references(anaphor, referent):
        if referent == None or anaphor == None:
            return False
        
        if anaphor == referent:
            return True
        else:
            result = False
            for rf in anaphor.referent_list:
                result = result or Centering_BFP.references(rf, referent)
            return result
     
        
    def getCenteringSets_asString(self):
        result = ''
        for i in range(len(self.utterances)):
            result = result + self.utterances[i].asString() + '\n'
            num_set = 1
            result = result + '\tSentence Sets:\n'
            for j in range(len(self.utterances[i].centeringSets)):
                if self.utterances[i].centeringSets[j].filtered == None:
                    filter = ''
                elif self.utterances[i].centeringSets[j].filtered == Centering_BFP.FILTERED_CONTRAINDEXED:
                    filter = 'FILTERED BY CONTRAINDICES'
                elif self.utterances[i].centeringSets[j].filtered == Centering_BFP.FILTERED_CB_NOT_FIRST:
                    filter = 'FILTERED BY Cb(Un) != Cf[0](Un-1)'
                elif self.utterances[i].centeringSets[j].filtered == Centering_BFP.FILTERED_CB_NOT_REALIZED:
                    filter = 'FILTERED BY Cb(Un) not realized'                
                                                                    
                
                
                if i > 0 and \
                self.utterances[i].centeringSet.linked_objects['choosen_centering_set'] == \
                self.utterances[i].centeringSets[j]:
                    choosen = 'THE CHOOSEN ONE!'
                else:
                    choosen = '' 
                
                result = result + '\t('+ str(num_set) +'° Set - '+ filter + choosen +')\n'
                result = result + self.utterances[i].centeringSets[j].asString() + '\n'                 
                num_set += 1
                                                
        return result                     