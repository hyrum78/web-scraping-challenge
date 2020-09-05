from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# sip the flask
app = Flask(__name__)

# PyMongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# route for index.html template
@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data  = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=destination_data )


# scrape route
@app.route("/scrape")
def scrape():

    collection = mongo.db.collection

    # Run the scrape function
    mars_stuff = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_stuff, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)