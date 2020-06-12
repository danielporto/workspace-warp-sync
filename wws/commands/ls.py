from pprint import pprint
import yaml
from tabulate import tabulate
from funcy import project
import re
class Ls:
    def __init__(self):
        super().__init__()

    def process(self, args):
        """ opens the warp database and print its content """
        with open(args['workspace_warp_database'],'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        # when ls, verify which dir exists and mark import emoji

        if args['alias']:
            data = [ d for d in data if any( [ a for a in args['alias'] if a.upper() in d['alias'].upper() ]  )    ]

        if not args['verbose']:
            data = [ project(d,['alias', 'src', 'dst' ]) for d in data] 

        print(tabulate(data, headers="keys", tablefmt = "psql"))
        
   
   