from sklearn.cluster import KMeans
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
import base64
from io import BytesIO

import numpy as np
import math
p1=np.array([0,0])
p2=np.array([1000,2000])
p3=p2-p1
p4=math.hypot(p3[0],p3[1])
p5=math.sqrt(p3[0]**2+p3[1]**2)
print(p4,p5)
print(max([1,2,3]))