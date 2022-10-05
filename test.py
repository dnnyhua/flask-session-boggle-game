from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """ Boiler plate for testing """
        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_home_page(self):
        with self.client: 
            resp = self.client.get("/")

            self.assertEqual(resp.status_code, 200)
            self.assertIn('game_board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('num_of_plays'))
            self.assertIn(b'<p>Current Score:', resp.data)
            self.assertIn(b'<p>High Score:', resp.data)
            self.assertIn(b'<p>Time Left:', resp.data)


    def test_check_word(self):
        with self.client as client:
            # Add all changes to session here
            with client.session_transaction() as session:
                session['game_board'] = [['B','A','T','C','I' ],
                                         ['R','B','B','A','B' ],
                                         ['U','L','B','O','E' ],
                                         ['T','E','L','L','S' ],
                                         ['E','B','O','A','F' ]]

            # the gameboard above is now included in Flask's session

            # test words going down
            resp = self.client.get("/check-submitted-word?inputWord=brute") # adjust string query to check for word   
            self.assertEqual(resp.json['result'], 'ok')

            # test words going right
            resp = self.client.get("/check-submitted-word?inputWord=bat")   
            self.assertEqual(resp.json['result'], 'ok')
            
            # test words going different direction
            resp = self.client.get("/check-submitted-word?inputWord=loaf")   
            self.assertEqual(resp.json['result'], 'ok')


    def test_not_word(self):
    # test non words
        self.client.get('/')
        resp = self.client.get("/check-submitted-word?inputWord=asd")   
        self.assertEqual(resp.json['result'], 'not-word')
            


   

