# Project 1

Web Programming with Python and JavaScript

The webapp is created with giving user the utmost priority and ease.

1. The users can register to the webapp by entering their name, unique username, password.
2. Once the user has registered, they can login using their username and password.
3.
4. import.py is used to enter all the book's info into the PostgreSQL database hosted on heroku called books for this app.
5. The user can search the books in the database using Author, Title, ISBN, Year. The searched query can be case insensitive and does not have to be exactly the name of the book/author/isbn/year. Then the user is directed to a page with all the book names.
6. User can select the book name and will be lead to a different page, specific to the book. There the user can see book's info - title, author, year, isbn, rating, no. of people who rated the book. Moreover, the user can write a review of the book and give it ratings from 1-5 (5 being the best)
7. The average rating at large is coming from the Goodreads data but as reviews are added with ratings in the app, it displays the accurate aggregate ratings.
8. Developers can beenefit from this website as they will be able to get the api for a book's latest info by making a GET request to the website's route at /api/<isbn>

Credits:

Wallpaper
Goodreads API
Database for heroku

TODO:
1. Readme
2. About page
3. Naming convention