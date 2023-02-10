class UserExists(Exception):
    def __str__(self):
        return "User with current username already exists"
