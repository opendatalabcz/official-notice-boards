from setuptools import setup

setup(
    name='official-notice-boards',
    author='Jakub Kucera',
    url='https://github.com/opendatalabcz/official-notice-boards',


    python_requires=">=3.10",
    # ...,
    entry_points={
        'flask.commands': [
            'import_all=app.commands:import_data'
        ],
    },
)