import dbcreds
import mariadb
from flask import Flask, request, Response
import json
from flask_cors import CORS
import string
import random
import datetime


app = Flask(__name__)
CORS(app)


def createToken():
    loginToken = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation) for _ in range(37))
    return loginToken


def createDate():
    created_at = datetime.datetime.now().strftime("%Y-%m-%d")
    return created_at


# Route to '/api/user' --------------------


@app.route('/api/user', methods=["GET", "POST", "PATCH", "DELETE"])
def usersAll():
    if request.method == "GET":
    # This REQUEST is working
        conn = None
        cursor = None
        user_id = request.args.get("user_id")
        user = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            if user_id == user_id:
                cursor.execute("SELECT * FROM user WHERE id=?", [user_id])
            else:
                cursor.execute("SELECT * FROM user")
            users = cursor.fetchall()
            list_users = []
            for user in users:
                 list_users.append({ 
                    "user_id": user[0],
                    "email": user[1],
                    "username": user[2],
                    "bio": user[4],
                    "birthdate": user[5],
                })
        except Exception as error:
            print("GET User Method Failed")
            print(error)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            if (user != None):
                return Response(json.dumps(list_users, default=str), mimetype="application/json", status=200)
            else:
                return Response("GET User Request Failed", mimetype="text/html", status=500)
    elif request.method == "POST":
        # This REQUEST is working
        conn = None
        cursor = None
        email = request.json.get("email")
        username = request.json.get("username")
        password = request.json.get("password")
        bio = request.json.get("bio")
        birthdate = request.json.get("birthdate")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user (email, username, password, bio, birthdate) VALUES (?, ?, ?, ?, ?)", [
                           email, username, password, bio, birthdate])
            rows = cursor.rowcount
            if (rows == 1):
                login_token = createToken()
                user_id = cursor.lastrowid
                cursor.execute("INSERT INTO user_session(login_token, user_id) VALUES(?, ?)", [
                    login_token, user_id])
            conn.commit()
            new_user = {
                "user_id": user_id,
                "email": email,
                "username": username,
                "bio": bio,
                "birthdate": birthdate,
                "loginToken": loginToken
            }
            sendUser = json.dumps(new_user)
        except Exception as error:
            print("POST User Method Failed")
            print(error)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success! User Was Added", mimetype="text/html", status=201)
            else:
                return Response("Error! User Not Added", mimetype="text/html", status=500)
    elif request.method == "PATCH":
        # This REQUEST is PARTIALLY working = whenever I try updating the account, it returns an error of list index is out of range
        conn = None
        cursor = None
        email = request.json.get("email")
        username = request.json.get("username")
        password = request.json.get("password")
        bio = request.json.get("bio")
        birthdate = request.json.get("birthdate")
        loginToken = request.json.get("loginToken")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [loginToken])
            user_id = cursor.fetchall()[0][0]
            if email != "" and email != None:
                cursor.execute(
                "UPDATE user SET email=? WHERE id=?", [email, user_id])
            if username != "" and username != None:
                cursor.execute(
                "UPDATE user SET username=? WHERE id=?", [username, user_id])
            if password != "" and password != None:
                cursor.execute(
                "UPDATE user SET password=? WHERE id=?", [password, user_id])
            if bio != "" and bio != None:
                cursor.execute("UPDATE user SET bio=? WHERE id=?", [
                               bio, user_id])
            if birthdate != "" and birthdate != None:
                cursor.execute(
                "UPDATE user SET birthdate=? WHERE id=?", [birthdate, user_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("PATCH User Method Failed")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success! User Was Updated", mimetype="text/html", status=204)
            else:
                return Response("Error! User Not Updated", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        # This REQUEST is working
        conn = None
        cursor = None
        password = request.json.get("password")
        loginToken = createToken()
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM user WHERE password=?", [password])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("DELETE User Method Failed")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success! User Was Deleted", mimetype="text/html", status=204)
            else:
                return Response("Error! User Not Deleted", mimetype="text/html", status=500)


# Route to '/api/login' ------------------


@app.route('/api/login', methods=["POST", "DELETE"])
def loginAll():
    if request.method == "POST":
        # This REQUEST is working
        conn = None
        cursor = None
        email = request.json.get("email")
        password = request.json.get("password")
        loginToken = createToken()
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM user WHERE email=? AND password=?", [email, password])
            user = cursor.fetchone()
            cursor.execute("INSERT INTO user_session(user_id, login_token) VALUES (?, ?)", [
                           user[0], loginToken])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("POST Login Method Failed")
            print(error)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            if (rows == 1):
                user_logged = {
                    "user_id": user[0],
                    "email": user[0],
                    "username": user[0],
                    "bio": user[0],
                    "birthdate": user[0],
                    "loginToken": loginToken
                }
                return Response(json.dumps(user_logged, default=str), mimetype="application/json", status=200)
            else:
                return Response("Error! Your Login Has Not Been Accepted", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        # This REQUEST is working
        conn = None
        cursor = None
        user_id = request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user WHERE id=?", [id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("DELETE Login Method Failed")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success! Login Was Deleted", mimetype="text/html", status=204)
            else:
                return Response("Error! Login Not Deleted", mimetype="text/html", status=500)


# Route to '/api/follows' ------------------


@app.route('/api/follows', methods=["POST", "DELETE"])
def followAll():
    if request.method == "POST":
        # This REQUEST is working
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        follow_id = request.json.get("follow_id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [loginToken])
            user_id = cursor.fetchone()[0]   
            if user_id != follow_id:
                cursor.execute("INSERT INTO follow (follow_id) VALUES (?)", [
                           follow_id])
                conn.commit()
                rows = cursor.rowcount
        except Exception as error:
            print("POST Follows Method Failed")
            print(error)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success! Follow Was Accepted", mimetype="text/html", status=201)
            else:
                return Response("Error! Follow Not Accepted", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        # This REQUEST is working
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        follow_id = request.json.get("follow_id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [loginToken])
            user_id = cursor.fetchone()[0]      
            cursor.execute("DELETE FROM follow WHERE follow_id=?", [
                           follow_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("DELETE Follow Method Failed")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success! Follow Was Deleted", mimetype="text/html", status=204)
            else:
                return Response("Error! Follow Not Deleted", mimetype="text/html", status=500)


# Route to '/api/likes' ------------------


@app.route('/api/tweet_likes', methods=["POST", "DELETE"])
def likesAll():
    if request.method == "POST":
        # This REQUEST is working
        conn = None
        cursor = None
        tweet_id = request.json.get("tweet_id")
        loginToken = request.json.get("loginToken")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [loginToken])
            user_id = cursor.fetchone()[0]      
            cursor.execute("INSERT INTO tweet_like (tweet_id, user_id) VALUES (?, ?)", [
                           tweet_id, user_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("POST Tweet Likes Method Failed")
            print(error)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success! Tweet Like Was Accepted", mimetype="text/html", status=201)
            else:
                return Response("Error! Tweet Like Not Accepted", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        # This REQUEST is working
        conn = None
        cursor = None
        tweet_id = request.json.get("tweet_id")
        loginToken = request.json.get("loginToken")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [loginToken])
            user_id = cursor.fetchone()[0]
            cursor.execute("DELETE FROM tweet_like WHERE tweet_id=? and user_id=?", [tweet_id, user_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("DELETE Tweet Like Method Failed")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success! Tweet Like Was Deleted", mimetype="text/html", status=204)
            else:
                return Response("Error! Tweet Like Not Deleted", mimetype="text/html", status=500)


# Route to '/api/tweet' -------------------


@app.route('/api/tweet', methods=["GET", "POST", "PATCH", "DELETE"])
def tweet():
    if request.method == "GET":
        # This REQUEST is working
        conn = None
        cursor = None
        tweet = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tweet INNER JOIN user ON tweet.user_id=user.id")
            tweets = cursor.fetchall()
            list_tweets = []
            for tweet in tweets:
                list_tweets.append({
                    "tweet_id": tweet[0],
                    "user_id": tweet[3],
                    "username": tweet[6],
                    "content": tweet[1],
                    "created_at": tweet[2],
                    })
        except Exception as error:
            print("GET Tweet Method Failed")
            print(error)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            if (tweets != None or tweets ==[]):
                return Response(json.dumps(list_tweets, default=str), mimetype="application/json", status=200)
            else:
                return Response("GET Tweet Request Failed", mimetype="text/html", status=500)
    elif request.method == "POST":
        # This REQUEST is working
        conn = None
        cursor = None
        content = request.json.get("content")
        created_at = createDate()
        loginToken = request.json.get("loginToken")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [loginToken])
            user_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO tweet (content, created_at, user_id) VALUES (?, ?, ?)", [
                           content, created_at, user_id ])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("POST Tweet Method Failed")
            print(error)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success! Tweet Was Added", mimetype="text/html", status=201)
            else:
                return Response("Error! Tweet Not Added", mimetype="text/html", status=500)
    elif request.method == "PATCH":
        # This REQUEST is working
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        tweet_id = request.json.get("tweet_id")
        content = request.json.get("content")
        created_at = createDate()
        rows = None        
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [loginToken])
            user_id = cursor.fetchone()[0]
            cursor.execute("UPDATE tweet SET content=?, created_at=? WHERE user_id=? AND id=?", [
                           content, created_at, user_id, tweet_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("PATCH Tweet Method Failed")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                tweet_edited = {
                    "tweet_id": tweet_id,
                    "content": content,
                }
                return Response(json.dumps(tweet_edited, default=str), mimetype="text/html", status=204)
            else:
                return Response("Error! Tweet Not Updated", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        # This REQUEST is working
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        tweet_id = request.json.get("tweet_id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [loginToken])
            user_id = cursor.fetchone()[0]    
            cursor.execute("DELETE FROM tweet WHERE id=? and user_id=?", [tweet_id, user_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("DELETE Tweet Method Failed")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success! Tweet Was Deleted", mimetype="text/html", status=204)
            else:
                return Response("Error! Tweet Not Deleted", mimetype="text/html", status=500)


# Route to '/api/comment' -----------------


@app.route('/api/comment', methods=["GET", "POST", "PATCH", "DELETE"])
def commentAll():
    if request.method == "GET":
        # This REQUEST is working
        conn = None
        cursor = None
        tweet = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM comment INNER JOIN user ON comment.user_id=user.id")
            comments = cursor.fetchall()
            list_comments = []
            for comment in comments:
                list_comments.append({
                    "comment_id": comment[0],
                    "tweet_id": comment[3],
                    "user_id": comment[4],
                    "username": comment[7],
                    "content": comment[1],
                    "created_at": comment[2],
                })
        except Exception as error:
            print("GET Comment Method Failed")
            print(error)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            if (comment != None):
                return Response(json.dumps(list_comments, default=str), mimetype="application/json", status=200)
            else:
                return Response("There Has Been An Error", mimetype="text/html", status=500)
    elif request.method == "POST":
        # This REQUEST is working
        conn = None
        cursor = None
        content = request.json.get("content")
        created_at = createDate()
        loginToken = request.json.get("loginToken")
        tweet_id = request.json.get("tweet_id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [loginToken])
            user_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO comment (content, created_at, user_id, tweet_id) VALUES (?, ?, ?, ?)", [content, created_at, user_id, tweet_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("POST Comment Method Failed")
            print(error)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success! Comment Was Added", mimetype="text/html", status=201)
            else:
                return Response("Error! Comment Not Added", mimetype="text/html", status=500)
    # elif request.method == "PATCH":
        # This REQUEST was NOT made available at front-end for the first part of this project
        # So, there is NO need to create/implement PATCH here
    elif request.method == "DELETE":
        # This REQUEST is working
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        comment_id = request.json.get("comment_id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password,
                                   user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [loginToken])
            user_id = cursor.fetchone()[0]       
            cursor.execute("DELETE FROM comment WHERE user_id=? and id=?", [user_id, comment_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("DELETE Comment Method Failed")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Success! Comment Was Deleted", mimetype="text/html", status=204)
            else:
                return Response("Error! Comment Not Deleted", mimetype="text/html", status=500)
