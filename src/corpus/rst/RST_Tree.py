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
from corpus.rst.RST_Relation import *
from utils.misc import *



class RST_Tree:
    '''
    Represents an RST Tree
    '''

    def __init__(self, discourse):
        '''
        Constructor
        '''
        self.root = None # The root RST_Relation on the tree
        self.leaves = [] # Set of Sentence Objects that are leaves of the tree
        self.discourse = discourse
    
    def insert_node_above(self, nodes, child_node):
        rst_relation_ex = RST_Relation(self)
        rst_relation_ex.id = self.ex_id
        self.ex_id += 1
        
        nodes.append(rst_relation_ex)
        
        rst_relation_ex.parent = child_node.parent
        rst_relation_ex.rel_id = child_node.rel_id
        rst_relation_ex.multinuc = False
        
        rst_relation_ex.children.append(child_node)
        child_node.parent = rst_relation_ex
        child_node.rel_id = rst_relation_ex
        child_node.multinuc = False
        child_node.parent.children.remove(child_node)
        
        return rst_relation_ex
        


    def insert_node_behind(self, nodes, parent_node):
        rst_relation_ex = RST_Relation(self)
        rst_relation_ex.id = self.ex_id
        self.ex_id += 1
        
        nodes.append(rst_relation_ex)
        
        ''' Put the new node behind the parent_node '''
        rst_relation_ex.parent = parent_node
        rst_relation_ex.rel_id = parent_node.id
        rst_relation_ex.multinuc = False
                        
        if len(parent_node.children) > 0: 
            last_child = parent_node.children[len(parent_node.children) - 1]
        
            if last_child.isNuclear:
                rst_relation_ex.setNuclear()
            else:
                rst_relation_ex.setSatellite()
        
                rst_relation_ex.children.append(last_child)
                parent_node.children.remove(last_child)
                last_child.parent = rst_relation_ex
        else:
            rst_relation_ex.setNuclear()
                
                
        parent_node.children.append(rst_relation_ex)        
        
        return rst_relation_ex

    def loadFromSumitCorpus(self, rst_file, discourse):        
        
        ''' Every sentence is considered as a available node at the beginning '''
        nodes = []
        for sen in discourse.sentences:
            nodes.append(sen)
            ''' Every sentence is a leaf into the RST tree '''
            self.leaves.append(sen)
            
        ''' Append every group tag to the node list as RST_Relation objects '''
        groups = rst_file.getElementsByTagName('body')[0].getElementsByTagName('group')
        for grp in groups:
            rst_relation = RST_Relation(self)                                    
            rst_relation.id = grp.attributes['id'].value
            if grp.attributes.has_key('type'):
                rst_relation.multinuc = ( grp.attributes['type'].value == 'multinuc' )
            if grp.attributes.has_key('relname'):
                rst_relation.rel_name = grp.attributes['relname'].value
                                
            if grp.attributes.has_key('parent'):            
                rst_relation.rel_id = grp.attributes['parent'].value
            else:
                ''' Only the root node doesn't have a parent '''
                self.root = rst_relation
                            
            nodes.append(rst_relation)
            
        self.ex_id = 1000    
            
        for i in range(len(nodes)):
            curr_node = nodes[i]
            parent_index = findEntryByKey(nodes, {'id':curr_node.rel_id})
            if parent_index < 0:
                continue
            else:
                parent_node = nodes[parent_index]
            
            
            if isinstance(parent_node, RST_Relation):                                                                        
                                             
                if parent_node.name != None and \
                   parent_node.name != 'span' and curr_node.rel_name != 'span' and \
                   parent_node.name != curr_node.rel_name:
                    
                    grandpa_node = nodes[findEntryByKey(nodes, {'id':parent_node.rel_id})]
                    if parent_node.rel_name == 'span' and \
                       (grandpa_node.name == 'span' or grandpa_node.name == None):
                        parent_node = grandpa_node
                    else:
                        parent_node = self.insert_node_behind(nodes, parent_node)
                                                            
                ''' Append the curr_node to the parent_node'''
                parent_node.children.append(curr_node)
                curr_node.parent = parent_node                 
                    
                ''' Set the parent_node's name if it wasn't already set '''
                if None == parent_node.name or "span" == parent_node.name:
                    parent_node.name = curr_node.rel_name
                                
                ''' Set the nuclear and satellite nodes '''
                if parent_node.multinuc :
                    curr_node.setNuclear()
                else:
                    if 'span' == curr_node.rel_name and not curr_node.isNuclear:
                        curr_node.setSatellite()
                    else:
                        curr_node.setNuclear() 
                                
            else:
                ''' The nuclear node is a sentence '''                
                sibling = parent_node
                                
                parent_node_index = findEntryByKey(nodes, {'id':sibling.rel_id})
                if parent_node_index >= 0:
                    parent_node = nodes[parent_node_index]
                                                                             
                    if parent_node.name != None and \
                       parent_node.name != 'span' and curr_node.rel_name != 'span' and \
                       parent_node.name != curr_node.rel_name:
                        parent_node = self.insert_node_behind(nodes, parent_node)
                else:
                   parent_node = self.insert_node_above(nodes, sibling)
                   ''' In this case, the new node is the root!!'''
                   self.root = parent_node                  
                                    
                parent_node.children.append(curr_node)                                                                
                curr_node.parent = parent_node                 
                parent_node.name = curr_node.rel_name
                                    
                ''' Always set curr_node to Satellite and sibling to Nuclear '''
                curr_node.setSatellite()
                sibling.setNuclear()
                
                if 'span' == curr_node.rel_name:
                    print 'RST_Tree ERROR: Sentence node with sentence parent and marked as span!!'                                        
                        
        
    def treeAsString(self):
        if self.root != None:         
            return self.root.nodeAsString(0)
        else:
            return ""
        
    
    def saveTree(self, file_address):
        fout = open(file_address, 'w')
        fout.write(self.treeAsString())
        fout.close 
                