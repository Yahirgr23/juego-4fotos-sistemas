# servidor/app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
import secrets
import string

# Configuración de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Cambiar en producción
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///juego_sistemas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db = SQLAlchemy(app)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# =============================================================================
# MODELOS DE BASE DE DATOS
# =============================================================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, default=0)
    levels_created = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_online = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self):
        return jwt.encode({
            'user_id': self.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm='HS256')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'score': self.score,
            'levels_created': self.levels_created,
            'is_online': self.is_online
        }

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), default='medio')
    image1_url = db.Column(db.String(255), nullable=False)
    image2_url = db.Column(db.String(255), nullable=False)
    image3_url = db.Column(db.String(255), nullable=False)
    image4_url = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(50), nullable=False)
    hint = db.Column(db.String(200))
    plays_count = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    creator = db.relationship('User', backref=db.backref('created_levels', lazy=True))

    def generate_code(self):
        """Genera un código único para el nivel"""
        while True:
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            if not Level.query.filter_by(code=code).first():
                return code

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'code': self.code,
            'creator': self.creator.username,
            'category': self.category,
            'difficulty': self.difficulty,
            'images': [self.image1_url, self.image2_url, self.image3_url, self.image4_url],
            'answer': self.answer,
            'hint': self.hint,
            'plays_count': self.plays_count,
            'likes': self.likes,
            'created_at': self.created_at.isoformat()
        }

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    time_taken = db.Column(db.Integer)  # en segundos
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('game_sessions', lazy=True))
    level = db.relationship('Level', backref=db.backref('sessions', lazy=True))

# =============================================================================
# UTILIDADES
# =============================================================================

def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token faltante'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Usuario no válido'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401
            
        return f(current_user, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

# =============================================================================
# RUTAS DE AUTENTICACIÓN
# =============================================================================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Usuario ya existe'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email ya registrado'}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    token = user.generate_token()
    
    return jsonify({
        'message': 'Usuario creado exitosamente',
        'token': token,
        'user': user.to_dict()
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Credenciales inválidas'}), 401
    
    user.is_online = True
    db.session.commit()
    
    token = user.generate_token()
    
    return jsonify({
        'message': 'Login exitoso',
        'token': token,
        'user': user.to_dict()
    })

@app.route('/api/logout', methods=['POST'])
@token_required
def logout(current_user):
    current_user.is_online = False
    db.session.commit()
    return jsonify({'message': 'Logout exitoso'})

# =============================================================================
# RUTAS DE NIVELES
# =============================================================================

@app.route('/api/levels', methods=['GET'])
def get_levels():
    category = request.args.get('category', '')
    difficulty = request.args.get('difficulty', '')
    
    query = Level.query
    if category:
        query = query.filter_by(category=category)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    
    levels = query.order_by(Level.created_at.desc()).all()
    return jsonify([level.to_dict() for level in levels])

@app.route('/api/levels/<code>', methods=['GET'])
def get_level_by_code(code):
    level = Level.query.filter_by(code=code).first()
    if not level:
        return jsonify({'message': 'Nivel no encontrado'}), 404
    
    # Incrementar contador de jugadas
    level.plays_count += 1
    db.session.commit()
    
    return jsonify(level.to_dict())

@app.route('/api/levels', methods=['POST'])
@token_required
def create_level(current_user):
    data = request.get_json()
    
    level = Level(
        title=data['title'],
        code=Level().generate_code(),
        creator_id=current_user.id,
        category=data['category'],
        difficulty=data.get('difficulty', 'medio'),
        image1_url=data['images'][0],
        image2_url=data['images'][1],
        image3_url=data['images'][2],
        image4_url=data['images'][3],
        answer=data['answer'].upper(),
        hint=data.get('hint', '')
    )
    
    db.session.add(level)
    current_user.levels_created += 1
    db.session.commit()
    
    # Notificar a usuarios conectados
    socketio.emit('new_level', {
        'level': level.to_dict(),
        'creator': current_user.username
    })
    
    return jsonify({
        'message': 'Nivel creado exitosamente',
        'level': level.to_dict()
    }), 201

@app.route('/api/levels/<int:level_id>/like', methods=['POST'])
@token_required
def like_level(current_user, level_id):
    level = Level.query.get_or_404(level_id)
    level.likes += 1
    db.session.commit()
    
    return jsonify({'message': 'Like agregado', 'likes': level.likes})

# =============================================================================
# RUTAS DE PUNTUACIONES
# =============================================================================

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    users = User.query.order_by(User.score.desc()).limit(10).all()
    return jsonify([{
        'username': user.username,
        'score': user.score,
        'levels_created': user.levels_created
    } for user in users])

@app.route('/api/game/complete', methods=['POST'])
@token_required
def complete_game(current_user):
    data = request.get_json()
    
    session = GameSession(
        user_id=current_user.id,
        level_id=data['level_id'],
        score=data['score'],
        completed=data['completed'],
        time_taken=data.get('time_taken', 0)
    )
    
    db.session.add(session)
    
    if data['completed']:
        current_user.score += data['score']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Sesión guardada',
        'total_score': current_user.score
    })

# =============================================================================
# EVENTOS DE SOCKET.IO
# =============================================================================

@socketio.on('connect')
def on_connect():
    print('Cliente conectado')

@socketio.on('disconnect')
def on_disconnect():
    print('Cliente desconectado')

@socketio.on('join_game')
def on_join_game(data):
    join_room(data['level_code'])
    emit('joined_game', {'level_code': data['level_code']})

@socketio.on('game_progress')
def on_game_progress(data):
    emit('player_progress', data, room=data['level_code'], include_self=False)

# =============================================================================
# INICIALIZACIÓN
# =============================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Crear algunos niveles de ejemplo
        if not Level.query.first():
            admin_user = User(username='admin', email='admin@sistemas.com')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            
            ejemplo_level = Level(
                title='Conceptos Básicos de BD',
                code='BD001SYS',
                creator_id=admin_user.id,
                category='base_datos',
                difficulty='facil',
                image1_url='https://example.com/tabla.jpg',
                image2_url='https://example.com/sql.jpg',
                image3_url='https://example.com/datos.jpg',
                image4_url='https://example.com/consulta.jpg',
                answer='DATABASE',
                hint='Sistema para almacenar información'
            )
            db.session.add(ejemplo_level)
            db.session.commit()
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)