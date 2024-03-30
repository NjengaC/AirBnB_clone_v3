#!/usr/bin/python3
""" State Module for HBNB project """
import models
from sqlalchemy.orm import declarative_base, relationship
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
import shlex
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete,\
                          delete-orphan', backref="state")
    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            curr = models.storage.all()
            lists = []
            res = []
            for key in curr:
                city = key.replace('.', ' ')
                city = shlex.split(city)
                if (city[0] == 'City'):
                    lists.append(curr[key])
            for lis in lists:
                if (lis.state_id == self.id):
                    res.append(lis)
            return (res)

#    if getenv("HBNB_TYPE_STORAGE") == "db":
