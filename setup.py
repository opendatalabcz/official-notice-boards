from setuptools import setup

setup(
    name='official-notice-boards',
    version='1.0.0',
    author='Jakub Kucera',
    author_email='kucerj56@fit.cvut.cz',
    url='https://github.com/opendatalabcz/official-notice-boards',
    license='GPLv3',


    python_requires=">=3.10",
    # install_requires=[] # REPLACED by requirements.txt file
    entry_points={
        'flask.commands': [
            'import_all_data=app.commands:import_all_data',
            'import_new_data=app.commands:import_new_data'
        ],
    },
)
