import re

text = "secret_access_key as AKIAIOSFODNN7EXAMPLE"

matchres = re.match(r"(\w*)(\s)([\w\d]*)", text)

print(matchres.group(1))
print(matchres.group(2))
print(matchres.group(3))
