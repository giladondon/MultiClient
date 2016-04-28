__author__ = 'Gilad Barak'


class ChatUser(object):
    def __init__(self, user_name, is_admin, is_muted):
        """
        :param user_name: name submitted by user
        :param is_admin: is this user an admin in chat
        :param is_muted: is this user muted in chat
        """
        self.user_name = user_name
        self.name_length = len(user_name)
        self.is_admin = is_admin
        self.is_muted = is_muted


