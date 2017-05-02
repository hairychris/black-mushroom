from distutils.core import setup
if __name__ == "__main__":
    setup(
        name='black_mushroom.base',
        version='0.0.1',
        url='http://github.com/hairychris/black-mushroom',
        description='A simple blackjack game built with Nameko microservices framework',
        author='Chris Franklin',
        author_email='chris@piemonster.me',
        package_dir = {
            'black_mushroom.base': 'base',
        },
        packages=[
            'black_mushroom.base',
        ],
        install_requires=[
            'nameko==2.5.4',                   # Framework for building microservices
            'SQLAlchemy==1.1.9',               # SQL toolkit and Object Relational Mapper
            'sqlalchemy-utils==0.32.14',       # Helpers for SQLAlchemy, we only need ScalarList
            'nameko-sqlalchemy==0.1.0',        # Requires SQLAlchemy but doesn't pin version
            'psycopg2==2.7.1',                 # PostgreSQL support
            'alembic==0.9.1',                  # Database migrations
            'marshmallow-sqlalchemy==0.13.1',  # Schemas for (de)serialization support
        ],
    )
