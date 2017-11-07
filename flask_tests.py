from flask import Flask
from flask_testing import TestCase
import unittest



class TopSubTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['Testing'] = True
        return app

    def testResp(self):
        client = self.create_app().test_client(True)
        response = self.client.get("/topsubs/api/v1.0/news/top/20")
        print(response)



if __name__ == '__main__':
    unittest.main()
