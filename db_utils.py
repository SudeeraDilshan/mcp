import asyncpg
from typing import List, Dict, Any, Optional
import logging

# Database connection parameters
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "root",  # Make sure this matches your PostgreSQL password
    "database": "postgres"   # Make sure this database exists
}

async def get_connection_pool():
    """Create and return a connection pool to the PostgreSQL database."""
    try:
        pool = await asyncpg.create_pool(**DB_CONFIG)
        return pool
    except Exception as e:
        logging.error(f"Failed to create database connection pool: {e}")
        return None

async def get_customers() -> List[Dict[str, Any]]:
    """Retrieve all customers from the customers table."""
    pool = await get_connection_pool()
    if not pool:
        return []
    
    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM customers")
            # Convert to list of dictionaries
            customers = [dict(row) for row in rows]
            return customers
    except Exception as e:
        logging.error(f"Database query error: {e}")
        return []
    finally:
        await pool.close()

async def get_customer_by_id(customer_id: int) -> Optional[Dict[str, Any]]: 
    """Retrieve a customer by their ID."""
    pool = await get_connection_pool()
    if not pool:
        return None
    
    try:
        async with pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM customers WHERE id = $1", customer_id)
            return dict(row) if row else None
    except Exception as e:
        logging.error(f"Database query error: {e}")
        return None
    finally:
        await pool.close()

async def get_customer_by_name(name: str) -> List[Dict[str, Any]]:
    """Retrieve customers by their name."""
    pool = await get_connection_pool()
    if not pool:
        return []
    
    try:
        async with pool.acquire() as conn:
            # Use ILIKE for case-insensitive search with pattern matching
            rows = await conn.fetch("SELECT * FROM customers WHERE name ILIKE $1", f"%{name}%")
            customers = [dict(row) for row in rows]
            return customers
    except Exception as e:
        logging.error(f"Database query error: {e}")
        return []
    finally:
        await pool.close()

async def add_customer(name: str, email: str, age: int = None,prefer_package: int=None) -> Optional[Dict[str, Any]]:
    """Add a new customer to the database."""
    pool = await get_connection_pool()
    if not pool:
        return None
    
    try:
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "INSERT INTO customers (name, email, age, prefer_package) VALUES ($1, $2, $3, $4) RETURNING *",
                name, email, age, prefer_package
            )
            return dict(row) if row else None
    except Exception as e:
        logging.error(f"Database insert error: {e}")
        return None
    finally:
        await pool.close()

async def update_customer(customer_id: int, name: str = None, email: str = None, age: int = None, prefer_package: int=None) -> Optional[Dict[str, Any]]:
    """Update an existing customer."""
    pool = await get_connection_pool()
    if not pool:
        return None
    
    try:
        async with pool.acquire() as conn:
            # Get current values
            current = await conn.fetchrow("SELECT id,name, email, age, prefer_package FROM customers WHERE id = $1", customer_id)
            if not current:
                return None
            
            # Update with new values or keep existing ones
            new_name = name if name is not None else current['name']
            new_email = email if email is not None else current['email']
            new_age = age if age is not None else current['age']
            new_prefer_package = prefer_package if prefer_package is not None else current['prefer_package']
            
            row = await conn.fetchrow(
                "UPDATE customers SET name = $1, email = $2, age = $3, prefer_package = $5 WHERE id = $4 RETURNING *",
                new_name, new_email, new_age, customer_id, new_prefer_package
            )
            return dict(row) if row else None
    except Exception as e:
        logging.error(f"Database update error: {e}")
        return None
    finally:
        await pool.close()

async def delete_customer(customer_id: int) -> bool:
    """Delete a customer by their ID."""
    pool = await get_connection_pool()
    if not pool:
        return False
    
    try:
        async with pool.acquire() as conn:
            result = await conn.execute("DELETE FROM customers WHERE id = $1", customer_id)
            # Check if any rows were affected
            return 'DELETE' in result
    except Exception as e:
        logging.error(f"Database delete error: {e}")
        return False
    finally:
        await pool.close()
