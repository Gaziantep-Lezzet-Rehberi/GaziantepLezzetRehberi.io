from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
# Contact form removed — contact page is no longer part of the site
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gaziantep.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Recipe(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), nullable=False)
	slug = db.Column(db.String(160), unique=True, nullable=False)
	category = db.Column(db.String(50), nullable=False)
	is_meat = db.Column(db.Boolean, default=False)
	cook_time = db.Column(db.Integer)
	difficulty = db.Column(db.String(20))
	servings = db.Column(db.Integer)
	description = db.Column(db.Text)
	ingredients = db.Column(db.Text)
	steps = db.Column(db.Text)
	image_url = db.Column(db.String(300))


class Place(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	address = db.Column(db.String(300))
	category = db.Column(db.String(100))
	lat = db.Column(db.Float)
	lng = db.Column(db.Float)
	description = db.Column(db.Text)
	rating = db.Column(db.Float)
	image_url = db.Column(db.String(300))


# ...contact form removed...


@app.route('/')
def index():
	featured = Recipe.query.limit(4).all()
	categories = ['Kebaplar', 'Tatlılar', 'Çorbalar', 'İçecekler']
	return render_template('index.html', featured=featured, categories=categories)


@app.route('/recipes')
def recipes():
	q = request.args.get('q', '')
	category = request.args.get('category', '')
	query = Recipe.query
	if q:
		query = query.filter(Recipe.name.ilike(f'%{q}%'))
	if category:
		query = query.filter(Recipe.category == category)
	items = query.all()
	return render_template('recipes.html', recipes=items, q=q, category=category)


@app.route('/recipes/<int:recipe_id>')
def recipe_detail(recipe_id):
	r = Recipe.query.get_or_404(recipe_id)
	# For demo, find 2 places that match category
	places = Place.query.filter(Place.category.ilike(f'%{r.category}%')).limit(3).all()
	return render_template('recipe_detail.html', recipe=r, places=places)


@app.route('/places')
def places():
	items = Place.query.all()
	return render_template('places.html', places=items)


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/api/recipes')
def api_recipes():
	items = Recipe.query.order_by(Recipe.id).all()
	data = []
	for r in items:
		data.append({
			'id': r.id,
			'name': r.name,
			'slug': r.slug,
			'category': r.category,
			'image_url': r.image_url,
		})
	from flask import jsonify
	return jsonify(data)


# Contact route removed — contact page has been removed from the site


if __name__ == '__main__':
	# Allow overriding host/port via environment variables for easier LAN testing
	host = os.environ.get('FLASK_HOST', '0.0.0.0')
	try:
		port = int(os.environ.get('FLASK_PORT', '5001'))
	except ValueError:
		port = 5001
	debug_env = os.environ.get('FLASK_DEBUG')
	debug = True if debug_env is None else (debug_env.lower() not in ('0', 'false'))
	app.run(host=host, port=port, debug=debug)
	
