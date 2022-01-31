from src.app import db


class Municipality(db.Model):
    """
    Municipality model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    ruian = db.Column(db.Integer, unique=True, nullable=False)
    ico = db.Column(db.Integer, unique=True, nullable=False)  # nullable?
    # only_municipality_part = db.Column(db.Boolean, unique=False, nullable=False)  # TODO maybe

    def __repr__(self):
        return f"<Municipality(id='{self.id}', name='{self.name}'," \
                             f"ruian='{self.ruian}, ico='{self.ico}')>"
