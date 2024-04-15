# Dotprompt

Dotprompt is a simple library allowing to store your GenAI prompts as .prompt files. 
It is a simple way to keep your prompts organized and easily accessible alongside your python code.

## How to use
Store your prompts as .prompts or .jprompt files in a prompts folder in your at the root of your code directory.
Exemple :
```
my_project/
    my_code.py
    prompts/
        my_prompt.system.prompt
        not_specific.prompt
        my_other_prompt.jprompt
```

Then simply import dotprompt in your code and get your prompts as object of dotprompts

```python
import dotprompt

...

res = gen_ai_client.complete(dotprompt.my_prompt.system)
```

When getting a prompt, the library return it as a string and you can use variables to enrich it.
```my_prompt.system.prompt
/* A system prompt with variables {speciality} and {age} */
You are an AI specialized in {speciality}. You are {age} years old.
```
```python
import dotprompt

res = genai_client.complete(
    prompt = dotprompt.my_prompt.system.format(
        speciality = "medicine",
        age = 3
    )
)
```

When comments have been add to the prompt files, the dotprompt store it in the info attribute of the prompt object.
```python
import dotprompt

print(dotprompt.my_prompt.info['system'])
>>>"A system prompt with variables {speciality} and {age}"
```


## Files format
### .prompt
The .prompt file format is a simple text file containing the prompt as a string.

It uses a second extension to specify the type of prompt in the file.

Example:
If you have a prompt with a system prompt and a user prompt, you'll make two files as follows:
- my_prompt.system.prompt
- my_prompt.user.prompt

And you'll be able to access them as follows:
```python
import dotprompt

res = gen_ai_client.complete(
    prompt = {
        "system": dotprompt.my_prompt.system, 
        "user": dotprompt.my_prompt.user
    })
```

If you don't provide a second extension in the prompt file name, the prompt will be considered as a "prompt".
```python
import dotprompt

...
res = gen_ai_client.complete(dotprompt.not_specific.prompt)
```

The .prompt files can contain comments at the beginning of the file, between /* and */ characters. 
The comments will be stored in the info attribute of the prompt object and will not be displayed as part of the prompt.

### .jprompt
The .jprompt file format is a json file containing multiple prompts with the specified type.
```json
{
    "system": "You are an AI specialized in {speciality}. You are {age} years old.",
    "user": "Tells me about the studies to be come an expert in {speciality}."
}
```
The jprompt can be commented the same way as the .prompt files.