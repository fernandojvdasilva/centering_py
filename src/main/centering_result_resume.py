'''
Created on Jun 13, 2010

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
from string import split

output_dir = "/media/DADOS/UNICAMP/corpus-analysis"

results_bfp = {'total_intra':0, 'total_inter':0, 'not_solved':0, 'total_all':0}
results_con = {'total_intra':0, 'total_inter':0, 'not_solved':0, 'total_all':0}
results_lrc = {'total_intra':0, 'total_inter':0, 'not_solved':0, 'total_all':0}
results_slist = {'total_intra':0, 'total_inter':0, 'not_solved':0, 'total_all':0}
results_veins_bfp = {'total_intra':0, 'total_inter':0, 'not_solved':0, 'total_all':0}
results_veins_lrc = {'total_intra':0, 'total_inter':0, 'not_solved':0, 'total_all':0}
results_veins_slist = {'total_intra':0, 'total_inter':0, 'not_solved':0, 'total_all':0}

total_intra_sentential = 0
total_inter_sentential = 0
total_anaphors = 0

''' Read the result log '''
fresult_log = open(output_dir + "/results_log.txt", "r")

result_log = fresult_log.read()

log_lines = result_log.split()

word_sent = 2
ref_id = 5
ref_sent = 7
ref2_id = 11
ref3_id = 17 
ref4_id = 23
ref5_id = 29
bfp_id = 35
con_id = 39
slist_id = 43
lrc_id = 47
veins_bfp_id = 51
veins_lrc_id = 55
veins_slist_id = 59

first_line = True                
for fline in log_lines:
    if first_line :
        first_line = False
        continue
    line = fline.split(";")
             
    ''' Checks if the result matches '''    
    total_anaphors += 1
    
    if line[ref_sent] == line[word_sent]:
        total_intra_sentential += 1
    else:
        total_inter_sentential += 1
    
    
    if line[bfp_id] == "None":
        results_bfp['not_solved'] += 1
    elif line[bfp_id] in [line[ref_id], line[ref2_id], \
                        line[ref3_id], line[ref4_id], line[ref5_id]]:
        if line[ref_sent] == line[word_sent]:            
            results_bfp['total_intra'] += 1
        else:
            results_bfp['total_inter'] += 1            
        results_bfp['total_all'] += 1    
        
    
    if line[con_id] == "None":
        results_con['not_solved'] += 1      
    elif line[con_id] in [line[ref_id], line[ref2_id], \
                        line[ref3_id], line[ref4_id], line[ref5_id]]:
        if line[ref_sent] == line[word_sent]:
            results_con['total_intra'] += 1
        else:
            results_con['total_inter'] += 1            
        results_con['total_all'] += 1
        
    
    if line[lrc_id] == "None":
        results_lrc['not_solved'] += 1
    elif line[lrc_id] in [line[ref_id], line[ref2_id], \
                        line[ref3_id], line[ref4_id], line[ref5_id]]:
        if line[ref_sent] == line[word_sent]:
            results_lrc['total_intra'] += 1
        else:
            results_lrc['total_inter'] += 1            
        results_lrc['total_all'] += 1           

            
    if line[slist_id] == "None":
        results_slist['not_solved'] += 1        
    elif line[slist_id] in [line[ref_id], line[ref2_id], \
                        line[ref3_id], line[ref4_id], line[ref5_id]]:
        if line[ref_sent] == line[word_sent]:
            results_slist['total_intra'] += 1
        else:
            results_slist['total_inter'] += 1            
        results_slist['total_all'] += 1

    if line[veins_bfp_id] == "None":
        results_veins_bfp['not_solved'] += 1        
    elif line[veins_bfp_id] in [line[ref_id], line[ref2_id], \
                        line[ref3_id], line[ref4_id], line[ref5_id]]:
        if line[ref_sent] == line[word_sent]:
            results_veins_bfp['total_intra'] += 1
        else:
            results_veins_bfp['total_inter'] += 1            
        results_veins_bfp['total_all'] += 1

    if line[veins_lrc_id] == "None":
        results_veins_lrc['not_solved'] += 1        
    elif line[veins_lrc_id] in [line[ref_id], line[ref2_id], \
                        line[ref3_id], line[ref4_id], line[ref5_id]]:
        if line[ref_sent] == line[word_sent]:
            results_veins_lrc['total_intra'] += 1
        else:
            results_veins_lrc['total_inter'] += 1            
        results_veins_lrc['total_all'] += 1

    if line[veins_slist_id] == "None":
        results_veins_slist['not_solved'] += 1        
    elif line[veins_slist_id] in [line[ref_id], line[ref2_id], \
                        line[ref3_id], line[ref4_id], line[ref5_id]]:
        if line[ref_sent] == line[word_sent]:
            results_veins_slist['total_intra'] += 1
        else:
            results_veins_slist['total_inter'] += 1            
        results_veins_slist['total_all'] += 1

    
fresult_resume = open(output_dir + "/result_resume.txt", "w")
result_resume = "Algorithm;Num. Not Solved;Perc. Not Solved;Num. Intra-sentential;Perc. Intra-sentencial;Num. Inter-sentential;Perc. Inter-sentential;Total Solved;Perc. Total solved\n"

perc_not_solved = float(results_bfp['not_solved']) / float(total_anaphors)
perc_total_intra = float(results_bfp['total_intra']) / float(total_intra_sentential)
perc_total_inter = float(results_bfp['total_inter']) / float(total_inter_sentential)
perc_total_all = float(results_bfp['total_all']) / float(total_anaphors)
result_resume += "BFP;%d;%f;%d;%f;%d;%f;%d;%f \n" % \
                (results_bfp['not_solved'], perc_not_solved , \
                 results_bfp['total_intra'], perc_total_intra , \
                 results_bfp['total_inter'], perc_total_inter, \
                 results_bfp['total_all'], perc_total_all \
                 )

perc_not_solved = float(results_con['not_solved']) / float(total_anaphors)
perc_total_intra = float(results_con['total_intra']) / float(total_intra_sentential)
perc_total_inter = float(results_con['total_inter']) / float(total_inter_sentential)
perc_total_all = float(results_con['total_all']) / float(total_anaphors)                
result_resume += "Conceptual;%d;%f;%d;%f;%d;%f;%d;%f\n" % \
                (results_con['not_solved'], perc_not_solved, \
                 results_con['total_intra'], perc_total_intra, \
                 results_con['total_inter'], perc_total_inter, \
                 results_con['total_all'], perc_total_all \
                 )

perc_not_solved = float(results_lrc['not_solved']) / float(total_anaphors)
perc_total_intra = float(results_lrc['total_intra']) / float(total_intra_sentential)
perc_total_inter = float(results_lrc['total_inter']) / float(total_inter_sentential)
perc_total_all = float(results_lrc['total_all']) / float(total_anaphors)                
result_resume += "LRC;%d;%f;%d;%f;%d;%f;%d;%f\n" % \
                (results_lrc['not_solved'], perc_not_solved, \
                 results_lrc['total_intra'], perc_total_intra, \
                 results_lrc['total_inter'], perc_total_inter, \
                 results_lrc['total_all'], perc_total_all \
                 )
                
perc_not_solved = float(results_slist['not_solved']) / float(total_anaphors)
perc_total_intra = float(results_slist['total_intra']) / float(total_intra_sentential)
perc_total_inter = float(results_slist['total_inter']) / float(total_inter_sentential)
perc_total_all = float(results_slist['total_all']) / float(total_anaphors)                
result_resume += "S-List;%d;%f;%d;%f;%d;%f;%d;%f\n" % \
                (results_slist['not_solved'], perc_not_solved, \
                 results_slist['total_intra'], perc_total_intra, \
                 results_slist['total_inter'], perc_total_inter, \
                 results_slist['total_all'], perc_total_all \
                 )

perc_not_solved = float(results_veins_bfp['not_solved']) / float(total_anaphors)
perc_total_intra = float(results_veins_bfp['total_intra']) / float(total_intra_sentential)
perc_total_inter = float(results_veins_bfp['total_inter']) / float(total_inter_sentential)
perc_total_all = float(results_veins_bfp['total_all']) / float(total_anaphors)                
result_resume += "Veins BFP;%d;%f;%d;%f;%d;%f;%d;%f\n" % \
                (results_veins_bfp['not_solved'], perc_not_solved, \
                 results_veins_bfp['total_intra'], perc_total_intra, \
                 results_veins_bfp['total_inter'], perc_total_inter, \
                 results_veins_bfp['total_all'], perc_total_all \
                 )

perc_not_solved = float(results_veins_lrc['not_solved']) / float(total_anaphors)
perc_total_intra = float(results_veins_lrc['total_intra']) / float(total_intra_sentential)
perc_total_inter = float(results_veins_lrc['total_inter']) / float(total_inter_sentential)
perc_total_all = float(results_veins_lrc['total_all']) / float(total_anaphors)                
result_resume += "Veins LRC;%d;%f;%d;%f;%d;%f;%d;%f\n" % \
                (results_veins_lrc['not_solved'], perc_not_solved, \
                 results_veins_lrc['total_intra'], perc_total_intra, \
                 results_veins_lrc['total_inter'], perc_total_inter, \
                 results_veins_lrc['total_all'], perc_total_all \
                 )

perc_not_solved = float(results_veins_slist['not_solved']) / float(total_anaphors)
perc_total_intra = float(results_veins_slist['total_intra']) / float(total_intra_sentential)
perc_total_inter = float(results_veins_slist['total_inter']) / float(total_inter_sentential)
perc_total_all = float(results_veins_slist['total_all']) / float(total_anaphors)                
result_resume += "Veins S-List;%d;%f;%d;%f;%d;%f;%d;%f\n" % \
                (results_veins_slist['not_solved'], perc_not_solved, \
                 results_veins_slist['total_intra'], perc_total_intra, \
                 results_veins_slist['total_inter'], perc_total_inter, \
                 results_veins_slist['total_all'], perc_total_all \
                 )

                
result_resume += "\n\n"
result_resume += "total_intra_sentential=%d\n" % total_intra_sentential
result_resume += "total_inter_sentential=%d\n" % total_inter_sentential
result_resume += "total_anaphors=%d\n" % total_anaphors
                
fresult_resume.write(result_resume)
fresult_resume.close
