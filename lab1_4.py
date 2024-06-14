import psycopg2
import time
import database as db
import threading

def setup_database():
    conn =psycopg2.connect(user=db.username,password=db.password,dbname=db.database)
    cursor = conn.cursor()
    cursor.execute(db.sqldrop)
    cursor.execute(db.sqlcreate)
    cursor.execute(db.sqlinsert)
    conn.commit()
    cursor.close()
    conn.close()

def optimistic_concurrency(thread_id):
    conn =psycopg2.connect(user=db.username,password=db.password,dbname=db.database)
    cursor = conn.cursor()
    for i in range(10000):
        while True:
            cursor.execute("SELECT counter, version FROM user_counter WHERE user_id = 1")
            result = cursor.fetchone()
            counter = result[0]
            version = result[1]
            counter = counter + 1
            cursor.execute("UPDATE user_counter SET counter = %s, version = %s WHERE user_id = %s AND version = %s",(counter, version + 1, 1, version))
            conn.commit()
            if cursor.rowcount > 0:
                break
    cursor.close()
    conn.close()

def main():
    setup_database()

    start_time = time.time()

    threads = []
    for i in range(10):
        thread = threading.Thread(target=optimistic_concurrency, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time= end_time - start_time
    print("Time:",total_time)

    conn =psycopg2.connect(user=db.username,password=db.password,dbname=db.database)
    cursor = conn.cursor()
    cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1")
    final_counter = cursor.fetchone()[0]
    print(f"Final counter value: {final_counter}")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()