import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Input text
text = """
The cat is on the table
The table has a cat on it.
Tesla is owned by Elon Musk.
Elon Musk owns Tesla.
"""

# Process text
doc = nlp(text)

triplets = []

# Loop through each sentence
for sent in doc.sents:

    # Process each token
    for token in sent:

        # -----------------------------
        # ACTIVE VOICE
        # Example:
        # John bought a laptop
        # -----------------------------
        if token.pos_ == "VERB":

            subject = None
            obj = None

            # Find subject and object
            for child in token.children:

                # subject
                if child.dep_ in ("nsubj",):
                    subject = child.text

                # direct object
                if child.dep_ in ("dobj", "attr"):
                    obj = child.text

            # Save triplet
            if subject and obj:

                relation = token.lemma_

                triplets.append(
                    (subject, relation, obj)
                )

        # -----------------------------
        # PREPOSITION RELATIONS
        # Example:
        # Alice works at OpenAI
        # -----------------------------
        if token.pos_ == "VERB":

            subject = None

            # Find subject
            for child in token.children:

                if child.dep_ == "nsubj":
                    subject = child.text

                # Find preposition
                if child.dep_ == "prep":

                    prep = child.text

                    # Find object of preposition
                    for pobj in child.children:

                        if pobj.dep_ == "pobj":

                            relation = f"{token.lemma_}_{prep}"

                            triplets.append(
                                (subject, relation, pobj.text)
                            )

        # -----------------------------
        # PASSIVE VOICE
        # Example:
        # Tesla was founded by Elon Musk
        # -----------------------------
        if token.pos_ == "VERB":

            subject = None
            agent = None

            for child in token.children:

                # passive subject
                if child.dep_ == "nsubjpass":
                    subject = child.text

                # agent ("by")
                if child.dep_ == "agent":

                    for agent_obj in child.children:

                        if agent_obj.dep_ == "pobj":
                            agent = agent_obj.text

            if subject and agent:

                relation = token.lemma_ + "_by"

                triplets.append(
                    (subject, relation, agent)
                )

# Print results
print("\nExtracted Triplets:\n")

for triplet in triplets:
    print(triplet)