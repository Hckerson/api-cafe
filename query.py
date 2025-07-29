import os
from db import Database
from operator import itemgetter
from dataclasses import dataclass, asdict

# -An instance of the Database(postgres) class
port = int(os.environ.get("PG_PORT", 5432))
db = Database(
    name=os.environ['DATABASE'], host=os.environ['HOSTNAME'], password=os.environ['PASSWORD'], user=os.environ['USERNAME'], port=port
)
cursor = db.get_connection()


@dataclass
class Cafe:
    id: int
    name: str
    map_url: str
    img_url: str
    location: str
    has_sockets: int
    has_toilet: int
    has_wifi: int
    can_take_calls: int
    seats: str
    coffee_price: str


def get_random_cafe():
    """
    Get a randomly selected Cafe
    """
    cursor.execute("SELECT * FROM cafe ORDER BY RANDOM() LIMIT 1;")
    row = cursor.fetchone()
    if row:
        cafe = Cafe(*row)
        return asdict(cafe)
    else:
        return None


def get_all_cafe():
    """
    Returns all cafe in the database
    """
    cursor.execute("SELECT * FROM cafe")
    rows = cursor.fetchall()
    cafes = [asdict(Cafe(*row)) for row in rows]
    return cafes


def get_cafe_by_location(location: str):
    """
    Get a cafe by location
    """
    cursor.execute("SELECT * FROM cafe WHERE location = %s", (location.title(),))
    rows = cursor.fetchall()
    if rows:
        cafes = [asdict(Cafe(*row)) for row in rows]
        return cafes
    else:
        return None


def add_new_cafe(formdata: dict):
    """
      Add a new cafe to the database
      Args:
        formdata (dict): A dictionary containing cafe details
      Returns:
        None
    """
    (
        name,
        map_url,
        img_url,
        location,
        has_sockets,
        has_toilet,
        has_wifi,
        can_take_calls,
        seats,
        coffee_price,
    ) = itemgetter(
        "name",
        "map_url",
        "img_url",
        "location",
        "has_sockets",
        "has_toilet",
        "has_wifi",
        "can_take_calls",
        "seats",
        "coffee_price",
    )(
        formdata
    )
    cursor.execute(
        """
        INSERT INTO cafe (name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (
            name,
            map_url,
            img_url,
            location.title(),
            has_sockets,
            has_toilet,
            has_wifi,
            can_take_calls,
            seats,
            coffee_price,
        ),
    )
    db.connection.commit()
    

def update_cafe_price(new_price: str,id: int):
    """"
      Updates a cafe's coffee price
      Args:
        id: identification no of the cafe to be updated
      Returns:
        
    """
    try:    
      cursor.execute('UPDATE cafe SET coffee_price = %s WHERE id = %s', (new_price, id))
      if cursor.rowcount == 0:
          db.connection.rollback()
          return f"Cafe with id {id} not found"
      db.connection.commit()
      return "success"
    except Exception as e:
        print(f"An error occurred: {e.__class__.__name__} - {e}")
        db.connection.rollback()
        return "failed"

        
def report_closed(cafe_id:int):
    """
      Report a cafe as closed
      Args:
        id: identification no of the cafe to be reported as closed
      Returns:
        None
    """
    cursor.execute("DELETE FROM cafe WHERE id = %s", (cafe_id,))
    if cursor.rowcount == 0:
        db.connection.rollback()
        return f"Cafe with id {cafe_id} not found"
    db.connection.commit()
    return "success"
