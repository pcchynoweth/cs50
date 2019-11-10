import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(("postgres://auwsrxnhxuewpn:8c87817b3d835ca88828ed61d64902a875ff4b7dfa105b2842f1016a2ccab0b1@ec2-174-129-253-53.compute-1.amazonaws.com:5432/derjiot5asaqtb"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    a_count = 1
    authors = {}
    f = open("books.csv")
    reader = csv.reader(f)
    l = next(reader)
    for isbn, title, author, year in reader:
        if author not in authors:
            authors[author] = a_count
            db.execute("INSERT INTO authors (id, author) VALUES (:id, :author)", {"id": a_count, "author": author})
            author_id = a_count
            a_count += 1
        else:
            author_id = authors[author]
        db.execute("INSERT INTO books (isbn, title, author_id, year) VALUES (:isbn, :title, :author_id, :year)", {"isbn": isbn, "title": title, "author_id": author_id, "year": year})
    db.commit()

if __name__ == "__main__":
    main()
