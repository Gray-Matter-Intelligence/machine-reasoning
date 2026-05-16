import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

text = """
The cat is on the table
The table has a cat on it.
Tesla is owned by Elon Musk.
Elon Musk owns Tesla.
"""

doc = nlp(text)
triplets = []

def get_full_phrase(token_text, sentence):
    token_text = token_text.strip()
    for chunk in sentence.noun_chunks:
        clean_chunk_text = chunk.text.lower().strip()
        if token_text in clean_chunk_text:
            words = [t.text.lower().strip() for t in chunk if t.pos_ not in ("DET", "PRON")]
            words = [w for w in words if w]
            return " ".join(words)
    return token_text

for sent in doc.sents:
    for token in sent:

        # PATTERN A: "is on"
        if token.pos_ == "AUX" and token.lemma_ == "be":
            subject, obj, relation = None, None, None
            for child in token.children:
                if child.dep_ == "nsubj": subject = child.text.lower().strip()
                if child.dep_ == "prep":
                    relation = child.text.lower().strip()
                    for gchild in child.children:
                        if gchild.dep_ == "pobj": obj = gchild.text.lower().strip()
            if subject and obj and relation:
                sub_p = get_full_phrase(subject, sent)
                obj_p = get_full_phrase(obj, sent)
                sorted_ents = sorted([sub_p, obj_p])
                triplets.append((sorted_ents[0], relation, sorted_ents[1]))

        # PATTERN B: "has a... on it"
        if token.pos_ == "VERB" and token.lemma_ == "have":
            subject, obj, relation = None, None, None
            for child in token.children:
                if child.dep_ == "nsubj": subject = child.text.lower().strip()
                if child.dep_ == "dobj":
                    obj = child.text.lower().strip()
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
                if child.dep_ in ("nsubj", "nsubjpass"): subject = child.text.lower().strip()
                if child.dep_ in ("dobj", "agent"):
                    if child.dep_ == "dobj": target = child.text.lower().strip()
                    else:
                        for gchild in child.children:
                            if gchild.dep_ == "pobj": target = gchild.text.lower().strip()
            if subject and target:
                sub_p = get_full_phrase(subject, sent)
                tar_p = get_full_phrase(target, sent)
                sorted_ents = sorted([sub_p, tar_p])
                triplets.append((sorted_ents[0], "own", sorted_ents[1]))

print("\nExtracted Normalized Triplets:\n")
for triplet in sorted(set(triplets)):
    print(triplet)
