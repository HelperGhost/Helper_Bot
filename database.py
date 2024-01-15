import aiosqlite

class Database:
    def __init__(self, db_path):
        self.db = db_path

    async def connect(self):
        try:
            return await aiosqlite.connect(self.db)
        except aiosqlite.Error as e:
            print(f"Error connecting to the database: {e}")
            return None
    
    def path(self, path):
        self.db = path

    async def execute_query(self, conn, query, *args):
        try:
            async with conn.execute(query, args) as cursor:
                return await cursor.fetchall()
        except aiosqlite.Error as e:
            print(f"Error executing query: {e}")
            return None
    
    async def close(self, conn):
        try:
            await conn.close()
            return True
        except aiosqlite.Error as e:
            print(f"Error closing the database connection: {e}")
            return False
