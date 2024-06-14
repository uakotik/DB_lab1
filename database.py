username = 'student01'
password = '1'
database = 'DB_LAB1'

sqldrop = '''
DROP TABLE IF EXISTS user_counter
'''
sqlcreate = '''
CREATE TABLE user_counter (
    user_id SERIAL PRIMARY KEY, 
    counter INTEGER NOT NULL,   
    version INTEGER NOT NULL 
)
'''
sqlinsert = '''
INSERT INTO user_counter (user_id, counter, version) VALUES (1, 0, 0)
'''