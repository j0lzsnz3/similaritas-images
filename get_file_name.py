import os

file_names = []
for root, dirs, files in os.walk("images"):
    for filename in files:
        if filename.endswith(".png"):
            file_names.append(filename)

for i in range(len(file_names)):
    print(file_names.__getitem__(i))