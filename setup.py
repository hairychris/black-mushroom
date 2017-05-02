from distutils.core import setup
if __name__ == "__main__":
    setup(
        name='black_mushroom.app',
        version='0.0.1',
        url='http://github.com/hairychris/black-mushroom',
        description='A simple blackjack game built with Nameko.',
        author='Chris Franklin',
        author_email='chris@piemonster.me',
        package_dir={
            'black_mushroom.app': 'src/app',
        },
        packages=[
            'black_mushroom.app',
        ],
        install_requires=[
            'black_mushroom.decks==0.0.1',
            'black_mushroom.games==0.0.1',
            'black_mushroom.players==0.0.1',
        ],
        classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Games/Entertainment',
        ],
    )
