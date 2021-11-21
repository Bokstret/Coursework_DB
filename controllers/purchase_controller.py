from sqlalchemy.orm import joinedload

from models import Session, Purchase, User, Code


def create(buyer_id, code_id):
    with Session() as session:
        purchase = Purchase(buyer_id=buyer_id, code_id=code_id)
        session.add(purchase)
        session.commit()
    return purchase


def get_by_buyer(buyer_id):
    with Session() as session:
        purchases = session.query(Purchase).options(joinedload(Purchase.code)).filter(Purchase.buyer_id==buyer_id).all()
    return purchases


def check_if_bought(buyer_id, code_id):
    with Session() as session:
        purchase = session.query(Purchase).get((buyer_id, code_id))
        if purchase:
            return True
        return False
