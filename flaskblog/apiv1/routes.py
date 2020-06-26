from datetime import datetime

from flask import Blueprint, request
from flask_restful import Resource, Api
from flask_login import current_user, login_required

from flaskblog import db
from flaskblog.models import Post

apiv1 = Blueprint('apiv1', __name__)
api = Api(apiv1, prefix='/api/1')


class PostApi(Resource):
    def get(self, post_id):
        post = Post.query.filter_by(id=post_id).first()

        if not post:
            return {'message': 'Post not found'}, 404

        return {'post': {'title': post.title, 'date_posted': str(post.date_posted),
                         'content': post.content}}

    @login_required
    def post(self):
        try:
            data = request.get_json()

            db.session.add(Post(title=data['title'], date_posted=datetime.now(), content=data['content'],
                                user_id=current_user))
            db.session.commit()

            return {'message': 'Post has been created'}, 201
        except Exception:
            return {'message': f'Error with text: {str(Exception)}'}, 400


api.add_resource(PostApi, '', '/post/<int:post_id>')
