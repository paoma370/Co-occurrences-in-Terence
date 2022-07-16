#Python 3##############################################################################################
#
#	open conllu file; look into the 'lemma' column; a list sets the lemmas of the modal markers it has to look for; if it finds, in the same sentence, two or more lemmas it saves the sentence in 
#a new file
#
#
############################################################
#
#	import parameters script
#
############################################################
import sys
if len(sys.argv) != 2:
	print ('Give name file to process')
	print ('Give complete path')
	print ('Exit...')
	sys.exit()
name_script,name_file = sys.argv

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
modal_lemmas_1 = ['debeo','possum','queo','nequeo','decet','licet','oportet','valet','iniquus','aptus','ineptus','certus','incertus',\
	'dubius','licitus','illicitus','necessarius','aeque','certe','certo','dubie','dubio','necessarium','necessario','dubium','facultas','possibilitas',\
	'potestas','necessitas','necessitudo','probabilitas','forsitan','fortasse', 'forte','indubitate','indubitanter','necessarie',\
	'possibiliter','probabiliter']
#modal_lemmas_2=['aequum est','meum est','ius est','necesse est','opus est','usus est']
#specific check on aequum est and aequus est line 144
modal_lemmas_2a = ['meum','ius','necesse','opus','usus']
modal_lemmas_2b = ['sum']

#####################################################################
#
#	opens, reads and closes the conllu file in input
#
######################################################################
f = open (name_file)
#reads the whole file (maybe memory problem if the file is too big?)
read_data = f.read()
f.closed

#############################################
#
#	prepares variables
#
#############################################
#output file conllu with extracted sentences = 0
output_sentences_conllu = ""
#output file to elaborate the matrix = 0
output_sentences_str = ''
#number sentences with cooccurrence = or > 2 set on 0
n_output_sentences = 0
#number of sentences with co-occurrence = 1, 2, 3 or more set on 0
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
for i in range(len(sentences)): #range to have them as a number: it iterates the cycle from 0 to x (x=number of sentences). import sentences as a list. sentences are in one file. how many objects in the list? iterate for the number of objects
	sentence = sentences[i] #i=1

	cooccurrence = 0 #increase the counter about the number of modal lemmas found. variable gives number of lemmas
	
	#################################################
	#################################################
	sequence_form = ''
	list_lemmas_in_sentence = '' #strings
  
	###############################################################################################
	#
	#internal loop, looks for each lemma in modal_lemmas lists and increases the counter (=n. of cooccurrences)
	#
	###############################################################################################
	for j in range (len (sentence)): #number of words (sentence vs. sentences)
		token = sentence[j] #token comes from conllu library. sentence becomes a list
		#print (token["lemma"]) #check if it prints the lemmas. in token there are all the fields for each token in the conllu file. check how conllu library works
		
		#########################################################################
		#########################################################################
		#checks simple lemmas from modal_lemmas_1
		#########################################################################
		if (j != (len(sentence)-1)): #if the counter has not arrived to the end of the sentence yet 
			token_2 = sentence[j+1] #create token_2 (used in the control, not here)
		
		count_lemmas = modal_lemmas_1.count(token["lemma"]) #count checks if the lemma appears in the list. it can only appear once. (count is a list method)
		#print (token["lemma"],count_lemmas)
		cooccurrence = cooccurrence + count_lemmas #count =0 o =1
		
		####################################################
		#file lemmas_str for elaboration of matrix
		####################################################
		sequence_form = sequence_form + (token["form"] + ' ') #reconstructs the sentence + ' ' puts space between words (NB. space with punctuation too)
		list_lemmas_in_sentence = list_lemmas_in_sentence + (count_lemmas * (token["lemma"]+',')) #lemmas in cooccurrence. conta = 0 or = 1
		
		#######################################################
		#######################################################
		#check on compound modal lemmas 
		#######################################################
		if (modal_lemmas_2a.count(token["form"]) != 0): #NB take form and not lemma because i am interested in the expression "meum est"
#		print (token["form"])
			#if modal_lemmas_2a is the last token in the sentence list it does not check on modal_lemmas_2b
			if (j == (len(sentence)-1)): #if this is the last token (NB i had already checked if j is the last token in r. 114 j+1)
				break
			elif (modal_lemmas_2b.count(token_2["lemma"]) != 0):
				cooccurrence = cooccurrence + 1 #it could only be 1, but I could also use count_lemmas
				
				#########################################################################
				#########################################################################
				list_lemmas_in_sentence = list_lemmas_in_sentence + token["form"] + ' ' + token_2["lemma"] + ',' #sequence_form is updated
                
		#######################################################################
		#######################################################################
		#check on aequus: can be simple or compound
		#######################################################################
		if (token["lemma"]) == 'aequus': #token["lemma"] is elaborated here
			cooccurrence = cooccurrence + 1 #it is modal anyways so i increase the counter on co-occurrence
			
			if (j == (len(sentence)-1)):
				list_lemmas_in_sentence = list_lemmas_in_sentence + token["lemma"] + ','
			
			elif (token["form"]) == 'aequum' and (token_2["lemma"]) == 'sum':
				list_lemmas_in_sentence = list_lemmas_in_sentence + token["form"] + ' ' + token_2["lemma"] + ','
			else:
				list_lemmas_in_sentence = list_lemmas_in_sentence + token["lemma"] + ',' #do it even if it is not the last token
				
				
				

	#if at least 2 modal markers co-occur writes sentence in output file
	#serialize converts again the token list created by parse in conllu format
	if (cooccurrence >= 2):
		output_sentences_conllu = output_sentences_conllu + (sentence.serialize()) #
		n_output_sentences = n_output_sentences + 1 #for stats
		
		#############################################################################################
		#file lemmas_str
		#############################################################################################
		output_sentences_str = output_sentences_str + '#' + sequence_form[:-1] + '\n' + list_lemmas_in_sentence[:-1] + '\n' #sequence_form[:-1] takes out the final space + new line + list lemmas in sentence without comma
		
  
	if cooccurrence == 0:
		n_sentences_0l = n_sentences_0l + 1
	elif cooccurrence == 1:
		n_sentences_1l = n_sentences_1l + 1
	elif cooccurrence == 2:
		n_sentences_2l = n_sentences_2l + 1
	else:
		n_sentences_3l = n_sentences_3l + 1

#print (output_sentences_str)
#####################################################################
#
#	open, write and close lemmas_str for the matrix
#
######################################################################
#print (output_sentences)
name_file_no_extension = name_file[0:-7] #takes out .conllu from the file name
f = open(name_file_no_extension + '_output' + '.lemmas_str', 'w') #open file in write 'w' (for reading 'r')
#string_output_sentences = str(output_sentences)
f.write(output_sentences_str) #f is a name: this file. open file and write the output of extracted sentences
f.closed #closes the file

#####################################################################
#
#	open, write and close the conllu output file (contains conllu annotation of extracted sentences
#
######################################################################
#print (output_sentences)
name_file_no_extension = name_file[0:-7] #already done in r 189
f = open(name_file_no_extension + '_output' + '.conllu', 'w')
#string_output_sentences = str(output_sentences)
f.write(output_sentences_conllu)
f.closed

#####################################################################
#
#	open and write file csv with statistics. it is a dictionary. creates couples of value + separator (comma, tab or others) 
#
######################################################################
dict = {'Total number of sentences:                    ' : len(sentences), 'Sentences with 0 markers:        ' : n_sentences_0l, 'Sentences with 1 marker:        ' : n_sentences_1l,\
  'Sentences with 2 markers:        ' : n_sentences_2l, 'Sentences with 3 or more markers: ' : n_sentences_3l, 'Sentences with at least 2 co-occurring markers: ' :n_output_sentences}
w = csv.writer(open(name_file_no_extension+'_statistics'+'.csv', 'w')) #w is a name (as f)
for key, val in dict.items(): 
	w.writerow([key, val]) #write the row with key + value

#no need of closing the library
######################################################################
#
#	Output in terminal
#
######################################################################
print ('########################################################')
print ('#')
print ('# Total number of sentences:                   ', len(sentences))
print ('# Sentences with 0 markers:       ', n_sentences_0l)
print ('# Sentences with 1 marker:       ', n_sentences_1l)
print ('# Sentences with 2 markers:       ', n_sentences_2l)
print ('# Sentences with 3 or more markers:', n_sentences_3l)
print ('# Sentences with at least 2 co-occurring markers: ', n_output_sentences)
print ('#')
print ('# Output written on '+ name_file_no_extension + '_output' + '.conllu')
print ('#')
print ('# Output stats written on '+ name_file_no_extension + '_statistics' + '.csv')
print ('#')
print ('# Output file for the matrix written on ' + name_file_no_extension + '_output' + '.lemmi_str')
print ('#')
print ('########################################################')
