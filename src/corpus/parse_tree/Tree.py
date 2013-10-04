'''
Created on Jul 1, 2010

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
from xml.dom import minidom
from Node import *
from Sentence_Node import *
from utils.misc import *

class Tree:
    '''
    This class represents the whole parse tree
    '''

    def __init__(self):
        self.sentences = []
        self.parent = None            
            
    def c_command(self, node1, node2):
        ''' Checks if node1 c-command node2 '''
        pass        
            
    def loadFromSumitCorpus(self, chunks_file, discourse):        
        sen = None
        for paragraph in chunks_file.getElementsByTagName('text')[0].getElementsByTagName('paragraph'):
            i = 0
            for sentence in getDirectChildElements(paragraph):
                sen = Sentence_Node(self)
                sen.index = i
                i += 1                    
                for chunk in getDirectChildElements(sentence):                    
                    child_node = self.loadNodeFromSumitChunk(sen, sen, chunk, discourse)
                    if child_node != None:
                        sen.children.append(child_node)                        
                self.sentences.append(sen)
         
    def loadNodeFromSumitChunk(self, sentence_node, parent, chunk, discourse):
        result = None
        
        ''' If the chunk is a non-atomic node '''
        if chunk.attributes['span'].value.find('..') >= 0:           
            result = Node(parent)
            ''' For child = each one of chunk's children '''
            for child in getDirectChildElements(chunk):  
                child_node = None              
                child_node = self.loadNodeFromSumitChunk(sentence_node, result, child, discourse)
                if child_node != None:
                    result.children.append(child_node)            
        else:
            ''' If the chunk is an atomic node (i.e., a word itself) '''
            ''' Look for the word in words list '''
            for sen in discourse.sentences:
                for word in sen.words:
                    if word.properties['id'] == chunk.attributes['span'].value:
                        result = word
                        result.parent = parent
                        sentence_node.words.append(result)
                        break
                if result != None:
                    break
             
                
        if result != None:       
            result.form = chunk.attributes['form'].value
        
            
        return result         
        
        
    def treeAsString(self):
        result = ""        
        for sentence in self.sentences:
            result += "S\n"
            for child in sentence.children:
                result += child.nodeAsString(1)
            result += "\n"
        return result
        
             
    def saveTree(self, file_address):
        fout = open(file_address, 'w')
        fout.write(self.treeAsString())
        fout.close  
        