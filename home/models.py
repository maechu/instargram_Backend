from pydoc import doc
from sqlalchemy import BigInteger, CheckConstraint, Column, Date, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.mysql import DATETIME, LONGTEXT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship,backref
from sqlalchemy.ext.declarative import declarative_base
from .database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    nickname = Column(String(50), nullable=False)
    profile_image = Column(String(255), nullable=True)