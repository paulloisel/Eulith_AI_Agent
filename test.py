import re

input_str = '"Initiate a swap between WETH and UNI"'
pattern = r'^"(.+)"$'

# Check if the pattern matches the input string
match = re.search(pattern, input_str)

if match:
    output_str = '"' + match.group(1) + '\\n\\n###\\n\\n"'
    print(output_str)
else:
    print("No match found")