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

class RST_Node:
    '''
    Represents a RST Node in the tree
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.isNuclear = False
        self.isSatellite = False
        self.id = None
        self.rel_id = None
        self.rel_name = None
        self.parent = None
        self.vein = [] #set of Word objects whose is present on this node vein
        self.head = [] #set of Word objects whose is present on this node head
        self.label = [] #set of Word objects whose is present on this node label
    
    
    def veinAsString(self):
        result = '{'
        for re in self.vein:
            if re.marked:
                marked = "(marked)"
            else:
                marked = ""
            result += re.word.properties['text'] + marked + ','
        result += '}'
        return result
    
    def headAsString(self):
        result = '{'
        for re in self.head:
            if re.marked:
                marked = "(marked)"
            else:
                marked = ""
            result += re.word.properties['text'] + marked + ','
        result += '}'
        return result
    
    def labelAsString(self):
        result = '{'
        for re in self.label:
            if re.marked:
                marked = "(marked)"
            else:
                marked = ""
            result += re.word.properties['text'] + marked + ','                    
        result += '}'
        return result
    
    def setSatellite(self):
        self.isNuclear = False
        self.isSatellite = True
        
    def setNuclear(self):
        self.isNuclear = True
        self.isSatellite = False
        
    def __getitem__(self, key):
        if key == 'id':
            return self.id
        
    def has_key(self, key):
        return (key == 'id')
                    
    def treeIndentation(self, depth):
        result = ''
        for i in range(depth-1):
            result += ' '
        result += '|_'
        return result
        
    def nodeAsString(self, depth):
        result = self.treeIndentation(depth)

        if self.isNuclear:
            type = "Nuclear"
        else:
            type = "Satellite"
        
        result += str(self.id) + "-" + self.asString() + " ("+ type + ")\n"
        
        #result += (" " * depth) + "label=" + self.labelAsString() + '\n'         
            
        #result += (" " * depth) + "head=" + self.headAsString() + '\n'
        
        #result += (" " * depth) + "vein=" + self.veinAsString() + '\n'
            
        return result        
        
    def getLeftSibling(self):
        if len(self.parent.children) > 2:
            print "WARNING: Node with more than two children!\n"
            print self.parent.nodeAsString(0) + "\n"
        for i in range(len(self.parent.children)):
            if self.parent.children[i] == self and i > 0:                
                return self.parent.children[i-1]             
        return None
    
    def getChildPos(self):
        for i in range(len(self.parent.children)):
            if self.parent.children[i] == self:
                return i
        return -1     
        
    def isLeftChild(self):
        if self.parent.children[0] == self:
            return True
        else:
            return False           
          
    def appendToVein(self, re_list):
        if re_list != None:
            for re in re_list:
                if not (re in self.vein):
                    self.vein.append(re)
            
    def appendUnmarkedToVein(self, re_list):
        if re_list != None:
            for re in re_list:
                if (not re.marked) and (not re in self.vein):
                    self.vein.append(re)
            
    def vt_mark(self, re_list):
        if re_list != None:
            for re in re_list:
                re.marked = True
                    
    def buildHead(self):
        ''' Heads: 1- The head of a terminal node is its label '''
        self.head = self.label                            
            
    def buildVein(self):
        ''' 1-The vein expression of the root is its head '''
        if None == self.parent:
            self.vein = self.head
        else:
            ''' 2- For each nuclear node whose parent node node has vein v
                   - if the node has a left non-nuclear sibling with head h,
                   then seq(mark(h),v) 
                   CHANGED: for each non-nuclear left sibling with head h, do seq(mark(h),v)
                   - otherwise, v
                3 - For each non-nuclear node of head h whose parent node has vein
                v, the vein expression is:
                - if the node is the left child of its parent, then seq(h,v)
                CHANGED: If there is any child at its right, then seq(h,v)
                - otherwise, seq(h,simpl(v))
            '''
            
            if len(self.head) > 0:
                child_pos = self.head[0].word.properties['id'][5:len(self.head[0].word.properties['id'])]
                child_pos = float(child_pos)
            else:
                child_pos = None
            self_pos = self.getChildPos()
            
            if self.isNuclear:                               
                for i in range(len(self.parent.children)):
                    sibling = self.parent.children[i]
                    if sibling != None and sibling != self:
                        if len(sibling.head) > 0 and child_pos != None:
                            sibl_pos = sibling.head[0].word.properties['id'][5:len(sibling.head[0].word.properties['id'])]
                            sibl_pos = float(sibl_pos) 
                            if  sibl_pos < child_pos and \
                                (not sibling.isNuclear):
                                self.appendToVein(self.vt_mark(sibling.head))                                                    
                            
                self.appendToVein(self.parent.vein)
            else:
                self.appendToVein(self.head)
                is_left = None                
                if child_pos != None:
                    for sibling in self.parent.children:
                        if sibling == self:
                            continue
                        if len(sibling.head) > 0:
                            sibl_pos = sibling.head[0].word.properties['id'][5:len(sibling.head[0].word.properties['id'])]
                            sibl_pos = float(sibl_pos)
                            if sibl_pos > child_pos:
                                 is_left = True
                                 break
                            else:
                                 is_left = False
                                 
                if None == is_left:
                    if self_pos <= (len(self.parent.children)-1):
                        is_left = True
                    else:
                        is_left = False
                
                if is_left:
                    self.appendToVein(self.parent.vein)
                else:
                    self.appendUnmarkedToVein(self.parent.vein)                    
