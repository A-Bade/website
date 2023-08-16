from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///search_history.db'
db = SQLAlchemy(app)

class SearchTerm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(120), nullable=False)

@app.route('/saveSearch', methods=['POST'])
def save_search():
    term = request.json.get('term')
    if term:
        new_search = SearchTerm(term=term)
        db.session.add(new_search)
        db.session.commit()
        return jsonify({"message": "Search saved"}), 200
    return jsonify({"error": "Invalid data"}), 400

@app.route('/getSearchHistory', methods=['GET'])
def get_search_history():
    terms = SearchTerm.query.all()
    return jsonify([t.term for t in terms])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
