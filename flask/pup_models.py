from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from typing import List
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_file = str('sqlite:///' + basedir + 'pup_data.sqlite')
engine = create_engine(db_file, echo=True)

Base = declarative_base()

class Puppy(Base):
    __tablename__ = 'puppies'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    owner: Mapped["Owner"] = relationship(back_populates="puppy")
    toys: Mapped[List["Toy"]] = relationship(back_populates="puppy")

    def __init__(self, name):
        self.name = name

    def list_owner(self):
        if self.owner:
            return self.owner.name
        else:
            return "None"
        
    def list_toys(self):
        if self.toys:
            for Ty in self.toys:
                return Ty.item_name.replace(',', ';')
        else:
            return "None"
        
    def __repr__(self):
        return f"Puppy name: {self.name}, Puppy ID: {self.id}, Puppy Owner: {self.list_owner()}, Puppy Toys: {self.list_toys()}"

class Owner(Base):
    __tablename__ = 'owners'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    puppy_id: Mapped[int] = mapped_column(ForeignKey("puppies.id"))
    puppy: Mapped["Puppy"] = relationship(back_populates="owner")

    def __init__(self, owner, puppy_id):
        self.name = owner
        self.puppy_id = puppy_id

class Toy(Base):
    __tablename__ = 'toys'
    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str]
    puppy_id: Mapped[int] = mapped_column(ForeignKey("puppies.id"))
    puppy: Mapped["Puppy"] = relationship(back_populates="toys")

    def __init__(self, item_name, puppy_id):
        self.item_name = item_name
        self.puppy_id = puppy_id
        