from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from pprint import pprint

db = 'project_db'

class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.ingredients = data['ingredients']
        self.cook_time = data['cook_time']
        self.description = data['description']
        self.image = data['image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner = None

    #create recipe
    @classmethod
    def create_recipe(cls,data):
        query = """ INSERT INTO recipes (title,ingredients,cook_time, description, image, user_id) 
                    VALUES (%(title)s, %(ingredients)s, %(cook_time)s, %(description)s, %(image)s, %(user_id)s );
                """
        return connectToMySQL(db).query_db(query,data)

    
    #Display all recipes
    @classmethod
    def all_recipe(cls, data):
        query = 'SELECT * FROM recipes WHERE user_id = %(user_id)s;'
        results = connectToMySQL(db).query_db(query, data)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_all_users(cls, data):
        query = "SELECT * FROM recipes JOIN users WHERE  users.id = recipes.user_id;"
        results = connectToMySQL(db).query_db(query, data)
        recipes = []
        for recipe in results:
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s'
        results = connectToMySQL(db).query_db(query,data)
        recipe = cls(results[0])
        owner_data = {
            'id': results[0]['users.id'],
            'first_name':results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'created_at':results[0]['users.created_at'],
            'updated_at':results[0]['users.updated_at'],
        }
        recipe.owner = User(owner_data)
        return recipe

    #update one recipe
    @classmethod
    def update_recipe(cls,form_data, id):
        query = f"UPDATE recipes SET title = %(title)s, ingredients = %(ingredients)s, cook_time = %(cook_time)s, description = %(description)s, image = %(image)s  WHERE id = {id};"
        return connectToMySQL(db).query_db(query,form_data)
    
    # delete one recipe
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query,data)


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['title']) < 1:
            flash("Title is requred.", "recipe")
            is_valid = False
        if len(recipe['ingredients']) < 1:
            flash("Ingredients are requred.", "recipe")
            is_valid = False
        if len(recipe['cook_time']) < 1 or int(recipe['cook_time']) == 0 or int(recipe['cook_time']) < 0:
            flash("Cook Time is requred.", "recipe")
            is_valid = False
        if len(recipe['description']) < 1:
            flash(" Description is requred.", "recipe")
            is_valid = False
        return is_valid

