import peewee 
import urllib.parse
import os

urllib.parse.uses_netloc.append('postgres')
url = urllib.parse.urlparse(os.environ['DATABASE_URL'])

db = peewee.PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)

#db = peewee.PostgresqlDatabase(app.config['DATABASE'])

class Thread(peewee.Model):
    title = peewee.TextField()
    create_date = peewee.DateTimeField()
    latest_date = peewee.DateTimeField()
    
    class Meta:
        database = db
        
class Piece(peewee.Model):
    thread = peewee.ForeignKeyField(Thread)
    content = peewee.TextField()
    colour = peewee.TextField()
    author = peewee.TextField()
    date = peewee.DateTimeField()
        
    class Meta:
        database = db
        
if __name__ == "__main__":
    try:
        Thread.create_table()
    except peewee.OperationalError:
        print("Thread table already exists")
        
    try:
        Piece.create_table()
    except peewee.OperationalError:
        print("Piece table already exists")