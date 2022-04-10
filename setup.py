from setuptools import setup

setup(
    name='official-notice-boards',
    version='0.0.9',
    author='Jakub Kucera',
    author_email='kucerj56@fit.cvut.cz',
    url='https://github.com/opendatalabcz/official-notice-boards',


    python_requires=">=3.10",
    install_requires=[
        'bootstrap-flask==2.0.2',
        'click==8.1.2',
        'docx2txt==0.8',
        'Flask-Caching==1.10.1',
        'Flask-Migrate==3.1.0',
        'Flask-SQLAlchemy==2.5.1',
        'pdfminer.six==20220319',
        'pdfminer.six[image]',
        'psycopg2-binary==2.9.3',
        'python-dotenv==0.20.0',
        'requests==2.27.1',
        'SPARQLWrapper==2.0.0',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_requires=[
        'pytest==7.1.1',
    ],
    # ...,
    entry_points={
        'flask.commands': [
            'import_all=app.commands:import_data'
        ],
    },
)