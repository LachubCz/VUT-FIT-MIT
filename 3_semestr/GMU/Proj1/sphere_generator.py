import numpy as np 

x = np.random.randint(1000, size=10)
y = np.random.randint(1000, size=10)
z = np.random.randint(1000, size=10)

for i, item in enumerate(zip(x, y, z)):
    if 1000 - max(item) > min(item):
        print(item[0], item[1], item[2], np.random.randint(1, min(item), size=1)[0])
    else:
        print(item[0], item[1], item[2], np.random.randint(1, 1000 - max(item), size=1)[0])
