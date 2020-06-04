#! env /usr/local/bin/python3
# -*- coding: UTF-8 -*-
from plumbum import local, FG, BG, TF, RETCODE
from plumbum.cmd import rsync
from pprint import pprint
import argparse
import yaml
import os.path
from os import path
from os.path import expanduser
home = expanduser("~")
from datetime import datetime 



# workspace warp

def _safe_print(msg, **kwargs):
    try:
        print(msg, **kwargs)
    except UnicodeEncodeError:
        print(msg.encode('ascii','ignore'), **kwargs)


def _info(msg, **kwargs):
    _safe_print(CCYAN + "¡" + CRESET + " " + msg, **kwargs)


def _local_with_brew_check(pkg):
    brew = local.get('brew','/usr/local/bin/brew')

    brew_has_pkg = brew['ls', '--versions', pkg].run(retcode=None)
    if brew_has_pkg[0] == 1:
        _info("Installing '" + pkg +"' terminal tool")
        if brew['install', pkg].run(retcode=None)[0] == 1:
            # return None if we fail to install
            return None

    return local.get(pkg, '/usr/local/bin/'+pkg)


settings = dict()
# settings['configuration_file'] =


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(prog="Workspace warp & sync")
    parser.add_argument("--config", "-c", default=home+"/.wkswarp.yaml", help="Set the configuration file", type=str  ,required=False)
    parser.add_argument('--test', '-t', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    # parser.add_argument('--update', '-u', action='store_true')
    # parser.add_argument('--method', '-m', type=str)
    args = vars(parser.parse_args())

    # pprint(args)

    data = list()
    with open(args['config'],'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    start = datetime.now()
    for item in data:
        if path.exists(item['src']):
            if args["verbose"]: # for safety always dry run
                pprint(f"synchronizing {item['src']}")
            for dst in item['dst']:
                params = []
                params.append("--exclude=Icon?")
                params.append("--exclude=.DS_Store")
                if args["test"]: # for safety always dry run
                    params.append("--dry-run")
                    print("dont actually performing any action.")
                params.append(item['opts'])
                params.append(item['src'])
                params.append(dst)
                if args["verbose"]: # for safety always dry run
                    print(f"\tto: {dst}")
                out = rsync[params].run() 
                if args["test"]: # for safety always dry run
                    pprint(out)
    end = datetime.now()
    if args["verbose"]: # for safety always dry run
        print(f"duration: {end-start}")
    



