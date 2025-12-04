from app import app, Recipe

with app.app_context():
    for r in Recipe.query.order_by(Recipe.id).all():
        print(r.id, r.name)
