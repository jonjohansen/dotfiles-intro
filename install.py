#!/usr/bin/env python3

from json import load
from os import symlink, remove, path, environ
from subprocess import run, CalledProcessError

DOTFILES_PATH = "$HOME/.dotfiles-macos"

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def underline(str):
  return f'{color.UNDERLINE}{str}{color.END}'

def bold(str):
  return f'{color.BOLD}{str}{color.END}'

# Help with confirm prompt
def confirm(prompt):
  response = None
  while (response != 'y' and response != 'n'):
    try:
      response = input(f"{prompt} [y/N]\n").lower()
    except KeyboardInterrupt:
      print("\nExiting")
      exit(1) 
  return response == 'y'

# Helper function for creating symlinks
def symlink_helper(label, src, dest):
  print(bold(f'{color.BLUE}Creating symbolic link for {label}'))

  # get full paths for files
  src = path.expandvars(src)
  dest = path.expandvars(dest)

  if not path.exists(src):
    raise FileNotFoundError(f"Could not find file at {src}")
  
  if path.exists(dest):
    filename = path.basename(dest)
    print(f'File {bold(filename)} already exists at {underline(dest)}')
    overwrite = confirm("Do you want to overwrite it?")
    if not overwrite:
      print(f"Skipping setting up {label}")
      return 

    remove(dest)

  symlink(src, dest)
  print(f'Symlinked {underline(src)} to {underline(dest)}\n')

# Helper function for running terminal commands
def command_helper(label, command, sudo):
    print(bold(f"Executing command: {color.BLUE}{label}"))
    if sudo:
      print("This may require sudo access")
    
    # Split arguments, and expand potential environment variables
    expanded = [path.expandvars(cmd) for cmd in command.split(' ')]
    run(expanded)

if __name__ == '__main__':
  # Expecting a dotfiles folder path as environment variable
  environ['DOTFILES'] = DOTFILES_PATH
  
  # check if brew installed
  try: 
    run(['which', 'brew'], check=True, capture_output=True)
  except CalledProcessError:
    print("Could not find a valid brew installation")
    print(f"Visit: {underline('https://brew.sh/')} to see how to install brew.")
    exit(1)

  # Read config.json
  with open('config.json', 'r') as configFile:
    config = load(configFile)

  for command in config['commands']:
    command_helper(**command)
    print("")

  # Create symbolic links  
  for link in config['symlinks']:
    symlink_helper(**link)
    print("")

  print(f"{color.GREEN + color.BOLD}dotfiles setup complete!", color.END)
