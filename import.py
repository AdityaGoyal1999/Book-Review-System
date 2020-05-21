import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://jbuimiitaijunf:5e006a287d39930d2922e0a6bdaf1a9e69b73547a92f13f272307a2016d9cf68@ec2-34-200-15-192.compute-1.amazonaws.com:5432/dbm2hr587tr7rj")
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
        print("\nLines counted", line_count)


if __name__ == "__main__":
    main()