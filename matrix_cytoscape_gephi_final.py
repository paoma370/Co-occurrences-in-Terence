#Python 3##############################################################################################
#
#	apre un file -- .lemmi_str -- che contiene frasi con 2 o piu' lemmi modali gia' separati,
#	compila la matrice delle relazioni e la scrive su file csv
#
############################################################
#
#	importa i parametri script (nome file da elaborare)
#	e separa nome_file e percorso file_output.lemmi.str
#
############################################################

import sys
if len(sys.argv)!=2:
	print ('Devi passare allo script il nome del file da elaborare')
	print ('Devi dare il percorso completo')
	print ('Sto uscendo...')
	sys.exit()
nome_script,percorso_e_nome_file=sys.argv

import os
percorso_e_nome_file_senza_estensione = percorso_e_nome_file[0:-10]
#print(percorso_e_nome_file_senza_estensione)
###################################
#
#	importa la libreria csv per
#	scrittura
#
###################################

import csv

##################################
#
#	lista dei lemmi modali
#
##################################

lemmi_modali=['debeo','possum','queo','nequeo','decet','licet','oportet','valet','aequum sum','meum sum','ius sum','necesse sum','opus sum','usus sum','aequus','iniquus',\
	'aptus','ineptus','certus','incertus','dubius','licitus','illicitus','necessarius','certo','dubium','dubio','necessarium','necessario','dubium','facultas','possibilitas',\
	'potestas','necessitas','necessitudo','probabilitas','aeque','certe','dubie','forsitan','fortasse', 'forte','indubitate','indubitanter','necessarie','possibiliter','probabiliter'] #lista aggiornata:eliminato certo e rivisti i composti


######################################################
#
#	dimensionamento matrice relazione lemmi modali
#
######################################################

matrix = [[0 for col in range(len(lemmi_modali))] for row in range(len(lemmi_modali))]

########################################################
#
#	apre file .lemmi_str
#	formato file: #frase\n lemma1,lemma2,lemman\n
#	scarta la frase e divide i lemmi modali
#
#######################################################

with open (percorso_e_nome_file) as f:
	for line in f:
		if line[0] == '#':
			#print (line)
			pass #scarta la frase, preceduta da #
		else:
			line = line[:-1] #elimina \n (newline) finale
			lemmi = line.split(',', -1) #divide in lemmi (virgola=separatore)
			print lemmi
			
			######################################################################
			#
			#	cerca la posizione del primo lemma nella lista lemmi_modali (x) e quella del successivo (y)
			#	e incrementa il contatore della relazione
			#
			######################################################################
			
			for i in range(len(lemmi)-1):
				for j in range((i + 1), len(lemmi)):
					x = lemmi_modali.index(lemmi[i])
					y = lemmi_modali.index(lemmi[j])
					matrix [x][y] = matrix [x][y] + 1
					#print (i,j,lemmi[i], lemmi[j],x,y)
				#print (lemmi_modali[x], matrix [x])
				


###########################################################################
#
#	scrive la matrice in csv nel formato per cytoscape
#
#
###########################################################################

with open(percorso_e_nome_file_senza_estensione + '_cytoscape.csv', 'w') as csvfile1:
	
	#intestazione colonne
	matrix_writer = csv.writer(csvfile1, delimiter = ',')
	matrix_writer.writerow(['Source', 'Target', 'Type', 'Id', 'Label', 'timeset', 'Weight'])

	id_count = 0	
	for i in range (len(lemmi_modali) - 1):
		for j in range (len(lemmi_modali) -1):
			if matrix [i][j] != 0:
				riga_n = [lemmi_modali[i], lemmi_modali[j], 'Directed', id_count, '', '', matrix[i][j]]
				id_count = id_count + 1
				#print (i,j,riga_n)
				matrix_writer.writerow(riga_n)
	



###########################################################################
#
#	scrive la matrice in csv con lista lemmi= intestazione colonne
#	e lemma(i)=intestazione riga per lettura su gephi
#
###########################################################################

with open(percorso_e_nome_file_senza_estensione + '_matrix_gephi.csv', 'w') as csvfile:
	
	#intestazione colonne
	matrix_writer = csv.writer(csvfile, delimiter = ',')
	matrix_writer.writerow(([''] + lemmi_modali))
	
	#righe della matrice con inserimento intestazione riga
	for i in range (len(lemmi_modali)):
		riga_n = matrix[i]
		riga_n.insert(0, lemmi_modali[i])
		#print (riga_n)
		matrix_writer.writerow(riga_n)
		

	
	
######################################################################
#
#	Output a video
#
######################################################################
print('#####################################################################')
print('#')
print('#	File csv per gephi scritto in     ' + percorso_e_nome_file_senza_estensione + '_matrix_gephi.csv')
print('#')
print('#	File csv per cytoscape scritto in ' + percorso_e_nome_file_senza_estensione + '_cytoscape.csv')
print('#')
print('#####################################################################')

