import peewee

database = peewee.SqliteDatabase('wee.db')

class Artist(peewee.Model):
    name = peewee.TextField()
    
    class Meta:
        databse = database
        
class Album(peewee.Model):
    artist = peewee.ForeignKeyField(Artist)
    title = peewee.TextField()
    release_date = peewee.DateTimeField()
    publisher = peewee.TextField()
    media_type = peewee.TextField()
    
    class Meta:
        database = database
        
if __name__ == "__main__":
    try:
        Artist.create_table()
    except peewee.OperationalError:
        print("Artist table already exists!")
        
    try:
        Album.create_table()
    except peewee.OperationalError:
        print("Album table already exists!")