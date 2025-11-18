# Flask CRUD Web Application

A simple yet functional web application built with Flask and SQLite for managing user data. This project demonstrates fundamental Create, Read, Update, and Delete (CRUD) operations with a clean, user-friendly interface.

## 📋 Features

- **Create**: Add new users with their details (name, email, age, city)
- **Read**: View all users and search through the user database
- **Update**: Edit existing user information
- **Delete**: Remove users from the database
- **Search**: Find users by name or email
- **Responsive Design**: Bootstrap-based responsive UI
- **Error Handling**: Custom error pages (404, 500)
- **Data Persistence**: SQLite database storage

## 🛠️ Tech Stack

- **Backend**: Flask 2.3.3
- **Database**: SQLite with Flask-SQLAlchemy ORM
- **Frontend**: HTML5, CSS, Bootstrap
- **Additional Libraries**: Flask-WTF (form handling and CSRF protection)

## 📁 Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── instance/             # Instance folder for database
│   └── exam_app.db      # SQLite database
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home/list users page
│   ├── add.html         # Add new user form
│   ├── update.html      # Update user form
│   ├── search.html      # Search results
│   ├── view.html        # View single user
│   ├── 404.html         # 404 error page
│   └── 500.html         # 500 error page
└── static/              # Static files (CSS, JS, images)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the repository**
   ```bash
   cd CICD_Security
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser and navigate to**
   ```
   http://localhost:5000
   ```

## 📖 Usage

### Home Page
- Displays all users in the database
- View user count and details
- Quick access to add, search, update, or delete users

### Add User
- Click "Add New User" button
- Fill in user details (first name, last name, email, age, city)
- Submit the form to create a new user

### Update User
- Click "Edit" next to a user
- Modify the desired fields
- Save changes

### Delete User
- Click "Delete" next to a user
- Confirm deletion (if prompted)
- User will be removed from the database

### Search
- Use the search functionality to find users by name or email
- View filtered results instantly

## 🔧 Configuration

Before running in production, update the following in `app.py`:

```python
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change to a secure key
```

Generate a secure key using:
```python
import secrets
print(secrets.token_hex(16))
```

## 📊 Database Schema

### User Table
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| first_name | String(50) | Not Null |
| last_name | String(50) | Not Null |
| email | String(120) | Unique, Not Null |
| age | Integer | Not Null |
| city | String(50) | Not Null |
| created_at | DateTime | Default: Current timestamp |

## 🔒 Security Notes

- Change the SECRET_KEY in production
- Use environment variables for sensitive configuration
- Enable CSRF protection (already configured with Flask-WTF)
- Validate and sanitize user inputs
- Consider adding authentication for multi-user scenarios

## 📝 Example Routes

- `GET /` - Home page, list all users
- `GET /add` - Show add user form
- `POST /add` - Create new user
- `GET /view/<id>` - View user details
- `GET /update/<id>` - Show update user form
- `POST /update/<id>` - Update user
- `GET /delete/<id>` - Delete user
- `GET /search` - Show search form
- `POST /search` - Perform search

## 🐛 Troubleshooting

### Database Issues
- Delete `instance/exam_app.db` and restart the app to reset the database
- Ensure the `instance/` directory has write permissions

### Port Already in Use
- The app runs on port 5000 by default
- To use a different port, modify `app.run(debug=True, port=5000)`

### Module Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

## 📚 Learning Resources

- [Flask Official Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap Documentation](https://getbootstrap.com/)

## 📄 License

This project is open-source and available for educational purposes.

## 👤 Author

Created as a learning project for Flask web development and CRUD operations.

---

**Happy Coding! 🚀**
