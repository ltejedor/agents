import spacy
nlp = spacy.load('en_core_web_sm')

doc = nlp("Nagal won the first set.")

for tok in doc:
  print(tok.text, "...", tok.dep_)