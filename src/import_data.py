from src.app import db
from src.models import *
from src.utils.sparql.mapper import fetch_mapper_data
from src.utils.sparql.municipality import fetch_municipality_list


def import_mapper():
    for map_raw in fetch_mapper_data():
        map = Mapper.extract_from_dict(map_raw)
        db.session.add(map)


def import_municipalities():
    for municipality_raw in fetch_municipality_list(is_part=False):
        municipality_record = Municipality.extract_from_dict(municipality_raw)
        db.session.add(municipality_record)

    for municipality_part_raw in fetch_municipality_list(is_part=True):
        municipality_part_record = Municipality.extract_from_dict(municipality_part_raw)
        db.session.add(municipality_part_record)


def main():
    db.create_all()
    import_mapper()
    import_municipalities()
    db.session.commit()


if __name__ == '__main__':
    main()
