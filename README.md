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

### Users

-   `GET /`: Redirect to a list of recent posts.
-   `GET /users`: Show all users with links to their details.
-   `GET /users/new`: Show a form to add a new user.
-   `POST /users/new`: Process the add form, adding a new user and redirecting to `/users`.
-   `GET /users/[user-id]`: Show information about a given user with options to edit or delete the user and a list of the user's posts.
-   `GET /users/[user-id]/edit`: Show the edit page for a user with options to save or cancel.
-   `POST /users/[user-id]/edit`: Process the edit form, updating the user and redirecting to `/users`.
-   `POST /users/[user-id]/delete`: Delete the user and redirect to `/users`.

### Posts

-   `GET /users/[user-id]/posts/new`: Show a form to add a new post for a specific user.
-   `POST /users/[user-id]/posts/new`: Process the add form, add a new post and redirect to the user's detail page.
-   `GET /posts/[post-id]`: Show details about a single post.
-   `GET /posts/[post-id]/edit`: Show a form to edit a specific post.
-   `POST /posts/[post-id]/edit`: Handle editing of a post and redirect back to post detail view.
-   `POST /posts/[post-id]/delete`: Delete a post and redirect to the user's detail page.


Testing
-------

The application includes unit tests for both the models and the routes. These tests ensure the correct functioning of the User model and the CRUD operations implemented in the routes.

In the `ModelsTests` class:

-   `test_create_user`: This test ensures that a user can be created and saved in the database.
-   `test_delete_user`: This test ensures that a user can be deleted from the database.
-   `test_full_name`: This test ensures the correct functionality of the `get_full_name` method of the User model.

In the `RouteTests` class:

-   `test_home_page`: This test ensures that the home page can be retrieved and contains the correct HTML.
-   `test_users_form`: This test ensures that the form for adding a new user can be retrieved and contains the correct HTML.
-   `test_show_user`: This test ensures that the page for a specific user can be retrieved and contains the correct HTML.
-   `test_add_user`: This test ensures that a new user can be added through the web interface.
-   `test_edit_user`: This test ensures that an existing user's information can be edited through the web interface.
-   `test_delete_user`: This test ensures that an existing user can be deleted through the web interface.