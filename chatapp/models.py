from .database import Base, engine
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from datetime import datetime
# Database Models


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    name = Column(String)
    password_hash = Column(String)
    profession = Column(String)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class GroupMember(Base):
    __tablename__ = 'group_members'
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    user_id = Column(Integer, ForeignKey('users.id'))


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    sent_by = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    likes = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.now())


Base.metadata.create_all(bind=engine)
