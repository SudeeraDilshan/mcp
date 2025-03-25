from db_utils import get_customers, get_customer_by_id, add_customer, update_customer, delete_customer, get_customer_by_name
from textwrap import dedent

async def list_customers() -> str:
    """List all customers in the database.
    
    Args:
        None
    """
    customers = await get_customers()
    
    if not customers:
        return "No customers found in the database."
    
    result = "Customers:\n"
    for customer in customers:
        result += dedent(f"""
        ID: {customer.get('id')}
        Name: {customer.get('name', 'N/A')}
        Email: {customer.get('email', 'N/A')}
        Age: {customer.get('age', 'N/A')}
        Prefer Package: {customer.get('prefer_package', 'N/A')}
        ---
        """)
    
    return result

async def get_customer(customer_id: int) -> str:
    """Get details of a specific customer by ID.
    
    Args:
        customer_id: Unique identifier of the customer to retrieve
    """
    customer = await get_customer_by_id(customer_id)
    
    if not customer:
        return f"No customer found with ID: {customer_id}"
    
    return dedent(f"""
    Customer Details:
    ID: {customer.get('id')}
    Name: {customer.get('name', 'N/A')}
    Email: {customer.get('email', 'N/A')}
    Age: {customer.get('age', 'N/A')}
    Prefer Package: {customer.get('prefer_package', 'N/A')}
    """)

async def create_customer(name: str, email: str, age: int = None, prefer_package: int = None) -> str:
    """Create a new customer in the database.
    
    Args:
        name: Customer's full name
        email: Customer's email address
        age: Customer's age (optional)
        prefer_package: Customer's preferred package ID (optional)
    """
    if not name or not email:
        return "Error: Customer name and email are required."
    
    customer = await add_customer(name, email, age ,prefer_package)
    
    if not customer:
        return "Failed to create customer. Please check database connection and try again."
    
    return dedent(f"""
    Customer created successfully:
    ID: {customer.get('id')}
    Name: {customer.get('name')}
    Email: {customer.get('email')}
    Age: {customer.get('age', 'N/A')}
    Prefer Package: {customer.get('prefer_package', 'N/A')}
    """)

async def modify_customer(customer_id: int, name: str = None, email: str = None, age: int = None, prefer_package: int = None) -> str:
    """Update an existing customer's information.
    
    Args:
        customer_id: Unique identifier of the customer to update
        name: New customer name (optional)
        email: New customer email (optional)
        age: New customer age (optional)
        prefer_package: New preferred package ID (optional)
    """
    if not any([name, email, age,prefer_package]):
        return "Error: At least one field (name, email, or phone) must be provided for update."
    
    customer = await update_customer(customer_id, name, email, age,prefer_package)
    
    if not customer:
        return f"Failed to update customer with ID: {customer_id}. Customer may not exist."
    
    return dedent(f"""
    Customer updated successfully:
    ID: {customer.get('id')}
    Name: {customer.get('name')}
    Email: {customer.get('email')}
    Age: {customer.get('age', 'N/A')}
    Prefer Package: {customer.get('prefer_package', 'N/A')}
    """)

async def remove_customer(customer_id: int) -> str:
    """Remove a customer from the database.
    
    Args:
        customer_id: Unique identifier of the customer to delete
    """
    success = await delete_customer(customer_id)
    
    if not success:
        return f"Failed to delete customer with ID: {customer_id}. Customer may not exist."
    
    return f"Customer with ID: {customer_id} has been successfully deleted."

async def find_customers_by_name(name: str) -> str:
    """Find customers by name (full or partial match).
    
    Args:
        name: Full or partial customer name to search for
    """
    if not name:
        return "Error: Customer name is required for searching."
    
    customers = await get_customer_by_name(name)
    
    if not customers:
        return f"No customers found with name containing: '{name}'"
    
    result = f"Found {len(customers)} customer(s) matching '{name}':\n"
    for customer in customers:
        result += dedent(f"""
        ID: {customer.get('id')}
        Name: {customer.get('name', 'N/A')}
        Email: {customer.get('email', 'N/A')}
        Age: {customer.get('age', 'N/A')}
        Prefer Package: {customer.get('prefer_package', 'N/A')}
        ---
        """)
    
    return result
