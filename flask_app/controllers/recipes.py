from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


#Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:   
        return redirect('/')
    # user_data = {
    #     'id' : session['user_id']       
    # }
    data = {
        "id": session['user_id']
    }
    recipe_user = {
        "user_id": session['user_id']
    }
    return render_template("dashboard.html", user=User.get_one(data), all = Recipe.get_all_users(recipe_user))

#create a new recipe Page
@app.route('/add_recipe')
def add_recipe():
    if 'user_id' not in session:    
        return redirect('/')
    user_data = {
        "id": session['user_id']
    }
    return render_template('new_recipe.html', user=User.get_one(user_data))

# Create recipe and  add to the DB
@app.route('/create_recipe', methods=["POST"])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/add_recipe')

    data = {  
            'title' : request.form['title'],
            'ingredients' : request.form['ingredients'],
            'cook_time' : request.form['cook_time'],
            'description' : request.form['description'],
            'image' : request.form['image'],
            'user_id': session['user_id'],
    }
    Recipe.create_recipe(data)
    return redirect('/dashboard')

#Show  one recipe
@app.route('/show_recipe/<int:recipe_id>')
def show_recipe(recipe_id):
    data = {
        'id' : recipe_id
    }
    user_data = {
        "id": session['user_id']
    }
    recipe = Recipe.get_one(data)
    return render_template('one_recipe.html', recipe = recipe, user=User.get_one(user_data))

# Edit recipe
@app.route('/edit_recipe/<int:recipe_id>')
def edit_recipe(recipe_id):
    data = {
        'id' : recipe_id
    }
    user_data = {
        "id": session['user_id']
    }
    recipe = Recipe.get_one(data)
    return render_template('edit_recipe.html',recipe = recipe, user=User.get_one(user_data))

# Update One Recipe
@app.route('/update_recipe/<int:recipe_id>', methods=['POST'])
def update_pet(recipe_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit_recipe/{recipe_id}')
    Recipe.update_recipe(request.form, recipe_id)
    return redirect('/dashboard')

# Delete One Pet
@app.route('/delete/<int:recipe_id>')
def delete(recipe_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect('/dashboard')