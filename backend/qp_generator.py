from database import get_all_queries_products,add_qp


def generate_qp_pair():
    qp=get_all_queries_products()

    queries=qp['queries']
    products=qp['products']

    pair = [(q,p) for q in queries for p in products]

    for qp in pair:
        add_qp(qp)

    return pair