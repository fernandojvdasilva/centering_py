'''
Created on May 4, 2010

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


@author: fernando
'''

import os
import copy

from corpus.Discourse import *
from corpus.Sentence import *
from corpus.Word import *
from anaphor_resolution.Centering_Algorithm import *
from anaphor_resolution.Centering_Conceptual import *
from anaphor_resolution.Centering_BFP import *
from anaphor_resolution.Centering_SList import *
from anaphor_resolution.Centering_LRC import *


corpus_dir = "/media/DADOS/UNICAMP/Summ-it_v3.0/corpusAnotado_CCR"
output_dir = "/media/DADOS/UNICAMP/corpus-analysis"


if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

corpus = []

print "Loading corpus ...\n"

''' Loads every corpus discourse into memory'''
for dis_addr in os.listdir(corpus_dir):
    discourse = {'content': Discourse(), 'label': dis_addr}
    discourse['content'].loadFromSummitCorpus(corpus_dir + "/"+ dis_addr)
    corpus.append(discourse)
    if not os.path.isdir(output_dir + "/" + dis_addr):
        os.mkdir(output_dir + "/" + dis_addr)
    print "%s loaded \n" % dis_addr

print "Running algorithms ... \n"

pronouns = []  

for discourse in corpus:
    
    ''' Loads the pronouns and their corrects referents '''
    for sentence in discourse['content'].sentences:
        for anaphor in sentence.anaphors:
            ref = discourse.findWordById(anaphor.word.properties['ref'])
            pronouns.append({'word_id': anaphor.word.properties['id'], \
                             'word_text': anaphor.word.properties['text'], \
                             'word_sent': sentence.index, \
                             'word_discourse': discourse['label'], \
                             'word_synt': anaphor.word.properties['synt'], \
                             'ref_id': ref.properties['id'], \
                             'ref_text': ref.properties['text'], \
                             'ref_sent': ref.sentence, \
                             'ref_synt': ref.properties['synt'], \
                             'bfp_id': None,
                             'bfp_text': None,
                             'bfp_sent': None,
                             'bfp_synt': None,
                             'con_id': None,
                             'con_text': None,
                             'con_sent': None,
                             'con_synt': None,
                             'slist_id': None,
                             'slist_text': None,
                             'slist_sent': None,
                             'slist_synt': None,
                             'lrc_id': None,
                             'lrc_text': None,
                             'lrc_sent': None,
                             'lrc_synt': None,
                             })
            ref = None                    

    try:
        print "Conceptual Algorithm on %s \n" % discourse["label"]
        alg_conceptual = Centering_Conceptual(discourse['content'])
        
        alg_conceptual.run()
        alg_conceptual.saveResult(output_dir + "/"+ discourse['label'] +"/alg_conceptual_log.txt")
    
        for sentence in alg_conceptual.discourse.sentences:
            for anaphor in sentence.anaphors:
                el = findEntryByKey(pronouns, 'word_id', anaphor.word.properties['id'])
                ref = anaphor.get_entity_referent()
                
                if ref == None or el == None:
                    continue
                
                el['con_id'] = ref.word.properties['id']
                el['con_text'] = ref.word.properties['text']
                el['con_sent'] = ref.word.sentence
                el['con_synt'] = ref.word.properties['synt']                    
                ref = None
        
    except:
        print "Error when loading alg_conceptual ...\n"            

    
    
        
    try:
        print "BFP Algorithm on %s \n" % discourse["label"]    
        alg_bfp = Centering_BFP(discourse['content'])    
        
        alg_bfp.run()
        alg_bfp.saveResult(output_dir + "/"+ discourse['label'] +"/alg_bfp_log.txt")
    
    
        for sentence in alg_bfp.discourse.sentences:
            for anaphor in sentence.anaphors:
                el = findEntryByKey(pronouns, 'word_id', anaphor.word.properties['id'])
                ref = anaphor.get_entity_referent()
                
                if ref == None or el == None:
                    continue
                
                el['bfp_id'] = ref.word.properties['id']
                el['bfp_text'] = ref.word.properties['text']
                el['bfp_sent'] = ref.word.sentence 
                el['bfp_synt'] = ref.word.properties['synt']
                ref = None
    except:
        print "Error when loading alg_bfp ...\n"
    
    try:
        print "S-List Algorithm on %s \n" % discourse["label"]
        
        alg_slist = Centering_SList(discourse['content'])    
        
        alg_slist.run()
        alg_slist.saveResult(output_dir + "/"+ discourse['label'] +"/alg_slist_log.txt")
    
        for sentence in alg_slist.discourse.sentences:
            for anaphor in sentence.anaphors:
                el = findEntryByKey(pronouns, 'word_id', anaphor.word.properties['id'])
                ref = anaphor.get_entity_referent()
                
                if ref == None or el == None:
                    continue
                
                el['slist_id'] = ref.word.properties['id']
                el['slist_text'] = ref.word.properties['text']
                el['slist_sent'] = ref.word.sentence
                el['slist_synt'] = ref.word.properties['synt']
                ref = None
    except:
        print "Error when loading alg_slist ... \n"
    
    
    try:
        print "LRC Algorithm on %s \n" % discourse["label"]
        alg_lrc = Centering_LRC(discourse['content'])
        
        alg_lrc.run()
        alg_lrc.saveResult(output_dir + "/"+ discourse['label'] +"/alg_lrc_log.txt")
    
        for sentence in alg_lrc.discourse.sentences:
            for anaphor in sentence.anaphors:
                el = findEntryByKey(pronouns, 'word_id', anaphor.word.properties['id'])
                ref = anaphor.get_entity_referent()
                
                if ref == None or el == None:
                    continue
                
                el['lrc_id'] = ref.word.properties['id']
                el['lrc_text'] = ref.word.properties['text']
                el['lrc_sent'] = ref.word.sentence
                el['lrc_synt'] = ref.word.properties['synt']
                ref = None
    except:
        print "Error when loading alg_lrc ... \n"
            
    print "------------------------------- \n"
        
    
print "Saving result's summary \n"

sresults = ""
for el in pronouns:
    sresults += el['word_id'] + ";" + \
                el['word_text'] + ";" + \
                el['word_sent'] + ";" + \
                el['word_discourse'] + ';' + \
                el['word_synt'] + ";" + \
                el['ref_id'] + ";" + \
                el['ref_text'] + ";" + \
                el['ref_sent'] + ";" + \
                el['ref_synt'] + ";" + \
                el['bfp_id'] + ";" + \
                el['bfp_text'] + ";" + \
                el['bfp_sent'] + ";" + \
                el['bfp_synt'] + ";" + \
                el['con_id'] + ";" + \
                el['con_text'] + ";" + \
                el['con_sent'] + ";" + \
                el['con_synt'] + ";" + \
                el['slist_id'] + ";" + \
                el['slist_text'] + ";" + \
                el['slist_sent'] + ";" + \
                el['slist_synt'] + ";" + \
                el['lrc_id'] + ";" + \
                el['lrc_text'] + ";" + \
                el['lrc_sent'] + ";" + \
                el['lrc_synt'] + "\n"
    
print "sresults = " + sresults
fresults = open(output_dir + "/results_log.txt", "w")
fresults.write(sresults)
fresults.close