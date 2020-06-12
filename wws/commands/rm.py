from pprint import pprint
class Rm:
    def __init__(self):
        super().__init__()

    def process(self, args):
        print("process command is called")
        pprint(args)
   
   
