# ISSUE: https://github.com/Gray-Matter-Intelligence/machine-reasoning/issues/2

from ..utils.wikidata_intf import search_entity, get_entity, get_typeof
from ..utils.sbert_dist import sbert_embeddings, nearest_vector
from ..core.models import KnowledgeTripletItem

def normalize_entity(self, item: str):
    # Convert to lowercase
    item = item.lower()

    # Wikidata API to look-up terms and map to standard ontology: https://towardsdatascience.com/extract-knowledge-from-text-end-to-end-information-extraction-pipeline-with-spacy-and-neo4j-502b2b1e0754
    try:
        # Search item in wikidata
        data = search_entity(item)

        if 'search' in data and len(data['search']) > 0:
            # First do an exact text match in labels from qurry result
            q_lbls = [d['label'].lower() for d in data['search']]
            if item in q_lbls:
                best_match = q_lbls.index(item)
            else:
                # TODO: Is it predictable?
                # Find closest match between various labels from search results and item
                embs = sbert_embeddings([item] + q_lbls)
                best_match = nearest_vector(embs[0], embs[1:])

            entity = data['search'][best_match]

            # TODO: How to select type from inst_of / subclass_of?
            inst_of = get_typeof(entity['id'])
            if len(inst_of) > 0:
                inst_of = get_entity(','.join(inst_of))

            subclass_of = get_typeof(entity['id'], subclass=True)
            if len(subclass_of) > 0:
                subclass_of = get_entity(','.join(subclass_of))

            return KnowledgeTripletItem(
                item=entity['label'],
                info=entity['description'],
                url=entity['concepturi'],
                type_=inst_of
            )
        else:
            return KnowledgeTripletItem(item=item)
    except:
        return KnowledgeTripletItem(item=item)