from flaskblog import db, bcrypt
from flaskblog.models import User


def create_user_service(username: str, email: str, password: str) -> None:
    """
    Create user in db
    :param username: username
    :param email: email
    :param password: Not hashed password
    """
    hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()


def update_user_service(user: User, username: str, email: str, image_file: str = None) -> None:
    """
    Update user data in db
    :param user: User to update
    :param username: New username
    :param email: New email
    :param image_file: New user image
    """
    user.username = username
    user.email = email

    if image_file:
        user.image_file = image_file

    db.session.commit()


def reset_user_password_service(user: User, password: str) -> None:
    """
    Refresh user password in db
    :param user: User
    :param password: New password
    """
    hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')
    user.password = hashed_password
    db.session.commit()
