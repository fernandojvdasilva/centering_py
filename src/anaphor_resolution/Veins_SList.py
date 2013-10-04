'''
Created on Jan 22, 2011

@author: fernando

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

from anaphor_resolution.Veins_Algorithm import *

class Veins_SList(Veins_Algorithm):
    '''
    This class represents the algorithm which looks for a referent into the vein using
    the BFP ordering and behaves like LRC
    '''

    def __init__(self, discourse, options):
        '''
        Constructor
        '''
        Veins_Algorithm.__init__(self, discourse, options)
    
    def run(self):        
        self.linkWords()
        Veins_Algorithm.run(self)
                    
                    
    def linkWords(self):        
        for un in self.discourse.parse_tree.sentences:
            prev_word = None            
            for i in range(len(un.words)):
                word = un.words[i]
                word.previous_word = prev_word
                word.utt_index = i
                                
                ''' Experimental: ignore adjetives'''                
                if word.properties['tag'] != 'adj':
                    prev_word = word
                
                       
    def orderVein(self, un, uttLen):        
        re_1 = None         
        for re in un.vein:
            
            if self.discourse.options.has_key('veins_head') and \
               'yes_ord' == self.discourse.options['veins_head']:
                if re.word.sentence.isNuclear:
                    nuc_ord = 0
                else:
                    nuc_ord = 1
            else:
                nuc_ord = 0 
            
            if (Word.PRON == re.word.properties['tag'] and \
                (re.word.properties['pron_type'] != 'pers' or \
                 re.word.properties['text'] == 'se')):
                self.inf_status = Centering_Algorithm.INF_STATUS_EVOKED
                            
            elif re.word.previous_word != None:
                ''' TODO: Ignore adjetives '''
                if re.word.previous_word.properties['tag'] == 'adj':
                    re_1 = RE(re.word.previous_word.previous_word)
                else:
                    re_1 = RE(re.word.previous_word)
                self.SH_Order(re, re_1)                
                surface_order = self.surface_order(re)
            else:
                surface_order = 3
            if self.options.has_key('utt_type') and \
               self.options['utt_type'] == 'sentence':
                sen_index = re.word.getSentenceRoot().index
            else:
                sen_index = re.word.sentence.index
            re.word.rank = ((uttLen-sen_index)*10000) + (nuc_ord * 1000) + \
                            (surface_order*100) + re.word.utt_index            
            
        quicksort_bykey(un.vein, 'rank', 0, len(un.vein)-1)
        
        
    def findReferents(self, un):
        for re in un.re_set:
            if re.word.properties['tag'] == Word.PRON:                
                for _re in re.word.sentence.vein:
                    
                    if self.options.has_key('utt_type') and \
                       self.options['utt_type'] == 'sentence':
                        _re_sen_index = _re.word.getSentenceRoot().index
                        re_sen_index = re.word.getSentenceRoot().index
                    else:
                        _re_sen_index = _re.word.sentence.index
                        re_sen_index = re.word.sentence.index
                    
                    _re_word_ind = _re.word.properties['id'][5:len(_re.word.properties['id'])]
                    re_word_ind = re.word.properties['id'][5:len(re.word.properties['id'])]
                    
                    if _re.word.realizes(re.word) and \
                       _re_sen_index <= re_sen_index and \
                       re != _re and \
                       int(re_word_ind) > int(_re_word_ind) and \
                       (check_binding_constraints(_re.word, re.word) or \
                         not self.options.has_key('bind_const') or \
                         not self.options['bind_const']):
                        re.referent_list.append(_re) 
                        break        
                
        