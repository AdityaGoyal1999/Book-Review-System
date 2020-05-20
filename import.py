import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://wulnronkubqzoy:33880c816471a23ae0fb3ccf19871e1f52f8dbe9f0102c57d479c39b706e923e@ec2-52-87-135-240.compute-1.amazonaws.com:5432/d9i2hu0qmbc0jm")
db = scoped_session(sessionmaker(bind=engine))

def main():
    with open('books.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        next(csv_reader)
        for row in csv_reader:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn": row[0], "title": row[1], "author": row[2], "year": row[3]})
            db.commit()
            line_count += 1
        print("\n\nLines counted", line_count)


if __name__ == "__main__":
    main()