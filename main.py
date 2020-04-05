from bottle import route, run, request
import sqlite3
import datetime
import hashlib

#Routing
@route('/stock')
def stock():
    store_id = request.query.storeId
    shopping_list = request.query.shoppingList
    shopping_list_as_list = shopping_list.split(" ")

    stock_data = {}
    updated_data = {}

    for i in range(len(shopping_list_as_list)):
        if check_if_item_in_stock(shopping_list_as_list[i]):
            stock_data[shopping_list_as_list[i]] = "In Stock"
        else:
            stock_data[shopping_list_as_list[i]] = "Out of Stock"
        updated_data[shopping_list_as_list[i]] = get_update((shopping_list_as_list[i]))

    return {
        "storeId": store_id,
        "stockData": stock_data,
        "updateData": updated_data,
        "account": account
    }

@route("/update")
def update():
    item_id = request.query.itemId
    value = request.query.value

    conn = sqlite3.connect("shoppingAid.db")
    c = conn.cursor()

    try:
        date_long = datetime.datetime.now()
        date = date_long.strftime("%c")
        c.execute("UPDATE items SET inStock = " + "'" + value + "'" + " WHERE id= " + "'" + item_id + "'")
        c.execute("UPDATE items SET updated = " + "'" + date + "'" + " WHERE id= " + "'" + item_id + "'")
        conn.commit()

        return {"completion": "succeeded", "updatedStock": value, "updatedTime": date}
    except:
        return {"completion": "failed"}

@route("/onboard", method="POST")
def onboard():
    username = request.forms.get("username")
    password = request.forms.get("password")

    password_hashed = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect("shoppingAid.db")
    c = conn.cursor()

    c.execute("SELECT * FROM accounts WHERE username=" + "'" + username + "'")
    results = c.fetchall()

    if results == []:
        c.execute("INSERT INTO accounts(username, password) VALUES(?, ?)", (username, password_hashed))
        conn.commit()
    else:
        return {"completion": "Username Taken"}
    return {"completion": "Success"}

@route("/login", method="POST")
def login():
    username = request.forms.get("username")
    password = request.forms.get("password")

    password_hashed = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect("shoppingAid.db")
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM accounts WHERE username=" + "'" + username + "'")
        results = c.fetchall()

        if results != []:
            if password_hashed == results[0][1]:
                return {"completion": "success", "username": username}
            else:
                return {"completion": "failed"}
    except:
        return {"completion": "error"}

@route("/savelist")
def savelist():
    username = request.query.username
    list = request.query.list

    list_id = str(create_list_id(username, list))

    conn = sqlite3.connect("shoppingAid.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO lists(username, listId, list) VALUES(?, ?, ?)", (username, list_id, list))
        conn.commit()
        return {"completed": "success", "listId": list_id}
    except:
        return {"completion": "failed", "listId": "null"}

@route("/getlist")
def getlist():
    username = request.query.username
    list_id = request.query.listId

    conn = sqlite3.connect("shoppingAid.db")
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM lists WHERE username=" + "'" + username + "'" + " AND listId=" + "'" + list_id + "'")
        results = c.fetchall()

        if results != []:
            return {"list": results[0][2]}
        return {"list": "null"}
    except:
        return {"list": "error"}

#@route("/savefavorite")
#def save_favorite():

#Functions related to database/store stock
def check_if_item_in_stock(item):
    conn = sqlite3.connect("shoppingAid.db")
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE id=" + "'" + item + "'")
    result = c.fetchall()
    if result != []:
        if result[0][3] == "true":
            return True
        else:
            return False
    conn.close()

def get_update(item):
    conn = sqlite3.connect("shoppingAid.db")
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE id=" + "'" + item + "'")
    results = c.fetchall()
    if results != []:
        return results[0][4]

#id for keeping track of lists
def create_list_id(username, list):
    user = username.encode()
    l = list.encode()
    id = hashlib.md5(user + l).hexdigest()

    return id

run(host='localhost', port=1234, reload=True)
