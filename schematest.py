import peewee 
db = peewee.SqliteDatabase('stories.db')

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
    except OperationalError:
        print("Thread table already exists")
        
    try:
        Piece.create_table()
    except OperationalError:
        print("Piece table already exists")