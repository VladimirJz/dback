from asyncio import open_connection
from db.jobs import backup, rotation

r=rotation()
b=backup()
b.run()
# r.run()
