# coding: utf-8 

'''
Created on 24/11/2009

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


@author: Fernando
'''

from corpus.Discourse import *
from corpus.Sentence import *
from corpus.Word import *
from anaphor_resolution.Centering_Algorithm import *
from anaphor_resolution.Centering_Conceptual import *
from anaphor_resolution.Centering_BFP import *
from anaphor_resolution.Centering_SList import *
from anaphor_resolution.Centering_LRC import *
from anaphor_resolution.Veins_BFP import *



#discourse = Discourse()
#
#discourse.sentences.append(\
#                           Sentence(\
#                                    [\
#                                     Word({'canon':'O', 'text':'O', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':None, 'number':Word.S, 'tag':'artd', 'pron_type': None}),\
#                                     Word({'canon':'réu', 'text':'réu', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
#                                     Word({'canon':'conduzir', 'text':'conduzia', 'synt':[Word.V_FIN], 'gender':None, 'person':'3s', 'number':Word.S, 'tag':'v', 'tense':'ps', 'pron_type': None}),\
#                                     Word({'canon':'um', 'text':'um', 'synt':[Word.ACC], 'gender':Word.M, 'person':None, 'number':Word.S, 'tag':'arti', 'pron_type': None}),\
#                                     Word({'canon':'Alfa-Romeu', 'text':'Alfa-Romeu', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
#                                    ]\
#                                     )\
#                            )
#
#discourse.sentences.append(\
#                           Sentence(\
#                                    [\
#                                     Word({'canon':'Ele', 'text':'Ele', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':'3s', 'number':'3s', 'tag':'pron', 'pron_type':'pers'}),\
#                                     Word({'canon':'trafegar', 'text':'trafegava', 'synt':[Word.V_FIN], 'gender':None, 'person':'1-3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
#                                     Word({'canon':'acima', 'text':'acima', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'adv', 'pron_type': None}),\
#                                     Word({'canon':'de', 'text':'de', 'synt':[Word.ACC], 'gender':Word.M_F, 'person':None, 'number':Word.S, 'tag':'prp', 'pron_type': None}),\
#                                     Word({'canon':'a', 'text':'a', 'synt':[Word.ACC], 'gender':Word.F, 'person':'3s', 'number':Word.S, 'tag':'artd', 'pron_type': None}),\
#                                     Word({'canon':'velocidade', 'text':'velocidade', 'synt':[Word.ACC], 'gender':Word.F, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
#                                     Word({'canon':'permitir', 'text':'permitida', 'synt':[Word.ACC], 'gender':Word.F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
#                                    ]\
#                                     )\
#                            )
#
#
#discourse.sentences.append(\
#                           Sentence(\
#                                    [\
#                                     Word({'canon':'O', 'text':'O', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'artd', 'pron_type': None}),\
#                                     Word({'canon':'radar', 'text':'radar', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
#                                     Word({'canon':'registrar', 'text':'registrou', 'synt':[Word.V_FIN], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'tense':'ps', 'pron_type': None}),\
#                                     Word({'canon':'que', 'text':'que', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'conj', 'pron_type': None}),\
#                                     Word({'canon':'ele', 'text':'ele', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':'3s', 'tag':'pron', 'pron_type':'pers'}),\
#                                     Word({'canon':'estar', 'text':'estava', 'synt':[Word.ACC], 'gender':Word.M_F, 'person':'1-3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
#                                     Word({'canon':'a', 'text':'a', 'synt':[Word.ACC], 'gender':Word.F, 'person':None, 'number':Word.P, 'tag':'prp', 'pron_type': None}),\
#                                     Word({'canon':'183', 'text':'183', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'num', 'pron_type': None}),\
#                                     Word({'canon':'km/h', 'text':'km/h', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
#                                    ]\
#                                     )\
#                            )
#
#centering_alg = Centering_Conceptual(discourse)
##centering_alg = Centering_BFP(discourse)
##centering_alg = Centering_SList(discourse)
##centering_alg = Centering_LRC(discourse)
#centering_alg.run()
#centering_alg.printResult()
#
#print '----------------------------------------------------------------------------------\n'
#
#
#discourse2 = Discourse()
#
#discourse2.sentences.append(\
#                            Sentence(\
#                                     [\
#                                      Word({'canon':'Eu', 'text':'Eu', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':'1s', 'number':'1s', 'tag':'pron', 'pron_type':'pers'}),\
#                                      Word({'canon':'não', 'text':'não', 'synt':[Word.SUBJ], 'gender':None, 'person':None, 'number':None, 'tag':'adv', 'pron_type': None}),\
#                                      Word({'canon':'ver', 'text':'vejo', 'synt':[Word.V_FIN], 'gender':Word.M, 'person':'1s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
#                                      Word({'canon':'João', 'text':'João', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
#                                      Word({'canon':'haver', 'text':'há', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'v', 'pron_type': None}),\
#                                      Word({'canon':'algum', 'text':'alguns', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3p', 'number':Word.P, 'tag':'pron', 'pron_type': 'det'}),\
#                                      Word({'canon':'dia', 'text':'dias', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3p', 'number':Word.P, 'tag':'n', 'pron_type': None})\
#                                      ]\
#                                     )\
#                            )
#
#discourse2.sentences.append(\
#                            Sentence(\
#                                     [\
#                                      Word({'canon':'Carlos', 'text':'Carlos', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
#                                      Word({'canon':'achar', 'text':'acha', 'synt':[Word.V_FIN], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
#                                      Word({'canon':'que', 'text':'que', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'conj', 'pron_type': None}),\
#                                      Word({'canon':'ele', 'text':'ele', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':'3s', 'tag':'pron', 'pron_type':'pers'}),\
#                                      Word({'canon':'estar', 'text':'está', 'synt':[Word.ACC], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
#                                      Word({'canon':'estudar', 'text':'estudando', 'synt':[Word.ACC], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
#                                      Word({'canon':'para', 'text':'para', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'prep', 'pron_type': None}),\
#                                      Word({'canon':'sua', 'text':'suas', 'synt':[Word.ACC], 'gender':Word.F, 'person':'3p', 'number':Word.P, 'tag':'pron', 'pron_type':'det'}),\
#                                      Word({'canon':'prova', 'text':'provas', 'synt':[Word.ACC], 'gender':Word.F, 'person':'3p', 'number':Word.P, 'tag':'n', 'pron_type': None})\
#                                      ]\
#                                     )\
#                            )
#
#discourse2.sentences.append(\
#                            Sentence(\
#                                     [\
#                                      Word({'canon':'Eu', 'text':'Eu', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':'1s', 'number':'1s', 'tag':'pron', 'pron_type':'pers'}),\
#                                      Word({'canon':'achar', 'text':'acho', 'synt':[Word.V_FIN], 'gender':Word.M, 'person':'1s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
#                                      Word({'canon':'que', 'text':'que', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'conj', 'pron_type': None}),\
#                                      Word({'canon':'ele', 'text':'ele', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':'3s', 'tag':'pron', 'pron_type':'pers'}),\
#                                      Word({'canon':'ir', 'text':'foi', 'synt':[Word.ACC], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
#                                      Word({'canon':'para', 'text':'para', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'prep', 'pron_type': None}),\
#                                      Word({'canon':'o', 'text':'o', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'artd', 'pron_type': None}),\
#                                      Word({'canon':'interior', 'text':'interior', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
#                                      Word({'canon':'com', 'text':'com', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'conj', 'pron_type': None}),\
#                                      Word({'canon':'Linda', 'text':'Linda', 'synt':[Word.ACC], 'gender':Word.F, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None})\
#                                      ]\
#                                     )\
#                            )
#
#centering_alg2 = Centering_Conceptual(discourse2)
##centering_alg2 = Centering_BFP(discourse2)
##centering_alg2 = Centering_SList(discourse2)
##centering_alg2 = Centering_LRC(discourse2)
#centering_alg2.run()
#centering_alg2.printResult()
#
#print '----------------------------------------------------------------------------------\n' 
#
discourse3 = Discourse()
#
discourse3.sentences.append(\
                            Sentence(\
                                     [\
                                      Word({'canon':'Ontem', 'text':'Ontem', 'synt':[Word.ADVL], 'gender':None, 'person':None, 'number':None, 'tag':'adv', 'pron_type': None}),\
                                      Word({'canon':'ser', 'text':'foi', 'synt':[Word.ADVL], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'um', 'text':'um', 'synt':[Word.ADVL], 'gender':Word.M, 'person':None, 'number':Word.S, 'tag':'arti', 'pron_type': None}),\
                                      Word({'canon':'lindo', 'text':'lindo', 'synt':[Word.ADVL], 'gender':Word.M, 'person':None, 'number':Word.S, 'tag':'adj', 'pron_type': None}),\
                                      Word({'canon':'dia', 'text':'dia', 'synt':[Word.ADVL], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
                                      Word({'canon':'e', 'text':'e', 'synt':[Word.ADVL], 'gender':None, 'person':None, 'number':None, 'tag':'co', 'pron_type': None}),\
                                      Word({'canon':'Hélio', 'text':'Hélio', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
                                      Word({'canon':'estar', 'text':'estava', 'synt':[Word.V_FIN], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'empolgar', 'text':'empolgado', 'synt':[Word.ADVL], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'para', 'text':'para', 'synt':[Word.ADVL], 'gender':None, 'person':None, 'number':None, 'tag':'prp', 'pron_type': None}),\
                                      Word({'canon':'testar', 'text':'testar', 'synt':[Word.V_INF], 'gender':None, 'person':None, 'number':None, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'seu', 'text':'seu', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'pron', 'pron_type':'det'}),\
                                      Word({'canon':'novo', 'text':'novo', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'adj', 'pron_type': None}),\
                                      Word({'canon':'barco', 'text':'barco', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None})\
                                      ]\
                                     )\
                            )

discourse3.sentences.append(\
                            Sentence(\
                                     [\
                                      Word({'canon':'Ele', 'text':'Ele', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':'3s', 'number':'3s', 'tag':'pron', 'pron_type':'pers'}),\
                                      Word({'canon':'querer', 'text':'queria', 'synt':[Word.V_FIN], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'que', 'text':'que', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'ks', 'pron_type': None}),\
                                      Word({'canon':'Antônio', 'text':'Antônio', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
                                      Word({'canon':'se', 'text':'se', 'synt':[Word.ACC], 'gender':Word.M_F, 'person':'3s', 'number':'3s', 'tag':'pron', 'pron_type':'pers'}),\
                                      Word({'canon':'juntar', 'text':'juntasse', 'synt':[Word.ACC], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'a', 'text':'a', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'prp', 'pron_type': None}),\
                                      Word({'canon':'ele', 'text':'ele', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':'3s', 'tag':'pron', 'pron_type':'pers'}),\
                                      Word({'canon':'para', 'text':'para', 'synt':[Word.ADVL], 'gender':None, 'person':None, 'number':None, 'tag':'prep', 'pron_type': None}),\
                                      Word({'canon':'um', 'text':'um', 'synt':[Word.ADVL], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'arti', 'pron_type': None}),\
                                      Word({'canon':'passeio', 'text':'passeio', 'synt':[Word.ADVL], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None})\
                                      ]\
                                     )\
                            )

discourse3.sentences.append(\
                            Sentence(\
                                     [\
                                      Word({'canon':'Ele', 'text':'Ele', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':'3s', 'number':'3s', 'tag':'pron', 'pron_type':'pers'}),\
                                      Word({'canon':'chamar', 'text':'chamou', 'synt':[Word.V_FIN], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'Antônio', 'text':'Antônio', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
                                      Word({'canon':'a', 'text':'a', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'prp', 'pron_type': None}),\
                                      Word({'canon':'as', 'text':'as', 'synt':[Word.ACC], 'gender':Word.F, 'person':'3p', 'number':Word.P, 'tag':'artd', 'pron_type': None}),\
                                      Word({'canon':'6:00hs', 'text':'6:00hs', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':Word.S, 'tag':'num', 'pron_type': None})\
                                      ]\
                                     )\
                            )

discourse3.sentences.append(\
                            Sentence(\
                                     [\
                                      Word({'canon':'Antônio', 'text':'Antônio', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
                                      Word({'canon':'ficar', 'text':'ficou', 'synt':[Word.V_FIN], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'furioso', 'text':'furioso', 'synt':[Word.ACC], 'gender':Word.M, 'person':None, 'number':Word.S, 'tag':'adj', 'pron_type': None}),\
                                      Word({'canon':'por', 'text':'por', 'synt':[Word.ADVL], 'gender':None, 'person':None, 'number':None, 'tag':'prp', 'pron_type': None}),\
                                      Word({'canon':'ser', 'text':'ser', 'synt':[Word.ADVL], 'gender':None, 'person':None, 'number':None, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'acordar', 'text':'acordado', 'synt':[Word.ADVL], 'gender':Word.M, 'person':None, 'number':Word.S, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'tão', 'text':'tão', 'synt':[Word.ADVL], 'gender':None, 'person':None, 'number':None, 'tag':'adv', 'pron_type': None}),\
                                      Word({'canon':'cedo', 'text':'cedo', 'synt':[Word.ADVL], 'gender':None, 'person':None, 'number':None, 'tag':'adv', 'pron_type': None})\
                                      ]\
                                     )\
                            )

discourse3.sentences.append(\
                            Sentence(\
                                     [\
                                      Word({'canon':'Ele', 'text':'Ele', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':'3s', 'number':'3s', 'tag':'pron', 'pron_type':'pers'}),\
                                      Word({'canon':'dizer', 'text':'disse', 'synt':[Word.V_FIN], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'a', 'text':'a', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'prp', 'pron_type': None}),\
                                      Word({'canon':'o', 'text':'o', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'artd', 'pron_type': None}),\
                                      Word({'canon':'Hélio', 'text':'Hélio', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
                                      Word({'canon':'que', 'text':'que', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'ks', 'pron_type': None}),\
                                      Word({'canon':'não', 'text':'não', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'adv', 'pron_type': None}),\
                                      Word({'canon':'querer', 'text':'queria', 'synt':[Word.ACC], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'ir', 'text':'ir', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'v', 'pron_type': None})\
                                      ]\
                                     )\
                            )

discourse3.sentences.append(\
                            Sentence(\
                                     [\
                                      Word({'canon':'Obviamente', 'text':'Obviamente', 'synt':[Word.ADVL], 'gender':None, 'person':None, 'number':None, 'tag':'adv', 'pron_type': None}),\
                                      Word({'canon':'Hélio', 'text':'Hélio', 'synt':[Word.SUBJ], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
                                      Word({'canon':'não', 'text':'não', 'synt':[Word.ADVL], 'gender':None, 'person':None, 'number':None, 'tag':'adv', 'pron_type': None}),\
                                      Word({'canon':'ter', 'text':'teve', 'synt':[Word.V_FIN], 'gender':Word.M_F, 'person':'3s', 'number':Word.S, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'a', 'text':'a', 'synt':[Word.ACC], 'gender':Word.F, 'person':'3s', 'number':Word.S, 'tag':'artd', 'pron_type': None}),\
                                      Word({'canon':'intenção', 'text':'intenção', 'synt':[Word.ACC], 'gender':Word.F, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None}),\
                                      Word({'canon':'de', 'text':'de', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'prp', 'pron_type': None}),\
                                      Word({'canon':'irritar', 'text':'irritar', 'synt':[Word.ACC], 'gender':None, 'person':None, 'number':None, 'tag':'v', 'pron_type': None}),\
                                      Word({'canon':'Antônio', 'text':'Antônio', 'synt':[Word.ACC], 'gender':Word.M, 'person':'3s', 'number':Word.S, 'tag':'n', 'pron_type': None})\
                                      ]\
                                     )\
                            )

alg_options = {'bind_const': True, 'utt_type':'sentence', 'veins_head':'no'}
centering_alg3 = Centering_Conceptual(discourse3, alg_options)
centering_alg3 = Centering_BFP(discourse3)
##centering_alg3 = Centering_SList(discourse3)
##centering_alg3 = Centering_LRC(discourse3)
centering_alg3.run()
centering_alg3.printResult()



print '----------------------------------------------------------------------------------\n'


alg_options = {'bind_const': True, 'utt_type':'sentence', 'veins_head':'no'}
#discourse4 = Discourse(None, alg_options)
#discourse4.loadFromSummitCorpus('G:/UNICAMP/Summ-it_v3.0/corpusAnotado_CCR/CIENCIA_2000_6380')
#discourse4.loadFromSummitCorpus('/media/DADOS/UNICAMP/Summ-it_v3.0/corpusAnotado_CCR/CIENCIA_2002_22015')
#discourse4.loadFromSummitCorpus('/media/DADOS/UNICAMP/Summ-it_v3.0/corpusAnotado_CCR/CIENCIA_2003_24212')
#discourse4.loadFromSummitCorpus('/media/DADOS/UNICAMP/Summ-it_v3.0/corpusAnotado_CCR/CIENCIA_2005_28766')
#centering_alg4 = Centering_BFP(discourse4, alg_options)
#centering_alg4 = Centering_Conceptual(discourse4, alg_options)
#centering_alg4 = Centering_SList(discourse4, alg_options)
#centering_alg4 = Centering_LRC(discourse4, alg_options)
#centering_alg4 = Veins_BFP(discourse4, alg_options)
#centering_alg4.run()
#centering_alg4.printResult()

