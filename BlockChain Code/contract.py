class Message:
    def __init__(self):
        self.message = ""
        

    def check_user(self, username):
        user_list = ["connor", "ashton", "brian"]
        if(username.lower() in user_list):
            return True
        else:
            return False
        

        
