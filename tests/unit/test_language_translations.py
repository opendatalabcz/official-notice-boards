import pytest

from app.utils.language_translations import capitalize_first, capitalize_all_first_letters, translate, \
    translate_only, split_column_name


@pytest.mark.parametrize('data', [
    {
        'input': '',
        'expected': ''
    },
    {
        'input': 'a',
        'expected': 'A'
    },
    {
        'input': 'aa',
        'expected': 'Aa'
    },
    {
        'input': 'foo',
        'expected': 'Foo'
    },
    {
        'input': 'Foo',
        'expected': 'Foo'
    },
    {
        'input': 'foo bar',
        'expected': 'Foo bar'
    },
    {
        'input': 'this is a sentence with multiple words and here are some extra characters . - = + ! @ # $ % ^ & * ( ) _ +',
        'expected': 'This is a sentence with multiple words and here are some extra characters . - = + ! @ # $ % ^ & * ( ) _ +'
    },
])
def test_capitalize_first(data):
    assert capitalize_first(data.get('input')) == data.get('expected')


@pytest.mark.parametrize('data', [
    {
        'input': '',
        'expected': ''
    },
    {
        'input': 'a',
        'expected': 'A'
    },
    {
        'input': 'aa',
        'expected': 'Aa'
    },
    {
        'input': 'foo',
        'expected': 'Foo'
    },
    {
        'input': 'Foo',
        'expected': 'Foo'
    },
    {
        'input': 'foo bar',
        'expected': 'Foo Bar'
    },
    {
        'input': 'this is a sentence with multiple words and here are some extra characters . - = + ! @ # $ % ^ & * ( ) _ +',
        'expected': 'This Is A Sentence With Multiple Words And Here Are Some Extra Characters . - = + ! @ # $ % ^ & * ( ) _ +',
    },
])
def test_capitalize_all_first_letters(data):
    assert capitalize_all_first_letters(data.get('input')) == data.get('expected')


@pytest.mark.parametrize('data', [
    {
        'input': {'language': 'cs', 'expressions': 'official notice boards'},
        'expected': 'Úrední desky'
    },
    {
        'input': {'language': 'en', 'expressions': 'official notice boards'},
        'expected': 'official notice boards'
    },
    {
        'input': {'language': 'cs', 'expressions': 'foo'},
        'expected': None
    },
    {
        'input': {'language': 'en', 'expressions': 'foo'},
        'expected': 'foo'
    },
])
def test_translate(data):
    assert translate_only(**data.get('input')) == data.get('expected')


@pytest.mark.parametrize('input', [
    {'language': 'sk', 'expressions': 'official notice boards'},
])
def test_translate(input):
    with pytest.raises(ValueError):
        translate(**input)


@pytest.mark.parametrize('data', [
    {
        'input': 'foo',
        'expected': 'foo'
    },
    {
        'input': 'foo bar',
        'expected': 'foo bar'
    },
    {
        'input': 'foo_bar',
        'expected': 'foo bar'
    },
    {
        'input': 'foo-bar',
        'expected': 'foo bar'
    },
])
def test_split_column_name(data):
    assert split_column_name(data.get('input')) == data.get('expected')