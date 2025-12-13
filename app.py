from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
# Contact form removed — contact page is no longer part of the site
import os
import time
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gaziantep.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Upload folder for recipe images
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.template_global()
def image_url(value):
	"""Normalize stored image value to a public URL.

	- If value is already an absolute URL or starts with /static/, return as-is.
	- If value is a bare filename (e.g. 'patlican.jpg'), return url_for('static', filename='uploads/<name>').
	- If value is None/empty, return None.
	"""
	if not value:
		return None
	# already a public path or full url
	if isinstance(value, str) and (value.startswith('/') or value.startswith('http://') or value.startswith('https://')):
		return value
	# treat as filename stored in DB
	return url_for('static', filename=f'uploads/{value}')

# Ensure template global is present in the Jinja environment (defensive)
app.jinja_env.globals['image_url'] = image_url


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


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password_hash = db.Column(db.String(200), nullable=False)
	is_admin = db.Column(db.Boolean, default=False)

	def set_password(self, password: str):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password: str) -> bool:
		return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
	try:
		return User.query.get(int(user_id))
	except Exception:
		return None


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


def admin_required(view_func):
	"""Simple session-based decorator to require admin login."""
	@wraps(view_func)
	def wrapped_view(*args, **kwargs):
		if not current_user.is_authenticated:
			return redirect(url_for('login', next=request.path))
		if not getattr(current_user, 'is_admin', False):
			flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
			return redirect(url_for('index'))
		return view_func(*args, **kwargs)
	return wrapped_view


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form.get('username', '')
		password = request.form.get('password', '')
		user = User.query.filter_by(username=username).first()
		if user and user.check_password(password):
			login_user(user)
			flash('Giriş başarılı.', 'success')
			next_url = request.args.get('next') or url_for('admin_index')
			return redirect(next_url)
		flash('Kullanıcı adı veya parola hatalı.', 'danger')
	return render_template('login.html')


@app.route('/logout')
def logout():
	logout_user()
	flash('Çıkış yapıldı.', 'info')
	return redirect(url_for('index'))


@app.route('/admin')
@admin_required
def admin_index():
	# Admin index: list recipes in reverse creation order
	recipes = Recipe.query.order_by(Recipe.id.desc()).all()
	return render_template('admin/index.html', recipes=recipes)


@app.route('/admin/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
	# Only admin users may change password here
	if not getattr(current_user, 'is_admin', False):
		flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
		return redirect(url_for('index'))

	if request.method == 'POST':
		current_pw = request.form.get('current_password', '')
		new_pw = request.form.get('new_password', '')
		new_pw2 = request.form.get('new_password2', '')
		if not current_user.check_password(current_pw):
			flash('Mevcut parola hatalı.', 'danger')
			return render_template('change_password.html')
		if new_pw != new_pw2:
			flash('Yeni parolalar eşleşmiyor.', 'danger')
			return render_template('change_password.html')
		if len(new_pw) < 6:
			flash('Yeni parola en az 6 karakter olmalı.', 'danger')
			return render_template('change_password.html')
		# update password
		user = User.query.get(current_user.get_id())
		user.set_password(new_pw)
		db.session.commit()
		flash('Parola başarıyla değiştirildi.', 'success')
		return redirect(url_for('admin_index'))

	return render_template('change_password.html')


@app.route('/admin/add', methods=['GET', 'POST'])
@admin_required
def admin_add():
	if request.method == 'POST':
		name = request.form['name']
		slug = request.form['slug']
		category = request.form['category']
		is_meat = 'is_meat' in request.form
		cook_time = request.form.get('cook_time') or None
		difficulty = request.form.get('difficulty')
		servings = request.form.get('servings') or None
		description = request.form.get('description')
		ingredients = request.form.get('ingredients')
		steps = request.form.get('steps')
		# handle uploaded image (file input named 'resim')
		image_url = None
		image_file = request.files.get('resim')
		if image_file and getattr(image_file, 'filename', None):
			filename = secure_filename(image_file.filename)
			unique = f"{int(time.time())}_{filename}"
			try:
				save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique)
				image_file.save(save_path)
				# store a public URL path
				image_url = f"/static/uploads/{unique}"
			except Exception as e:
				flash(f'Resim kaydedilemedi: {e}', 'danger')

		new_recipe = Recipe(
			name=name,
			slug=slug,
			category=category,
			is_meat=is_meat,
			cook_time=cook_time,
			difficulty=difficulty,
			servings=servings,
			description=description,
			ingredients=ingredients,
			steps=steps,
			image_url=image_url,
		)
		db.session.add(new_recipe)
		db.session.commit()
		flash("Yeni yemek eklendi!", "success")
		return redirect(url_for('admin_index'))

	return render_template('admin/add.html')


@app.route('/admin/delete/<int:recipe_id>', methods=['POST'])
@admin_required
def admin_delete(recipe_id):
	recipe = Recipe.query.get_or_404(recipe_id)
	db.session.delete(recipe)
	db.session.commit()
	flash("Yemek silindi!", "danger")
	return redirect(url_for('admin_index'))


@app.route('/admin/edit/<int:recipe_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit(recipe_id):
	recipe = Recipe.query.get_or_404(recipe_id)

	if request.method == 'POST':
		recipe.name = request.form['name']
		recipe.slug = request.form['slug']
		recipe.category = request.form['category']
		recipe.is_meat = 'is_meat' in request.form
		recipe.cook_time = request.form.get('cook_time') or None
		recipe.difficulty = request.form.get('difficulty')
		recipe.servings = request.form.get('servings') or None
		recipe.description = request.form.get('description')
		recipe.ingredients = request.form.get('ingredients')
		recipe.steps = request.form.get('steps')
		# image handling: keep existing unless a new file uploaded or remove requested
		remove = 'remove_image' in request.form
		image_file = request.files.get('resim')
		if image_file and getattr(image_file, 'filename', None):
			filename = secure_filename(image_file.filename)
			unique = f"{int(time.time())}_{filename}"
			old_image = recipe.image_url
			try:
				save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique)
				image_file.save(save_path)
				# set public path
				recipe.image_url = f"/static/uploads/{unique}"
				# remove old file if different
				if old_image:
					try:
						old_fname = os.path.basename(old_image)
						old_path = os.path.join(app.config['UPLOAD_FOLDER'], old_fname)
						if os.path.exists(old_path) and old_path != save_path:
							os.remove(old_path)
					except Exception:
						pass
			except Exception as e:
				flash(f'Resim kaydedilemedi: {e}', 'danger')
		elif remove:
			# delete existing file if present
			if recipe.image_url:
				try:
					fname = os.path.basename(recipe.image_url)
					path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
					if os.path.exists(path):
						os.remove(path)
				except Exception:
					pass
			recipe.image_url = None

		db.session.commit()
		flash("Yemek güncellendi!", "info")
		return redirect(url_for('admin_index'))

	return render_template('admin/edit.html', recipe=recipe)


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


	def create_admin_user():
		"""Create a default admin user if none exists. Password comes from ADMIN_PASS env or fallback to a sensible default."""
		admin_user = os.environ.get('ADMIN_USER', 'admin')
		admin_pass = os.environ.get('ADMIN_PASS', '234356na')
		with app.app_context():
			try:
				# create tables if they don't exist
				db.create_all()
			except Exception:
				pass
			user = User.query.filter_by(username=admin_user).first()
			if not user:
				user = User(username=admin_user, is_admin=True)
				user.set_password(admin_pass)
				db.session.add(user)
				db.session.commit()
				print(f"Created admin user '{admin_user}' (default or from ADMIN_PASS).")

	create_admin_user()

	app.run(host=host, port=port, debug=debug)
	
