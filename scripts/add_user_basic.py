"""
Script to add 4 users to the Flask CRUD application database
Adds students from FAST NUCES with their information
"""

import sys
from pathlib import Path

# Add parent directory to path to import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app, db, User


def add_users():
    """
    Add 4 users to the database with the following information:
    1. Fassih ul Hassny - i221730@nu.edu.pk - 21 - Lahore
    2. Hunain Raza - i221614@nu.edu.pk - 22 - Karachi
    3. Ahmed Umar - i221580@nu.edu.pk - 22 - Rawalpindi
    4. Abdul Munim - i227425@nu.edu.pk - 22 - Islamabad
    """

    # User data to add
    users_data = [
        {"first_name": "Fassih", "last_name": "ul Hassny", "email": "i221730@nu.edu.pk", "age": 21, "city": "Lahore"},
        {"first_name": "Hunain", "last_name": "Raza", "email": "i221614@nu.edu.pk", "age": 22, "city": "Karachi"},
        {"first_name": "Ahmed", "last_name": "Umar", "email": "i221580@nu.edu.pk", "age": 22, "city": "Rawalpindi"},
        {"first_name": "Abdul", "last_name": "Munim", "email": "i227425@nu.edu.pk", "age": 22, "city": "Islamabad"},
    ]

    # Create application context
    with app.app_context():
        print("Starting to add users to database...")
        print("=" * 60)

        added_count = 0
        skipped_count = 0

        for user_data in users_data:
            # Check if user already exists
            existing_user = User.query.filter_by(email=user_data["email"]).first()

            if existing_user:
                print(
                    f"⚠️  User already exists: {user_data['first_name']} {user_data['last_name']} ({user_data['email']})"
                )
                skipped_count += 1
            else:
                # Create new user
                new_user = User(
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    email=user_data["email"],
                    age=user_data["age"],
                    city=user_data["city"],
                )

                try:
                    # Add user to database
                    db.session.add(new_user)
                    db.session.commit()

                    print(
                        f"✅ Added: {user_data['first_name']} {user_data['last_name']} ({user_data['email']}) - Age: {user_data['age']}, City: {user_data['city']}"
                    )
                    added_count += 1

                except Exception as e:
                    db.session.rollback()
                    print(f"❌ Error adding {user_data['first_name']} {user_data['last_name']}: {str(e)}")

        print("=" * 60)
        print(f"Summary: {added_count} users added, {skipped_count} users skipped (already exist)")
        print("\n✅ Script completed successfully!")


if __name__ == "__main__":
    add_users()
