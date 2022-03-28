class Config:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:example@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BOOTSTRAP_BOOTSWATCH_THEME = 'Flatly'
