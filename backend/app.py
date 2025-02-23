from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS  # Importa CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Chat, Message

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    return response

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@db/mydatabase'
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    # Crea utenti di default se non esistono già
    if not User.query.first():
        admin = User(username='admin', email='admin@example.com', password_hash=generate_password_hash('password'), role='admin')
        counselor = User(username='counselor', email='counselor@example.com', password_hash=generate_password_hash('password'), role='counselor')
        db.session.add(admin)
        db.session.add(counselor)
        db.session.commit()

jwt = JWTManager(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


# Auth routes
@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'OPTIONS'})


    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "User already exists"}), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password,
        role='user'
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201


@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'OPTIONS'})


    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity={
        'id': user.id,
        'role': user.role
    })
    return jsonify(access_token=access_token)


# Chat routes
@app.route('/api/chats', methods=['POST', 'OPTIONS'])
@jwt_required()
def create_chat():
    if request.method == 'OPTIONS':
        return jsonify({'msg': 'OPTIONS'})


    current_user = get_jwt_identity()
    counselor = User.query.filter_by(role='counselor').first()

    new_chat = Chat(
        user_id=current_user['id'],
        counselor_id=counselor.id
    )
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({"chat_id": new_chat.id}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)