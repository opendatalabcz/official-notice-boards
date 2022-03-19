from typing import Optional

from src.app import db
from src.models.mapper import Mapper
from src.utils.random_stuff import nested_get


class Municipality(db.Model):
    """
    Municipality model
    """
    name = db.Column(db.String(100), unique=False, nullable=False)
    ruian = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    # municipality parts aside from Prague parts use their mains municipality office ico
    ico = db.Column(db.Integer, unique=True, nullable=True)
    parent_ruian = db.Column(db.Integer, db.ForeignKey('municipality.ruian'))
    parent = db.relationship("Municipality", remote_side=[ruian])

    def __repr__(self):
        return f"<Municipality(name='{self.name}', ico={self.ico}, ruian={self.ruian}, parent_ruian={self.parent_ruian})>"

    @classmethod
    def extract_from_dict(cls, data):
        name = nested_get(data, ['nazev', 'cs'])
        ruian = data['kod']
        ico = Mapper.get_ico(ruian)
        parent_ruian: Optional[str] = None
        if 'obec' in data:
            parent_ruian = data['obec'].split(sep='/')[-1]
        return cls(name=name, ruian=ruian, ico=ico, parent_ruian=parent_ruian)
