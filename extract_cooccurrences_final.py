#Python 3##############################################################################################
#
#	open conllu file; look into the 'lemma' column; a list sets the lemmas of the modal markers it has to look for; if it finds, in the same sentence, two or more lemmas it saves the sentence in 
#a new file
#
#
############################################################
#
#	importa i parametri script (nome file da elaborare)
#
############################################################
import sys
if len(sys.argv) != 2:
	print ('Devi passare allo script il nome del file da elaborare')
	print ('Devi dare il percorso completo')
	print ('Sto uscendo...')
	sys.exit()
nome_script,nome_file = sys.argv

import os

###################################
#
#	import csv library for the statistics file
#	
#
###################################
import csv

###################################
#
#	import conllu library to read conllu file
#
###################################
from conllu import parse

##################################
#
#	list of modal markers
#
##################################
lemmi_modali_1 = ['debeo','possum','queo','nequeo','decet','licet','oportet','valet','iniquus','aptus','ineptus','certus','incertus',\
	'dubius','licitus','illicitus','necessarius','certo','dubium','dubio','necessarium','necessario','dubium','facultas','possibilitas',\
	'potestas','necessitas','necessitudo','probabilitas','aeque','certe','dubie','forsitan','fortasse', 'forte','indubitate','indubitanter','necessarie',\
	'possibiliter','probabiliter']
#lemmi_modali_2=['aequum est','meum est','ius est','necesse est','opus est','usus est']
#il controllo su aequum est e aequus e' specifico in programma 
lemmi_modali_2a = ['meum','ius','necesse','opus','usus']
lemmi_modali_2b = ['sum']

#####################################################################
#
#	opens, reads and closes the conllu file in input
#
######################################################################
f = open (nome_file)
#reads the whole file (maybe memory problem if the file is too big?)
read_data = f.read()
f.closed

#############################################
#
#	prepares variables
#
#############################################
#azzera la stringa di output file conllu sentences selezionate
output_sentences_conllu = ""
#azzera la stringa di output file per elaborazione matrice
output_sentences_str = ''
#azzera numero sentences con concorrenza lemmi modali pari o superiore a 2 (selezionate per l'output)
n_output_sentences = 0
#azzera numero sentences con ricorrenza lemmi modali pari a 1, 2, 3 o piu'
n_sentences_0l = 0
n_sentences_1l = 0
n_sentences_2l = 0
n_sentences_3l = 0

####################################################################
#
#	imports sentences as a list (uses conllu library)
#
####################################################################
sentences = parse(read_data)

###############################################################
#
#	main cycle, iterated for each sentence
#
###############################################################
for i in range(len(sentences)): #range serve perché il valore sia numberabile: mettendo range fa tutto il ciclo da 0 a x (x=numero sentences). importa le sentences come lista. le sentences sono un unico file. quanti oggetti ci sono nella lista? fai cicli da 1 a x (numero sentences)
	sentence = sentences[i] #i=1

	cocorrenza = 0 #man mano incremento numero di lemmi modali che trovo.variabile di appoggio che dà numero di lemmi
	
	#################################################
	#################################################
	sequenza_form = ''
	lista_lemmi_in_sentence = '' #stringhe
  
	###############################################################################################
	#
	#ciclo interno, cerca per ogni lemma i lemmi modali e incrementa il contatore (concorrenza)
	#
	###############################################################################################
	for j in range (len (sentence)): #numero parole NB sentences vs. sentence
		token = sentence[j] #token comes from conllu library. sentence è diventato una lista
		#print (token["lemma"]) #check if it prints the lemmas. in token there are all the fields for each token in the conllu file. check how conllu library works
		
		#########################################################################
		#########################################################################
		#checks simple lemmas from lemmi_modali_1
		#########################################################################
		if (j != (len(sentence)-1)): #se il contatore non è arrivato alla fine 
			token_2 = sentence[j+1] #se if è vero crea token_2 (serve nel secondo controllo non qui)
		
		conta = lemmi_modali_1.count(token["lemma"]) #count controlla se il lemma compare nella lista. può comparire solo una volta. controllo se il lemma compare nella lista. count è un metodo delle liste.
		#print (token["lemma"],conta)
		cocorrenza = cocorrenza + conta #conta =0 o =1
		
		####################################################
		#file intermedio lemmi_str da elaborare per matrix
		####################################################
		sequenza_form = sequenza_form + (token["form"] + ' ') #ricostruisce la frase + ' ' mette spazi tra le parole.NB mette lo spazio anche su interpunzione
		lista_lemmi_in_sentence = lista_lemmi_in_sentence + (conta * (token["lemma"]+',')) #lemmi in co-occorrenza. conta è =0 o =1.
		
		#######################################################
		#######################################################
		#controlla lemmi modali composti 
		#######################################################
		if (lemmi_modali_2a.count(token["form"]) != 0): #NB prendo il form e non il lemma perché mi interessa meum non meus
#		print (token["form"])
			#se e' l'ultimo token della sentence non controlla per lemmi_modali_2b
			if (j == (len(sentence)-1)): #se siamo all'ultimo token. NB ricontrollo se j non è l'ultimo token ma l'avevo già fatto in 114
				break
			elif (lemmi_modali_2b.count(token_2["lemma"]) != 0):
				cocorrenza = cocorrenza + 1 #può essere solo 1, potevo usare anche conta però
				
				#########################################################################
				#########################################################################
				lista_lemmi_in_sentence = lista_lemmi_in_sentence + token["form"] + ' ' + token_2["lemma"] + ',' #sequenza_form è stata già aggiornata

		#######################################################################
		#######################################################################
		#controlla aequus che puo' essere lemma semplice o composto
		#######################################################################
		if (token["lemma"]) == 'aequus': #token["lemma"] viene elaborato qui
			cocorrenza = cocorrenza + 1 #è modale in ogni caso quindi incremento co-occorrenza
			
			if (j == (len(sentence)-1)):
				lista_lemmi_in_sentence = lista_lemmi_in_sentence + token["lemma"] + ','
			
			elif (token["form"]) == 'aequum' and (token_2["lemma"]) == 'sum':
				lista_lemmi_in_sentence = lista_lemmi_in_sentence + token["form"] + ' ' + token_2["lemma"] + ','
			else:
				lista_lemmi_in_sentence = lista_lemmi_in_sentence + token["lemma"] + ',' #eseguito anche se non è l'ultimo token
				
				
				

	#se ricorrono almeno 2 lemmi modali appende la sentence al file di output
	#serialize converte nuovamente la tokenlist creata da parse in formato conllu
	if (cocorrenza >= 2): #per contare tutte le occorrenze
		output_sentences_conllu = output_sentences_conllu + (sentence.serialize()) #
		n_output_sentences = n_output_sentences + 1 #statistiche
		
		#############################################################################################
		#file intermedio lemmi_str
		#############################################################################################
		output_sentences_str = output_sentences_str + '#' + sequenza_form[:-1] + '\n' + lista_lemmi_in_sentence[:-1] + '\n' #sequenza_form[:-1] tolgo lo spazio finale + vai a capo + lista lemmi in sentence senza la virgola
		
  
	if cocorrenza == 0:
		n_sentences_0l = n_sentences_0l + 1
	elif cocorrenza == 1:
		n_sentences_1l = n_sentences_1l + 1
	elif cocorrenza == 2:
		n_sentences_2l = n_sentences_2l + 1
	else:
		n_sentences_3l = n_sentences_3l + 1

#print (output_sentences_str)
#####################################################################
#
#	apre, scrive e chiude in lettura il file intermedio 
#	lemmi_str elaborato per matrix
#
######################################################################
#print (output_sentences)
nome_file_senza_estensione = nome_file[0:-7] #prendo inizio del nome togliendo i 7 caratteri finali (toglie estensione .conllu)
f = open(nome_file_senza_estensione + '_output' + '.lemmi_str2', 'w') #apre un file in scrittura 'w' (lettura 'r')
#stringa_output_sentences = str(output_sentences)
f.write(output_sentences_str) #f è un nome: questo file. apri file e ci scrivi ('write') l'output delle sentences
f.closed #sempre aprire e chiudere

#####################################################################
#
#	apre, scrive e chiude in lettura il file conllu elaborato
#
######################################################################
#print (output_sentences)
nome_file_senza_estensione = nome_file[0:-7] #superfluo, già fatto a r 189
f = open(nome_file_senza_estensione + '_output' + '.conllu', 'w')
#stringa_output_sentences = str(output_sentences)
f.write(output_sentences_conllu)
f.closed

#####################################################################
#
#	apre e scrive il file csv con le statistiche come dizionario. #dict=dizionario. crea coppie. valore + separatore (comma, tab o altro) 
#
######################################################################
dict = {'Numero sentences totale:                    ' : len(sentences), 'Numero sentences con 0 lemmi modali:        ' : n_sentences_0l, 'Numero sentences con 1 lemma modale:        ' : n_sentences_1l,\
  'Numero sentences con 2 lemmi modali:        ' : n_sentences_2l, 'Numero sentences con 3 o piu\' lemmi modali: ' : n_sentences_3l, 'Numero frasi trovate (almeno 2 occorrenze): ' :n_output_sentences}
w = csv.writer(open(nome_file_senza_estensione+'_statistiche'+'.csv', 'w')) #w è come f, nome qualunque. nome_file_senza_estensione era già stato definito
for key, val in dict.items(): #per ogni chiave e valore in (dict.items() è un metodo di dict)
	w.writerow([key, val]) #scrive la riga con la dupla key e val

#non c'è bisogno di chiuderla libreria
######################################################################
#
#	Output a video
#
######################################################################
print ('########################################################')
print ('#')
print ('# Numero sentences totale:                   ', len(sentences))
print ('# Numero sentences con 0 lemmi modali:       ', n_sentences_0l)
print ('# Numero sentences con 1 lemma modale:       ', n_sentences_1l)
print ('# Numero sentences con 2 lemmi modali:       ', n_sentences_2l)
print ('# Numero sentences con 3 o piu\' lemmi modali:', n_sentences_3l)
print ('# Numero frasi trovate (almeno 2 occorrenze: ', n_output_sentences)
print ('#')
print ('# Output scritto su '+ nome_file_senza_estensione + '_output' + '.conllu')
print ('#')
print ('# Output statistiche scritto su '+ nome_file_senza_estensione + '_statistiche' + '.csv')
print ('#')
print ('# Output file intermedio per elaborazione matrice scritto su ' + nome_file_senza_estensione + '_output' + '.lemmi_str')
print ('#')
print ('########################################################')
