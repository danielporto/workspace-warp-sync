import commands.utils 
import yaml
from os import path
from os.path import expanduser
from plumbum import local, FG, BG, TF, RETCODE
from plumbum.cmd import rsync
from pprint import pprint
from funcy import project


class sync:
    def __init__(self):
        super().__init__()

    def up(self, args):
        with open(args['workspace_warp_database'],'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        # filter only the selected aliases
        if args["alias"]:
            data = project(data, args['alias'])
        for item in data:
            if path.exists(item['src']):
                if args["verbose"]: # for safety always dry run
                    print(f"synchronizing {item['src']}")

                for dst in item['dst']:
                    # prevent creating remote before it exists ( if drive not mounted), 
                    # we better use a command to force pushing to prevent errors
                    # this approach need rework for remote locations (rsync over ssh)...
                    if not path.exists(dst): 
                        if args['debug'] or args['verbose']:
                            print(f"Destination path '{dst}' does not exits, skipping.")
                        continue

                    params = []
                    if args["dry_run"]:
                        params.append("--dry-run")

                    # include global patterns
                    for ex in args['exclude_patterns']:
                        params.append(f"--exclude={ex}")

                    # include per workspace options
                    if item['opts']:
                        params.extend(item['opts'])

                    params.append(item['src'])
                    params.append(dst)
                    if args["verbose"]: # for safety always dry run
                        print(f"\tto: {dst}")
                    
                    out = rsync[params].run() 
                    if args["debug"] or args['dry_run']: 
                        pprint(out) 
            elif args['debug'] or args['verbose']:
                print(f"Source path '{item['src']}' does not exits, skipping.")
 


    def down(self, args):
        with open(args['workspace_warp_database'],'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        # filter only the selected aliases
        if args["alias"]:
            data = project(data, args['alias'])

        # reverse source and destination
        for item in data:
            source = item['src']
            item['src'] = item['dst'][0]
            item['destination'] = [source] 

        for item in data:
            if path.exists(item['src']):
                if args["verbose"]: # for safety always dry run
                    print(f"synchronizing {item['src']}")

                for dst in item['dst']:
                    # prevent creating remote before it exists ( if drive not mounted), 
                    # we better use a command to force pushing to prevent errors
                    # this approach need rework for remote locations (rsync over ssh)...
                    if not path.exists(dst): 
                        if args['debug'] or args['verbose']:
                            print(f"Destination path '{dst}' does not exits, skipping.")
                        continue

                    params = []
                    if args["dry_run"]:
                        params.append("--dry-run")

                    # include global patterns
                    for ex in args['exclude_patterns']:
                        params.append(f"--exclude={ex}")

                    # include per workspace options
                    if item['opts']:
                        params.extend(item['opts'])

                    params.append(item['src'])
                    params.append(dst)
                    if args["verbose"]: # for safety always dry run
                        print(f"\tto: {dst}")
                    
                    out = rsync[params].run() 
                    if args["debug"] or args['dry_run']: 
                        pprint(out) 
            elif args['debug'] or args['verbose']:
                print(f"Source path '{item['src']}' does not exits, skipping.") 
    