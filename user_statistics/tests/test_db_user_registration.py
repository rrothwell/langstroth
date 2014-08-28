from django.test import TestCase

from user_statistics.models.registration import UserRegistration

class UserRegistrationDBTest(TestCase):

    multi_db = True

    def setUp(self):
        UserRegistration.objects.create(user_name="1234", creation_time="2014-02-16T23:21:59Z")
        UserRegistration.objects.create(user_name="4321", creation_time="2014-03-16T16:14:30Z")

    def test_code_has_name(self):
        barrym = UserRegistration.objects.get(user_name="1234")
        phyllisu = UserRegistration.objects.get(user_name="4321")
        self.assertEqual('2014-02-16 23:21:59', barrym.creation_time.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2014-03-16 16:14:30', phyllisu.creation_time.strftime('%Y-%m-%d %H:%M:%S'))       
                
    def test_dict(self):
        expected_map = {'1234': '2014-02-16 23:21:59', '4321': '2014-03-16 16:14:30'}
        actual_map = UserRegistration.user_dict()
        different_items = set(expected_map.items()) ^ set(actual_map.items())
        self.assertEqual(0, len(different_items))
               
    def test_history(self):
        expected_list = [{'user_name':'1234', 'creation_time':'2014-02-16 23:21:59'}, 
        {'user_name':'4321', 'creation_time':'2014-03-16 16:14:30'}]
        actual_list = UserRegistration.history()
        self.assertEqual(2, len(actual_list))
        self.assertEqual(expected_list, actual_list)

