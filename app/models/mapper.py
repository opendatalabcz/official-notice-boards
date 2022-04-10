import re
from typing import Optional

from app import db


# TODO add relationships to Municipality and maybe others
from app.utils.random_stuff import nested_get


class Mapper(db.Model):
    """
    Mapper model that maps together RUIAN and ICO of municipalities and municipality parts
    """
    ruian = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    ico = db.Column(db.Integer, unique=True, nullable=True)  # , index=True)

    def __repr__(self):
        return f"<Mapper(ico={self.ico}, ruian={self.ruian})>"

    @classmethod
    def extract_from_dict(cls, data):
        ruian = nested_get(data, ['ruian', 'value'])
        ico = None
        if 'ico' in data:
            ico = nested_get(data, ['ico', 'value'])
        return cls(ruian=ruian, ico=ico)

    @classmethod
    def get_ico(cls, ruian: int) -> Optional[int]:
        record = cls.query.filter_by(ruian=ruian).first()
        if record is None:
            return None
        return record.ico

    @classmethod
    def get_ruian(cls, ico: int) -> Optional[int]:
        record = cls.query.filter_by(ico=ico).first()
        if record is None:
            return None
        return record.ruian
