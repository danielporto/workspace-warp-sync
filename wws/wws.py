#! env python3
import sys
from pprint import pprint
from os import path
import commands.utils as utils
from funcy import merge

def agent(args):
    """  
        Synchronization agent command dispatcher
    """
    from commands import agent
    if ['verbose']:
        print("agent command invoked")
    cmd = agent.Agent()
    cmd.process(args)

def cmd_agent(subparsers):
    subcommand = 'cmd_agent'
    cmd_parser = subparsers.add_parser('agent', help='Workspace synchronization agent management')
    action_cmd_parser = cmd_parser.add_mutually_exclusive_group(required=True)
    action_cmd_parser.add_argument('-s','--start',     action='store_const', const='start', dest=subcommand, help='Start the synchronization agent')
    action_cmd_parser.add_argument('-p','--stop',      action='store_const', const='stop', dest=subcommand, help='Stop the synchronization agent')
    action_cmd_parser.add_argument('-r','--reload',    action='store_const', const='reload', dest=subcommand, help='Reload the synchronization agent')
    action_cmd_parser.add_argument('-c','--configure', action='store_const', const='configure', dest=subcommand, help='Configure the synchronization agent')
    cmd_parser.add_argument("--timer", "-t", default=1200, type=int  ,required=False)

# --------------------- --------------------- --------------------- --------------------- ---------------------

def ls(args):
    """  
        List workspace command dispatcher
    """
    from commands import ls
    if ['verbose']:
        print("ls command invoked")
    cmd = ls.Ls()
    cmd.process(args)
 
def cmd_ls(subparsers):
    # ls command
    subcommand = 'cmd_ls'
    cmd_parser = subparsers.add_parser('ls', help='List synchronized workspaces')
    cmd_parser.add_argument("-a","--alias", nargs='+', required=False, help='specify the item or items to list')
    cmd_parser.add_argument("-o","--with-options", action = 'store_true', required=False, help='print detailed options')

    # action_cmd_parser = cmd_parser.add_mutually_exclusive_group(required=True)
    # action_cmd_parser.add_argument('-s','--start',     action='store_const', const='start', dest=subcommand, help='Start the synchronization agent')

# --------------------- --------------------- --------------------- --------------------- ---------------------
def add(args):
    """  
        Add workspace command dispatcher
    """

    from commands import add
    if ['verbose']:
        print("Add command invoked")
    cmd = add.Add()
    cmd.process(args)
 
def cmd_add(subparsers):
    # add command
    cmd_parser = subparsers.add_parser('add', help='Add synchronized workspaces')
    cmd_parser.add_argument("-a","--alias", type=str, required=False, help='Specify an alias for the warp point')
    cmd_parser.add_argument("-s","--src", "--source", type=str, required=True, help='Specify source path')
    cmd_parser.add_argument("-d","--dst", "--destination", nargs='+', required=True, help='Specify destination path')


# --------------------- --------------------- --------------------- --------------------- ---------------------
def rm(args):
    """  
        Remove workspace command dispatcher
    """
    from commands import rm
    if ['verbose']:
        print("rm command invoked")
    cmd = rm.Rm()
    cmd.process(args)
 
def cmd_rm(subparsers):
    # ls command
    subcommand = 'cmd_rm'
    cmd_parser = subparsers.add_parser('rm', help='Remove synchronized workspaces')
    # action_cmd_parser = cmd_parser.add_mutually_exclusive_group(required=True)
    # action_cmd_parser.add_argument('-s','--start',     action='store_const', const='start', dest=subcommand, help='Start the synchronization agent')
# --------------------- --------------------- --------------------- --------------------- ---------------------
def sync(args):
    """  
        Sync workspace command dispatcher
    """
    from commands import sync
    if ['verbose']:
        print("Sync command invoked")
    cmd = sync.Sync()
    cmd.process(args)
    
 
def cmd_sync(subparsers):
    # sync command
    subcommand = 'cmd_sync'
    cmd_parser = subparsers.add_parser('sync', help='Sync command to force  operations on workspaces')
    cmd_parser.add_argument("--dry-run", action='store_true', required=False, help='Non destructive operation, don\'t actually copies anything')
    cmd_parser.add_argument("-a","--alias", nargs='+', required=False, help='specify the item or items to selective sync')
    action_cmd_parser = cmd_parser.add_mutually_exclusive_group(required=True)
    action_cmd_parser.add_argument('--up', action='store_const', const='up', dest=subcommand, help='Copy data from local to remote')
    action_cmd_parser.add_argument('--down', action='store_const', const='down', dest=subcommand, help='Copy data from remote to local')


# --------------------- --------------------- --------------------- --------------------- ---------------------

def main():
    """ Workspace warp and sync utility. 
    This application helps you to keep local directories in synch with
    remote locations, usually cloud drives.
    """
    import argparse
    main_parser = argparse.ArgumentParser()
    main_parser.add_argument('-v', '--verbose', action = 'store_true', help = "Make the command verbose")
    main_parser.add_argument( "-c", "--config", default = "./settings.yaml", help = "Set the configuration file", type=str  ,required=False)
    main_parser.add_argument( "-w", "--warp-database", dest='workspace_warp_database', default = "./wkswarp.yaml", help = "Set workspace warp file", type=str  ,required=False)
    main_parser.add_argument( "-g", "--debug", dest='debug', action='store_true', required=False)

    # define commands 
    subparsers = main_parser.add_subparsers(dest='cmd_main', help="Available Workspace Warp and Sync commands")
    subparsers.required = True
    cmd_add(subparsers)
    cmd_rm(subparsers)
    cmd_ls(subparsers)
    cmd_sync(subparsers)
    cmd_agent(subparsers)

    # flatten arguments and invoke command dispatcher
    args = vars(main_parser.parse_args())
    
    # load settings
    settings = utils.load_settings(args['config'])
    default_options = dict()
    # coalesce a list of dicts into a single dict
    for conf in settings:
        default_options =  merge(default_options, conf)

    # join settings overriding the default for command line  
    args = merge(default_options, args)
    
    
    if args['debug'] or args['verbose']:
        pprint(args)

    # invoke command
    getattr(sys.modules[__name__], args['cmd_main'])(args)
# --------------------- --------------------- --------------------- --------------------- ---------------------


if __name__ == '__main__':
    main()
