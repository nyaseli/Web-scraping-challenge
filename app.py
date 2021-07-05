import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

conn = 'mongodb://localhost:27017/marsDB'


app = Flask(__name__)
mongo = PyMongo(app,conn)


# 1st route homepage
@app.route("/")
def homepage():
    data = mongo.db.collection.find_one()
    return render_template('index.html',mars = data)


# 2nd route: Scrape
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({},mars_data,upsert= True)
    return redirect("/")
   

if __name__ == '__main__':
    app.run(debug =  True)

    

        
