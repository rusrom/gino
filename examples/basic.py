from gino import Gino

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger(), primary_key=True)
    nickname = db.Column(db.Unicode(), default='noname')
    profile = db.Column(db.JSONB())

    def __repr__(self):
        return '{}<{}>'.format(self.nickname, self.id)


async def main():
    # In this example we create the database tables directly using SQLAlchemy
    # and non-async Postgres (uses psycopg2 python module, not asyncpg which
    # GINO uses). For a production application you would probably use a full
    # schema migration solution like Alembic.
    import sqlalchemy as sa
    db_engine = sa.create_engine('postgresql://localhost/gino')
    db.create_all(bind=db_engine)
    db_engine.dispose()

    # Here starts the normal async application
    await db.create_engine('asyncpg://localhost/gino')

    print(await User.create(nickname='fantix'))
    print(await User.get(1))


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
