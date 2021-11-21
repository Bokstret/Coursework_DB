import time

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship, sessionmaker, deferred
from sqlalchemy.ext.declarative import declarative_base

from config import Config


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)


class Code(Base):
    __tablename__ = 'code'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(ForeignKey('user.id'), nullable=False)
    data = deferred(Column(LargeBinary, nullable=False))
    title = Column(String, nullable=False)
    image = deferred(Column(LargeBinary, nullable=False))

    author = relationship('User', backref='works')


class Purchase(Base):
    __tablename__ = 'purchase'
    buyer_id = Column(ForeignKey('user.id'), primary_key=True)
    code_id = Column(ForeignKey('code.id'), primary_key=True)

    buyer = relationship('User', backref='purchases')
    code = relationship('Code', backref='buyers')


while True:
    try:
        engine = create_engine(Config.SQLACHEMY_DATABASE_URI)
        break
    except Exception as exc:
        print(exc)
        print('Waiting for db')
        time.sleep(5)

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine, expire_on_commit=False)
