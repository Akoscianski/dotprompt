import os
import logging
import sys
import re
import json
from .exceptions import PromptFileError

class Prompt:
    def __init__(self, prompt_file, ext):
        self.infos = {}
        if ext == "prompt":
            self.prompt_name = self.__read_prompt(prompt_file)
        elif ext == "jprompt":
            self.prompt_name = self.__read_jprompt(prompt_file)
        else:
            raise PromptFileError("Extension {} not recognized".format(ext))

    def __read_prompt(self, prompt_file):
        pargs = os.path.basename(prompt_file).split('.')
        if len(pargs) == 3:
            p_name, p_type, p_ext = pargs
        elif len(pargs) == 2:
            p_name, p_ext = pargs
            p_type = "prompt"
        else:
            raise PromptFileError("Impossible to read file {}".format(prompt_file))
        with open(prompt_file, 'r', encoding='utf8') as f_in:
            content = f_in.read()
            commentaires = re.findall(r'/\*.*?\*/', content, re.DOTALL)
            self.infos[p_type] = {"description": commentaires, "variables": {}}
            texte = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            varaibles_pattern = r'\{([^}]+)\}'
            variables = re.findall(varaibles_pattern, texte)
            for var in variables:
                if ":" in var:
                    var_name, var_type = var.split(":")
                    texte = texte.replace("{" + var + "}", "{" + var_name + "}")    #Don't keep teh description in the prompt
                    self.infos[p_type]['variables'][var_name] = var_type
                else:
                    self.infos[p_type]['variables'][var] = "No description found"
            setattr(self, p_type, texte)
            return p_name

    def add_file(self, prompt_file):
        self.__read_prompt(prompt_file)

    def __read_jprompt(self, prompt_file):
        pargs = os.path.basename(prompt_file).split('.')
        if len(pargs) == 2:
            p_name, p_ext = pargs
            with open(prompt_file, 'r', encoding='utf8') as f_in:
                content = f_in.read()
                commentaires = re.findall(r'/\*.*?\*/', content, re.DOTALL)
                self.infos["prompt"] = commentaires
                texte = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
                prompts = json.loads(texte)
                for key in prompts:
                    if type(prompts[key]) != str:
                        raise TypeError("Prompt {} from file {} is not a string".format(key, prompt_file))
                    setattr(self, key, prompts[key])
                return p_name
        else:
            raise PromptFileError("Impossible to read file {}".format(prompt_file))
