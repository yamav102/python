import re
print(bool(re.search('(?=abc)(?!def)', 'abcdef')))
