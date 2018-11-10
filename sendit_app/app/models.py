"""
This module holds the pretend-models for the application
"""
from random import randint
from app.utilities import check_type, check_email_format

def binary_search(character, list_of_characters, position=0):
    """
    Searches for character using binary search
    returns None if character is not found
    otherwise returns character's position in sorted list
    """
    length_of_list = len(list_of_characters)
    if length_of_list <= 1:
        if length_of_list == 0:
            return None
        if character != list_of_characters[0]:
            return None
        return position

    random_int = randint(0, length_of_list - 1)
    if character < list_of_characters[random_int]:
        new_list = list_of_characters[:(random_int)]
        position += 0
    else:
        new_list = list_of_characters[random_int:]
        position += random_int
    # return this so that it recursively comes back to the surface
    return binary_search(character, new_list, position)


class Database:
    """This is the database for the application"""
    def __init__(self):
        self.users = {}
        self._user_keys = []
        self.user_email_key_map = {}
 

    @property
    def user_keys(self):
        self._user_keys =  list(set(self._user_keys))
        return self._user_keys

    def get_next_key(self, type_of_object):
        """Gets the next key basing on the type of object"""
        # type_of_object should be of type type
        if check_type(type_of_object, type):
            if type_of_object == User:
                return self.__get_max_value(self.user_keys) + 1

           

    def __get_max_value(self, unsorted_list):
        """Returns the maximum value of a list or 0 if list is empty"""
        if check_type(unsorted_list, list):
            length = len(unsorted_list)
            if length == 0:
                return 0

            unsorted_list.sort()
            return unsorted_list[length - 1]

    
    def create_user(self, user_data):
        """Creates a new user and adds the user to self.users"""
        try:
            if self.user_email_key_map[user_data['email']]:
                raise ValueError('User already exists')
        except KeyError:
            # if the key does not exist, pass
            pass
        user_key = self.get_next_key(User)
        try:
            user = User(**user_data, key=user_key)
            user.save(self)
        except:
            raise ValueError('invalid user data')
        return user

    def get_user(self, user_key):
        """
        returns the User object corresponding to user_key or
        None if user does not exist
        """
        if check_type(user_key, int):
            try:
                user = self.users[user_key]
            except KeyError:
                return None
            return user

    def get_user_by_email(self, email):
        """
        Returns a user object corresponding to the email
        passed in or None is user does not exist
        """
        if check_type(email, str):
            try:
                user_key = self.user_email_key_map[email]
            except KeyError:
                return None
            return self.get_user(user_key)
        
   

class User:
    """
    Any user who interfaces with the app falls in this category
    """
    def __init__(self, key, first_name, last_name, email, password):
        if check_type(key, int):
            self.key = key
        if check_type(first_name, str):
            self.first_name = first_name
        if check_type(last_name, str):
            self.last_name = last_name
        if check_type(email, str):
            if check_email_format(email):
                self.email = email
        if check_type(password, str):
            self.password = password
        # a list of recipe_category keys
        self._recipe_categories = []

   

    def save(self, database):
        """Saves user to the database appropriately"""
        # add self's key to db's set of user keys
        # Add self to db.users dict with key as self.key
        if check_type(database, Database):
            database.user_keys.append(self.key)
            database.users[self.key] = self
            database.user_email_key_map[self.email] = self.key

   

    # 
# A global db
db = Database()
