import spacy
import coreferee

# Load model and add coreferee to the pipeline
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("coreferee")

text = """
Elon Musk owns Tesla. He is a billionaire. 
The cat is on the table. It has a tail.
"""

doc = nlp(text)

def get_resolved_token(token):
    # Check if the token is part of a coreference chain
    chain = doc._.coref_chains.resolve(token)
    if chain:
        # Returns the first/main mention (e.g., "Elon Musk" instead of "He")
        return " ".join([t.text for t in chain]).lower()
    return token.text.lower()

triplets = []

for sent in doc.sents:
    for token in sent:
        # Pattern: Ownership
        if token.pos_ == "VERB" and token.lemma_ == "own":
            subject, target = None, None
            for child in token.children:
                if child.dep_ in ("nsubj", "nsubjpass"):
                    # Resolve "He" -> "Elon Musk"
                    subject = get_resolved_token(child)
                if child.dep_ in ("dobj", "agent"):
                    if child.dep_ == "dobj":
                        target = get_resolved_token(child)
                    else:
                        for gchild in child.children:
                            if gchild.dep_ == "pobj":
                                target = get_resolved_token(gchild)
            
            if subject and target:
                triplets.append((subject, "own", target))

print("Extracted Triplets:")
for t in set(triplets):
    print(t)
