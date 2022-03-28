import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR


# taken from https://amitosh.medium.com/full-text-search-fts-with-postgresql-and-sqlalchemy-edc436330a0c
class TSVector(sa.types.TypeDecorator):
    impl = TSVECTOR
    cache_ok = True
