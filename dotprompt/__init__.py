import logging
import os
import traceback
import sys
from .prompt import Prompt
from .exceptions import PrompDirectoryNotFoundError, PromptError

__version__ = "0.1.8"

IGNORED_EXT = ['py']


def load_folder(prompt_dir):
    if not os.path.isdir(prompt_dir):
        logging.warning("No prompts directory detected in the project structure.")
        # raise PrompDirectoryNotFoundError("Prompt directory \"prompts\" not found")
    else:
        for f in os.listdir(prompt_dir):
            parts = f.split('.')
            if parts[-1] == "prompt":
                if parts[0] in globals():
                    globals()[parts[0]].add_file(os.path.join(prompt_dir, f))
                else:
                    globals()[parts[0]] = Prompt(os.path.join(prompt_dir, f), ext="prompt")
            elif parts[-1] == "jprompt":
                if parts[0] in globals():
                    raise PromptError("Prompt {} already exists".format(parts[0]))
                else:
                    globals()[parts[0]] = Prompt(os.path.join(prompt_dir, f), ext="jprompt")
            elif parts[-1] in IGNORED_EXT:
                logging.debug("Ignoring file {}".format(f))
            else:
                logging.warning("File {} unrecognized as prompt".format(f))


logging.info("Loading prompt files")

# Getting the script importing dotprompt module
import_path = None
for i in traceback.extract_stack():
    if "import" in i._line and "dotprompt" in i._line:
        import_path = i.filename
        pass

logging.info(f"Module dotprompt imported from {import_path}")

__prompt_dir = os.path.join(os.getcwd(), 'prompts')
if not os.path.isdir(__prompt_dir):
    logging.warning(f"Prompt directory \"prompts\" not found in {__prompt_dir}")
    not_found = True
    ROOT_DIR = os.path.abspath(os.curdir)
    caller_path = os.path.dirname(import_path)
    logging.warning(f"Crawling from {caller_path}")
    while not_found:
        if "prompts" in os.listdir(caller_path):
            __prompt_dir = os.path.join(caller_path, "prompts")
            not_found = False
        elif caller_path == ROOT_DIR:
            logging.warning(f"No prompt dir found in {ROOT_DIR}")
        caller_path = os.path.dirname(caller_path)
load_folder(__prompt_dir)
