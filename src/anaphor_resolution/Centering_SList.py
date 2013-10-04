# coding: utf-8 
'''
Created on 08/02/2009

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
import copy

class Centering_SList(Centering_Algorithm):
    '''
    This class implements the S-List algorithm for pronoun resolution based on Centering Theory
    
    '''
    
    def __init__(self, discourse, options):
        Centering_Algorithm.__init__(self, discourse, options)
                 
  
    def run(self):        
            
        uttLen = len(self.utterances)    
        for i in range(uttLen):
            un = self.utterances[i]          
            self.realized = list()
            un.centeringSet = CenteringSet()
            un.centeringSet.Cf = [[], [], []]            
            if i > 0:
                un_1 = self.utterances[i-1]                            
                for surface_order in range(len(un_1.centeringSet.Cf)):
                    for el in un_1.centeringSet.Cf[surface_order]:
                        un.centeringSet.Cf[surface_order].append(el)
            
            self.find_referents(un, i, uttLen)
            self.remove_not_realized(un)
            
    def find_referents(self, un, i, uttLen):
        re_1 = None 
        for j in range(len(un.words)):
            word = un.words[j]
            if not word.properties['tag'] in [Word.PRON, Word.N, Word.PROP] or \
               (word.properties['tag'] == Word.PRON and (word.properties['pron_type'] != 'pers' or \
                                                         word.properties['text'] == 'se')):
                ''' Experimental: ignore adjetives'''                
                if word.properties['tag'] != 'adj':
                    re_1 = RE(word)
                continue                        
            
            re = RE(word)            
            self.SH_Order(re, re_1)
            re.utt = ((uttLen-i)*1000) + j
            ''' Mark this entity as realized (to avoid it to be removed later) '''            
            self.realized.append(re)            
            
            if re.word.properties['tag'] == Word.PRON:
                stop = False
                for surface_order in range(len(un.centeringSet.Cf)):
                    if stop:
                        break
                    for _re in un.centeringSet.Cf[surface_order]:
                                        
                        if _re.word.realizes(re.word) and \
                           (check_binding_constraints(_re.word, re.word) or \
                            not self.options.has_key('bind_const') or \
                            not self.options['bind_const']):
                            
                            if not _re.inf_status in Centering_Algorithm.INF_STATUS_SET_OLD:
                                un.centeringSet.Cf[surface_order].remove(_re)
                                _re.inf_status = Centering_Algorithm.INF_STATUS_EVOKED
                                self.SList_insert(un, _re)
                            else:
                                _re.inf_status = Centering_Algorithm.INF_STATUS_EVOKED
                                re.inf_status = Centering_Algorithm.INF_STATUS_EVOKED
                            
                            re.referent_list.append(_re)
                            self.realized.append(_re)
                            stop = True
                            break
                un.anaphors.append(re)
                
            self.SList_insert(un, re)
            
            re_1 = re            
        
    def SList_insert(self, un, re):        
        surface_order = self.surface_order(re)        
        binary_insertion(un.centeringSet.Cf[surface_order-1], re, 'utt')                                
        
    
    def remove_not_realized(self, un):              
        for surface_order in range(len(un.centeringSet.Cf)):
            num_re = len(un.centeringSet.Cf[surface_order])
            j = 0
            while j<num_re and num_re <> 0:
                re = un.centeringSet.Cf[surface_order][j]
                if not re in self.realized:
                    un.centeringSet.Cf[surface_order].remove(re)
                    num_re -= 1  
                else:
                    j += 1
                
    def getCenteringSets_asString(self):
        result = ''
            
        for i in range(len(self.utterances)):
            result = result + self.utterances[i].asString() + '\n'
            result = result + '\tS-List = {'
            for surface_order in range(len(self.utterances[i].centeringSet.Cf)):
                for re in self.utterances[i].centeringSet.Cf[surface_order]:
                    result = result + re.referents_asString()
                    result = result + '(' + Centering_Algorithm.SH_Order_asString(re) + '), '
            result = result + '} \n'
            
             
                        
        return result                      