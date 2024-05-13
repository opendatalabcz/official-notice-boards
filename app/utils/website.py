from typing import Type, Any

from flask_sqlalchemy import Model

from app.utils.language_translations import split_column_name, translate


def filter_model_to_table(instance: Model) -> dict[str, Any]:
    """Filters chosen columns from model instance to a dictionary"""
    # print(instance.__dict__)
    # if '__website_columns__' not in instance.__dict__.keys():
    #     raise AttributeError('__website_columns__ not found in class {}'.format(instance.__class__.__name__))
    return {key: getattr(instance, key) for key in instance.__website_columns__}


def map_table_key_names(cls: Type[Model]) -> list[tuple[str, str]]:
    """Maps chosen columns names from model to a tuple of the columns name and its corresponding translated name"""
    # if '__website_columns__' not in cls.__dict__:
    #     raise AttributeError('__website_columns__ not found in class {}'.format(cls.__name__))
    #     # return []
    output: list[tuple[str, str]] = []
    for key in cls.__website_columns__:
        split_key = split_column_name(key)
        translated_key = translate('cs', split_key, 2)
        output.append((key, translated_key))
    return output
    # return [(key, key) for key in cls.__website_columns__]