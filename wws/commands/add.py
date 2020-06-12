from pprint import pprint

class Add:
    def __init__(self):
        super().__init__()

    def process(self, args):
        """ edits the warp database  """
        with open(args['workspace_warp_database'],'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        # expand 
   