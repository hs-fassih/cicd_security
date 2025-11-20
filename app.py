# FLASK CRUD WEB APPLICATION
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'  # TODO: Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    """
    User model for the application
    
    Fields:
    - id: Primary key (auto-increment)
    - first_name: User's first name (required)
    - last_name: User's last name (required)
    - email: User's email (unique, required)
    - age: User's age (required)
    - city: User's city (required)
    - created_at: Timestamp when user was created
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<User {self.id}: {self.first_name} {self.last_name}>"

# Routes

@app.route('/')
def index():
    """
    Home page - Display all users
    
    TODO: Implement the following:
    1. Query all users from database
    2. Pass users to template
    3. Handle case when no users exist
    """
    # Get all users from database
    users = User.query.all()
    
    # Pass users to template (template will handle empty list case)
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    """
    Add new user
    
    GET: Display form to add user
    POST: Process form data and create new user
    
    TODO: Implement the following:
    1. Handle GET request - render add form
    2. Handle POST request - process form data
    3. Validate form data
    4. Create new user object
    5. Add to database
    6. Handle errors (duplicate email, validation errors)
    7. Redirect to home page on success
    """
    if request.method == 'POST':
        # Get form data from request
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        age = request.form.get('age')
        city = request.form.get('city')
        
        # Validate form data updated by ahmed
        if not all([first_name, last_name, email, age, city]):
            flash('All fields are required!', 'error')
            return render_template('add.html')
        
        # Check if age is a valid number
        try:
            age = int(age)
            if age <= 0 or age > 150:
                flash('Please enter a valid age (1-150)!', 'error')
                return render_template('add.html')
        except ValueError:
            flash('Age must be a valid number!', 'error')
            return render_template('add.html')
        
        # Check if email is unique
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists! Please use a different email.', 'error')
            return render_template('add.html')
        
        try:
            # Create new user object
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                age=age,
                city=city
            )
            
            # Add user to database
            db.session.add(new_user)
            db.session.commit()
            
            # Add success message
            flash('User added successfully!', 'success')
            
            # Redirect to home page
            return redirect(url_for('index'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding user: {str(e)}', 'error')
            return render_template('add.html')
    
    # Render add user form for GET request
    return render_template('add.html')

@app.route('/view/<int:user_id>')
def view_user(user_id):
    """
    View individual user details
    
    TODO: Implement the following:
    1. Get user by ID from database
    2. Handle case when user doesn't exist
    3. Pass user to template
    """
    # Get user by ID (returns 404 if not found)
    user = User.query.get_or_404(user_id)
    
    # Pass user to template
    return render_template('view.html', user=user)

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    """
    Update existing user
    
    GET: Display form with current user data
    POST: Process form data and update user
    
    TODO: Implement the following:
    1. Get user by ID from database
    2. Handle GET request - render update form with current data
    3. Handle POST request - process form data
    4. Validate form data
    5. Update user object
    6. Save changes to database
    7. Handle errors
    8. Redirect to home page on success
    """
    # Get user by ID (returns 404 if not found)
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Get form data from request
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        age = request.form.get('age')
        city = request.form.get('city')
        
        # Validate form data
        if not all([first_name, last_name, email, age, city]):
            flash('All fields are required!', 'error')
            return render_template('update.html', user=user)
        
        # Check if age is a valid number
        try:
            age = int(age)
            if age <= 0 or age > 150:
                flash('Please enter a valid age (1-150)!', 'error')
                return render_template('update.html', user=user)
        except ValueError:
            flash('Age must be a valid number!', 'error')
            return render_template('update.html', user=user)
        
        # Check if email is unique (excluding current user)
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != user_id:
            flash('Email already exists! Please use a different email.', 'error')
            return render_template('update.html', user=user)
        
        try:
            # Update user object with new data
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.age = age
            user.city = city
            
            # Save changes to database
            db.session.commit()
            
            # Add success message
            flash('User updated successfully!', 'success')
            
            # Redirect to home page
            return redirect(url_for('index'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'error')
            return render_template('update.html', user=user)
    
    # Render update form with current user data for GET request
    return render_template('update.html', user=user)

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    """
    Delete user
    
    TODO: Implement the following:
    1. Get user by ID from database
    2. Delete user from database
    3. Add success message
    4. Redirect to home page
    """
    # Get user by ID (returns 404 if not found)
    user = User.query.get_or_404(user_id)
    
    try:
        # Delete user from database
        db.session.delete(user)
        db.session.commit()
        
        # Add success message
        flash(f'User {user.first_name} {user.last_name} deleted successfully!', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    
    # Redirect to home page
    return redirect(url_for('index'))

@app.route('/search')
def search_users():
    """
    Search users by name or city
    
    TODO: Implement the following:
    1. Get search query from request parameters
    2. Search users by first_name, last_name, or city
    3. Pass results to template
    """
    # Get search query from request
    query = request.args.get('query', '')
    
    # Search users by first_name, last_name, or city
    if query:
        search_pattern = f"%{query}%"
        users = User.query.filter(
            db.or_(
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern),
                User.city.ilike(search_pattern)
            )
        ).all()
    else:
        users = []
    
    # Pass query and results to template
    return render_template('search.html', users=users, query=query)

# Error Handlers

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500

# Database initialization
def create_tables():
    """Create database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

# Application entry point
if __name__ == '__main__':
    # TODO: Create database tables before running
    # Hint: Call create_tables() function
    create_tables()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
