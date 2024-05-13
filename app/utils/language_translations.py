from enum import Enum, auto
from typing import Final


class Language(Enum):
    CZECH = auto()
    ENGLISH = auto()


CS: Final[dict[str, str]] = {
    "official notice boards": "úřední desky",
    "official notice board": "úřední deska",
    "documents": "dokumenty",
    "document": "dokument",
    "notices": "vývěsky",
    "notice": "vývěska",
    "municipalities": "obce",
    "municipality": "obec",
    "municipality parts": "části obcí",
    "municipality part": "část obce",
    "graphs": "grafy",
    "graph": "graf",

    "id": "id",
    "ico": "IČO:",
    "ruian": "ruian",
    "has board": "má úřední desku",
    "name": "název",
    "name missing": "chybí název",
    "office name": "název úřadu",
    "post date": "datum vyvěšení",
    "url": "url",
    "download url": "adresa ke stažení",
    "download url missing": "chybí adresa ke stažení",
    "attempted download": "pokus o stažení",
    "download url unreachable": "adresa ke stažení není dostupná",
    "downloaded file url": "adresa staženého souboru",
    "file extension": "přípona souboru",
    "shortened extracted text": "zkrácený extrahováný text",

    # TODO add more
}


class Translator:
    supported_languages = ['cs', 'en']

    def __init__(self, language: str, capitalize_mode: int = 0):
        if language not in self.supported_languages:
            raise ValueError(f"Language code {language} is not supported.")

        self.language = language
        self.capitalize_mode = capitalize_mode

    # def _get_capitalize_function(self) -> callable:
    #     return capitalize_function

    # def translate(self, expressions: str) -> str:
    #     return CS[key]

    def translate_only(self, expressions: str) -> str | None:
        if self.language == 'cs':
            return CS[expressions]
        # if self.language == 'en':
        return expressions


def translate(language: str, expressions: str, capitalize_mode: int = 0) -> str | None:
    """
    Translate a selected string to the given language.
    :param language: Language code of language to translate to.
    :param expressions: String to translate.
    :param capitalize_mode: 0 - no capitalization, 1 - capitalize first letter, 2 - capitalize all first letters, 3 - capitalize all letters
    """
    translated_expressions = translate_only(language, expressions)
    if translated_expressions is None or capitalize_mode == 0:
        return translated_expressions
    if capitalize_mode == 1:
        return capitalize_first(translated_expressions)
    if capitalize_mode == 2:
        return capitalize_all_first_letters(translated_expressions)
    if capitalize_mode == 3:
        return translated_expressions.upper()


def translate_only(language: str, expressions: str) -> str | None:
    if language == 'cs':
        return CS[expressions]
    if language == 'en':
        return expressions
    raise ValueError(f"Language code {language} is not supported.")


def capitalize_first(string: str) -> str:
    if len(string) == 0:
        return string
    if len(string) == 1:
        return string[0].upper()
    return string[0].upper() + string[1:]


def capitalize_all_first_letters(string: str) -> str:
    return " ".join(capitalize_first(word) for word in string.split(" "))


def split_column_name(name: str) -> str:
    return name.replace("_", " ").replace("-", " ")

