from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from database import find_user,add_annotated_qp,fetch_one_qp, login
from qp_generator import generate_qp_pair

from model import Qp,Login

app = FastAPI()

origins=[
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post('/',tags=["root"])
async def read_root(cred:Login):
    print(1)
    login(cred.username,cred.password)
    print(4)
@app.get('/admin/find_users')
def find_users(username:str):
    return find_user(username)

@app.get('/admin/generate_qp')
def generate_qp():
    return generate_qp_pair()

@app.post('/annotate')
def annotate(qp:Qp):
    print(qp)
    return add_annotated_qp(qp.query,qp.product,qp.score,qp.created_at,qp.created_by)

@app.get('/randomqp')
def random_qp():   
    print(fetch_one_qp())

