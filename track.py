from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
db = SQLAlchemy(app)

class Link(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    click_count = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track.py', methods=['POST'])
def create_link():
    original_url = request.form['url']
    tracking_id = str(uuid.uuid4())
    new_link = Link(id=tracking_id, original_url=original_url)
    db.session.add(new_link)
    db.session.commit()
    return f"Tracking link created: /{tracking_id}"

@app.route('/<tracking_id>')
def track_link(tracking_id):
    link = Link.query.get(tracking_id)
    if link:
        link.click_count += 1
        db.session.commit()
        return redirect(link.original_url)
    return "Link not found", 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
