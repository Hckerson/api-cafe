import psycopg2


class Database:
    """
    Database class to manage connection to postgres
    Attributes:
      name (str): Name of the database
      host (str): Host where the database is located
      password (str): Password for the database user
      user (str): Username for the database
      port (int): Port number for the database connection
    Methods:
      get_connection: Returns a cursor instance to interact with the database
      close_connection: Close the database connection
    """

    def __init__(
        self, name: str, host: str, password: str, user: str, port: int
    ) -> None:

        self.connection = psycopg2.connect(
            dbname=name,
            host=host,
            password=password,
            user=user,
            port=port,
        )
        self.cursor = None
        self.get_connection()

    def get_connection(self):
        # Return the connection object
        self.cursor = self.connection.cursor()
        return self.cursor

    def close_connection(self):
        # Close the cursor and connection to the database
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
