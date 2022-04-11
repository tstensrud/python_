class Users:
    
    def __init__(self, username, password, email, name):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
    
    def getUsername(self):
        return self.username
    
    def getEmail(self):
        return self.email
    
    def getName(self):
        return self.name
    
    def getPassword(self):
        return self.password
    
    def setNewPassword(self, newPassword):
        self.password = newPassword