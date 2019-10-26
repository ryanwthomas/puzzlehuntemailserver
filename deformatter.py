import re

def df_string(value):
    if (value != None):
        value = str(value)
        # set to uppercase, then remove all non-alphanumeric characters
        temp = re.sub(r'[^A-Z0-9]', '', value.upper())
        return temp
    else:
        return None

def compare_strings(alpha, bravo):
    return df_string(alpha) == df_string(bravo)
