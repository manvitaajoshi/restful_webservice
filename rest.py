import sqlite3
from flask import Flask, jsonify, request


def connect_to_db():
    db_connection = sqlite3.connect('database.db')
    return db_connection


def create_db_table():
    try:
        db_connection = connect_to_db()
        cursor = db_connection.cursor()
        cursor.execute('''
         CREATE TABLE items(
                item_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                price TEXT NOT NULL,
                quantity TEXT NOT NULL,
                discount TEXT NOT NULL
            );
        ''')

        db_connection.commit()
        print("Item table created successfully!")
    except:
        print("Item table creation failed.")
    finally:
        db_connection.close()

def insert_item(item):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO items (name, price, quantity, discount) VALUES (?, ?, ?, ?)", (item['name'], item['price'], item['quantity'], item['discount']))
        conn.commit()
        inserted_item = get_item_by_id(cur.lastrowid)
    except:
        conn().rollback()
    finally:
        conn.close()
    return inserted_item


def get_items():
    items = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM items")
        rows = cur.fetchall()

        for i in rows:
            item = {}
            item["item_id"] = i["item_id"]
            item["name"] = i["name"]
            item["price"] = i["price"]
            item["quantity"] = i["quantity"]
            item["discount"] = i["discount"]
            items.append(item)
    except:
        items = []

    return items


def get_item_by_id(item_id):
    item = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM items WHERE item_id = ?", (item_id,))
        row = cur.fetchone()
        item["item_id"] = row["item_id"]
        item["name"] = row["name"]
        item["price"] = row["price"]
        item["quantity"] = row["quantity"]
        item["discount"] = row["discount"]
    except:
        item = {}
    return item


def update_item(item):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE items SET name = ?, price = ?, quantity = ?, discount = ? WHERE item_id =?", (item['name'], item['price'], item['quantity'], item['discount'], item["item_id"],))
        conn.commit()
        # return the user
        updated_item = get_item_by_id(item["item_id"])
        print(updated_item)
    except:
        conn.rollback()
        updated_item = {}
    finally:
        conn.close()
    return updated_item


def delete_item(item_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from items WHERE item_id = ?", (item_id, ))
        conn.commit()
        message["status"] = "Item deleted successfully!"
    except Exception as e:
        print(e)
        # conn.rollback()
        # message["status"] = "Cannot delete item."
    finally:
        conn.close()

    return message

items = []
item0 = {
    "name": "Beans",
    "price": 300,
    "quantity": 15,
    "discount": 10,
}

item1 = {
    "name": "Legumes",
    "price": 350,
    "quantity": 10,
    "discount": 20,
}

item2 = {
    "name": "Lentils",
    "price": 250,
    "quantity": 30,
    "discount": 15,
}

item3 = {
    "name": "Seaweed",
    "price": 500,
    "quantity": 5,
    "discount": 5,
}

items.append(item0)
items.append(item1)
items.append(item2)
items.append(item3)

create_db_table()

for row in items:
    print(insert_item(row))

app = Flask(__name__)


@app.route('/')
def index():
    return "WELCOME TO VIVA VEGAN STORE!"

@app.route('/items', methods=['GET'])
def get_all_items():
    return jsonify(get_items())


@app.route('/items/<int:item_id>', methods=['GET'])
def get_specific_item(item_id):
    return jsonify(get_item_by_id(item_id))


@app.route('/items/add',methods=['GET', 'POST'])
def add_item_rest():
    item = request.get_json()
    return insert_item(item)

@app.route('/items/add/<string:name>/<int:price>/<int:quantity>/<int:discount>',
           methods=['GET', 'POST'])
def add_item(name, price, quantity, discount):
    item = {
        "name": name,
        "price": price,
        "quantity": quantity,
        "discount": discount
    }
    return jsonify(insert_item(item))

@app.route('/items/update',methods=['GET', 'PUT'])
def update_an_item_rest():
    item = request.get_json()
    return update_item(item)

@app.route('/items/update/<int:itemid>/<string:name>/<int:price>/<int:quantity>/<int:discount>',
           methods=['GET', 'PUT'])
def update_an_item(itemid, name, price, quantity, discount):
    item = {
        "item_id": itemid,
        "name": name,
        "price": price,
        "quantity": quantity,
        "discount": discount
    }
    return jsonify(update_item(item))

@app.route('/items/delete',methods=['GET', 'DELETE'])
def delete_an_item_rest():
    item = request.get_json()
    print(item)
    return delete_item(item["item_id"])

@app.route('/items/delete/<int:item_id>', methods=['GET', 'DELETE'])
def delete_an_item(item_id):
    return jsonify(delete_item(item_id))


if __name__ == "__main__":
    app.run()
