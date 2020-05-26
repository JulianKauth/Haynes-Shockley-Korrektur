import os

for file in os.listdir("data"):
    print(file)
    with open("data/" + file, "r") as f:
        lines = f.readlines()
    if len(lines) < 1:
        print("fail: " + file)
        continue
    lines[0] = "#" + lines[0]
    lines[1] = "#" + lines[1]
    lines[2] = "#" + lines[2]
    with open("data/" + file, "w") as f:
        for line in lines:
            f.write(line)
