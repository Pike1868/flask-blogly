Overview
--------

"Blogly" is a blogging app to practice performing CRUD operations on user profiles. The application allows creating, reading, updating, and deleting users within a web interface. Each user has details such as first name, last name, and profile image.

Features
--------
-   Creates a new user with first name, last name, and profile image URL.
-   Displays a list of all users with links to their detailed view.
-   Shows detailed information about a specific user.
-   Allows editing and updating the user details.
-   Implements functionality to delete a user.
-   Includes Python backend tests for at least 4 routes.
-   Uses Flask Debug Toolbar for improved debugging.

Technologies Used
-----------------

-   Flask (Python web framework)
-   SQLAlchemy (Python SQL toolkit and ORM)
-   HTML/CSS
-   Flask Debug Toolbar
-   Python unittest for backend testing.

Installation
------------

The application requires psycopg2-binary and Flask-SQLAlchemy which can be installed using pip:

bashCopy code

`(env) $ pip install psycopg2-binary
(env) $ pip install flask-sqlalchemy`

Structure
---------

The application adopts Flask's Application Factory pattern to ensure a clean, maintainable, and scalable project structure. This was an area I was keen to learn about and implement to practice a typical Flask application structure.

The User model is defined in a models.py file. Routes are defined in a routes.py file. The HTML templates are located in a templates folder. The Flask application is created and configured in the __init__.py file, adhering to the Application Factory pattern. The application uses a PostgreSQL database for persistence.

Routes
------

The application includes the following routes:

-   GET /: Redirect to list of users.
-   GET /users: Show all users with links to their details and an add-user form.
-   GET /users/new: Show an add form for users.
-   POST /users/new: Process the add form, adding a new user and redirecting to /users.
-   GET /users/[user-id]: Show information about a given user with options to edit or delete the user.
-   GET /users/[user-id]/edit: Show the edit page for a user with options to save or cancel.
-   POST /users/[user-id]/edit: Process the edit form, updating the user and redirecting to /users.
-   POST /users/[user-id]/delete: Delete the user and redirect to /users.

Testing
-------

- Still working on tests :/