import logging
import os
from .prompt import Prompt
from .exceptions import PrompDirectoryNotFoundError, PromptError


IGNORED_EXT = ['py']


logging.info("Loading prompt files")
__prompt_dir =os.path.join(os.getcwd(), 'prompts')
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
