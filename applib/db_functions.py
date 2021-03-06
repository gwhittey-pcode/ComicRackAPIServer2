from peewee import (
    SqliteDatabase,
    CharField,
    IntegerField,
    ForeignKeyField,
    TextField,
    Model,
    ManyToManyField,
    DeferredThroughModel,
    DatabaseProxy,
    BooleanField,
)


from kivy.app import App
import os

database_proxy = DatabaseProxy()
from playhouse.fields import PickleField  # noqa


def start_db():
    print("stardb2")
    db_file =  "ComicRackAPIServer2.db"

    database_proxy.initialize(SqliteDatabase(db_file))
    database_proxy.create_tables(
        [
            #ReadingList,
            Comic,
            #ComicIndex,
            #ReadingList.comics.get_through_model(),
        ]
    )


class BaseModel(Model):
    class Meta:
        # This model uses the "ComicRackAPIServer2.db" database.
        database = database_proxy


class Comic(BaseModel):
    Id = CharField(primary_key=True)
    Number = CharField()
    Series = CharField(null=True)
    Year = IntegerField(null=True)
    Month = IntegerField(null=True)
    LastPageRead = IntegerField(null=True)
    CurrentPage = IntegerField(null=True)
    PageCount = IntegerField(null=True)
    Summary = TextField(null=True)
    FilePath = CharField(null=True)
    Volume = CharField(null=True)
    


ComicIndexDeferred = DeferredThroughModel()


# class ReadingList(BaseModel):
#     name = CharField()
#     slug = CharField(primary_key=True)
#     data = PickleField(null=True)
#     comics = ManyToManyField(
#         Comic, backref="readinglists", through_model=ComicIndexDeferred
#     )
#     cb_limit_active = BooleanField(null=True)
#     limit_num = IntegerField(null=True)
#     cb_only_read_active = BooleanField(null=True)
#     cb_purge_active = BooleanField(null=True)
#     cb_optimize_size_active = BooleanField(null=True)
#     sw_syn_this_active = BooleanField(null=True)
#     end_last_sync_num = IntegerField(default=0)
#     totalCount = IntegerField()


# class ComicIndex(BaseModel):
#     comic = ForeignKeyField(Comic, backref="comic_index")
#     readinglist = ForeignKeyField(ReadingList, backref="Indexes")
#     index = IntegerField()


# ComicIndexDeferred.set_model(ComicIndex)