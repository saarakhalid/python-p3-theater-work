from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    character_name = Column(String)

    @property
    def auditions(self):
        return [audition for audition in self.role_auditions]

    @property
    def actors(self):
        return [audition.actor for audition in self.role_auditions]

    @property
    def locations(self):
        return [audition.location for audition in self.role_auditions]

    def lead(self):
        hired_audition = next((audition for audition in self.role_auditions if audition.hired), None)
        return hired_audition.actor if hired_audition else "no actor has been hired"

    def understudy(self):
        hired_auditions = [audition for audition in self.role_auditions if audition.hired]
        return hired_auditions[1].actor if len(hired_auditions) > 1 else "no actor has been hired as understudy"


class Audition(Base):
    __tablename__ = "auditions"
    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(Integer)
    hired = Column(Boolean)
    role_id = Column(Integer, ForeignKey('roles.id'))

    def call_back(self):
        self.hired = True