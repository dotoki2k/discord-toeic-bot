import os
import json
import copy
from question import Question


def check_data_is_exist(session):
    result = session.query(Question).first() is not None
    return result


def insert_data_to_db(session):
    if check_data_is_exist(session):
        print("The database already exists")
        return None
    print("Inserting data ...")
    directory = "./data"
    count = 0
    for file in os.scandir(directory):
        list_questions = []
        with open(file.path, "r") as rf:
            data = json.load(rf)
        for v in data.values():
            for obj in v.values():
                q = Question(
                    question_number=obj["question_number"],
                    question_text=obj["question_text"],
                    transcript=obj["transcript"],
                    answers=obj["answers"],
                )
                list_questions.append(q)
        count += len(list_questions)
        session.add_all(list_questions)
        session.commit()
    print(f"total question: {count}")


def fetch_data(session):
    """Fetch 5 rows data from database and remove it."""
    questions = session.query(Question).limit(5).all()
    new = copy.deepcopy(questions)
    for q in questions:
        session.delete(q)
    session.commit()
    return new
