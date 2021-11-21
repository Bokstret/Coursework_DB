from models import User, Session


def create(email, password, name):
    user = User(email=email, password=password, name=name)

    with Session() as session:
        session.add(user)
        session.commit()

    return user


def login(email, password):
    with Session() as session:
        user = session.query(User).filter(User.email==email).first()
    if not user:
        return None
    if user.password != password:
        return None
    return user


def check_by_email(email):
    with Session() as session:
        user = session.query(User.email).filter(User.email==email).first()
        if user:
            return True
        return False
