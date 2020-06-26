from datetime import datetime

from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse
from flask_login import current_user, login_required

from flaskblog import db
from flaskblog.models import Post, User

apiv1 = Blueprint('apiv1', __name__)
api = Api(apiv1, prefix='/api/1')

posts_parser = reqparse.RequestParser()
posts_parser.add_argument('user', type=str)
posts_parser.add_argument('count', type=int, required=False, help='Count of last records')


class PostApi(Resource):
    def get(self, post_id):
        post = Post.query.filter_by(id=post_id).first()

        if not post:
            return {'message': 'Post not found'}, 404

        return {'post': {'title': post.title, 'date_posted': str(post.date_posted),
                         'content': post.content}}

    def post(self):
        try:
            data = request.get_json()

            db.session.add(Post(title=data['title'], date_posted=datetime.now(), content=data['content'],
                                user_id=current_user))
            db.session.commit()

            return {'message': 'Post has been created'}, 201
        except Exception:
            return {'message': f'Error with text: {str(Exception)}'}, 400


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


api.add_resource(PostApi, '/post/<int:post_id>')
api.add_resource(PostsByUserApi, '/posts')