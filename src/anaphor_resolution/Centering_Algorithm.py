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
import copy
from corpus.Discourse import *
from corpus.Sentence import *
from anaphor_resolution.Centering_Elements import *


class Centering_Algorithm:
    '''
    This is the base class for Centering Algorithms' implementation
    '''
    
    # Transition Types
    CONTINUING   = 4
    RETAINING    = 3
    SMOOTH_SHIFT = 2
    SHIFT        = 1
    
    def __init__(self, discourse, options):
        '''
        Constructor
        '''
        '''self.discourse = discourse.copy()'''
        self.discourse = copy.deepcopy(discourse)
        self.options = options
        if 'sentence' == self.options['utt_type']:
            self.utterances = self.discourse.parse_tree.sentences
        elif 'rst' == self.options['utt_type']:
            self.utterances = self.discourse.sentences

    def getCenteringSets_asString(self):
        result = ''
        for i in range(len(self.utterances)):
            result = result + self.utterances[i].asString() + '\n'
            num_set = 1
            result = result + '\tSentence Sets:\n'
            for j in range(len(self.utterances[i].centeringSets)):
                result = result + '\t('+ str(num_set) +'° Set)\n'
                result = result + self.utterances[i].centeringSets[j].asString() + '\n'                 
                num_set += 1
            
            num_set = 1
            for j in range(len(self.utterances[i].anaphors)):
                result = result + '\tSets for "'+ self.utterances[i].anaphors[j].word.properties['text'] + '"\n'
                for k in range (len(self.utterances[i].anaphors[j].centeringSets)):
                    choosen = ''
                    if self.utterances[i].anaphors[j].centeringSets[k] == self.utterances[i].anaphors[j].centeringSet:
                        choosen = 'THE CHOOSEN ONE!'
                    result = result + '\t('+ str(num_set) +'° Set - '+ choosen +' : '+ \
                             self.utterances[i].anaphors[j].centeringSets[k].referents_asString() +')\n'
                    result = result + self.utterances[i].anaphors[j].centeringSets[k].asString() + '\n'                 
                    num_set += 1 
                        
        return result
        
    def printResult(self):
        print self.getCenteringSets_asString()

    def saveResult(self, file_address):
        fout = open(file_address, 'w')
        fout.write(self.getCenteringSets_asString())
        fout.close

    def center_transition_order(self, un_centeringSet, un_1_centeringSet):
        if un_centeringSet == None or un_1_centeringSet == None:
            return Centering_Algorithm.SHIFT
        
        equals_Cb = Centering_Algorithm.references(un_centeringSet.Cb, un_1_centeringSet.Cb, un_centeringSet)
        if len(un_centeringSet.Cf) > 0:                    
            Cb_equals_Cp = Centering_Algorithm.references(un_centeringSet.Cf[0], un_centeringSet.Cb, un_centeringSet)
        else:
            Cb_equals_Cp = False
        
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
    def references(anaphor, referent, un_centeringSet):
        if referent == None or anaphor == None:
            return False
        
        if anaphor == referent:
            return True
        elif anaphor.centeringSet != None:
            result = False
            for rf in anaphor.centeringSet.referent_list:
                result = result or Centering_Algorithm.references(rf, referent, un_centeringSet)
            return result
        elif len(anaphor.centeringSets) > 0:
            result = False
            for cs in anaphor.centeringSets:
                if cs == un_centeringSet:                                
                    for rf in cs.referent_list:
                        result = result or Centering_Algorithm.references(rf, referent, un_centeringSet)                    
                    break
            return result
        else:
            return False
            
        
    '''
        It Gives a rank index for a word, following the order defined in
        Brennan, Friedman e Pollard (1987) 
    '''
    def BFP_Order(self, word):
        if word.SUBJ in word.properties['synt']:
            word.rank = 1
            return 1
        if word.ACC in word.properties['synt']:
            word.rank = 2
            return 2
        if word.DAT in word.properties['synt']:
            word.rank = 3
            return 3
        if word.ADVL in word.properties['synt']:
            word.rank = 5
            return 5
        
        # if the word has another syntactic classification not mentioned above, them return 4 
        word.rank = 4
        return 4
    
    
    '''
        It Gives a rank index for a word, following the order defined in
        Rambow (1993) 
    '''
    def Rambow_Order(self, word, un):
        pass
    
    
    '''
        It Gives a rank index for a word, following the order defined in
        Gernsbacher and Hargreaves (1998)
    '''
    r = 1
    def GH_Order(self, word):
        word.rank = self.r
        self.r += 1
         
    
    ''' Information status used to rank the Cf following SH_Order Algorithm '''
    INF_STATUS_EVOKED           = 1
    INF_STATUS_UNUSED           = 2
    INF_STATUS_SET_OLD          = [INF_STATUS_EVOKED,\
                                   INF_STATUS_UNUSED]        
    
    INF_STATUS_INFERRABLES      = 3
    INF_STATUS_CINFERRABLES     = 4
    INF_STATUS_ANC_BRAND_NEW    = 5
    INF_STATUS_SET_MED          = [INF_STATUS_INFERRABLES, \
                                   INF_STATUS_CINFERRABLES, \
                                   INF_STATUS_ANC_BRAND_NEW]
    
    INF_STATUS_BRAND_NEW        = 6
    INF_STATUS_SET_NEW          = [INF_STATUS_BRAND_NEW]
    
    '''
        It gives a rank index to a word, following the order defined in
        Strube and Hahn (1999)
    '''
    def SH_Order(self, re, re_1):
                    
        ''' (1) If word is preceded by an indefinite article, then mark word as BRAND-NEW '''
        if re_1 != None and re_1.word.properties['tag'] == 'arti':
            re.inf_status = Centering_Algorithm.INF_STATUS_BRAND_NEW
            return re.inf_status
        
        
            '''elif re_1 == None or \ '''
        elif re.word.properties['tag'] == Word.PROP and \
            (re_1 == None or \
            not ((re_1.word.properties['tag'] == 'pron' and re_1.word.properties['pron_type'] == 'det') or \
            (re_1.word.properties['tag'] in ['artd', 'arti']))):
             
            ''' (2) If word is not preceded by a determiner, then mark word as UNUSED '''     
            re.inf_status = Centering_Algorithm.INF_STATUS_UNUSED
            return re.inf_status
        
        
        else:
            ''' (3) Else, mark word as ANCHORED BRAND-NEW '''
            re.inf_status = Centering_Algorithm.INF_STATUS_ANC_BRAND_NEW
            return re.inf_status
        
        
    @staticmethod      
    def surface_order(re):
        if re.inf_status in Centering_Algorithm.INF_STATUS_SET_OLD:
            return 1
        
        if re.inf_status in Centering_Algorithm.INF_STATUS_SET_MED:
            return 2
        
        if re.inf_status in Centering_Algorithm.INF_STATUS_SET_NEW:
            return 3
        
        
    @staticmethod
    def SH_Order_asString(re):
        if re.inf_status == Centering_Algorithm.INF_STATUS_EVOKED:
            return 'Evoked (OLD)'
        elif re.inf_status == Centering_Algorithm.INF_STATUS_UNUSED:
            return 'Unused (OLD)'
        elif re.inf_status == Centering_Algorithm.INF_STATUS_INFERRABLES:
            return 'Inferrables (MED)'
        elif re.inf_status == Centering_Algorithm.INF_STATUS_CINFERRABLES:
            return 'Containing Inferrables (MED)'
        elif re.inf_status == Centering_Algorithm.INF_STATUS_ANC_BRAND_NEW:
            return 'Anch. Brand New (MED)'
        elif re.inf_status == Centering_Algorithm.INF_STATUS_BRAND_NEW:
            return 'Brand New (NEW)'
