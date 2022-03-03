from .. import models,schemas
from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter()

@router.get("/posts",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("select * from posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
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

# @router.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return post

@router.get("/posts/{id}",response_model=schemas.Post)
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

@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/posts/{id}",response_model=schemas.Post)
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