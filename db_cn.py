import mongodb
client = mongodb.client()
db = client.euchr_test
edge_col = db['edges']

def set_up_collection(name):
    """
    Set up a collection of edges for a named graph
    This will ensure that the fields edge, source and target exists, that edges are unique and there's an index on source
    """
    client = mongodb.client()
    db = client['edges']
    db.create_index('edge', unique=True)
    db.create_index('source')
    return db

def get_common_neighbors(x,y,G):
    try
    u = set(scoped_neighborhood(x,x,G))
    v = set(scoped_neighborhood(y,x,G))
    return u.intersection(v)

def get_precalculated(candidate_edges, field):
    pre_calculated = list(edge_col.find({'edge': {'$in': candidate_edges}}, {'source': True, 'target': True, field: True}))
    results = [(record['source'], record['target'], {'score': record[field]}) for record in pre_calculated]
    candidate_edges = list(set(candidate_edges) - set([(record['source'], record['target']) for record in pre_calculated]))
    return results, validation_set

def save_precalculated(records, field):
    records = [{'edge': (x,y), field: data['score']}]
    db.insert_many(records)

def common_neighbors(validation_set, G, weighting_scheme=None, recalculate=False):
    """
    Perform common neighbors scoring on a list of edges, backed by the database
    
    arguments:
    validation_set -- list of edges to score
    G -- digraph containing the nodes in the edges of the validation set
    
    returns:
    list of edges with score as an attribute
    """

    results = []
    if not recalculate:
        results, validation_set = get_precalculated(validation_set, 'common_neighbors')

    for non_edge in validation_set:
        x = non_edge[0]
        y = non_edge[1]
        cn = get_common_neighbors(x,y,G)
        if weighting_scheme and weighting_scheme.is_local():
            weights = []
            for z in cn:
                weights.append(weighting_scheme.score(z, x, G) * 1.0)
            s = sum(weights)
        else:
            s = len(cn)
        if weighting_scheme and weighting_scheme.is_global():
            s = s*weighting_scheme.score(x,y,G)
            non_edge[2]['score'] = s
            results.append(non_edge)
        else:
            results.append(s)

    save_precalculated(results, 'common_neighbors')
    return results
