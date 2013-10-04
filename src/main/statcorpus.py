# decoding:iso-8859-1
'''
Created on 22/09/2009

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


@author: Fernando
'''

import sys
from corpus.SummaryCorpus import *


''' input_file = sys.argv[1]
if input_file == '' or input_file == None:
    print 'Error: Input XML corpus file invalid'
    exit()
    
output_file = sys.argv[2]
if output_file == '' or output_file == None:
    output_file = input_file + '2'
    
summarycorpus = SummaryCorpus(input_file)
summarycorpus.saveXmlFile(output_file)
summarycorpus.saveStatFile() '''

''' Using the Rhetalho corpus 
summarycorpus = SummaryCorpus(None, 'G:/UNICAMP/rhetalho')
summarycorpus.saveXmlFile('G:/UNICAMP/rhetalho_stat.xml')
summarycorpus.saveStatFile('G:/UNICAMP/rhetalho_wordcount.csv','G:/UNICAMP/rhetalho_pronouns.csv') '''

''' Using the Summ-it corpus 
summarycorpus2 = SummaryCorpus(None, 'G:/UNICAMP/Summ-it_v3.0/textos_originais')
summarycorpus2.saveXmlFile('G:/UNICAMP/summ-it_stat.xml')
summarycorpus2.saveStatFile('G:/UNICAMP/summ-it_wordcount.csv','G:/UNICAMP/summ-it_pronouns.csv') ''' 

'''Using the Dialog Summaries corpus '''
summarycorpus3 = SummaryCorpus('G:/UNICAMP/summaries_tagged.xml')
summarycorpus3.saveXmlFile('G:/UNICAMP/summaries_stat.xml')
summarycorpus3.saveStatFile('G:/UNICAMP/summaries_wordcount.csv','G:/UNICAMP/summaries_pronouns.csv')

