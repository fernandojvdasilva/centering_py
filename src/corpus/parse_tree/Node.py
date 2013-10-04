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
from corpus.Word import *

class Node:
    '''
    This class represents a Node in the parse tree
    '''
    def __init__(self, parent):
        self.children = []
        self.form = None
        self.parent = parent
        
    def treeIndentation(self, depth):
        result = ''
        for i in range(depth-1):
            result += ' '
        result += '|_'
        return result
        
    def nodeAsString(self, depth):
        result = self.treeIndentation(depth)

        result += self.form + "\n"
        for child in self.children:
            result += child.nodeAsString(depth+1)
            
        return result
    
    ''' Returns true if this node c-commands the given node '''
    def c_commands(self, node):
        '''
        A c-commands B iff (= if and only if)
        - neither A nor B dominates the other, and
        - the first branching node that dominates A also dominates B.
        '''
        return (not self.dominate(node)) and \
               (not node.dominate(self)) and \
               self.getBranchingNode().dominate(node)
        
    
    ''' Returns true if this node dominates the given node '''
    def dominate(self, node):
        if None == node.parent:
            return False
        elif node == self:
            return True
        else:
            return self.dominate(node.parent)
                    
    
    def getBranchingNode(self):
        return self.parent
        
    
    def getSentenceRoot(self):
        if None == self.parent:
            print 'form= %s' % self.form 
                    
        return self.parent.getSentenceRoot()
    
    def getClauseRoot(self):
        if self.form in ['fcl','acl','icl']:
            return self
        else:
            return self.parent.getClauseRoot()                        