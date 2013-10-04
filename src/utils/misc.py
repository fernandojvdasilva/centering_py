# coding: utf-8 
'''
Created on 16/11/2009

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

''' ==================== Data Structure misc functions ==================== '''

'''Quicksort algorithm written by Magnus Lie Hetland'''
''' http://hetland.org/coding/python/quicksort.html '''

def partition(list, start, end):
    pivot = list[end]
    bottom = start-1
    top = end

    done = 0
    while not done:

        while not done:
            bottom = bottom + 1

            if bottom == top:
                done = 1
                break

            if list[bottom] > pivot:
                list[top] = list[bottom]
                break

        while not done:
            top = top-1

            if top == bottom:
                done = 1
                break

            if list[top] < pivot:
                list[bottom] = list[top]
                break

    list[top] = pivot
    return top

def quicksort(list, start, end):
   if start < end:
        split = partition(list, start, end)
        quicksort(list, start, split-1)
        quicksort(list, split+1, end)
   else:
        return 
    
    
''' Quicksort by key algorithm written by Fernando J V da Silva, adapted from the original written by Magnus Lie Hetland '''

def partition_bykey(list, keyfield, start, end):
    pivot = list[end]
    bottom = start-1
    top = end

    done = 0
    while not done:

        while not done:
            bottom = bottom + 1

            if bottom == top:
                done = 1
                break

            if list[bottom][keyfield] > pivot[keyfield]:
                list[top] = list[bottom]
                break

        while not done:
            top = top-1

            if top == bottom:
                done = 1
                break

            if list[top][keyfield] < pivot[keyfield]:
                list[bottom] = list[top]
                break

    list[top] = pivot
    return top

def quicksort_bykey(list, keyfield, start, end):
   if start < end:
        split = partition_bykey(list, keyfield, start, end)
        quicksort_bykey(list, keyfield, start, split-1)
        quicksort_bykey(list, keyfield, split+1, end)
   else:
        return
    
''' Combines two vectors (v1 and v2) such that the 
returned array will be in the form [x][y] where
x = len(v1) * len(v2) and y = 2 This returned
array is the cartesian product between the elements of the two arrays'''   
def vector_cartesian_product(v1, v2):
    result = []
    for i in range(len(v1)):
        for j in range(len(v2)):
            cel = []
            if type(v1[i]) is list:                                
                for k in range(len(v1[i])):
                    cel.append(v1[i][k])
            else:
                cel.append(v1[i])
                
            if type(v2[j]) is list:
                for k in range(len(v2[j])):            
                    cel.append(v2[j][k])                    
            else:
                cel.append(v2[j])
                
            result.append(cel)
    return result

''' Binary Insertion algorithm '''
def binary_insertion(list, el, field, start=None, finish=None):
    if start != None:
        left = start
    else:
        left = 0
        
    if finish != None:
        right = finish
    else:
        right = len(list)-1
        
    if len(list) == 0:
        list.append(el)
        return 0
            
    if el[field] < list[left][field]:
        list.insert(left, el)
        return 0    
    if el[field] > list[right][field]:
        list.insert(right+1, el)
        return right+1
    
    while left < right:
        center = (left + right) / 2
        if el[field] == list[center][field]:
            pos = center
            break
        elif el[field] < list[center][field]:
            right = center
        elif el[field] > list[center][field]:
            center += 1
            left = center
        pos = center
        
    list.insert(pos, el)

           
def findEntryByKey(array, key_values):
    for i in range(len(array)):
        match = True
        for k in key_values.keys():
            if array[i].has_key(k):
                match = match and array[i][k] == key_values[k] 
            else:
                match = False
        if match:
            return i
                    
    return -1
            


def unsplit(array, char):
    result = "" 
    for item in array:
        result += item + char
    return result[0:len(result)-1]


''' ==================== XML Helping Functions     ===================='''

''' Returns an DOM Element inside an DOM elements vector which it's id is equal to the given id'''
def findDOMElementById(elements, id):
    # TODO: Improve this algorithm's complexity ...    
    for el in elements:
        if not el.attributes.has_key('id'):
            continue
        if el.attributes['id'].value == id:
            return el
    print id
    print elements
    return False

def getNonNullDOMChildElement(elements, index):
    if elements == None:
        return None
    
    i = 0
    j = 0
    while i <= index and j < len(elements.childNodes):
        if elements.childNodes[j].nodeValue != '\n' and \
           elements.childNodes[j].nodeValue != '\t' and \
           elements.childNodes[j].nodeValue != ' ':        
            i += 1
        j += 1

    if j == len(elements.childNodes):
        return None
    else:
        return elements.childNodes[j-1]
    
def NonNullDOMChildElements(element):
    result = []
    for el in element.childNodes:
        if el.nodeValue != '\n' and \
           el.nodeValue != '\t' and \
           el.nodeValue != ' ':
            result.append(el)
    return result

def getDirectChildElements(node):
    result = []
    for e in node.childNodes:
        if e.ELEMENT_NODE == e.nodeType:
            result.append(e)
    return result



''' ====================         String specific functions     ===================='''


TOK_IGNORED_CHARS = [',', '.', '?', '"', '!', '=', ':', '_', '\'', '\n', ';']
TOK_SPACE_REPLACED_CHARS = ['-']

def extractSpecialHTMLChars(str):
    special_chars = re.findall('&[a-zA-Z0-9]+;', str)
    for char in special_chars:
        str = str.replace(char, '')
    
    return str

def extractIgnoredChars(str):
    str = replaceChars(str, TOK_SPACE_REPLACED_CHARS, ' ')
    str = replaceChars(str, TOK_IGNORED_CHARS, '')
                              
    return str

def replaceChars(str, chars, new_char):
    for char in chars:
        str = str.replace(char, new_char)        
    return str

''' ==================== Linguistic specific functions     ===================='''
CNT_CONTRACTION_LIST = [\
                        {'prep':'de', 'word':'o', 'cont':'do'},\
                        {'prep':'de', 'word':'os', 'cont':'dos'},\
                        {'prep':'de', 'word':'a', 'cont':'da'},\
                        {'prep':'de', 'word':'as', 'cont':'das'},\
                        {'prep':'de', 'word':'um', 'cont':'dum'},\
                        {'prep':'de', 'word':'uns', 'cont':'duns'},\
                        {'prep':'de', 'word':'uma', 'cont':'duma'},\
                        {'prep':'de', 'word':'umas', 'cont':'dumas'},\
                        {'prep':'de', 'word':'ele', 'cont':'dele'},\
                        {'prep':'de', 'word':'eles', 'cont':'deles'},\
                        {'prep':'de', 'word':'ela', 'cont':'dela'},\
                        {'prep':'de', 'word':'elas', 'cont':'delas'},\
                        {'prep':'de', 'word':'este', 'cont':'deste'},\
                        {'prep':'de', 'word':'estes', 'cont':'destes'},\
                        {'prep':'de', 'word':'esta', 'cont':'desta'},\
                        {'prep':'de', 'word':'estas', 'cont':'destas'},\
                        {'prep':'de', 'word':'esse', 'cont':'desse'},\
                        {'prep':'de', 'word':'esses', 'cont':'desses'},\
                        {'prep':'de', 'word':'essa', 'cont':'dessa'},\
                        {'prep':'de', 'word':'essas', 'cont':'dessas'},\
                        {'prep':'de', 'word':'aquele', 'cont':'daquele'},\
                        {'prep':'de', 'word':'aqueles', 'cont':'daqueles'},\
                        {'prep':'de', 'word':'aquela', 'cont':'daquela'},\
                        {'prep':'de', 'word':'aquelas', 'cont':'daquelas'},\
                        {'prep':'de', 'word':'aqueloutro', 'cont':'daqueloutro'},\
                        {'prep':'de', 'word':'aqueloutros', 'cont':'daqueloutros'},\
                        {'prep':'de', 'word':'aqueloutra', 'cont':'daqueloutra'},\
                        {'prep':'de', 'word':'aqueloutras', 'cont':'daqueloutras'},\
                        {'prep':'de', 'word':'isto', 'cont':'disto'},\
                        {'prep':'de', 'word':'isso', 'cont':'disso'},\
                        {'prep':'de', 'word':'aquilo', 'cont':'daquilo'},\
                        {'prep':'de', 'word':'aqui', 'cont':'daqui'},\
                        {'prep':'de', 'word':'aí', 'cont':'daí'},\
                        {'prep':'de', 'word':'ali', 'cont':'dali'},\
                        {'prep':'de', 'word':'outro', 'cont':'doutro'},\
                        {'prep':'de', 'word':'outros', 'cont':'doutros'},\
                        {'prep':'de', 'word':'outra', 'cont':'doutra'},\
                        {'prep':'de', 'word':'outras', 'cont':'doutras'},\
                        
                        {'prep':'com', 'word':'o', 'cont':'co'},\
                        {'prep':'com', 'word':'os', 'cont':'cos'},\
                        {'prep':'com', 'word':'a', 'cont':'coa'},\
                        {'prep':'com', 'word':'as', 'cont':'coas'},\
                        {'prep':'com', 'word':'mim', 'cont':'comigo'},\
                        {'prep':'com', 'word':'migo', 'cont':'comigo'},\
                        {'prep':'com', 'word':'ti', 'cont':'contigo'},\
                        {'prep':'com', 'word':'tigo', 'cont':'contigo'},\
                        {'prep':'com', 'word':'si', 'cont':'consigo'},\
                        {'prep':'com', 'word':'sigo', 'cont':'consigo'},\
                        {'prep':'com', 'word':'nós', 'cont':'conosco'},\
                        {'prep':'com', 'word':'nosco', 'cont':'conosco'},\
                        {'prep':'com', 'word':'vós', 'cont':'convosco'},\
                        {'prep':'com', 'word':'vosco', 'cont':'convosco'},\
                        
                        {'prep':'em', 'word':'o', 'cont':'no'},\
                        {'prep':'em', 'word':'os', 'cont':'nos'},\
                        {'prep':'em', 'word':'a', 'cont':'na'},\
                        {'prep':'em', 'word':'as', 'cont':'nas'},\
                        {'prep':'em', 'word':'um', 'cont':'num'},\
                        {'prep':'em', 'word':'uns', 'cont':'nuns'},\
                        {'prep':'em', 'word':'uma', 'cont':'numa'},\
                        {'prep':'em', 'word':'umas', 'cont':'numas'},\
                        {'prep':'em', 'word':'ele', 'cont':'nele'},\
                        {'prep':'em', 'word':'eles', 'cont':'neles'},\
                        {'prep':'em', 'word':'ela', 'cont':'nela'},\
                        {'prep':'em', 'word':'elas', 'cont':'nelas'},\
                        {'prep':'em', 'word':'este', 'cont':'neste'},\
                        {'prep':'em', 'word':'estes', 'cont':'nestes'},\
                        {'prep':'em', 'word':'esta', 'cont':'nesta'},\
                        {'prep':'em', 'word':'estas', 'cont':'nestas'},\
                        {'prep':'em', 'word':'esse', 'cont':'nesse'},\
                        {'prep':'em', 'word':'esses', 'cont':'nesses'},\
                        {'prep':'em', 'word':'essa', 'cont':'nessa'},\
                        {'prep':'em', 'word':'essas', 'cont':'nessas'},\
                        {'prep':'em', 'word':'aquele', 'cont':'naquele'},\
                        {'prep':'em', 'word':'aqueles', 'cont':'naqueles'},\
                        {'prep':'em', 'word':'aquela', 'cont':'naquela'},\
                        {'prep':'em', 'word':'aquelas', 'cont':'naquelas'},\
                        {'prep':'em', 'word':'aqueloutro', 'cont':'naqueloutro'},\
                        {'prep':'em', 'word':'aqueloutros', 'cont':'naqueloutros'},\
                        {'prep':'em', 'word':'aqueloutra', 'cont':'naqueloutra'},\
                        {'prep':'em', 'word':'aqueloutras', 'cont':'naqueloutras'},\
                        {'prep':'em', 'word':'isto', 'cont':'nisto'},\
                        {'prep':'em', 'word':'isso', 'cont':'nisso'},\
                        {'prep':'em', 'word':'aquilo', 'cont':'naquilo'},\
                        {'prep':'em', 'word':'outro', 'cont':'noutro'},\
                        {'prep':'em', 'word':'outros', 'cont':'noutros'},\
                        {'prep':'em', 'word':'outra', 'cont':'noutra'},\
                        {'prep':'em', 'word':'outras', 'cont':'noutras'},\
                        
                        {'prep':'a', 'word':'o', 'cont':'ao'},\
                        {'prep':'a', 'word':'os', 'cont':'aos'},\
                        {'prep':'a', 'word':'a', 'cont':'à'},\
                        {'prep':'a', 'word':'as', 'cont':'às'},\
                        {'prep':'a', 'word':'aquele', 'cont':'àquele'},\
                        {'prep':'a', 'word':'aqueles', 'cont':'àqueles'},\
                        {'prep':'a', 'word':'aquela', 'cont':'àquela'},\
                        {'prep':'a', 'word':'aquelas', 'cont':'àquelas'},\
                        {'prep':'a', 'word':'aqueloutro', 'cont':'àqueloutro'},\
                        {'prep':'a', 'word':'aqueloutros', 'cont':'àqueloutros'},\
                        {'prep':'a', 'word':'aqueloutra', 'cont':'àqueloutra'},\
                        {'prep':'a', 'word':'aqueloutras', 'cont':'àqueloutras'},\
                        {'prep':'a', 'word':'aquilo', 'cont':'àquilo'},\
                        
                        {'prep':'para', 'word':'o', 'cont':'pro'},\
                        {'prep':'para', 'word':'os', 'cont':'pros'},\
                        {'prep':'para', 'word':'a', 'cont':'pra'},\
                        {'prep':'para', 'word':'as', 'cont':'pras'},\
                        
                        {'prep':'por', 'word':'lo', 'cont':'polo'},\
                        {'prep':'por', 'word':'los', 'cont':'polos'},\
                        {'prep':'por', 'word':'la', 'cont':'pola'},\
                        {'prep':'por', 'word':'las', 'cont':'polas'},\
                        {'prep':'por', 'word':'o', 'cont':'pelo'},\
                        {'prep':'por', 'word':'os', 'cont':'pelos'},\
                        {'prep':'por', 'word':'a', 'cont':'pela'},\
                        {'prep':'por', 'word':'as', 'cont':'pelas'},\
                        
                        {'prep':'per', 'word':'o', 'cont':'pelo'},\
                        {'prep':'per', 'word':'os', 'cont':'pelos'},\
                        {'prep':'per', 'word':'a', 'cont':'pela'},\
                        {'prep':'per', 'word':'as', 'cont':'pelas'}\
                        ]


def isContraction(word):
    for cont in CNT_CONTRACTION_LIST:
        if cont['cont'] == word:
            return {'prep': cont['prep'], 'word': cont['word']}
    return False        
    
def isContractionPrep(word):
    for cont in CNT_CONTRACTION_LIST:
        if cont['prep'] == word:
            return True
    return False
    
def isContractionPair(prep, word):
    for cont in CNT_CONTRACTION_LIST:
        if cont['prep'] == prep and cont['word'] == word:
            return cont['cont']
    return False
    
def expand_Contractions(tokens):    
    result = []
    for t in tokens:
        cont = isContraction(t.lower())
        if not cont:
            result.append(t)
        else:
            result.append(cont['prep'])
            result.append(cont['word'])
    return result

''' List all collective substantives. The gender is relative to the word which it represents the
collective, i.e.:
    "arquipélago" (archipelago) is the collective(group) of "ilhas"(islands)
    Despite "arquipélago" being a male gender word, "ilhas" is a female gender. So the gender
    stored here is the "ilhas"'s. 

'''
COLLECTIVE_WORDS = [\
                    {'word':'grupo','gender':'m-f'},
                    {'word':'colméia','gender':'f'},
                    {'word':'arquipélago','gender':'f'},
                    {'word':'abecedário','gender':'f'},
                    {'word':'alfabeto','gender':'f'},
                    {'word':'abotoadura','gender':'m-f'},
                    {'word':'alameda','gender':'f'},
                    {'word':'álbum','gender':'f'},
                    {'word':'arvoredo','gender':'f'},
                    {'word':'armada','gender':'m'},
                    {'word':'esquadra','gender':'m'},
                    {'word':'frota','gender':'m'},
                    {'word':'atlas','gender':'m'},
                    {'word':'baixela','gender':'m-f'},
                    {'word':'biblioteca','gender':'m'},
                    {'word':'bosque','gender':'f'},
                    {'word':'floresta','gender':'f'},
                    {'word':'mata','gender':'f'},
                    {'word':'cacho','gender':'f'},
                    {'word':'constelação','gender':'f'},
                    {'word':'cordilheira','gender':'m-f'},
                    {'word':'serra','gender':'m-f'},
                    {'word':'discoteca','gender':'m'},
                    {'word':'esquadrilha','gender':'m'},
                    {'word':'flora','gender':'f'},
                    {'word':'mó','gender':'m-f'},
                    {'word':'molho','gender':'f'},
                    {'word':'penca','gender':'f'},
                    {'word':'pilha','gender':'m'},
                    {'word':'pinacoteca','gender':'f'},
                    {'word':'pomar','gender':'f'},
                    {'word':'prelatura','gender':'m'},
                    {'word':'programa','gender':'m'},
                    {'word':'ramalhete','gender':'f'},
                    {'word':'réstia','gender':'m-f'},
                    {'word':'banda','gender':'m-f'},
                    {'word':'batalhão','gender':'m-f'},
                    {'word':'legião','gender':'m-f'},
                    {'word':'pelotão','gender':'m-f'},
                    {'word':'tropa','gender':'m-f'},
                    {'word':'caravana','gender':'m-f'},
                    {'word':'choldra','gender':'m-f'},
                    {'word':'corja','gender':'m-f'},
                    {'word':'conclave','gender':'m'},
                    {'word':'congregação','gender':'m'},
                    {'word':'consistório','gender':'m'},
                    {'word':'elenco','gender':'m-f'},
                    {'word':'exército','gender':'m-f'},
                    {'word':'família','gender':'m-f'},
                    {'word':'farandula','gender':'m'},
                    {'word':'multidão','gender':'m-f'},
                    {'word':'orquestra','gender':'m-f'},
                    {'word':'camerata','gender':'m-f'},
                    {'word':'plêiade','gender':'m-f'},
                    {'word':'população','gender':'m'},
                    {'word':'povo','gender':'m'},
                    {'word':'quadrilha','gender':'m-f'},
                    {'word':'tertúlia','gender':'m-f'},
                    {'word':'time','gender':'m-f'},
                    {'word':'turma','gender':'m-f'},
                    {'word':'classe','gender':'m-f'},
                    {'word':'alcatéia','gender':'m'},
                    {'word':'bando','gender':'m-f'},
                    {'word':'cardume','gender':'m'},
                    {'word':'cáfila','gender':'m'},
                    {'word':'enxame','gender':'f'},
                    {'word':'escola','gender':'m'},
                    {'word':'fato','gender':'f'},
                    {'word':'fauna','gender':'m'},
                    {'word':'manada','gender':'m-f'},
                    {'word':'matilha','gender':'m'},
                    {'word':'ninhada','gender':'m'},
                    {'word':'nuvem','gender':'m'},
                    {'word':'rebanho','gender':'m-f'},
                    {'word':'vara','gender':'m'},
                    {'word':'canzoada','gender':'m'},
                    {'word':'revoada','gender':'m-f'},
                    {'word':'trompa','gender':'m-f'},                    
                    {'word':'novena','gender':'m'},
                    {'word':'biênio','gender':'m'},
                    {'word':'triênio','gender':'m'},
                    {'word':'quadriênio','gender':'m'},
                    {'word':'lustro','gender':'m'},
                    {'word':'década','gender':'m'},
                    {'word':'século','gender':'m'},
                    {'word':'milênio','gender':'m'},
                    {'word':'bimestre','gender':'m'},
                    {'word':'trimestre','gender':'m'},
                    {'word':'quadrimestre','gender':'m'},
                    {'word':'quinquimestre','gender':'m'},
                    {'word':'semestre','gender':'m'},
                    {'word':'septuamestre','gender':'m'},
                    {'word':'octamestre','gender':'m'},
                    {'word':'nonamestre','gender':'m'},
                    {'word':'decamestre','gender':'m'},
                    {'word':'andecamestre','gender':'m'}
                  ]


def isCollective(word):
    en = findEntryByKey(COLLECTIVE_WORDS, {'word':word})
    if en >= 0 and en < len(COLLECTIVE_WORDS): 
        return COLLECTIVE_WORDS[en]
    else:
        return None
    

def check_binding_constraints(word1, word2):
    ''' Checks only the principle B of Chomsky theory '''
    result = False
    
    ''' If both belong to different clauses, then returns true'''
    word1_clause = word1.getClauseRoot()
    word2_clause = word2.getClauseRoot()  
    if word1_clause != word2_clause:
        result = True
    else:                    
        ''' Otherwise returns true if word1 does not c-command word2 '''
        result = not word1.c_commands(word2)
        
        if result == False and word1.properties.has_key('ref_id') and \
           word1.properties['ref_id'] == word2.properties['id']:
            print 'ERROR: Binding constraint violated!\n'
            print 'word1.properties[id] == %s\n' % word1.properties['id']
            print 'word2.properties[id] == %s\n' % word2.properties['id']
        
    return result
            