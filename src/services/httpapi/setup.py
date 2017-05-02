from distutils.core import setup
if __name__ == "__main__":
    setup(
        name='black_mushroom.httpapi',
        version='0.0.1',
        url='http://github.com/hairychris/black-mushroom',
        description='A simple blackjack game built with Nameko.',
        author='Chris Franklin',
        author_email='chris@piemonster.me',
        package_dir={
            'black_mushroom.httpapi': 'httpapi',
        },
        packages=[
            'black_mushroom.httpapi',
        ],
        install_requires=[
            # 'black_mushroom.base==0.0.1',
            'black_mushroom.decks==0.0.1',
            'black_mushroom.players==0.0.1',
            'black_mushroom.games==0.0.1',
        ],
    )
