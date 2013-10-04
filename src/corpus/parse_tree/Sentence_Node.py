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
from Node import Node
from corpus.Sentence import *

class Sentence_Node(Node, Un):
    '''
    This class represents a Sentence Node in the parse tree
    '''

    def __init__(self, parent):
        Node.__init__(self, parent)
        Un.__init__(self)
        self.words = []
        
    ''' Overrides the getSentenceRoot() method from Node class'''
    def getSentenceRoot(self):
        return self
    
    def asString(self):
        result = ''
        for word in self.words:
            result = result + word.properties['text'] + ' '
        return result
    
    def getClauseRoot(self):
        return self