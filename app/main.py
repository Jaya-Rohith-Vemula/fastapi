from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from passlib.context import CryptContext
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='password',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection successfull!")
        break
    except Exception as error:
        print("Connectoin to database failed due to ", error)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content":"content of post 1","id":1},
            {"title": "favorite food", "content":"i like pizza", "id":2}]

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i

@app.get("/")
def root():
    return {"message": "Welcome to API!!!"}

@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("select * from posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute(""" insert into posts (title, content, published) values (%s,%s,%s) returning * """,
    #                 (post.title, post.content, post.published) )
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return post

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id:int,response:Response,db: Session = Depends(get_db)):
    # cursor.execute(""" select * from posts where id= %s """,(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:   #if response=404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id: {id} was not found"}
    return post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db)):
    # cursor.execute(""" delete from posts where id= %s returning * """,(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # if deleted_post==None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} does not exists")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exists")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" update posts set title = %s, content = %s, published = %s where id = %s returning *""",
    #                 (post.title, post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exists")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def creat_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash the password
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user