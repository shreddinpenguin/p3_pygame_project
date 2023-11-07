from sqlalchemy import ForeignKey, Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, relationship, validates

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    high_score = Column(Integer)
    results = relationship("Result", back_populates="player")

class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True)
    player_name = Column(String)
    score = Column(Integer)
    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="results")

if __name__ == "__main__":
    engine = create_engine("sqlite:///pyguy.db")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        taylor = Player(name="Taylor", high_score=0)
        first_game = Result(player_name="Taylor", score=0, player=taylor)
        session.add_all([taylor, first_game])
        session.commit()