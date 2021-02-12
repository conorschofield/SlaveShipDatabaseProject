from app import app 
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'STr1pes250**'
app.config['MYSQL_DATABASE_DB'] = 'History'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'kbleich'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'abc123'
# app.config['MYSQL_DATABASE_DB'] = 'kbleich'
# app.config['MYSQL_DATABASE_HOST'] = 'ambari-head.csc.calpoly.edu'
mysql.init_app(app)
