# ![Logo](logo.png) Black Mushroom

A very simple BlackJack game built with [Nameko] microservices framework.

## Design considerations

* Enable code reuse where possible (Deck is generic, Player is generic, Game is project specific).
* Enable horizontal scaling by keeping services loosely coupled, seperate databases too.
* This is a tech demo so it was smashed out quickly, this is not an excuse but there be dragons.
* Service must operate over RPC.
* Make it easy to switch database engine.
* Use migrations to avoid having to manually mess with a database (what year is it?)
* Test coverage is unacceptable, this is not a real world project.
* I ran out of time to implement the various Docker containers but these would have been:
	1. Postgres container for each service.
	2. Application container for each service.
	3. RabbitMQ container.
	4. Some sort of load balancer such as Traefik
* I would have also liked to explore adding an HTTP / WebSocket API.
* If this was a real project I would have built a proper frontend for it (probably with React.JS)

## Requirements

### Core requirements

* [SQLAlchemy] - 1.1.9
* [SQLAlchemy-Utils] - 0.32.14
* [Nameko] - 2.5.4
* [Nameko-SQLAlchemy] - 0.1.0
* [Marshmallow] - 2.13.5
* [Marshmallow-SQLAlchemy] - 0.13.1
* [Alembic] - 0.9.1

[SQLAlchemy]: <https://www.sqlalchemy.org/>
[SQLAlchemy-Utils]: <https://sqlalchemy-utils.readthedocs.io/en/latest/>
[Nameko]: <https://github.com/nameko/nameko>
[Nameko-SQLAlchemy]: <https://github.com/onefinestay/nameko-sqlalchemy>
[Marshmallow]: <https://marshmallow.readthedocs.io/en/latest/>
[Marshmallow-SQLAlchemy]: <https://marshmallow-sqlalchemy.readthedocs.io/en/latest/>
[Alembic]: <http://alembic.zzzcomputing.com>


### Database driver

You will need a database driver, the default is psycopg2 but you could use sqlite or whatever.

* [Psycopg2] - 2.7.1

[Psycopg2]: <http://initd.org/psycopg/>

### Test requirements

* [py.test] - 3.0.7

[py.test]: <https://docs.pytest.org/en/latest/>


## Install

### Install requirements

You can install the wrapper package:

```
pip install .
```

You must then also install the services

```
pip install src/services/base
pip install src/services/decks
pip install src/services/games
pip install src/services/players
```

### Database migrations

To create / update the database schema run the following command:

```
python black_mushroom/migrate.py
```

## Running

### Run all services

```
nameko run black_mushroom.app --config black_mushroom/config.yml
```

### Running individual services

Run one or more of the following commands:

```
nameko run black_mushroom.players.services --config config.yml
nameko run black_mushroom.decks.services --config config.yml
nameko run black_mushroom.games.services --config config.yml
```

## Usage

You can interact with this application by using the Nameko shell, run the following:

```
nameko shell --config config.yml
```

This gives you a prompt back which you can use to call services for example to start a game:

```
n.rpc.game.create(n.rpc.player.create('Chris'))
```

After running the above command you should get a game_id returned, you can interact with the game like so:

```
n.rpc.game.hit(YOUR_GAME_ID_HERE)
```

or alternatively you could choose to stick

```
n.rpc.game.stick(YOUR_GAME_ID_HERE)
```

Which should return you a JSON representation of the game state.

## Testing

You can install the test requirements by running:

```
pip install -r requirements.txt
```

When running tests you can pass database test url with ``--test-db-url`` parameter or override ``db_url`` fixture.

### With in-memory SQLite database

```
py.test black_mushroom/tests.py
```

### With seperate test database

```
py.test src/black_mushroom/tests.py --test-db-url=sqlite:///test_db.sql
```

## Docker

Each service can be run in an independent Docker container, all dependencies (e.g. PostgreSQL, RabbitMQ etc) can be run as Docker containers. This is all handled by a docker-compose file.

If you would like to start all services under Docker please run the following command:

```
docker-compose run --rm wait_for_rabbit && docker-compose up
```
