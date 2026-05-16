# ISSUE: https://github.com/Gray-Matter-Intelligence/machine-reasoning/issues/1

# OPEN: Can https://github.com/Gray-Matter-Intelligence/machine-reasoning/issues/7 also be done in this functionality itself?

from typing import List

from transformers import pipeline

class KnowledgeExtractor:
    # TODO: Add language param
    def __init__(self) -> None:
        self.rebel = None

    def load_babel(self):
        # Babel for text to entity, relation triples: https://huggingface.co/Babelscape/rebel-large
        self.rebel = pipeline('text-generation', model='Babelscape/rebel-large', tokenizer='Babelscape/rebel-large'
    def run_babel(self, text: str):
        # We need to use the tokenizer manually since we need special tokens.
        extracted_text = self.rebel.tokenizer.batch_decode([self.rebel(text, return_tensors=True, return_text=False)[0]["generated_token_ids"]])
        # print(extracted_text[0])
        return extracted_text

        # Parse the generated text and extract the triplets

    def babel_extract_2_triple(self, text: str):
        triplets = []
        relation, subject, relation, object_ = '', '', '', ''
        text = text.strip()
        current = 'x'
        for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
            if token == "<triplet>":
                current = 't'
                if relation != '':
                    triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
                    relation = ''
                subject = ''
            elif token == "<subj>":
                current = 's'
                if relation != '':
                    triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
                object_ = ''
            elif token == "<obj>":
                current = 'o'
                relation = ''
            else:
                if current == 't':
                    subject += ' ' + token
                elif current == 's':
                    object_ += ' ' + token
                elif current == 'o':
                    relation += ' ' + token
        if subject != '' and relation != '' and object_ != '':
            triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
        return triplets
    
engine = KnowledgeExtractor()

# Load and Run Babel
engine.load_babel()

texts = ["Eiffel Tower is located in Paris",
         "Punta Cana is a resort town in the municipality of Higuey, in La Altagracia Province, the eastern most province of the Dominican Republic",
         "Dog is a mammal",
         "Cleopatra was very beautiful",
         "Mahatma Gandhi was born on 2nd October"]

result = {}
for text in texts:
    result[text] = engine.extract(text)

print('done')