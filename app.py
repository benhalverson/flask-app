from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import os

app = Flask(__name__)

# Configure the MySQL database connection
db_host = os.getenv('DB_HOST', 'db')
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', 'rootpassword')
db_name = os.getenv('DB_NAME', 'flask_app')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define a sample model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


# Create the database tables during application startup
with app.app_context():
    db.create_all()


# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Check database connection
        db.session.execute(text('SELECT 1'))
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


# Sample route to add a user
@app.route('/add_user/<string:name>/<string:email>', methods=['GET'])
def add_user(name, email):
    try:
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User added successfully!", "user": new_user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# Sample route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
