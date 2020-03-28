# error-explainer
This is a project aimed at tool developers who want to create custom error checks 
provide better messages with improved location, accuracy and message quality for different errors in Python.

Some checks for syntax errors are provided out of the box.

Currently available checks can be found in `error-explainer/messages.py`

## Installation
To install this package use `pip install error-explainer`

## Usage

### Check a Python file for possible errors
```python
from error_explainer.check_runner import run_checks

messages = run_checks("path/to/file")
```
Messages will be a list of strings containing the generated messages.

### Add a new custom check
Custom checks can be added to the list of checks ran while calling run_checks().
To add a new check use `@add_check` annotation.
```python
from error_explainer.check_runner import add_check, add_message

@add_check
def custom_check(filename):
    # code for the check  
    if error_in_file:
        # To add a message to the list of messages returned when calling run_checks() use 
        add_message("code_for_the_message", argument1="foo", argument2="bar")
        # Custom arguments can be used in the message text to make messages more dynamic
```

### Manage messages
Messages used in checks can be:

added
```python
from error_explainer.messages import add_message

# message text can contain arguments in curly brackets these can be later given values using kwargs
add_message("code_for_the_message", "Message text with {dynamic_arguments}")
```

removed
```python
from error_explainer.messages import remove_message

remove_message("code_for_the_message")
```

overwritten
```python
from error_explainer.messages import overwrite_message

overwrite_message("code_for_the_message", "Message text with {dynamic_arguments}")
```