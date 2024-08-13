from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import time
import logging
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
db = SQLAlchemy(app)

# Setting up logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Model definition
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    domain = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.Integer, nullable=False)
    date_updated = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website,
            'domain': self.domain,
            'date_created': self.date_created,
            'date_updated': self.date_updated
        }

# Function to seed the database with mock data
def seed_db():
    with app.app_context():
        db.create_all()

        if not Company.query.first():
            for _ in range(300):
                name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                website = f"http://{name.lower()}.com"
                domain = name.lower() + ".com"
                date_created = int(time.time() * 1000)
                date_updated = date_created + random.randint(0, 1000000000)  # some future dates
                company = Company(
                    name=name,
                    website=website,
                    domain=domain,
                    date_created=date_created,
                    date_updated=date_updated
                )
                db.session.add(company)
            db.session.commit()

# GET endpoint to filter and sort records
@app.route('/companies', methods=['GET'])
def get_companies():
    date_updated = request.args.get('date_updated')
    
    if date_updated:
        companies = Company.query.filter(Company.date_updated >= int(date_updated)).order_by(Company.date_updated.asc()).all()
    else:
        companies = Company.query.order_by(Company.date_updated.asc()).all()
    
    response = jsonify([company.to_dict() for company in companies])

    # Logging the request
    log_message = f"GET /companies - Params: date_updated={date_updated}"
    app.logger.info(log_message)
    print(log_message)

    return response

# Seed the database when the application starts
if __name__ == '__main__':
    seed_db()  # Seed the database
    app.run(debug=True)
