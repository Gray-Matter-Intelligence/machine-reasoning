import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

text = """
The book is on the desk.
The desk has a book on it.
A coffee mug is on the laptop.
The laptop has a coffee mug on it.
The lamp is on the nightstand.
The nightstand has a lamp on it.
An apple is on the plate.
The plate has an apple on it.
The key is on the key ring.
The key ring has a key on it.
Tesla is owned by Elon Musk.
Elon Musk owns Tesla.
The space company is owned by Elon Musk.
Elon Musk owns the space company.
The luxury villa is owned by an artist.
An artist owns the luxury villa.
The rocket company is owned by Jeff Bezos.
Jeff Bezos owns the rocket company.
The ancient castle is owned by a duke.
A duke owns the ancient castle.
"""

doc = nlp(text)
triplets = []

# FIX: Expect the spaCy Token object instead of a text string
def get_full_phrase(token_obj, sentence):
    for chunk in sentence.noun_chunks:
        # Check if the specific token index falls inside the noun chunk boundaries
        if chunk.start <= token_obj.i < chunk.end:
            words = [t.text.lower().strip() for t in chunk if t.pos_ not in ("DET", "PRON")]
            words = [w for w in words if w]
            return " ".join(words)
    return token_obj.text.lower().strip()

for sent in doc.sents:
    for token in sent:

        # PATTERN A: "is on"
        if token.pos_ == "AUX" and token.lemma_ == "be":
            subject, obj, relation = None, None, None
            for child in token.children:
                if child.dep_ == "nsubj": subject = child # FIX: Keep as token object
                if child.dep_ == "prep":
                    relation = child.text.lower().strip()
                    for gchild in child.children:
                        if gchild.dep_ == "pobj": obj = gchild # FIX: Keep as token object
            if subject and obj and relation:
                sub_p = get_full_phrase(subject, sent)
                obj_p = get_full_phrase(obj, sent)
                sorted_ents = sorted([sub_p, obj_p])
                triplets.append((sorted_ents[0], relation, sorted_ents[1]))

        # PATTERN B: "has a... on it"
        if token.pos_ == "VERB" and token.lemma_ == "have":
            subject, obj, relation = None, None, None
            for child in token.children:
                if child.dep_ == "nsubj": subject = child # FIX: Keep as token object
                if child.dep_ == "dobj":
                    obj = child # FIX: Keep as token object
                    for gchild in child.children:
                        if gchild.dep_ == "prep": relation = gchild.text.lower().strip()
            if subject and obj and relation:
                sub_p = get_full_phrase(subject, sent)
                obj_p = get_full_phrase(obj, sent)
                sorted_ents = sorted([sub_p, obj_p])
                triplets.append((sorted_ents[0], relation, sorted_ents[1]))

        # PATTERN C & D: Ownership (Active & Passive)
        if token.pos_ == "VERB" and token.lemma_ == "own":
            subject, target = None, None
            for child in token.children:
                if child.dep in (spacy.symbols.nsubj, spacy.symbols.nsubjpass) or child.dep_ in ("nsubj", "nsubjpass"): 
                    subject = child # FIX: Keep as token object
                if child.dep_ in ("dobj", "agent"):
                    if child.dep_ == "dobj": 
                        target = child # FIX: Keep as token object
                    else:
                        for gchild in child.children:
                            if gchild.dep_ == "pobj": target = gchild # FIX: Keep as token object
            if subject and target:
                sub_p = get_full_phrase(subject, sent)
                tar_p = get_full_phrase(target, sent)
                sorted_ents = sorted([sub_p, tar_p])
                triplets.append((sorted_ents[0], "own", sorted_ents[1]))

print("\nExtracted Normalized Triplets:\n")
for triplet in sorted(set(triplets)):
    print(triplet)

# Extracted Normalized Triplets:
# 
# ('ancient castle', 'own', 'duke')
# ('apple', 'on', 'plate')
# ('artist', 'own', 'luxury villa')
# ('book', 'on', 'desk')
# ('coffee mug', 'on', 'laptop')
# ('elon musk', 'own', 'space company')
# ('elon musk', 'own', 'tesla')
# ('jeff bezos', 'own', 'rocket company')
# ('key', 'on', 'key ring')
# ('lamp', 'on', 'nightstand')
 