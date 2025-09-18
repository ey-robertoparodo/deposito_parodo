import spacy
from spacy import displacy

nlp = spacy.load("it_core_news_sm")

testo = """Ieri Marco Rossi è partito da Milano con un volo Alitalia diretto a New York, dove visiterà la sede delle Nazioni Unite e andrà al Metropolitan Museum of Art per vedere la collezione di dipinti di Van Gogh."""

doc = nlp(testo)

displacy.serve(doc, style="dep", port=8654, host="127.0.0.1")