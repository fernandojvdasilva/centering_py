'''
Created on Jan 18, 2011

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
from corpus.Word import *
from anaphor_resolution.Centering_Algorithm import *
from anaphor_resolution.Centering_Elements import *

class Veins_Algorithm(Centering_Algorithm):    


    def __init__(self, discourse, options):
        '''
        Constructor
        '''        
        Centering_Algorithm.__init__(self, discourse, options)        
        self.rst_tree = self.discourse.rst_tree
        self.global_re_set = []
        
    def run(self):
        self.buildVeins()
        
        utt_len = len(self.utterances)
        for sentence in self.discourse.sentences:            
            self.orderVein(sentence, utt_len)
                
        for un in self.utterances:
            if self.options.has_key('utt_type') and self.options['utt_type'] == 'sentence':
                for word in un.words:
                    if word.properties['tag'] in [Word.PRON, Word.N, Word.PROP]:
                        if word.properties['tag'] == Word.PRON and \
                           (word.properties['pron_type'] != 'pers' or \
                            word.properties['text'] == 'se'):
                                continue
                        ind_re = findEntryByKey(self.global_re_set, {'word_id': word.properties['id']}) 
                        assert(ind_re >= 0)
                        un.re_set.append(self.global_re_set[ind_re])  
                        
                        if word.properties['tag'] == Word.PRON:
                            un.anaphors.append(self.global_re_set[ind_re])                                 
            self.findReferents(un)
    
    def buildVeins(self):
        for leaf_node in self.rst_tree.leaves:
            ''' The leaf_node label is composed by its referential expressions '''
            for word in leaf_node.words:                        
                if word.properties['tag'] in [Word.PRON, Word.N, Word.PROP]:
                    if word.properties['tag'] == Word.PRON and \
                       (word.properties['pron_type'] != 'pers' or \
                        word.properties['text'] == 'se'):
                            continue
                    re = RE(word)
                    leaf_node.label.append(re)
                    
                    leaf_node.re_set.append(re)
                    self.global_re_set.append(re)
                    
                    if word.properties['tag'] == Word.PRON:
                        leaf_node.anaphors.append(re)
                
        self.rst_tree.root.buildHead()
        
        self.rst_tree.root.buildVein()
                                
    def resultAsString(self):
        result = '\n'
                                
        for un in self.utterances:
            result += un.asString() + "\n"
            result += "veins = {"
            veins_printed = []
            for re in un.anaphors:
                if not re.word.sentence in veins_printed:
                    result += "\n{"
                    veins_printed.append(re.word.sentence)
                    for ent_ve in re.word.sentence.vein:
                        
                        if self.options.has_key('utt_type') and \
                           self.options['utt_type'] == 'sentence':
                            ent_ve_sen_index = ent_ve.word.getSentenceRoot().index
                            re_sen_index = re.word.getSentenceRoot().index
                        else:
                            ent_ve_sen_index = ent_ve.word.sentence.index
                            re_sen_index = re.word.sentence.index                                                
                        
                        if ent_ve_sen_index <= re_sen_index:
                            result += ent_ve.referents_asString() + ","
                            
                    result += "}\n"
            result += "}\n\n"                                                                
                                    
        return result        
        
    def printResult(self):
        print self.discourse.rst_tree.treeAsString()
        print self.resultAsString()

    def saveResult(self, file_address):                
        fout = open(file_address, 'w')
        fout.write(self.discourse.rst_tree.treeAsString())
        fout.write(self.resultAsString())        
        fout.close        
                
                