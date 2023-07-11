from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import List
import uvicorn

from chatapp.database import SessionLocal, Base, engine
from chatapp.schemas import *
from chatapp.models import *
from chatapp.utils import generate_token, verify_token, authenticate, JWTBearer
app = FastAPI()
security = HTTPBasic()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Error handler


def error_handler(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(e)
            return {"error": str(e)}
    return wrapper
# API routes


@app.post('/users', tags=['Admin'])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    @error_handler
    def run():
        # Hash the password
        hashed_password = pwd_context.hash(user.password)
        db_user = User(username=user.username,
                       password_hash=hashed_password,
                       name=user.name,
                       profession=user.profession)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db_user.password_hash = None
        return db_user
    return run()


@app.put('/users/{user_id}', tags=['Admin'])
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    @error_handler
    def run():
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail='User not found')

        if user.password:
            db_user.password_hash = pwd_context.hash(user.password)
        if user.profession:
            db_user.profession = user.profession
        if user.name:
            db_user.name = user.name
        if user.name == 'admin':
            raise ValueError('name is not allowed')
        db.commit()
        db.refresh(db_user)
        db_user.password_hash = None
        return db_user
    return run()


@app.post('/auth/login', tags=['Users'])
def login(credentials: HTTPBasicCredentials, db: Session = Depends(get_db)):
    @error_handler
    def run():
        db_user = db.query(User).filter(
            User.username == credentials.username).first()
        if not db_user or not pwd_context.verify(credentials.password, db_user.password_hash):
            raise HTTPException(
                status_code=401, detail='Invalid username or password')
        jwt_token = generate_token(
            {'id': db_user.id, 'username': db_user.username})
        return {'message': 'Logged in successfully', 'token': jwt_token}
    return run()


@app.post('/auth/logout/{user_id}', tags=['Users'])
def logout(user_id):
    return {'message': 'Logged out successfully'}


@app.post('/groups', tags=['Users'], dependencies=[Depends(JWTBearer())])
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    @error_handler
    def run():
        db_group = Group(name=group.name)
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
        if group.members:
            for member in group.members:
                db.add(GroupMember(group_id=db_group.id, user_id=member))
        db.commit()
        grp = db.query(GroupMember).filter(
            GroupMember.group_id == db_group.id).all()
        return {'group_name': db_group.name, 'group_id': db_group.id, 'members': grp}
    return run()


@app.get('/groups', tags=['Users'], dependencies=[Depends(JWTBearer())])
def get_groups(db: Session = Depends(get_db), criterta=None, keyword=None):
    @error_handler
    def run():
        members = []
        groups = []
        if not criterta or criterta == "all":

            members = db.query(GroupMember).all()
            groups = db.query(Group).all()
            # print(members, groups)
        elif criterta == "name":
            groups = db.query(Group).filter(Group.name == keyword)
            members = db.query(GroupMember).filter(
                GroupMember.group_id.in_([grp.id for grp in list(groups)]))
        elif criterta == "username":
            user = db.query(User).filter(User.username == keyword).first()
            members = db.query(GroupMember).filter(
                GroupMember.user_id == user.id)
            groups = db.query(Group).filter(
                Group.id.in_([mbr.group_id for mbr in members]))
        response = {}
        for group in groups:
            response[group.id] = {'name': group.name, 'members': list()}
        # print(response)
        for member in members:
            response[member.group_id]['members'].append(member.user_id)
        # print(response)
        return response
    return run()


@app.delete('/groups/{group_id}', tags=['Users'], dependencies=[Depends(JWTBearer())])
def delete_group(group_id: int, db: Session = Depends(get_db)):
    @error_handler
    def run():
        db_group = db.query(Group).filter(Group.id == group_id).first()
        if not db_group:
            raise HTTPException(status_code=404, detail='Group not found')

        db.delete(db_group)
        db.commit()
        return {'message': 'Group deleted successfully'}
    return run()


def send_message():
    pass


if __name__ == '__main__':
    uvicorn.run(app)
