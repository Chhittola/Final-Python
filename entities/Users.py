from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required

from configuretion import *


class Users(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    code = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)

    @app.route("/test", methods=["GET"])
    def testing():
        return jsonify({"message": "Hello"})

    @app.route("/user", methods=["POST"])
    def create_user():
        request_data = request.get_json()
        user = Users()
        user.username = request_data['username']
        user.password = request_data['password']
        user.code = str(uuid.uuid4())
        hashed_password = generate_password_hash(request_data['password'], method='sha256')
        user.password = hashed_password
        user.status = True
        user.created_at = datetime.now()
        db.session.add(user)
        db.session.commit()
        message = {"message": "User created"}
        return jsonify(message), 200

    @app.route("/user", methods=["GET"])
    @jwt_required()
    def get_all():
        users = Users.query.all()
        results = []
        for col in users:
            user = {
                'id': col.id,
                'username': col.username,
                'code': col.code,
                'status': col.status,
                'createdAt': col.created_at
            }
            results.append(user)
        return jsonify(results)

    @app.route("/user/<username>")
    def get_by_username(username):
        get_user = Users.query.filter_by(username=username).first()
        if not get_user:
            return jsonify({"message": f"Username {username} not found"}), 400
        results = []
        for col in get_user:
            user = {
                'id': col.id,
                'username': col.username,
                'code': col.code,
                'status': col.status,
                'createdAt': col.created_at
            }
            results.append(user)
        return jsonify(results), 200

    @app.route("/user/<id>", methods=["DELETE"])
    def delete_user(id):
        get_user = Users.query.filter_by(id=id).first()
        if not get_user:
            return jsonify({"message": f"User id {id} not found"}), 400
        db.session.delete(get_user)
        db.session.commit()
        return jsonify({"message": "deleted"}), 202

    @app.route("/login", methods=["POST"])
    def login():
        user_request = request.get_json()
        name = user_request['username']
        password = user_request['password']
        user = Users.query.filter_by(username=name).first()
        if not user:
            return jsonify({"msg": "Bad username or password"}), 401
        if not check_password_hash(user.password, password):
            return jsonify({"msg": "Bad username or password"}), 401
        response = jsonify({"msg": "login successful"})
        access_token = create_access_token(identity=user.code)
        set_access_cookies(response, access_token)
        results = {
            'access_token': access_token,
            'user_id': user.id,
            'username': user.username
        }
        return json.dumps(results), 200
