import dbcreds
import mariadb
from flask import Flask, request, Response
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/api/tweets', methods=["GET", "POST", "PATCH", "DELETE"])
def tweet_feed():
    if request.method == "GET":
        conn = None
        cursor = None
        tweet_feed = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tweet_feed")
            tweet_feed = cursor.fetchall()
        except Exception as error:
            print("Something Went Wrong: ")
            print(error)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            if (tweet_feed != None):
                return Response(json.dumps(tweet_feed, default=str), mimetype="application/json", status=200)
            else:
                return Response("There Has Been An Error", mimetype="text/html", status=500)
    elif request.method == "POST":
        conn = None
        cursor = None
        content = request.json.get("content")
        date_created = request.json.get("date_created")
        tweet_id = request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tweet_feed (content, date_created) VALUES (?, ?)", [
                           content, date_created])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Oops! Something Went Wrong: ")
            print(error)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success! Your Tweet Has Been Added", mimetype="text/html", status=201)
            else:
                return Response("Error! Your Tweet Has Not Been Added", mimetype="text/html", status=500)
    elif request.method == "PATCH":
        conn = None
        cursor = None
        content = request.json.get("content")
        date_created = request.json.get("date_created")
        tweet_id = request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            if content != "" and content != None:
                cursor.execute("UPDATE tweet_feed SET content=? WHERE id=?", [
                               content, tweet_id])
            if date_created != "" and date_created != None:
                cursor.execute("UPDATE tweet_feed SET date_created=? WHERE id=?", [
                               date_created, tweed_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Error! Somtehing Went Wrong")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows != 1):
                return Response("Success! Updated", mimetype="text/html", status=204)
            else:
                return Response("Error! Updating Failed", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        conn = None
        cursor = None
        tweed_id = request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tweet_feed WHERE id=?", [tweed_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Error... Something Went Wrong")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success... Deleted", mimetype="text/html", status=204)
            else:
                return Response("Error... Delete Request Failed", mimetype="text/html", status=500)
