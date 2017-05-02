import argparse
import os

from alembic.config import Config
from alembic import command


def migrate(app):
    dirname, filename = os.path.split(os.path.abspath(__file__))
    os.chdir(os.path.join(dirname, app))
    alembic_cfg = Config('alembic.ini')
    command.upgrade(alembic_cfg, "head")


def migrate_all(apps):
    for app in apps:
        migrate(app)


def main():
    parser = argparse.ArgumentParser(
        description='Helper to run database migrations.',
    )
    parser.add_argument('-s', action='store',
                        dest='apps',
                        help='Name of app to migrate')
    input_args = parser.parse_args()
    if isinstance(input_args.apps, list):
        migrate_all(input_args.apps)
    elif isinstance(input_args.apps, str):
        migrate(input_args.apps)
    else:
        raise ValueError('apps should be a list or string')


if __name__ == '__main__':
    # Module was called directly
    main()
