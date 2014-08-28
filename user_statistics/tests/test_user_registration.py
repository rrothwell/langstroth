from django.utils import unittest

from user_statistics.models.registration import UserRegistration

class UserRegistrationTest(unittest.TestCase):
    
    barrym = None
    phyllisu = None
    
    def setUp(self):
        self.barrym = UserRegistration(user_name="1234", creation_time="2014-02-16")
        self.phyllisu = UserRegistration(user_name="4321", creation_time="2014-03-08")

    def tearDown(self):
        self.barrym = None
        self.phyllisu = None
    
    def test_UserRegistration_has_user_name(self):
           
        self.assertEqual(self.barrym.user_name, '1234')
        self.assertEqual(self.phyllisu.user_name, '4321')

    def test_UserRegistration_has_creation_time(self):            
        self.assertEqual(self.barrym.creation_time, '2014-02-16')
        self.assertEqual(self.phyllisu.creation_time, '2014-03-08')
