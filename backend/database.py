import os
import random

from dotenv import load_dotenv,find_dotenv
from pymongo import MongoClient

load_dotenv(find_dotenv())

connection_string=os.environ.get("MONGODB_URL")

client=MongoClient(connection_string)
database=client.product_annotator

user_collection=database.user_cred
qp_collection=database.query_product_pairs
annotated_qp_collection=database.annotated_qp
randomized_qp_collection=database.randomized_qp

def login(username,password):
    users=user_collection.find()
    print(users)
    for user in users:
        if username==user['username']:
            if password==user['password']:
                return {'data':f"{username} is present"} 
            else :
                return {'message':"incorrect password"}
        else :
                return {'message':"incorrect username"}   
    return 0
def insert_queries_products():
    doc={
        "query":['Jacket','Cargo','Shoes','Jeans','Hoodie'],
        "product":['Yellow Winter Coat For Women',
                "Men's Multi-colored Cotton Camouflage Printed Cargo","Solid Black Casual Shoes","Women Blue Jean",
                "Cute Printed Hoodie Sweatshirt"]
    }
    inserted_id=qp_collection.insert_one(doc).inserted_id
    print(inserted_id)

# insert_doc()

def admin_add_user(username,password):
    doc={
        "username":username,
        "password":password
    }
    inserted_id=user_collection.insert_one(doc).inserted_id
    print(inserted_id)

# admin_add_user('zevi_admin','zevi')

def find_user(username):
    collections=user_collection
    users=collections.find()
    print(users)
    for user in users:
        # print(user['username'])
        if username==user['username']:
            return {'data':f"{username} present"}
    
    return {'data':f"{username} not present"}
    # print(list(users))

def get_all_queries_products():
    qp=qp_collection.find()
    queries_buffer=[]
    products_buffer=[]
    for i in qp:
        queries=i['query']
        for q in queries:
            if q not in queries_buffer:
                queries_buffer.append(q)
        products=i['product']
        for p in products:
            if p not in products_buffer:
                products_buffer.append(p)

    return {'queries':queries_buffer,'products':products_buffer} 

def add_qp(qp):
    q=qp[0]
    p=qp[1]
    doc={
        "query":q,
        "product":p
    }
    if randomized_qp_collection.count_documents({'query': q, "product": p}) > 0:
        print('exists')
        pass
    else:
        inserted_id=randomized_qp_collection.insert_one(doc).inserted_id
        print(inserted_id)

def fetch_one_qp():
    qps=randomized_qp_collection.find() 
    print(1)
    r=random.randint(0, randomized_qp_collection.count_documents({}))
    print(2)
    return qps[r]

def remove_qp(q,p):
    if randomized_qp_collection.count_documents({'query': q, "product": p}) > 0:
        print('removing...')
        randomized_qp_collection.delete_one({"query":q,"product":p}) 


def add_annotated_qp(q,p,score,created_at,user):
    doc={
        "query":q,
        "product":p,
        "score":score,
        "created_at":created_at,
        "created_by":user
    }
    if annotated_qp_collection.count_documents({'query': q, "product": p})>0:
        return {'message':'already exists'}
    else:
        inserted_id=annotated_qp_collection.insert_one(doc).inserted_id
        print(inserted_id)
        remove_qp(q,p)
        return {'message':"added","data":doc}


