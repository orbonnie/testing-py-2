import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"board games, rainbows, and ice cream sundaes", result.data)
        print("Test 1 passed")

    def test_no_rsvp_yet(self):
        # FIXME: Add a test to show we see the RSVP form, but NOT the
        # party details
        result = self.client.get("/")
        self.assertIn(b"<h2>Please RSVP</h2>", result.data)
        self.assertNotIn(b"<h2>Party Details</h2>", result.data)
        print("Test 2 passed")

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        # FIXME: Once we RSVP, we should see the party details, but
        # not the RSVP form
        result = self.client.get("/")
        self.assertIn(b"<h2>Party Details</h2>", result.data)
        self.assertNotIn(b"<h2>Please RSVP</h2>", result.data)
        print("Test 3 passed")


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///games_test")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):
        # FIXME: test that the games page displays the game from example_data()
        result = self.client.get('/games')
        self.assertIn(b"<td>Unicorn Tail</td>", result.data)
        print("Test 4 passed")


if __name__ == "__main__":
    unittest.main()
