import stanza
from stanza.utils.conll import CoNLL
# stanza.download(lang='la', package='perseus')
nlp = stanza.Pipeline(lang="la", package='ittb')
input = open('phormio.txt', 'r') #input function prompts the user: in this case it asks the text to annotate. The open() function opens a file, and returns it as a file object. The syntax is open(file, mode)
doc = input.read()
results = nlp(doc)
#print(results)

mylist = results.to_dict()
myconll = CoNLL.convert_dict(mylist)
oufi = "phormio_annotated.txt"

with open(oufi, mode="w") as f:
    for sent in myconll:
        for token in sent:
            print(*token, sep="\t", file=f)
        print("\n", file=f)
