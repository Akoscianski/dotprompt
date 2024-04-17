import logging
import os
import inspect
import sys
from .prompt import Prompt
from .exceptions import PrompDirectoryNotFoundError, PromptError


__version__ = "0.1.6"


IGNORED_EXT = ['py']


logging.info("Loading prompt files")
__prompt_dir =os.path.join(os.getcwd(), 'prompts')
if not os.path.isdir(__prompt_dir):
    not_found = True
    ROOT_DIR = os.path.abspath(os.curdir)
    caller_path = os.path.dirname(sys.argv[0])
    while not_found:
        if "prompts" in os.listdir(caller_path):
            __prompt_dir = os.path.join(caller_path, "prompts")
            not_found = False
        elif caller_path == ROOT_DIR:
            raise PrompDirectoryNotFoundError(f"No prompt dir found in {ROOT_DIR}")
        caller_path = os.path.dirname(caller_path)
if not os.path.isdir(__prompt_dir):
    raise PrompDirectoryNotFoundError("Prompt directory \"prompts\" not found")
for f in os.listdir(__prompt_dir):
    parts = f.split('.')
    if parts[-1] == "prompt":
        if parts[0] in globals():
            globals()[parts[0]].add_file(os.path.join(__prompt_dir, f))
        else:
            globals()[parts[0]] = Prompt(os.path.join(__prompt_dir, f), ext="prompt")
    elif parts[-1] =="jprompt":
        if parts[0] in globals():
            raise PromptError("Prompt {} already exists".format(parts[0]))
        else:
            globals()[parts[0]] = Prompt(os.path.join(__prompt_dir, f), ext="jprompt")
    elif parts[-1] in IGNORED_EXT:
        logging.debug("Ignoring file {}".format(f))
    else:
        logging.warning("File {} unrecognized as prompt".format(f))
