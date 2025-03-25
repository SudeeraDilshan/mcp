import asyncio
import asyncpg
from db_utils import DB_CONFIG

async def create_tables():
    """Create the necessary database tables if they don't exist."""
    try:
        # Connect to the database
        conn = await asyncpg.connect(**DB_CONFIG)
        
        # Create the customers table if it doesn't exist
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER,
                prefer_package INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        print("Database tables initialized successfully.")
        
        # Close the connection
        await conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    # Run the async function
    asyncio.run(create_tables())
