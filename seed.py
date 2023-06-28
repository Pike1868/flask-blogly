from app import create_app
from app.models import User, db

# Create the Flask app
app = create_app()


# Create the database tables
with app.app_context():
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()

    # Add test users
    users_data = [
        {'first_name': 'John', 'last_name': 'Doe'},
        {'first_name': 'Jane', 'last_name': 'Smith'},
        {'first_name': 'Alice', 'last_name': 'Johnson'},
        {'first_name': 'Bob', 'last_name': 'Brown'},
    ]

    for user_data in users_data:
        user = User(**user_data)
        db.session.add(user)

    db.session.commit()
