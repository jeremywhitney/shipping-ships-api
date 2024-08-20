import sqlite3
import json


def update_ship(id, ship_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Ship
                SET
                    name = ?,
                    hauler_id = ?
            WHERE id = ?
            """,
            (ship_data["name"], ship_data["hauler_id"], id),
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False


def delete_ship(pk):
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        DELETE FROM Ship WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def list_ships(url):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Check if _expand query parameter is present
        expand = url["query_params"].get("_expand", [""])[0]

        if expand == "hauler":
            db_cursor.execute(
                """
            SELECT
                s.id,
                s.name,
                s.hauler_id,
                h.id haulerId,
                h.name haulerName,
                h.dock_id
            FROM Ship s
            JOIN Hauler h
                ON h.id = s.hauler_id
            """
            )
        else:
            db_cursor.execute(
                """
            SELECT
                s.id, 
                s.name, 
                s.hauler_id 
            FROM Ship s
            """
            )
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        ships = []
        for row in query_results:
            ship = {"id": row["id"], "name": row["name"], "hauler_id": row["hauler_id"]}

            if expand == "hauler":
                # Only add hauler data if _expand is set to "hauler"
                hauler = {
                    "id": row["haulerId"],
                    "name": row["haulerName"],
                    "dockId": row["dock_id"],
                }
                ship["hauler"] = hauler

            ships.append(ship)

        # Serialize Python list to JSON encoded string
        serialized_ships = json.dumps(ships)

    return serialized_ships


def retrieve_ship(pk, url):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Check if _expand query parameter is present
        expand = url["query_params"].get("_expand", [""])[0]

        if expand == "hauler":
            db_cursor.execute(
                """
            SELECT
                s.id,
                s.name,
                s.hauler_id,
                h.id haulerId,
                h.name haulerName,
                h.dock_id
            FROM Ship s
            JOIN Hauler h
                ON h.id = s.hauler_id
            WHERE s.id = ?
            """,
                (pk,),
            )
        else:
            db_cursor.execute(
                """SELECT
                s.id,
                s.name,
                s.hauler_id
            FROM Ship s
            WHERE s.id = ?
            """,
                (pk,),
            )
        query_result = db_cursor.fetchone()

        if query_result:
            ship = {
                "id": query_result["id"],
                "name": query_result["name"],
                "hauler_id": query_result["hauler_id"],
            }

            if expand == "hauler":
                # Add hauler data if _expand is set to "hauler"
                hauler = {
                    "id": query_result["haulerId"],
                    "name": query_result["haulerName"],
                    "dockId": query_result["dock_id"],
                }
                ship["hauler"] = hauler

            # Serialize Python dict to JSON encoded string
            serialized_ship = json.dumps(ship)
        else:
            serialized_ship = json.dumps({})  # Return empty object if no result

    return serialized_ship


def create_ship(ship_data):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Ship (name, hauler_id)
            VALUES(?, ?)
            """,
            (ship_data["name"], ship_data["hauler_id"]),
        )

        conn.commit()
        return True if db_cursor.rowcount > 0 else False
