from flaskblog import db
from flaskblog.models import Post, User


def create_post_service(title: str, content: str, user: User) -> None:
    """
    Create post in db
    :param title: Post title
    :param content: Post content
    :param user: Post user
    """
    post = Post(title=title, content=content, author=user)
    db.session.add(post)
    db.session.commit()


def update_post_service(post: Post, title: str, content: str) -> None:
    """
    Update post in db
    :param post: Post to be deleted
    :param title: New post title
    :param content: New post content
    """
    post.title = title
    post.content = content
    db.session.commit()


def delete_post_service(post: Post) -> None:
    """
    Delete post in db
    :param post: Post to be deleted
    """
    db.session.delete(post)
    db.session.commit()
