'''
Created on 19/09/2009

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
from corpus.Discourse import *
'''from parser.Tokenizer import *'''

class WordCounter:
    '''
    classdocs
    '''

    

    words = {}
    pronouns = {'ele':0,'ela':0,'eles':0, 'elas':0, 'seu':0, 'seus':0,'sua':0, 'suas':0, 'dele':0, 'dela':0, 'deles':0, 'delas':0, 'te':0, 'se':0, 'lhe': 0, 'lo':0, 'la':0, 'lhes':0, 'este':0, 'esta':0, 'estes':0, 'estas':0, 'deste':0, 'desta':0, 'destes':0, 'destas':0, 'esse':0, 'essa':0, 'esses':0, 'essas':0, 'desse':0, 'dessa':0, 'desses':0, 'dessas':0, 'isto':0, 'isso':0, 'disto':0, 'disso':0, 'qual':0, 'quais':0, 'que':0, 'quanto':0, 'quantos':0, 'onde':0, 'cujo':0, 'cuja':0, 'cujos':0, 'cujas':0, 'quem':0}
    summaries = None

    def __init__(self, summs=None):
        '''
        Constructor
        '''
        self.summaries = summs                     
    
    def wordtags(self, word_dict):
        xml_output = '<wordcount>\n'
        for word, count in word_dict.iteritems():
            xml_output = xml_output + '<word w="'+ word + '" count="'+ str(count) +'"></word>\n'
        xml_output = xml_output + '</wordcount>\n'
        return xml_output
    
    def wordCounts(self, word_dict):
        csv_output = ''
        for word, count in word_dict.iteritems():
            csv_output = csv_output + word + ';'+ str(count) +'\n'
        return csv_output
        
    def extractIgnoredChars(self, str):
        str = str.replace(',','')
        str = str.replace('.','')
        str = str.replace('?','')
        str = str.replace('"','')
        str = str.replace('-',' ')
        str = str.replace('!','')
        str = str.replace('=','')
        str = str.replace(':','')
        str = str.replace('_','')
        str = str.replace('\'','')
        str = str.replace('\n','')
        str = str.replace('(','')
        str = str.replace(')','')
        str = str.replace('"','')
        str = str.replace(';','')        
        return str        
        
    def count(self):
        for i in range(len(self.summaries)):
            wordlist = self.extractIgnoredChars(self.summaries[i].content).split(' ')
            self.summaries[i].words = {}
            self.summaries[i].pronouns = {'ele':0,'ela':0,'eles':0, 'elas':0, 'seu':0, 'seus':0,'sua':0, 'suas':0, 'dele':0, 'dela':0, 'deles':0, 'delas':0, 'te':0, 'se':0, 'lhe': 0, 'lo':0, 'la':0, 'lhes':0, 'este':0, 'esta':0, 'estes':0, 'estas':0, 'deste':0, 'desta':0, 'destes':0, 'destas':0, 'esse':0, 'essa':0, 'esses':0, 'essas':0, 'desse':0, 'dessa':0, 'desses':0, 'dessas':0, 'isto':0, 'isso':0, 'disto':0, 'disso':0, 'qual':0, 'quais':0, 'que':0, 'quanto':0, 'quantos':0, 'onde':0, 'cujo':0, 'cuja':0, 'cujos':0, 'cujas':0, 'quem':0}
            for word in wordlist:
                if word == '' or word == '\n':
                    continue
                if self.summaries[i].words.has_key(word.lower()):
                    self.summaries[i].words[word.lower()] = self.summaries[i].words[word.lower()] + 1
                else:
                    self.summaries[i].words[word.lower()] = 1
                
                if self.summaries[i].pronouns.has_key(word.lower()):
                    self.summaries[i].pronouns[word.lower()] = self.summaries[i].pronouns[word.lower()] + 1 
                    
                if self.words.has_key(word.lower()):
                    self.words[word.lower()] = self.words[word.lower()] + 1
                else:
                    self.words[word.lower()] = 1
                    
                if self.pronouns.has_key(word.lower()):
                    self.pronouns[word.lower()] = self.pronouns[word.lower()] + 1
                    