from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#CAFE TABLE BLUEPRINT IN DATABASE
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

# db.create_all()

#HOME
@app.route("/")
def home():
    return render_template("index.html", )

#html route to show all cafes in db
@app.route('/all')
def all_cafes():
    cafe_list= db.session.query(Cafe).all()
    return render_template("all.html", cafes=cafe_list)

#cafe link
@app.route('/page/<int:cafe_id>')
def page(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    return render_template("cafe.html", cafe=cafe)


@app.route('/find')
def find_cafe():
    return render_template("find.html")






if __name__ == "__main__":
    app.run(debug=True)