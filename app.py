from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps
import jwt
import datetime

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

# JWT Token Decorator
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            token = token.split("Bearer ")[1]  # Extract token after "Bearer "
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            g.member = Member.query.get(data['id'])
            if not g.member:
                raise ValueError("User not found")
        except Exception as e:
            return jsonify({"error": "Invalid or expired token", "details": str(e)}), 401
        return f(*args, **kwargs)
    return decorated_function

# Register Endpoint
@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    """
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not all([name, email, username, password]):
        return jsonify({"error": "All fields are required"}), 400

    if Member.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    if Member.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_member = Member(name=name, email=email, username=username, password=hashed_password)
    db.session.add(new_member)
    db.session.commit()

    token = jwt.encode({
        'id': new_member.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({"message": "User registered successfully", "token": token}), 201

# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    """
    Login an existing user.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"error": "Username and password are required"}), 400

    member = Member.query.filter_by(username=username).first()
    if not member or not bcrypt.check_password_hash(member.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Generate JWT Token
    token = jwt.encode({
        'id': member.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({"message": f"Welcome, {member.name}!", "token": token}), 200

# Get All Members (Protected)
@app.route('/members', methods=['GET'])
@token_required
def get_all_members():
    """
    Get all members (Requires Authentication).

    Example request:
    GET /members
    Authorization: Bearer <token>
    """
    members = Member.query.all()
    member_list = [
        {"id": member.id, "name": member.name, "email": member.email, "username": member.username}
        for member in members
    ]
    return jsonify(member_list), 200

# Get Member by ID (Protected)
@app.route('/members/<int:member_id>', methods=['GET'])
@token_required
def get_member_by_id(member_id):
    """
    Get a member by their ID (Requires Authentication).
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

# Update Member (Protected)
@app.route('/update/<int:member_id>', methods=['PUT'])
@token_required
def update_member(member_id):
    """
    Update a member's data (Requires Authentication).
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

# Delete Member (Protected)
@app.route('/delete/<int:member_id>', methods=['DELETE'])
@token_required
def delete_member(member_id):
    """
    Delete a member by ID (Requires Authentication).
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
