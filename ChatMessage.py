__author__ = 'Gilad Barak'


class ChatMessage(object):
    def __init__(self, user, function, function_param):
        """
        :param user: A ChatUser Object
        :param function: using given protocol numbers
        :param function parameters if needed
        """
        self.user = user
        self.function = function
        self.function_param = function_param


class ChatUser(object):
    def __init__(self, user_name, is_admin, is_muted):
        """
        :param user_name: name submitted by user
        :param is_admin: is this user an admin in chat
        :param is_muted: is this user muted in chat
        """
        self.user_name = user_name
        self.is_admin = is_admin
        self.is_muted = is_muted


