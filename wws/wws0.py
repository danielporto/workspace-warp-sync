# -*- coding: UTF-8 -*-
import click
from plumbum import local, FG, BG, TF, RETCODE
from plumbum.cmd import rsync
from pprint import pprint
import argparse
import yaml
import os.path
from os import path
from os.path import expanduser
home = expanduser("~")
import time

# TODO ensure that the dependencies are installed and available for the python interpreter

# workspace warp

# http://launched.zerowidth.com/ how to run jobs on mac like cron


# currently this is osx only
def gen_schedule_conf(seconds):
    base = home + "/scripts/wws/"
    path_to_wws = base + "wws.py"
    path_to_agent = home + "/Library/LaunchAgents/com.porto.wws.plist"
    path_to_configfile = base + "wkswarp.yaml"
    args = ["-c", path_to_configfile]

    seconds = int(seconds) # clear decimals
    print(f"Configuring agent to fire at every {seconds} seconds.")
    text = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.porto.wws</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>{path_to_wws}</string>
        <string>{args[0]}</string>
        <string>{args[1]}</string>
    </array>
    <key>StandardErrorPath</key>
	<string>/tmp/wws.err</string>
	<key>StandardOutPath</key>
	<string>/tmp/wws.log</string>
    <key>StartInterval</key>
    <integer>{seconds}</integer>
</dict>
</plist>    """
    
    with open(path_to_agent, "+w") as f:
        f.writelines(text)
    
    # deploy
    from plumbum.cmd import launchctl
    print("Undeploying old agent")
    launchctl['unload', '-w', path_to_agent].run()
    print("Deploying new agent")
    launchctl['load', '-w', path_to_agent].run()
    print("Done.")

    




@click.command()
def cli():
    pass


@cli.group()
@click.argument()
def agent():
    pass

settings = dict()
# settings['configuration_file'] =


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Workspace warp & sync")
    parser.add_argument("--config", "-c", default=home+"/scripts/wws/wkswarp.yaml", help="Set the configuration file", type=str  ,required=False)
    parser.add_argument("--timer", "-t", default=1200, type=int  ,required=False)
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--start', '-s', action='store_true')

    args = vars(parser.parse_args())


    if args['start']:
        gen_schedule_conf(args["timer"])
        exit()
    
    # pprint(args)
    data = list()
    with open(args['config'],'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    start = time.time()
    for item in data:
        if path.exists(item['src']):
            if args["verbose"]: # for safety always dry run
                pprint(f"synchronizing {item['src']}")
            for dst in item['dst']:
                if not path.exists(dst): 
                    # prevent create before exist (drive not mounted), we better use a command to force pushing to prevent errors
                    # this approach will not work with remote locations (rsync over ssh)...
                    continue
                params = []
                params.append("--exclude=Icon?")
                params.append("--exclude=.DS_Store")
                if args["debug"]: # for safety always dry run
                    params.append("--dry-run")
                    print("don't actually performing any action.")
                params.append(item['opts'])
                params.append(item['src'])
                params.append(dst)
                if args["verbose"]: # for safety always dry run
                    print(f"\tto: {dst}")
                out = rsync[params].run() 
                if args["debug"]: # for safety always dry run
                    pprint(out)
    end = time.time()

    # notify mac
    from plumbum.cmd import osascript
    osascript['-e',f'display notification "[WWS] Workspace synchronized in {int(end - start)} seconds!"'].run()

    # if args["verbose"]: # for safety always dry run
    print(f"[WWS] Workspace synchronized finished. Duration: {int(end-start)}")
    



