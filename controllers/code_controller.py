from models import Session, Code, Purchase, User
from controllers.user_controller import is_admin


def create(author_id, title, zip_bytes, image_bytes):
    with Session() as session:
        code = Code(title=title, author_id=author_id, data=zip_bytes, image=image_bytes)
        session.add(code)
        session.commit()
    return code


def get_by_user(user_id):
    with Session() as session:
        codes = session.query(Code).filter(Code.author_id==user_id).filter(Code.removed!=True).all()
        return codes


def get_image_by_id(code_id):
    with Session() as session:
        image = session.query(Code.image).filter(Code.id==code_id).first()
        return image


def get_all_codes():
    with Session() as session:
        codes = session.query(Code).filter(Code.removed != True).all()
        return codes


def check_if_available(code_id, user_id):
    with Session() as session:
        code = session.query(Code).get(code_id)
        if code.author_id == user_id:
            return True
        purchase = session.query(Purchase).get((user_id, code_id))
        if purchase:
            return True
        return False


def get_zip(code_id):
    with Session() as session:
        res = session.query(Code.data, Code.title).filter(Code.id==code_id).first()
        return res


def get(code_id):
    with Session() as session:
        code = session.query(Code).get(code_id)
        return code


def delete(code_id, user_id):
    with Session() as session:
        code = session.query(Code).get(code_id)
        if code and (code.author_id == user_id or is_admin(user_id)):
            code.removed = True
            session.add(code)
            session.commit()
            return True
        return False
