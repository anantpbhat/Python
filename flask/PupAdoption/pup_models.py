from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from PupAdoption import db, login_manager

class Puppy(db.Model):
    __tablename__ = 'puppies'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    owner: Mapped['Owner'] = relationship(back_populates="puppy")
    toys: Mapped[List['Toy']] = relationship(back_populates="puppy")

    def __init__(self, name):
        self.name = name

    def list_owner(self):
        if self.owner:
            return self.owner.name
        else:
            return "None"
        
    def list_toys(self):
        if self.toys:
            ltoys = []
            for Ty in self.toys:
                ltoys.append(Ty.item_name)
            return ";".join(ltoys)
        else:
            return "None"
        
    def __repr__(self):
        return f"Puppy name: {self.name}, Puppy ID: {self.id}, Puppy Owner: {self.list_owner()}, Puppy Toys: {self.list_toys()}"

class Owner(db.Model):
    __tablename__ = 'owners'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    puppy_id: Mapped[int] = mapped_column(ForeignKey("puppies.id"))
    puppy: Mapped['Puppy'] = relationship(back_populates="owner")

    def __init__(self, owner, puppy_id):
        self.name = owner
        self.puppy_id = puppy_id

class Toy(db.Model):
    __tablename__ = 'toys'
    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str]
    puppy_id: Mapped[int] = mapped_column(ForeignKey("puppies.id"))
    puppy: Mapped['Puppy'] = relationship(back_populates="toys")

    def __init__(self, item_name, puppy_id):
        self.item_name = item_name
        self.puppy_id = puppy_id

@login_manager.user_loader
def load_user(user_id):
    user = db.get_or_404(User, user_id)
    return user

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]

    def __init__(self, email, username, passwd):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(passwd, method='pbkdf2', salt_length=16)

    def check_password(self, passwd):
        return check_password_hash(self.password_hash, passwd)
    