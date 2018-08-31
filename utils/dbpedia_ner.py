from hdt import HDTDocument

DBPEDIA_RESOURCE_URI = "http://dbpedia.org/resource/{resource_name}"
DBPEDIA_ONTOLOGY_URI = "http://dbpedia.org/ontology/"

FR_DBPEDIA_RESOURCE_URI = "http://fr.dbpedia.org/resource/{resource_name}"

try:
    eng_dbpedia = HDTDocument("data_dumps/dbpedia/en/instance_type.hdt")
except RuntimeError:
    raise RuntimeError("DBpedia english dump not found: Put dbpedia dump into data_dumps/dbpedia/en/ folder")
try:
    fr_dbpedia = HDTDocument("data_dumps/dbpedia/fr/instance_type.hdt")
except RuntimeError:
    raise RuntimeError("DBpedia french dump not found: Put dbpedia dump into data_dumps/dbpedia/fr/ folder")


def entity_types_request(query, language='en'):
    if query:
        query = query.encode("utf-8")
        query = to_dbpedia_format(query)
        if language == 'fr':
            subject_query_fr = FR_DBPEDIA_RESOURCE_URI.format(resource_name=query)
            (triples, cardinality) = fr_dbpedia.search_triples(subject_query_fr, "", "")
        else:
            subject_query = DBPEDIA_RESOURCE_URI.format(resource_name=query)
            (triples, cardinality) = eng_dbpedia.search_triples(subject_query, "", "")
        classes = []
        for triple in triples:
            cl = triple[2]
            if "owl#Thing" not in cl:
                cl = cl.replace(DBPEDIA_ONTOLOGY_URI, '')
                classes.append(cl)
        if classes:
            return classes
    return None


def to_dbpedia_format(query):
    query = query.title()
    query = query.replace(' ', '_')
    return query
