from django.test import TestCase

from user_statistics.models.registration import UserRegistration

class UserStatisticsViewTest(TestCase):
 
    fixtures = ['user_statistics_0']
    multi_db = True
    
    # Web pages

    def setUp(self):
        self.barrym = UserRegistration(user_name="1234", creation_time="2014-02-16")
        self.phyllisu = UserRegistration(user_name="4321", creation_time="2014-03-08")
   
    def test_page_index(self):
        response = self.client.get("/user_statistics/")
        self.assertEqual(200, response.status_code) 
   
    def test_page_visualisation(self):
        response = self.client.get("/user_statistics/registrations/visualisation")
        self.assertEqual(200, response.status_code) 
   
    # Web services with JSON pay loads.
          
    def test_rest_for_code(self):
        response = self.client.get("/user_statistics/rest/registrations/history")
        self.assertEqual(200, response.status_code)          
