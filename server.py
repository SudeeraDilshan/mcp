from mcp.server.fastmcp import FastMCP
from tools import get_alerts, get_forecast
from db_tools import list_customers, get_customer, create_customer, modify_customer, remove_customer, find_customers_by_name

# Initialize FastMCP server
mcp = FastMCP("weather")

# Attach weather tools
mcp.add_tool(get_alerts, name="Get-Weather-Alerts", description="Get weather alerts for a US state")
mcp.add_tool(get_forecast, name="Get-Forecast", description="Get weather forecast for a location by coordinates")

# Attach database tools
mcp.add_tool(list_customers, name="List-Customers", description="List all customers in the database")
mcp.add_tool(get_customer, name="Get-Customer", description="Get details of a specific customer by ID")
mcp.add_tool(find_customers_by_name, name="Find-Customers-By-Name", description="Find customers by full or partial name match")
mcp.add_tool(create_customer, name="Create-Customer", description="Create a new customer in the database")
mcp.add_tool(modify_customer, name="Update-Customer", description="Update an existing customer's information")
mcp.add_tool(remove_customer, name="Delete-Customer", description="Remove a customer from the database")

if __name__ == "__main__":
    # Run the server
    mcp.run(transport='stdio')
