from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://username:password@localhost/dbname"
)
db = SQLAlchemy(app)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    area = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=False)

@app.route("/", methods=['GET', 'POST'])
def home():
    cities = db.session.query(Property.city.distinct()).order_by(Property.city).all()
    cities = [city[0] for city in cities]
    
    selected_city = request.form.get('city')
    selected_district = request.form.get('district')
    
    if selected_city:
        districts = db.session.query(Property.district.distinct()).filter(Property.city == selected_city).order_by(Property.district).all()
        districts = [district[0] for district in districts]
        
        if selected_district:
            properties = Property.query.filter_by(city=selected_city, district=selected_district).all()
        else:
            properties = Property.query.filter_by(city=selected_city).all()
    else:
        districts = []
        properties = Property.query.all()

    return render_template("home.html", properties=properties, cities=cities, districts=districts, 
                           selected_city=selected_city, selected_district=selected_district)

if __name__ == "__main__":
    app.run(debug=True)