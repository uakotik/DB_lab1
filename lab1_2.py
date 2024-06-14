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

def in_place(thread_id):
    conn =psycopg2.connect(user=db.username,password=db.password,dbname=db.database)
    cursor = conn.cursor()
    for i in range(10000):
        cursor.execute("UPDATE user_counter SET counter = counter + 1 WHERE user_id = %s", (1,))
        conn.commit()
    cursor.close()
    conn.close()

def main():
    setup_database()

    start_time = time.time()
    threads = []
    for i in range(10):
        thread = threading.Thread(target=in_place, args=(i,))
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