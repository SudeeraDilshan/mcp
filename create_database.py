import asyncio
import asyncpg

async def create_database():
    """Create the customers database if it doesn't exist."""
    try:
        # Connect to the default PostgreSQL database
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password="root",
            database="postgres"  # Connect to default database first
        )
        
        # Set autocommit mode for database creation
        await conn.execute("CREATE DATABASE customers")
        print("Database 'customers' created successfully.")
        
        await conn.close()
    except asyncpg.exceptions.DuplicateDatabaseError:
        print("Database 'customers' already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    # Run the async function
    asyncio.run(create_database())
