import json
from tqdm import tqdm
from matplotlib import pyplot as plt
from random import randrange
import sys

i = int(sys.argv[1])
# Opening JSON file
f = open('cleaned.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)

# i = randrange(0, 2199)
img = plt.imread('images/' + str(i) + '.png')
plt.imshow(img)
print(data[i]['description'])
plt.show()
