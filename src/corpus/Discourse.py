'''
Created on 20/09/2009

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
import re
from statistic.WordCounter import *
from corpus.rst.RST_Node import *
from corpus.rst.RST_Relation import *
from corpus.rst.RST_Tree import *
from corpus.Sentence import *
from corpus.Word import *
from parse_tree.Tree import *
from parse_tree.Sentence_Node import *
from parse_tree.Node import *
from xml.dom import minidom
from utils.misc import *


class Discourse:
    '''
    This class represents a discourse
    '''
    
    pronouns = {'ele':0,'ela':0,'eles':0, 'elas':0, 'seu':0, 'seus':0,'sua':0, 'suas':0, 'dele':0, 'dela':0, 'deles':0, 'delas':0, 'te':0, 'se':0, 'lhe': 0, 'lo':0, 'la':0, 'lhes':0, 'este':0, 'esta':0, 'estes':0, 'estas':0, 'deste':0, 'desta':0, 'destes':0, 'destas':0, 'esse':0, 'essa':0, 'esses':0, 'essas':0, 'desse':0, 'dessa':0, 'desses':0, 'dessas':0, 'isto':0, 'isso':0, 'disto':0, 'disso':0, 'qual':0, 'quais':0, 'que':0, 'quanto':0, 'quantos':0, 'onde':0, 'cujo':0, 'cuja':0, 'cujos':0, 'cujas':0, 'quem':0}
    
    def __init__(self, content=None, options=None):
        '''
        Constructor
        '''
        '''self.xml = xmlnode
        self.content = self.xml.getElementsByTagName('content')[0].childNodes[0].toxml()'''
        self.content = content
        self.last_id = 0
        self.xml = None
        self.words = {}
        self.sentences = [] # Set of Sentence objects whose represents the sentences of this discourse
        self.rst_tree = None
        self.parse_tree = None
        self.options = options
        
    def copy(self):
        result = Discourse()
        result.content = self.content
        result.last_id = self.last_id
        result.xml = self.xml
        for sentence in self.sentences:
            result.sentences.append(sentence.copy())
        return result
            
    def toxml(self):
        if self.xml != None:
            xml_output = '<summ id="'+ self.xml.attributes['id'].value + '" view="'+ self.xml.attributes['view'].value +'">\n'
        else:
            xml_output = '<summ id="'+ str(++self.last_id) + '">\n'
        xml_output = xml_output + '<statistics>\n'
        xml_output = xml_output + WordCounter().wordtags(self.words)
        xml_output = xml_output + '</statistics>\n'
        xml_output = xml_output + '<content>\n'
        xml_output = xml_output + self.content
        xml_output = xml_output + '</content>\n'
        xml_output = xml_output + '</summ>\n'
        return xml_output
    
    def findWordById(self, id):
        for sentence in self.sentences:
            for word in sentence.words:                
                if word.properties.has_key('id') and word.properties['id'] == id:
                    return word
    
    def loadFromSummitCorpus(self, dir):
        ''' Reads the several files inside the dir and loads the semantic and 
           syntactic information '''
        base_name = dir[dir.rfind('/')+1:len(dir)] 
        pos_file_addr = dir + '/' + base_name + '.txt.pos.xml'
        word_file_addr = dir + '/' +  base_name +'.txt.words.xml'
        chunks_file_addr = dir + '/' + base_name +'.txt.chunks.xml'
        rst_file_addr = dir + '/' + base_name +'.rs3'
        
        ''' Reads both rst_file, word_file and pos_file to build the data structure '''
        try:
            rst_file = minidom.parse(rst_file_addr)
        except:
            print rst_file_addr
        word_file = minidom.parse(word_file_addr)
        pos_file = minidom.parse(pos_file_addr)
        chunks_file = minidom.parse(chunks_file_addr)
        
        chunks = Discourse.getSyntFromChunks(chunks_file)
        
        sentences = rst_file.getElementsByTagName('body')[0].getElementsByTagName('segment')
        words = word_file.getElementsByTagName('words')[0].getElementsByTagName('word')
        words_pos = pos_file.getElementsByTagName('words')[0].getElementsByTagName('word')                
        i = 0
        ''' Counter for the sentences '''
        j = 0
        for tmp_sen in sentences:            
            sentence = Sentence()
            sentence.index = j  
            ''' Set RST_Node id and its related node id '''
            if tmp_sen.attributes.has_key('id'):
                sentence.id = tmp_sen.attributes['id'].value
            if tmp_sen.attributes.has_key('parent'):
                sentence.rel_id = tmp_sen.attributes['parent'].value
            if tmp_sen.attributes.has_key('relname'):
                sentence.rel_name = tmp_sen.attributes['relname'].value
                                   
            sen_tokens = extractIgnoredChars(extractSpecialHTMLChars(tmp_sen.childNodes[0].toxml())).lower().split(' ')
            sen_tokens = expand_Contractions(sen_tokens)
            
            word_to_compare = ''
            rebuild_contraction = False
            prep = ''            
            ''' Not all of the representations forms are either known or easy-to-handle
                so we implemented a kind of "tolerance limit". This way, if a word in RST
                file doesn't match to it's respective in words file, then we still can jump
                to the following word until the tolerance is reach.'''
            mismatch_tolerance = 3 
            
            
            for tmp_word in sen_tokens:                
                    
                
                if tmp_word == ' ' or tmp_word == '':
                    continue
                
                ''' Ignores special characters '''
                if words[i].childNodes[0].toxml() in TOK_IGNORED_CHARS:
                    i += 1                                        
                
                ''' A contraction may be inside a noun phrase. If so,
                    then it will be necessary to rebuild it to compare ...
                 '''
                if rebuild_contraction:
                    cont = isContractionPair(prep, tmp_word)
                    if cont != False:
                        if pos_underscore < 0:
                            word_to_compare = cont
                        else:
                            word_to_compare = word_to_compare[0:pos_underscore] + '_' + cont                       
                    else:
                        word_to_compare += '_' + tmp_word
                    rebuild_contraction = False
                else:
                    word_to_compare += tmp_word                 
                                
                ''' If the word inside the sentence is equal to 
                the word in the words file, then add it to the sentence structure'''                
                tmp_word2 = replaceChars(words[i].childNodes[0].toxml().lower(), 
                                         [',', '.', '?', '"', '!', '=', ':', '-', '\'', '\n', ';'], '')
                if word_to_compare == tmp_word2:
                    el = findDOMElementById(words_pos, words[i].attributes['id'].value)
                    if el != False:                                        
                        word = Discourse.loadWordFromPosFile(el)
                    else:
                        word = Discourse.loadWordFromPosFile(None)
                    
                    if words[i].attributes.has_key('ref'):
                        word.properties['ref'] = words[i].attributes['ref'] 
                    
                    word.properties['text'] = tmp_word2
                    word.properties['id'] = words[i].attributes['id'].value
                                                
                    if chunks.has_key(words[i].attributes['id'].value):
                        word.properties['synt'] = chunks[words[i].attributes['id'].value]                        
                        
                    ''' Stores the referent (if there is one)'''
                    if words[i].attributes.has_key('ref'):
                        word.properties['ref'] = words[i].attributes['ref'].value
                        
                    sentence.words.append(word)
                    word.sentence = sentence
                    i += 1
                    word_to_compare = ''
                else:
                    
                    '''May be a contraction '''
                    pos_underscore = word_to_compare.rfind('_')
                    prep = word_to_compare[pos_underscore+1:len(word_to_compare)]
                    is_cont = isContractionPrep(prep)
                    
                    '''It may be some noun phrase ... '''
                    if word_to_compare in tmp_word2 or is_cont:
                        '''May be a contraction '''                        
                        if is_cont:
                            rebuild_contraction = True
                        else:
                            word_to_compare += '_'                 
                    else:
                        if mismatch_tolerance > 0:
                            mismatch_tolerance -= 1
                            el = findDOMElementById(words_pos, words[i].attributes['id'].value)
                            if el != False:                                        
                                word = Discourse.loadWordFromPosFile(el)
                            else:
                                word = Discourse.loadWordFromPosFile(None)
                                
                            if words[i].attributes.has_key('ref'):
                                word.properties['ref'] = words[i].attributes['ref'].value
                                
                            word.properties['text'] = tmp_word2
                            word.properties['id'] = words[i].attributes['id'].value
                            if chunks.has_key(words[i].attributes['id'].value):
                                word.properties['synt'] = chunks[words[i].attributes['id'].value]
                            sentence.words.append(word)
                            word.sentence = sentence
                            i += 1
                            word_to_compare = ''                                        
            
            self.sentences.append(sentence)
            j += 1
            
        self.parse_tree = Tree()
        self.parse_tree.loadFromSumitCorpus(chunks_file, self)
        
        self.rst_tree = RST_Tree(self)
        self.rst_tree.loadFromSumitCorpus(rst_file, self)
                    
                                     
    @staticmethod
    def loadWordFromPosFile(pos_tag):            
        result = Word()
        
        element = getNonNullDOMChildElement(pos_tag, 0)
        
        if element == None:
            result.properties['tag'] = 'unk'
            return result
        
        result.properties['tag'] = element.tagName.lower()
        result.properties['canon'] = element.attributes['canon'].value.lower()        
        if element.attributes.has_key('gender'):
            result.properties['gender'] = element.attributes['gender'].value.lower()            
        if element.attributes.has_key('number'):
            result.properties['number'] = element.attributes['number'].value.lower()
        if element.attributes.has_key('person'):
            result.properties['person'] = element.attributes['person'].value.lower()
        if element.attributes.has_key('mode'):
            result.properties['mode'] = element.attributes['mode'].value.lower()
        
        ''' If pos_tag element is a pronoun, then it may have children 
        with syntactic attributes ... '''        
        if element.tagName.lower() == 'pron':
            children = NonNullDOMChildElements(element)
            for child in children:
                has_synt_tags = False                
                if child.attributes == None:
                    continue
                
                if child.attributes.has_key('gender'):
                    result.properties['gender'] = child.attributes['gender'].value.lower()
                    has_synt_tags = True
                if child.attributes.has_key('number'):
                    result.properties['number'] = child.attributes['number'].value.lower()                    
                    has_synt_tags = True
                if child.attributes.has_key('person'):
                    result.properties['person'] = child.attributes['person'].value.lower()
                    has_synt_tags = True                                            
                
                if has_synt_tags:
                    result.properties['pron_type'] = child.tagName.lower()            
            
        ''' If pos_tag element is an article, then it may have a tag 
        in its children as well '''
        if element.tagName.lower() == 'art':
            children = NonNullDOMChildElements(element)
            for child in children:
                if child.attributes == None:
                    continue
                
                if child.attributes.has_key('tag') and child.attributes['tag'].value.lower() in ['artd', 'arti']:
                    result.properties['tag'] = child.attributes['tag'].value.lower()
        
        return result
    
        
    @staticmethod
    def getSyntFromChunks(chunks_file):
        result = {}
        for paragraph in chunks_file.getElementsByTagName('text')[0].getElementsByTagName('paragraph'):
            for sentence in paragraph.getElementsByTagName('sentence'):
                for chunk in getDirectChildElements(sentence):
                    Discourse.processChunks(chunk, result)
        return result
    
                                
    @staticmethod            
    def processChunks(chunk, result):
        span = chunk.attributes['span'].value.split('..')
        start = int(span[0][5:len(span[0])])
        if len(span) > 1:
            finish = int(span[1][5:len(span[0])])
        else:
            finish = start
        for i in range(start, finish+1):
            if not result.has_key('word_'+ str(i)):
                result['word_'+ str(i)] = []
            if not (chunk.attributes['ext'].value in result['word_'+ str(i)]):
                result['word_'+ str(i)].append(chunk.attributes['ext'].value.lower())
            
        for child_chunk in chunk.getElementsByTagName('chunk'):
            Discourse.processChunks(child_chunk, result)      
            
                        