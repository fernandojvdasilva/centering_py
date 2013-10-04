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
from xml.dom import minidom
from corpus.Discourse import *
from statistic.WordCounter import *
import os.path

class SummaryCorpus:
    '''
    classdocs
    '''
    
        

    def __init__(self, xmlFile=None, directory=None):
        '''
        Constructor
        '''
        self.wordCounter = None
        self.xmldoc = None
        self.summaries = []
        if xmlFile != None:
            self.loadFromXml(xmlFile)
            self.loadSummariesCollection(self.xmldoc.getElementsByTagName('summaries')[0].getElementsByTagName('collection')[0])
        elif directory != None:
            self.loadSummariesFromDir(directory)        
        self.wordCounter = WordCounter(self.summaries)
        self.wordCounter.count()
        
        
    def loadFromXml(self, xmlFile):
        self.xmldoc = minidom.parse(xmlFile)
        
        
    def loadSummariesFromDir(self, dir):
        for filename in os.listdir(dir):
            if os.path.isdir(os.path.join(dir, filename)):
                continue
            f = open(os.path.join(dir,filename), 'r+')
            self.summaries.append(Summary(f.read()))
            
    
    def loadSummariesCollection(self, collection):
        tmp_summaries = collection.getElementsByTagName('summ') 
        for summ in tmp_summaries:
            self.summaries.append(Summary(summ.getElementsByTagName('content')[0].childNodes[0].toxml()))                        
        
    def toxml(self):
        xml_output = '<?xml version="1.0" encoding="iso-8859-1" ?>\n'
        xml_output = xml_output + '<summaries>\n'
        xml_output = xml_output + '<general_statistics>\n'
        xml_output = xml_output + self.wordCounter.wordtags(self.wordCounter.words)
        xml_output = xml_output + '</general_statistics>\n'
        xml_output = xml_output + '<collection>\n'
        for summ in self.summaries:
            xml_output = xml_output + summ.toxml()
        xml_output = xml_output + '</collection>\n'
        xml_output = xml_output + '</summaries>\n'
        return xml_output
            
    def pronounsCSV(self):

        csv_head = ''
        for k, v in self.wordCounter.pronouns.iteritems():
            csv_head += k + ';'
        csv_head += '\n'
        
        csv_output = ''
        for summ in self.summaries:
            for k, v in summ.pronouns.iteritems():
                csv_output += str(v) + ';'
            csv_output += '\n'
        
        csv_output = csv_head + csv_output  
        
        '''csv_output = 'ele;ela;eles;seu;seus;sua;dele;dela;deles;te;se;lhe;lo;la;lhes\n'        
        for summ in self.summaries:
            csv_output = csv_output + str(summ.pronouns['ele']) + ';'+ str(summ.pronouns['ela']) + ';'+ str(summ.pronouns['eles']) + ';'+ str(summ.pronouns['seu']) + ';'+ str(summ.pronouns['seus']) + ';'+ str(summ.pronouns['sua']) + ';'+ str(summ.pronouns['dele']) + ';'+ str(summ.pronouns['dela']) + ';'+ str(summ.pronouns['deles']) + ';'+ str(summ.pronouns['te']) + ';'+ str(summ.pronouns['se']) + ';'+ str(summ.pronouns['lhe']) + ';'+ str(summ.pronouns['lo']) + ';'+ str(summ.pronouns['la']) + ';'+ str(summ.pronouns['lhes']) + '\n' '''
        
        return csv_output            
        
    def saveXmlFile(self, xmlFile):
        '''TODO'''
        fileObj = open(xmlFile, 'w')
        fileObj.write(self.toxml())
        fileObj.close()
        
    def saveStatFile(self, wordcountfile, pronounfile):
        fileObj = open(wordcountfile, 'w')
        fileObj.write(self.wordCounter.wordCounts(self.wordCounter.words))
        fileObj.close()
        
        fileObj = open(pronounfile, 'w')
        fileObj.write(self.pronounsCSV())
        fileObj.close()
        