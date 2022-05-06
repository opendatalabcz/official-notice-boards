from typing import Optional

from app import db
from app.utils.random_stuff import nested_get


class Municipality(db.Model):
    """
    Municipality model
    """
    __website_columns__ = ['name', 'ruian', 'ico', 'has_board']

    name = db.Column(db.String(100), unique=False, nullable=False)
    has_extended_competence = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    ico = db.Column(db.Integer, unique=True, nullable=True)
    ruian = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    parent_ruian = db.Column(db.Integer, db.ForeignKey('municipality.ruian'))
    parent = db.relationship("Municipality", remote_side=[ruian])

    boards = db.relationship('OfficialNoticeBoard', backref='municipality', lazy=True)
    has_board = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    def __repr__(self):
        return f"<Municipality(name='{self.name}', ico={self.ico}, ruian={self.ruian}, " \
               f"has_board={self.has_board}, parent_ruian={self.parent_ruian})>"

    @classmethod
    def extract_from_dict(cls, data):
        name = nested_get(data, ['nazev', 'cs'])
        ruian = data['kod']
        parent_ruian: Optional[str] = None
        if 'obec' in data:
            parent_ruian = data['obec'].split(sep='/')[-1]
        return cls(name=name, ruian=ruian, parent_ruian=parent_ruian)

    # def add_board(self, board):
    #     self.has_board = True
    #     self.boards.append(board)
    #     if len(self.boards) > 1:
    #         self.has_multiple_boards = True
