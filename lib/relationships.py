from sqlalchemy import ForeignKey, Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, relationship, validates
from level import *

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    results = relationship("Result", back_populates="user")

class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True)
    player_name = Column(String)
    score = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="results")

# if __name__ == "__main__":
engine = create_engine("sqlite:///flappy.db")
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
session = Session(engine)
#     taylor = User(name="Taylor")
#     first_game = Result(player_name="Taylor", score=0, user=taylor)
#     session.add_all([taylor, first_game])
#     session.commit()