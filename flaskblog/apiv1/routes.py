from datetime import datetime

from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from flaskblog import db, bcrypt
from flaskblog.models import Post, User

apiv1 = Blueprint('apiv1', __name__)
api = Api(apiv1, prefix='/api/1')

posts_parser = reqparse.RequestParser()
posts_parser.add_argument('user', type=str)
posts_parser.add_argument('count', type=int, required=False, help='Count of last records')


class PostByIdApi(Resource):
    def get(self, post_id):
        post = Post.query.filter_by(id=post_id).first()

        if not post:
            return {'message': 'Post not found'}, 404

        return {'post': {'title': post.title, 'date_posted': str(post.date_posted),
                         'content': post.content}}


class CreatePostApi(Resource):
    @jwt_required
    def post(self):
        try:
            email = get_jwt_identity()
            user = User.query.filter_by(email=email).first()

            if not user:
                return {'message': 'User is not found'}, 400

            if not request.is_json:
                return {"msg": "Missing JSON in request"}, 400

            title = request.json.get('title', None)
            content = request.json.get('content', None)

            if not title:
                return {"msg": "Missing title parameter"}, 400
            if not content:
                return {"msg": "Missing content parameter"}, 400

            db.session.add(Post(title=title, date_posted=datetime.now(), content=content,
                                user_id=user.id))
            db.session.commit()

            return {'message': 'Post has been created'}, 201
        except Exception:
            return {'message': f'Error'}, 400


class PostsByUserApi(Resource):
    def get(self):
        args = posts_parser.parse_args()
        user = User.query.filter_by(username=args['user']).first()
        count = args['count']

        if not user:
            return {'message': 'User is not found'}, 400

        output = []

        for post in user.posts if not count else user.posts[::-1][:count]:
            output.append({'id': post.id, 'title': post.title, 'date_posted': str(post.date_posted),
                           'content': post.content})

        return {'posts': output}


class LoginApi(Resource):
    def post(self):
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400

        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if not email:
            return {"msg": "Missing email parameter"}, 400
        if not password:
            return {"msg": "Missing password parameter"}, 400

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=email)
            return {'access_token': access_token}, 200
        else:
            return {"msg": "Bad email or password"}, 401


api.add_resource(PostByIdApi, '/post/<int:post_id>')
api.add_resource(CreatePostApi, '/post')
api.add_resource(PostsByUserApi, '/posts')
api.add_resource(LoginApi, '/login')
