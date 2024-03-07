from flask import Flask, render_template

#Imports
import pymongo
import os

#Création de l'application
app = Flask("TravelAgency")

#Connection à la bdd
mongo = pymongo.MongoClient(os.getenv("MONGO_KEY"))


@app.route('/')
def index():
  return render_template("index.html")


@app.route('/login')
def login():
  return render_template("login.html")


@app.route('/logout')
def logout():
  return render_template("index.html")


@app.route('/register')
def register():
  return render_template("register.html")


@app.route('/continent')
def continent():
  return render_template("continent.html")


@app.route('/destination')
def destination():
  return render_template("destination.html")


app.run(host='0.0.0.0', port=81)
