from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
import bs4

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'
Bootstrap(app)

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

#-------------------------------FORMS-------------------------------#

#FILTER FORM
class FilterForm(FlaskForm):
    location = StringField("Location")
    toilet = BooleanField("Toilets")
    wifi = BooleanField("Wifi")
    sockets = BooleanField("Sockets")
    calls = BooleanField("Calls")
    submit = SubmitField("Filter")


#ADD CAFE FORM
class CafeForm(FlaskForm):
     cafe = StringField("Cafe Name", validators=[DataRequired()])
     map_url = StringField("Map URL (click the cafe's share link on google maps. Then click the embed button and copy and paste the html here)", validators=[DataRequired()])
     img_url = StringField("IMG URL", validators=[DataRequired()])
     location = StringField("Location", validators=[DataRequired()])
     has_sockets = BooleanField("Does cafe have electric outlets?", validators=[DataRequired()])
     has_toilets = BooleanField("Does cafe have toilets?", validators=[DataRequired()])
     has_wifi = BooleanField("Does cafe have Wifi?", validators=[DataRequired()])
     can_take_calls = BooleanField("Can you take calls here?", validators=[DataRequired()])
     seats = StringField("How many seats does cafe have? (ex: 10-20, 20-30, 50+)", validators=[DataRequired()])
     coffee_price = StringField("What is the price of a regular coffee here?", validators=[DataRequired()])
     submit = SubmitField("Add Cafe")
#-------------------------------ROUTES-------------------------------#


#HOME
@app.route("/")
def home():
    return render_template("index.html", )

#html route to show all cafes in db
@app.route('/all', methods=['GET','POST'])
def all_cafes():
    form = FilterForm()
    if form.validate_on_submit():
        #Temporary brute filter till I think of better filter code
        if form.validate_on_submit():
            if form.location.data == "":
                cafe_list = Cafe.query.filter_by(has_toilet=form.toilet.data,
                                 has_wifi=form.wifi.data,
                                 has_sockets=form.sockets.data,
                                 can_take_calls=form.calls.data)
                return render_template("all.html", cafes=cafe_list, form=form)
            else:
                cafe_list = Cafe.query.filter_by(location=form.location.data,
                                     has_toilet=form.toilet.data,
                                     has_wifi=form.wifi.data,
                                     has_sockets=form.sockets.data,
                                     can_take_calls=form.calls.data)
                return render_template("all.html", cafes=cafe_list, form=form)
    cafe_list = db.session.query(Cafe).all()
    
    return render_template("all.html", cafes=cafe_list, form=form)

#cafe link
@app.route('/page/<int:cafe_id>')
def page(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    return render_template("cafe.html", cafe=cafe)


#add a cafe using post method
@app.route('/add', methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():

        #--------use beautiful soup to obtain ifram embed html from google maps-----#
        #Parse the data to get the src to be saved into database which is then grab in the
        #cafe.html to display a map
        html = form.map_url.data
        print(html)
        soup = bs4.BeautifulSoup(html, "html.parser")
        map_data = soup.iframe['src']

        #-------add cafe into the database-----#
        new_cafe = Cafe(
            name=form.cafe.data,
            map_url=map_data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=form.has_toilets.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("all_cafes"))
    return render_template("add.html", form=form)


@app.route('/edit/<int:cafe_id>', methods=['GET', 'POST'])
def edit_cafe(cafe_id):
    pass






if __name__ == "__main__":
    app.run(debug=True)