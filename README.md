# Project 1

Web Programming with Python and JavaScript

This project is a full stack web app with FrontEnd in HTML, CSS(with Boostrap 4); Backend in Python(Flask) and Database in PostgreSQL(Heroku). It is a book review system where the user can review 5000 english books. Moreover, it utilizes third party API provided by Goodreads(https://www.goodreads.com/api).

The webapp is created with giving user the utmost priority and ease. The project also contains comments when necessary for communicating with a fellow developer. 
Moreover, before running the project, developers should run ``` pip3 install -r requirements.txt ``` to download necessary packages of FLASK and SQLAlcehmy.


The project's database has 3 tables - 
1. users - for storing login info
2. books - for storing info of 5000 books
3. book-reviews - for storing reviews given by the users via. this webapp

FILES-
1. import.py
2. application.py
3. welcome.py
4. login.html
5. search.html
6. books.html
7. book.html
8. message.html
9. layout.html
10. loggedInLayout.html
11. base.css
12. book.css, books.css, login.css, search.css, welcome.css

Broad functions of the project-
1. The users can register to the webapp by entering their name, unique username, password.
2. Once the user has registered, they can login using their username and password.
3. At any time after logging in/ Signign up, the user can log out and their changes will be saved.
4. ``` import.py ``` is used to enter all the book's info into the PostgreSQL database from ``` books.csv ``` hosted on heroku.
5. The user can search the books in the database using Author, Title, ISBN, Year. The searched query can be case insensitive and does not have to be exactly same as the name of the book/author/isbn/year. Following search, the user is directed to a page with all the book names.
6. User can select the book name and will be lead to a different page, specific to the book. There the user can see book's info - title, author, year, isbn, rating, no. of people who rated the book. Moreover, the user can write a review of the book and give it ratings from 1-5 (5 being the best)
7. The average rating at large is coming from the Goodreads data but as reviews are added with ratings in the app, it displays the accurate aggregate ratings.
8. Developers can beenefit from this website as they will be able to get the api for a book's latest info by making a GET request to the website's route at ``` /api/<isbn> ```

Credits:

Goodreads API
Database - heroku

TODO:
1. Readme
2. Session