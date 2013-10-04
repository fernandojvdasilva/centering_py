'''
Created on 03/11/2009

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

from corpus.rst.RST_Node import *
from anaphor_resolution.Centering_Elements import *

class Sentence(RST_Node, Un):
    '''
    This class holds the words of a sentence
    '''
    
    
    def __init__(self, words=None):
        '''
        Constructor
        '''
        RST_Node.__init__(self)
        Un.__init__(self)
        #set of Word objects which constitutes the sentence
        if words != None:
            self.words = words
        else:
            self.words = []                 
        
    def copy(self):
        result = Sentence()
        for word in self.words:
            result.words.append(word.copy(result))
        for word in self.vein:
            result.vein.append(word.copy(result))
        for word in self.head:
            result.head.append(word.copy(result))
        for word in self.label:
            result.label.append(word.copy(result))
        result.index = self.index
        return result
        
    def asString(self):
        result = ''
        for word in self.words:
            result = result + word.properties['text'] + ' '
        return result