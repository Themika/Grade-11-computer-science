import re

def validate_input(value, pattern, error_label, error_message):
    if not re.match(pattern, value):
        error_label.config(text=error_message)
        return False
    else:
        error_label.config(text="")
        return True