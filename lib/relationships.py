from sqlalchemy import ForeignKey, Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, relationship, validates
# from level import *

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
with Session(engine) as session:
    pass
    # taylor = User(name="Taylor")
    # sam = User(name="Sam")
    # danny = User(name="Danny")
    # first_game = Result(player_name="Sam", score=37, user=taylor)
    # second_game = Result(player_name="Taylor", score=1337, user=taylor)
    # third_game = Result(player_name="Danny", score=38, user=taylor)
    # session.add_all([taylor, sam, danny, first_game, second_game, third_game])
    # session.commit()