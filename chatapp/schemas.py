from pydantic import BaseModel
from typing import Optional, List

# Schemas


class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    profession: Optional[str] = None


class UserUpdate(BaseModel):
    password: Optional[str] = None
    name: Optional[str] = None
    profession: Optional[str] = None


class Login(BaseModel):
    username: str
    password: str


class Logout(BaseModel):
    username: str


class GroupCreate(BaseModel):
    name: str
    members: Optional[List[str]] = []


class AddMember(BaseModel):
    grp_id: str
    members: list


class SearchGroup(BaseModel):
    criteria: str
    keyword: str


class SendMessage(BaseModel):
    content: str
    grp_id: str


class LikeMessage(BaseModel):
    msg_id: str
