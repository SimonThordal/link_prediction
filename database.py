import MySQLdb as sql
db = sql.connect('localhost', 'root', 'root', 'enys')
court = 'cjeu'


def get_node_paragraphs(node, section):
    id_query = 'SELECT id FROM {}_cases WHERE case_true_id="{}" LIMIT 1'.format(court, node)
    crs = db.cursor()
    crs.execute(id_query)
    db_id = crs.fetchone()
    if db_id is None:
        raise Exception('No case found with id: {}'.format(node))
    case_query = 'SELECT paragraph_content FROM {}_paragraphs WHERE case_id="{}" and section_type="{}"'.format(court, db_id[0], section)
    crs.execute(case_query)
    data = crs.fetchall()
    return data

def get_node_section(node):
    data = get_node_paragraphs()
