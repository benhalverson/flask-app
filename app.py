from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:flask_password@db/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Member Model
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Register Endpoint
@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    Example request (JSON):
    {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "password": "securepassword"
    }

    Example response (JSON):
    {
        "message": "User registered successfully"
    }

    Error responses:
    - {"error": "All fields are required"} (400)
    - {"error": "Username already exists"} (400)
    - {"error": "Email already exists"} (400)
    """
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not all([name, email, username, password]):
        return jsonify({"error": "All fields are required"}), 400

    # Check if username or email already exists
    if Member.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    if Member.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a new member
    new_member = Member(name=name, email=email, username=username, password=hashed_password)
    db.session.add(new_member)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    """
    Login an existing user.

    Example request (JSON):
    {
        "username": "johndoe",
        "password": "securepassword"
    }

    Example successful response (JSON):
    {
        "message": "Welcome, John Doe!"
    }

    Error responses:
    - {"error": "Username and password are required"} (400)
    - {"error": "Invalid username or password"} (401)
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"error": "Username and password are required"}), 400

    # Find user by username
    member = Member.query.filter_by(username=username).first()
    if not member:
        return jsonify({"error": "Invalid username or password"}), 401

    # Check password
    if not bcrypt.check_password_hash(member.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": f"Welcome, {member.name}!"}), 200

# Get All Members
@app.route('/members', methods=['GET'])
def get_all_members():
    """
    Get all members.

    Example request:
    GET /members

    Example response (JSON):
    [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "username": "johndoe"
        },
        {
            "id": 2,
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "username": "janedoe"
        }
    ]
    """
    members = Member.query.all()
    member_list = [
        {"id": member.id, "name": member.name, "email": member.email, "username": member.username}
        for member in members
    ]
    return jsonify(member_list), 200

# Get Member by ID
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member_by_id(member_id):
    """
    Get a member by their ID.

    Example request:
    GET /members/1

    Example response (JSON):
    {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "username": "johndoe"
    }
    """
    member = Member.query.get(member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    member_data = {
        "id": member.id,
        "name": member.name,
        "email": member.email,
        "username": member.username
    }
    return jsonify(member_data), 200

# Update Member Endpoint
@app.route('/update/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """
    Update a member's data.
    """
    data = request.get_json()
    member = Member.query.get(member_id)

    if not member:
        return jsonify({"error": "Member not found"}), 404

    member.name = data.get('name', member.name)
    member.email = data.get('email', member.email)
    member.username = data.get('username', member.username)
    
    if 'password' in data:
        member.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    db.session.commit()
    return jsonify({"message": "Member data updated successfully"}), 200

# Delete Member Endpoint
@app.route('/delete/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """
    Delete a member by ID.
    """
    member = Member.query.get(member_id)

    if not member:
        return jsonify({"error": "Member not found"}), 404

    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member deleted successfully"}), 200

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
