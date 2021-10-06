
import os, requests
from unittest import TestCase
from models import Category, Glass, db, Drink, Ingredient, Language, User

os.environ["DATABASE_URL"] = "postgresql:///mixology-test"

from app import app, USER_KEY

app.config["SQLALCHEMY_ECHO"] = False

db.drop_all()
db.create_all()

json_data = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=11007").json()
drink_data = json_data["drinks"][0]

ingr_data = requests.get("https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list").json()
ingredients = [Ingredient(name=ingr["strIngredient1"].lower()) for ingr in ingr_data["drinks"]]

languages = [
    Language(code="EN", name="English"),
    Language(code="DE", name="German"),
    Language(code="ES", name="Spanish"),
    Language(code="FR", name="French"),
    Language(code="IT", name="Italian"),
    Language(code="ZH-HANS", name="Mandarin Chinese, Simplified"),
    Language(code="ZH-HANT", name="Mandarin Chinese, Traditional")
]
glass = Glass(name=drink_data["strGlass"].lower())
category = Category(name=drink_data["strCategory"].lower())

db.session.add_all([*ingredients, glass, *languages, category])
db.session.commit()

class DrinkViewsTestCase(TestCase):

    def setUp(self):
        """Set up drink model"""

        Drink.query.delete()

        [drink, instructions, drink_ingredients] = Drink.parse_drink_data(drink_data)

        db.session.add(drink)
        db.session.commit()

        db.session.add_all(instructions)
        db.session.add_all(drink_ingredients)

        db.session.commit()

        self.drink = Drink.query.get(11007)

        self.client = app.test_client()

    def test_drinks_list(self):
        """Test drinks list page"""

        with self.client as c:

            resp = c.get("/drinks")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.drink.name.title(), html)
            self.assertIn(self.drink.category.name.title(), html)
    
    def test_drink_view(self):

        with self.client as c:

            resp = c.get(f"/drinks/{self.drink.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.drink.name.title(), html)
            self.assertIn(self.drink.instructions[0].text, html)
            self.assertIn(self.drink.category.name.title(), html)
            self.assertIn(self.drink.glass.name.title(), html)
    
    def test_drink_view_logged_in(self):
        """Test drink page when logged in. Should have a bookmark icon."""

        with self.client as c:

            id = User.register("test", "test123", 1).id

            with c.session_transaction() as sess:
                sess[USER_KEY] = id
            
            resp = c.get("/drinks/11007")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<i class="bi bi-bookmark fs-2"></i>', html)
    