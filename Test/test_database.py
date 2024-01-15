import asyncio
from database import Database

async def test_database_operations():
    # Create an instance of the Database class
    my_db = Database('test.db')

    # Connect to the database
    connection = await my_db.connect()
    if connection:
        try:
            # Execute CREATE TABLE query
            create_table_query = '''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL
                )
            '''
            await my_db.execute_query(connection, create_table_query)

            # Execute INSERT query
            insert_query = 'INSERT INTO users (username) VALUES (?)'
            await my_db.execute_query(connection, insert_query, 'JohnDoe')

            # Execute SELECT query
            select_query = 'SELECT * FROM users'
            result = await my_db.execute_query(connection, select_query)
            print(result)
        finally:
            # Close the connection
            await my_db.close(connection)

if __name__ == "__main__":
    asyncio.run(test_database_operations())
