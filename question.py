from sqlalchemy import Column, Integer, String
from sqlalchemy.types import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_number = Column(String, nullable=False)
    question_text = Column(String, nullable=False)
    answers = Column(JSON, nullable=False)
    transcript = Column(String, nullable=False)

    def __repr__(self):
        title = f"{self.id}-{self.question_number}: {self.question_text}"
        option = f"\t{self.answers[0]}\n\t{self.answers[1]}\n\t{self.answers[2]}\n\t{self.answers[3]}"
        return f"{title}\n{option}"
