 import unittest

from app.models import Database,User

class DatabaseTest(unittest.TestCase):

	def setUp(self):
		self.db=Database()
		self.user_data={
			'first_name':'Wamula',
			'last_name':'Bashir',
			'email':'wamulabash1@gmail.com',
			'password':'password',
			}

		self.user =User(**self.user_data,key=1)
		self.category_data={
			'key':1,
			'name':'hello',
			'description':'hello world',
			'user':self.user.key,
			}

	def test_get_next_key(self):
		self.assertEqual(self.db.get_next_key(User),1)
		self.db._user_keys +=[1,2,3]
		self.assertEqual(self.db.get_next_key(User),4)
		self.assertRaises(TypeError, self.db.get_next_key,2)



