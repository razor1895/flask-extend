from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=80)),
    Column('body', Text),
    Column('pub_date', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].columns['timestamp'].drop()
    pre_meta.tables['post'].columns['user_id'].drop()
    post_meta.tables['post'].columns['pub_date'].create()
    post_meta.tables['post'].columns['title'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].columns['timestamp'].create()
    pre_meta.tables['post'].columns['user_id'].create()
    post_meta.tables['post'].columns['pub_date'].drop()
    post_meta.tables['post'].columns['title'].drop()
