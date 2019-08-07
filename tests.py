import os
import unittest
from unittest import TestCase
from app import *
from get_data import *

class Basic_url_tests(TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()