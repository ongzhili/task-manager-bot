import re

class ValidateHelper:
    def __init__(self, msg):
        self.toValidate = str(msg)
    
    def validateAddTask(self):
        re1 = re.compile(r"[<>/{}[\]~`]")
        if re1.search(self.toValidate) or self.toValidate == "" or self.toValidate is None:
            return False
        else:
            return True