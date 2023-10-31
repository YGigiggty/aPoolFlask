from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR

db =  SQLAlchemy()

class TSVector(sa.types.TypeDecorator):
    impl = TSVECTOR

class NameTsvector(sa.types.TypeDecorator):
    impl =TSVECTOR

