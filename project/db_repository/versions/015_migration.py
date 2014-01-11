from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tags = Table('tags', pre_meta,
    Column('tag_id', Integer),
    Column('post_id', Integer),
)

tag_post = Table('tag_post', post_meta,
    Column('tag_id', Integer),
    Column('post_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tags'].drop()
    post_meta.tables['tag_post'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tags'].create()
    post_meta.tables['tag_post'].drop()
