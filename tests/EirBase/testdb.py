import psycopg2

# Connect to your postgres DB
connection = psycopg2.connect(
    database="eirbase",
    user="postgres",
    password="root",
    host="localhost",
    port="5432",
)

# Open a cursor to perform database operations
cur = connection.cursor()

# Execute a query
cur.execute(
    """SELECT * from scale_readings;
    """
)
query_results = cur.fetchall()
print(query_results)
