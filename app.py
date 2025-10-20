from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_mysqldb import MySQL
import os


app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')


mysql = MySQL(app)




# @app.route("/")
# def index():
#     return render_template("static/index.html")


@app.route("/test-db")
def test_db():
    return render_template("index.html")
    # message = "MySQL is connected!"
    # try:
    #     cur = mysql.connection.cursor()
    #     cur.execute("SELECT 1")
    #     cur.close()
    # except Exception as e:
    #     message = f"Error connecting to MySQL: {e}"
    # return message



@app.route("/cards", methods=["GET"])
def get_cards():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, heading, date, content FROM cards")
        rows = cur.fetchall()
        cur.close()
        # Convert rows to list of dicts
        cards = [{"id": r[0], "heading": r[1], "date": str(r[2]), "content": r[3]} for r in rows]
        return {"status": "success", "cards": cards}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    
@app.route("/cards", methods=["POST"])
def add_card():
    data = request.get_json()  # get JSON data from frontend
    heading = data.get("heading")
    date = data.get("date")
    content = data.get("content")
    
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO cards (heading, date, content) VALUES (%s, %s, %s)",
            (heading, date, content)
        )
        mysql.connection.commit()
        cur.close()
        return {"status": "success", "message": "Card added!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3306)))
