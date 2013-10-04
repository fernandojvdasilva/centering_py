'''
Created on May 4, 2010

@author: fernando
'''

import os
import copy
import sys

from corpus.Discourse import *
from corpus.Sentence import *
from corpus.Word import *
from anaphor_resolution.Centering_Algorithm import *
from anaphor_resolution.Centering_Conceptual import *
from anaphor_resolution.Centering_BFP import *
from anaphor_resolution.Centering_SList import *
from anaphor_resolution.Centering_LRC import *
from anaphor_resolution.Veins_BFP import *
from anaphor_resolution.Veins_LRC import *
from anaphor_resolution.Veins_SList import *

def run_algorithm(algorithm, alg_name, output_dir, dis_addr, pronouns):
           
 #   try:
        print "Running alg_%s Algorithm on %s \n" % (alg_name, dis_addr)        
        
        algorithm.run()
        algorithm.saveResult(output_dir + "/"+ dis_addr +"/alg_"+ alg_name +"_log.txt")
    
        for sentence in algorithm.utterances:
            for anaphor in sentence.anaphors:                
                
                if not anaphor.word.properties.has_key('id'):
                    continue
                
                el = findEntryByKey(pronouns, {'word_id': anaphor.word.properties['id'][5:len(anaphor.word.properties['id'])], \
                                               'word_discourse': dis_addr})
                
                ref_ids = []
                ref_texts = []
                ref_sents = []
                ref_synts = []
                refs_in_vein = []
                refs_bind_con = []
                
                                                                    
                if el < 0:                    
                    if anaphor.word.properties.has_key('ref'):
                        ref_ids = anaphor.word.properties['ref'].split(',')                                            
                        for id in ref_ids:
                            ref = algorithm.discourse.findWordById(id)                                                                                
                            
                            '''if algorithm.options.has_key('utt_type') and \
                               algorithm.options['utt_type'] == 'sentence':
                                sen_index = ref.getSentenceRoot().index
                            else:
                                sen_index = ref.sentence.index'''
                            
                            sen_index = ref.getSentenceRoot().index
                            
                            if ref != None:
                                ref_texts.append(ref.properties['text'])
                                ref_sents.append(sen_index)
                                ref_synts.append(unsplit(ref.properties['synt'], '|'))
                                                                
                    if len(ref_ids) >= 5:
                        ref5_id = ref_ids[4][5:len(ref_ids[4])]
                        ref5_text = ref_texts[4]
                        ref5_sent = ref_sents[4]
                        ref5_synt = ref_synts[4]                        
                    else:
                        ref5_id = None
                        ref5_text = None
                        ref5_sent = None
                        ref5_synt = None                        
                        
                    if len(ref_ids) >= 4:
                        ref4_id = ref_ids[3][5:len(ref_ids[3])]
                        ref4_text = ref_texts[3]
                        ref4_sent = ref_sents[3]
                        ref4_synt = ref_synts[3]                        
                    else:
                        ref4_id = None
                        ref4_text = None
                        ref4_sent = None
                        ref4_synt = None                        
                        
                    if len(ref_ids) >= 3:
                        ref3_id = ref_ids[2][5:len(ref_ids[2])]
                        ref3_text = ref_texts[2]
                        ref3_sent = ref_sents[2]
                        ref3_synt = ref_synts[2]                        
                    else:
                        ref3_id = None
                        ref3_text = None
                        ref3_sent = None
                        ref3_synt = None                        
                        
                        
                    if len(ref_ids) >= 2:
                        ref2_id = ref_ids[1][5:len(ref_ids[1])]
                        ref2_text = ref_texts[1]
                        ref2_sent = ref_sents[1]
                        ref2_synt = ref_synts[1]                        
                    else:
                        ref2_id = None
                        ref2_text = None
                        ref2_sent = None
                        ref2_synt = None                        
                        
                    if len(ref_ids) >= 1:
                        ref_id = ref_ids[0][5:len(ref_ids[0])]
                        ref_text = ref_texts[0]                                                    
                        ref_sent = ref_sents[0]
                        ref_synt = ref_synts[0]                        
                    else:
                        ref_id = None
                        ref_text = None
                        ref_sent = None
                        ref_synt = None
                        
                        
                    num_candidates = 0
                    num_candidates_nearby = 0
                    
                    for sentence_ in algorithm.utterances:
                        for cand in sentence_.re_set:
                            if sentence_.index <= sentence.index:
                                anaphor_id = int(anaphor.word.properties['id'][5:len(anaphor.word.properties['id'])])
                                cand_id = int(cand.word.properties['id'][5:len(cand.word.properties['id'])])
                                if cand.word != anaphor.word and \
                                   cand_id < anaphor_id and \
                                   cand.word.realizes(anaphor.word):
                                    num_candidates += 1
                                    if sentence.index - sentence_.index <= 1:
                                        num_candidates_nearby += 1                                                                  
                        
                    pronouns.append({'word_id': anaphor.word.properties['id'][5:len(anaphor.word.properties['id'])], \
                                     'word_text': anaphor.word.properties['text'], \
                                     #'word_sent': sentence.index, \
                                     'word_sent': anaphor.word.getSentenceRoot().index, \
                                     'word_discourse': dis_addr, \
                                     'word_synt': unsplit(anaphor.word.properties['synt'],'|'), \
                                     'ref_id': ref_id, \
                                     'ref_text': ref_text, \
                                     'ref_sent': ref_sent, \
                                     'ref_synt': ref_synt, \
                                     'ref_in_vein': None, \
                                     'ref_bind_con': None, \
                                     'ref2_id': ref2_id, \
                                     'ref2_text': ref2_text, \
                                     'ref2_sent': ref2_sent, \
                                     'ref2_synt': ref2_synt, \
                                     'ref2_in_vein': None, \
                                     'ref2_bind_con': None, \
                                     'ref3_id': ref3_id, \
                                     'ref3_text': ref3_text, \
                                     'ref3_sent': ref3_sent, \
                                     'ref3_synt': ref3_synt, \
                                     'ref3_in_vein': None, \
                                     'ref3_bind_con': None, \
                                     'ref4_id': ref4_id, \
                                     'ref4_text': ref4_text, \
                                     'ref4_sent': ref4_sent, \
                                     'ref4_synt': ref4_synt, \
                                     'ref4_in_vein': None, \
                                     'ref4_bind_con': None, \
                                     'ref5_id': ref5_id, \
                                     'ref5_text': ref5_text, \
                                     'ref5_sent': ref5_sent, \
                                     'ref5_synt': ref5_synt, \
                                     'ref5_in_vein': None, \
                                     'ref5_bind_con': None, \
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
                				     'veins_bfp_id': None,
                				     'veins_bfp_text': None,
                				     'veins_bfp_sent': None,
                				     'veins_bfp_synt': None,
                                     'veins_lrc_id': None,
                                     'veins_lrc_text': None,
                                     'veins_lrc_sent': None,
                                     'veins_lrc_synt': None,
				                     'veins_slist_id': None,
                                     'veins_slist_text': None,
                                     'veins_slist_sent': None,
                                     'veins_slist_synt': None,
                                     'num_candidates': num_candidates,
                                     'num_candidates_nearby': num_candidates_nearby
                                     })
                    el = len(pronouns) - 1
                                          
                el = findEntryByKey(pronouns, {'word_id': anaphor.word.properties['id'][5:len(anaphor.word.properties['id'])], \
                                               'word_discourse': dis_addr})
                     
                if  el >= 0 and \
                    anaphor.word.properties.has_key('ref') and \
                    len(anaphor.word.sentence.vein) > 0:
                    
                    ref_ids = anaphor.word.properties['ref'].split(',')
                    for id in ref_ids:
                            ref = algorithm.discourse.findWordById(id)
                            if ref != None:
                                check_in_vein = False                                
                                for ent in anaphor.word.sentence.vein:
                                    if ref == ent.word:
                                        check_in_vein = True
                                refs_in_vein.append(check_in_vein)
                                
                                if check_binding_constraints(ref, anaphor.word):
                                    refs_bind_con.append(True)
                                else:
                                    refs_bind_con.append(False)
                                
                    if len(ref_ids) >= 5:                        
                        pronouns[el]['ref5_in_vein'] = refs_in_vein[4]
                        pronouns[el]['ref5_bind_con'] = refs_bind_con[4]
                                                                
                    if len(ref_ids) >= 4:                        
                        pronouns[el]['ref4_in_vein'] = refs_in_vein[3] 
                        pronouns[el]['ref4_bind_con'] = refs_bind_con[3]                   
                        
                    if len(ref_ids) >= 3:                        
                        pronouns[el]['ref3_in_vein'] = refs_in_vein[2]
                        pronouns[el]['ref3_bind_con'] = refs_bind_con[2]                    
                                                
                    if len(ref_ids) >= 2:                        
                        pronouns[el]['ref2_in_vein'] = refs_in_vein[1]  
                        pronouns[el]['ref2_bind_con'] = refs_bind_con[1]                  
                        
                    if len(ref_ids) >= 1:                        
                        pronouns[el]['ref_in_vein'] = refs_in_vein[0]
                        pronouns[el]['ref_bind_con'] = refs_bind_con[0]
                     
                                
                ref = anaphor.get_entity_referent()                                
                
                if ref == None or el < 0:
                    continue
                
                '''if algorithm.options.has_key('utt_type') and \
                   algorithm.options['utt_type'] == 'sentence':
                    sen_index = ref.word.getSentenceRoot().index
                else:
                    sen_index = ref.word.sentence.index'''
                    
                sen_index = ref.word.getSentenceRoot().index
                
                pronouns[el][alg_name + '_id'] = copy.deepcopy(ref.word.properties['id'][5:len(ref.word.properties['id'])])                                   
                pronouns[el][alg_name + '_text'] = copy.deepcopy(ref.word.properties['text'])
                pronouns[el][alg_name + '_sent'] = copy.deepcopy(sen_index)
                pronouns[el][alg_name + '_synt'] = copy.deepcopy(unsplit(ref.word.properties['synt'],'|'))                                    
        
#    except:
#        print "Error when running %s ...\n" % alg_name 
        
sys.setrecursionlimit(1000000)        

corpus_dir = "/media/DADOS/UNICAMP/Summ-it_v3.0/corpusAnotado_CCR"
output_dir = "/media/DADOS/UNICAMP/corpus-analysis"
#corpus_dir="D:/UNICAMP/Summ-it_v3.0/corpusAnotado_CCR"
#output_dir="D:/UNICAMP/corpus-analysis"

all_pronouns = []

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)             

#alg_options = {'bind_const': False, 'utt_type':'sentence', 'veins_head':'yes_ord'}
alg_options = {'bind_const': False, 'utt_type':'sentence', 'veins_head':'no'}
#alg_options = {'bind_const': False, 'utt_type':'rst', 'veins_head':'yes_all'}


for dis_addr in os.listdir(corpus_dir):
       
    if not os.path.isdir(output_dir + "/" + dis_addr):
        os.mkdir(output_dir + "/" + dis_addr)
        
    else:
        print "Discourse %s already evaluated\n" % dis_addr
        continue   
       
    discourse = Discourse(None, alg_options)
    print "Loading corpus %s ...\n" % dis_addr   
    discourse.loadFromSummitCorpus(corpus_dir + "/"+ dis_addr)        
    
    print "%s loaded \n" % dis_addr
    
    print "Saving Discourse's parse tree\n"
    
    discourse.parse_tree.saveTree(output_dir + "/" + dis_addr + "/parse_tree.txt")            
        
    print "Centering Algorithms\n"    
        
    try:
        print "Loading Conceptual Algorithm on %s \n" % dis_addr
        alg_conceptual = Centering_Conceptual(discourse, alg_options)
    except:
        print "Error when loading Conceptual Algorithm ... \n"
        
    run_algorithm(alg_conceptual, "con", output_dir, dis_addr, all_pronouns)    
                                                    
    try:
        print "Loading BFP Algorithm on %s \n" % dis_addr
        alg_bfp = Centering_BFP(discourse, alg_options)
    except:
        print "Error when loading BFP Algorithm ... \n"
        
    run_algorithm(alg_bfp, "bfp", output_dir, dis_addr, all_pronouns)
        
    try:
        print "Loading S-List Algorithm on %s \n" % dis_addr
        alg_slist = Centering_SList(discourse, alg_options)
    except:
        print "Error when loading S-List Algorithm ... \n"
        
    run_algorithm(alg_slist, "slist", output_dir, dis_addr, all_pronouns)
        
    try:
        print "Loading LRC Algorithm on %s \n" % dis_addr
        alg_lrc = Centering_LRC(discourse, alg_options)
    except:
        print "Error when loading LRC Algorithm ... \n"
        
    run_algorithm(alg_lrc, "lrc", output_dir, dis_addr, all_pronouns)

    print "Veins Algorithms:\n"
        
    try:
        print "Loading Veins BFP Algorithm on %s \n" % dis_addr
        alg_veins_bfp = Veins_BFP(discourse, alg_options)
    except:
        print "Error when loading Veins BFP Algorithm ... \n"
        
    
    run_algorithm(alg_veins_bfp, "veins_bfp", output_dir, dis_addr, all_pronouns)
    
        
    try:
        print "Loading Veins LRC Algorithm on %s \n" % dis_addr
        alg_veins_lrc = Veins_LRC(discourse, alg_options)
    except:
        print "Error when loading Veins LRC Algorithm ... \n"
        
    run_algorithm(alg_veins_lrc, "veins_lrc", output_dir, dis_addr, all_pronouns)
    

    try:
        print "Loading Veins S-List Algorithm on %s \n" % dis_addr
        alg_veins_slist = Veins_SList(discourse, alg_options)
    except:
        print "Error when loading Veins S-List Algorithm ... \n"


    run_algorithm(alg_veins_slist, "veins_slist", output_dir, dis_addr, all_pronouns)
    
        
    print "------------------------------- \n"

    discourse = None
        
    
print "Saving result's summary \n"

sresults = ""
sresults += "word_id;word_text;word_sent;word_discourse;word_synt;ref_id;ref_text;ref_sent;ref_synt;ref_in_vein;ref_bind_con;ref2_id;ref2_text;ref2_sent;ref2_synt;ref2_in_vein;ref2_bind_con;" + \
            "ref3_id;ref3_text;ref3_sent;ref3_synt;ref3_in_vein;ref3_bind_con;ref4_id;ref4_text;ref4_sent;ref4_synt;ref4_in_vein;ref4_bind_con;ref5_id;ref5_text;ref5_sent;ref5_synt;ref5_in_vein;ref5_bind_con;" + \
            "bfp_id;bfp_text;bfp_sent;bfp_synt;con_id;con_text;con_sent;con_synt;slist_id;slist_text;slist_sent;slist_synt;lrc_id;lrc_text;lrc_sent;lrc_synt;" + \
            "veins_bfp_id;veins_bfp_text;veins_bfp_sent;veins_bfp_synt;veins_lrc_id;veins_lrc_text;veins_lrc_sent;veins_lrc_synt;veins_slist_id;veins_slist_text;veins_slist_sent;veins_slist_synt;num_candidates;num_candidates_nearby\n"


sresults_all_errors = sresults
sresults_all_notfound = sresults
sresults_equ_results = sresults
sresults_diff = sresults
sresults_only_vt = sresults
sresults_only_ct = sresults
sresults_not_in_vein = sresults
                
for el in all_pronouns:
    if el['ref_id'] == None:
        continue  
    
    rec =       str(el['word_id']) + ";" + \
                str(el['word_text']) + ";" + \
                str(el['word_sent']) + ";" + \
                str(el['word_discourse']) + ';' + \
                str(el['word_synt']) + ";" + \
                str(el['ref_id']) + ";" + \
                str(el['ref_text']) + ";" + \
                str(el['ref_sent']) + ";" + \
                str(el['ref_synt']) + ";" + \
                str(el['ref_in_vein']) + ";" + \
                str(el['ref_bind_con']) + ";" + \
                str(el['ref2_id']) + ";" + \
                str(el['ref2_text']) + ";" + \
                str(el['ref2_sent']) + ";" + \
                str(el['ref2_synt']) + ";" + \
                str(el['ref2_in_vein']) + ";" + \
                str(el['ref2_bind_con']) + ";" + \
                str(el['ref3_id']) + ";" + \
                str(el['ref3_text']) + ";" + \
                str(el['ref3_sent']) + ";" + \
                str(el['ref3_synt']) + ";" + \
                str(el['ref3_in_vein']) + ";" + \
                str(el['ref3_bind_con']) + ";" + \
                str(el['ref4_id']) + ";" + \
                str(el['ref4_text']) + ";" + \
                str(el['ref4_sent']) + ";" + \
                str(el['ref4_synt']) + ";" + \
                str(el['ref4_in_vein']) + ";" + \
                str(el['ref4_bind_con']) + ";" + \
                str(el['ref5_id']) + ";" + \
                str(el['ref5_text']) + ";" + \
                str(el['ref5_sent']) + ";" + \
                str(el['ref5_synt']) + ";" + \
                str(el['ref5_in_vein']) + ";" + \
                str(el['ref5_bind_con']) + ";" + \
                str(el['bfp_id']) + ";" + \
                str(el['bfp_text']) + ";" + \
                str(el['bfp_sent']) + ";" + \
                str(el['bfp_synt']) + ";" + \
                str(el['con_id']) + ";" + \
                str(el['con_text']) + ";" + \
                str(el['con_sent']) + ";" + \
                str(el['con_synt']) + ";" + \
                str(el['slist_id']) + ";" + \
                str(el['slist_text']) + ";" + \
                str(el['slist_sent']) + ";" + \
                str(el['slist_synt']) + ";" + \
                str(el['lrc_id']) + ";" + \
                str(el['lrc_text']) + ";" + \
                str(el['lrc_sent']) + ";" + \
                str(el['lrc_synt']) + ";" + \
		        str(el['veins_bfp_id']) + ";" + \
		        str(el['veins_bfp_text']) + ";" + \
		        str(el['veins_bfp_sent']) + ";" + \
		        str(el['veins_bfp_synt']) + ";" + \
                str(el['veins_lrc_id']) + ";" + \
		        str(el['veins_lrc_text']) + ";" + \
		        str(el['veins_lrc_sent']) + ";" + \
		        str(el['veins_lrc_synt']) + ";" + \
                str(el['veins_slist_id']) + ";" + \
		        str(el['veins_slist_text']) + ";" + \
		        str(el['veins_slist_sent']) + ";" + \
		        str(el['veins_slist_synt']) + ";" + \
                str(el['num_candidates']) + ";" + \
                str(el['num_candidates_nearby']) + "\n"
    
    sresults += rec
    
    alg_results = [str(el['bfp_id']), str(el['con_id']), 
                   str(el['slist_id']), str(el['lrc_id']), str(el['veins_bfp_id']), 
                   str(el['veins_lrc_id']), str(el['veins_slist_id'])]
				   
    alg_cent_results = [str(el['bfp_id']), str(el['con_id']), str(el['slist_id']), str(el['lrc_id'])]
    alg_vt_results = [str(el['veins_bfp_id']), str(el['veins_lrc_id']), str(el['veins_slist_id'])]
    
    all_none = True
    all_equ = True
    for i in range(len(alg_results)):
        if alg_results[0] != alg_results[i]:
            all_equ = False
        if alg_results[i] != "None":
            all_none = False
        
    ''' When every algorithm got wrong '''
    if not str(el['ref_id']) in alg_results and \
       ( el['ref2_id'] == None or 
         not str(el['ref2_id']) in alg_results ) and \
       ( el['ref3_id'] == None or 
         not str(el['ref2_id']) in alg_results ) and \
       ( el['ref4_id'] == None or 
         not str(el['ref4_id']) in alg_results ) and \
       ( el['ref5_id'] == None or 
         not str(el['ref5_id']) in alg_results ):
         
         ''' When all results are equal'''
         if all_equ and not all_none:
             sresults_equ_results += rec
         elif all_none:
             ''' When all results are None'''
             sresults_all_notfound += rec
         else:
             ''' When every algorithm returned a different error '''             
             sresults_all_errors += rec
    else:
        if (str(el['ref_id']) in alg_results or \
           ( el['ref2_id'] != None and 
             str(el['ref2_id']) in alg_results ) or \
           ( el['ref3_id'] != None and 
             str(el['ref3_id']) in alg_results ) or \
           ( el['ref4_id'] != None and 
             str(el['ref4_id']) in alg_results ) or \
           ( el['ref5_id'] != None and 
             str(el['ref5_id']) in alg_results )) and not all_equ:
         sresults_diff += rec
		 	
        ''' Check if only a VT algorithm was successful '''     
        if (str(el['ref_id']) in alg_vt_results or \
           ( el['ref2_id'] != None and 
            str(el['ref2_id']) in alg_vt_results ) or \
           ( el['ref3_id'] != None and 
           str(el['ref3_id']) in alg_vt_results ) or \
           ( el['ref4_id'] != None and 
           str(el['ref4_id']) in alg_vt_results ) or \
           ( el['ref5_id'] != None and 
           str(el['ref5_id']) in alg_vt_results )) and \
           ( not (str(el['ref_id']) in alg_cent_results) and \
           (None == el['ref2_id'] or (not str(el['ref2_id']) in alg_cent_results )) and \
           (None == el['ref3_id'] or (not str(el['ref3_id']) in alg_cent_results )) and \
           (None == el['ref4_id'] or (not str(el['ref4_id']) in alg_cent_results )) and \
           (None == el['ref5_id'] or (not str(el['ref5_id']) in alg_cent_results )) \
           ):
                sresults_only_vt += rec
                
        ''' Check if only a CT algorithm was successful '''     
        if (str(el['ref_id']) in alg_cent_results or \
           ( el['ref2_id'] != None and 
            str(el['ref2_id']) in alg_cent_results ) or \
           ( el['ref3_id'] != None and 
           str(el['ref3_id']) in alg_cent_results ) or \
           ( el['ref4_id'] != None and 
           str(el['ref4_id']) in alg_cent_results ) or \
           ( el['ref5_id'] != None and 
           str(el['ref5_id']) in alg_cent_results )) and \
           ( not (str(el['ref_id']) in alg_vt_results) and \
           (None == el['ref2_id'] or (not str(el['ref2_id']) in alg_vt_results )) and \
           (None == el['ref3_id'] or (not str(el['ref3_id']) in alg_vt_results )) and \
           (None == el['ref4_id'] or (not str(el['ref4_id']) in alg_vt_results )) and \
           (None == el['ref5_id'] or (not str(el['ref5_id']) in alg_vt_results )) \
           ):
                sresults_only_ct += rec
			
                
fresults = open(output_dir + "/results_log.txt", "w")
fresults.write(sresults)
fresults.close

fresults_equ_results = open(output_dir + "/results_equ_log.txt", "w")
fresults_equ_results.write(sresults_equ_results)
fresults_equ_results.close

fresults_all_errors = open(output_dir + "/results_all_errors_log.txt", "w")
fresults_all_errors.write(sresults_all_errors)
fresults_all_errors.close

fresults_all_notfound = open(output_dir + "/results_all_notfound_log.txt", "w")
fresults_all_notfound.write(sresults_all_notfound)
fresults_all_notfound.close
                
fresults_diff = open(output_dir + "/results_diff_log.txt", "w")
fresults_diff.write(sresults_diff)
fresults_diff.close

fresults_only_vt = open(output_dir + "/results_only_vt.txt", "w")
fresults_only_vt.write(sresults_only_vt)
fresults_only_vt.close

fresults_only_ct = open(output_dir + "/results_only_ct.txt", "w")
fresults_only_ct.write(sresults_only_ct)
fresults_only_ct.close

print "Result summary saved\n"
                
