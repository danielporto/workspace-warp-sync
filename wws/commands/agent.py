import platform
from os.path import expanduser
import commands.utils 


class agent:
    def __init__(self):
        super().__init__()

    def configure(self, args):
        if args['verbose']:
            print("Command agent configure was called.")

        if args['verbose']:
            print(f"Configuring agent to fire at every {args['timer']} seconds.")

        if 'Darwin' in platform.system():
            _configure_osx_timer(args)
        elif 'Linux' in platform.system():
            _configure_linux_timer(args)
        else:
            raise EnvironmentError("Unsupported operating system")


    def start(self, args):
        if 'Darwin' not in platform.system():
            raise EnvironmentError("Unsupported operating system - only Mac OSX is supported right now")

        from plumbum.cmd import launchctl

        if args['verbose']: 
            print("Deploying new agent")

        launchctl['load', '-w', osxagent_file_path].run()


    def stop(self, args):
        if 'Darwin' not in platform.system():
            raise EnvironmentError("Unsupported operating system - only Mac OSX is supported right now")

        from plumbum.cmd import launchctl

        if args['verbose']:
            print("Command agent stop was called.")
            print("Undeploying old agent")

        launchctl['unload', '-w', osxagent_file_path].run()



    def reload(self, args):
        if args['verbose']:
            print("Command agent reload was called.")
        self.stop(args)
        self.start(args)
        

    def status(self, args):
        if 'Darwin' not in platform.system():
            raise EnvironmentError("Unsupported operating system - only Mac OSX is supported right now")

        if args['verbose']:
            print("Command agent status was called.")




def _configure_osx_timer(args):
    script_path = expanduser(args['install_dir'] + '/wws.py')
    configuration_file_path = expanduser(args['settings'])
    database_file_path = expanduser(args['workspace_warp_database'])
    osxagent_file_path = expanduser(args['osx_agent_conf_path'])

    seconds = int(args['timer'])

    text = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.porto.wws</string>
        <key>ProgramArguments</key>
        <array>
            <string>/usr/local/bin/python3</string>
            <string>{script_path}</string>
            <string>-c</string>
            <string>{configuration_file_path}</string>
            <string>-d</string>
            <string>{database_file_path}</string>
        </array>
        <key>StandardErrorPath</key>
        <string>/tmp/wws.err</string>
        <key>StandardOutPath</key>
        <string>/tmp/wws.log</string>
        <key>StartInterval</key>
        <integer>{seconds}</integer>
    </dict>
    </plist>    """
        
    with open(osxagent_file_path, "+w") as f:
        f.writelines(text)
    

def _configure_linux_timer(args):
    raise EnvironmentError("Unsupported OS")