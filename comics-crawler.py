import argparse
import updater


def launch_command_line_interface():
    import cli
    return


parser = argparse.ArgumentParser()
parser.add_argument("--update", help="update from all sites after everything else is done.", action="store_true")
args = parser.parse_args()

if args.update:
    updater.update_all()
    exit()
if not any(vars(args).values()):
    launch_command_line_interface()
    exit()