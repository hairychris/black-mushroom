from distutils.core import setup
if __name__ == "__main__":
    setup(
        name='black_mushroom.players',
        version='0.0.1',
        url='http://github.com/hairychris/black-mushroom',
        description='A simple blackjack game built with Nameko microservices framework',
        author='Chris Franklin',
        author_email='chris@piemonster.me',
        package_dir = {
            'black_mushroom.players': 'players',
        },
        packages=[
            'black_mushroom.players',
        ],
        install_requires=[
            'black_mushroom.base==0.0.1',
        ],
    )
