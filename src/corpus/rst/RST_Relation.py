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


class RST_Relation(RST_Node):
    '''
    This class represents a relationship in a RST tree
    '''    

    def __init__(self, rst_tree):
        '''
        Constructor
        '''
        RST_Node.__init__(self)
        self.children = []
        self.parent = None # RST_Relation node that is it's parent on the tree        
        self.name = None
        self.multinuc = False
        self.rst_tree = rst_tree
        
    def nodeAsString(self, depth):
        result = ""        
        result = self.treeIndentation(depth)

        if self.isNuclear:
            type = "Nuclear"
        else:
            type = "Satellite"                

        result += str(self.id) + "-" + str(self.name) + "("+ type + ") \n"
                
        #result += (" " * depth) + "label=" + self.labelAsString() + '\n'          
                    
        #result += (" " * depth) + "head=" + self.headAsString() + '\n'
                
        #result += (" " * depth) + "vein=" + self.veinAsString() + '\n'        
                
        for child in self.children:
            if child != None:
                result += child.nodeAsString(depth+1)
                            
        return result         
    
    def buildHead(self):        
        for child in self.children:
            child.buildHead()
            
            if self.rst_tree.discourse.options.has_key('veins_head'):
                veins_head = self.rst_tree.discourse.options['veins_head']
            else:
                veins_head = None
               
            if veins_head != None and \
               ('yes_all' == veins_head or 'yes_ord' == veins_head):
                for re in child.head:
                    self.head.append(re)
            elif child.isNuclear:
                for re in child.head:
                    self.head.append(re)                    
    
    def buildVein(self):
        RST_Node.buildVein(self)
        for child in self.children:
            child.buildVein()                
            