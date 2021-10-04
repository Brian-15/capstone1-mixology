from app import db
from models import Ingredient, Language, Drink, Category, Glass
import requests

# add all standalone data

db.drop_all()
db.create_all()

languages = [
    Language(code="EN", name="English"),
    Language(code="DE", name="German"),
    Language(code="ES", name="Spanish"),
    Language(code="FR", name="French"),
    Language(code="IT", name="Italian"),
    Language(code="ZH-HANS", name="Mandarin Chinese, Simplified"),
    Language(code="ZH-HANT", name="Mandarin Chinese, Traditional")
]
db.session.add_all(languages)

cat_data = requests.get("https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list").json()
categories = [Category(name=cat["strCategory"].lower()) for cat in cat_data["drinks"]]

db.session.add_all(categories)

glass_data = requests.get("https://www.thecocktaildb.com/api/json/v1/1/list.php?g=list").json()
glasses = [Glass(name=glass["strGlass"].lower()) for glass in glass_data["drinks"]]

db.session.add_all(glasses)

ingr_data = requests.get("https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list").json()
ingredients = [Ingredient(name=ingr["strIngredient1"].lower()) for ingr in ingr_data["drinks"]]

db.session.add_all(ingredients)
db.session.commit()

# gather drink IDS
drink_ids = []
for glass in glasses:
    name_str = glass.name.replace(" ", "_")
    resp_data = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?g={name_str}").json()

    drink_ids.extend([drink["idDrink"] for drink in resp_data["drinks"]])

[drinks, drinks_instructions, drinks_ingredients] = [[], [], []]

for id in drink_ids:
    drink_data = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={id}").json()

    if drink_data["drinks"][0]["strCreativeCommonsConfirmed"] == "Yes":
        [drink_model, instruction_models, drink_ingr_models] = Drink.parse_drink_data(drink_data["drinks"][0])
    
        drinks.append(drink_model)
        drinks_instructions.extend(instruction_models)
        drinks_ingredients.extend(drink_ingr_models)

db.session.add_all(drinks)
db.session.commit()

db.session.add_all(drinks_instructions)
db.session.add_all(drinks_ingredients)
db.session.commit()