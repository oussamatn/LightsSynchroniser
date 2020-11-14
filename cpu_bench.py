from collections import namedtuple
from math import sqrt
import random
from PIL import Image
import pyscreenshot as ImageGrab
import time
#Results
# --- 0.315089941025 seconds ---
# --- 0.727060079575 seconds ---
# ['#6a5235']
# --- 0.370645046234 seconds ---
# [107, 82, 54]

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def colorz(n=3):
    img = ImageGrab.grab(backend="pil", childprocess=False)
    img = img.resize((150, 150), Image.BILINEAR)
    #img.thumbnail((200, 200))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)

def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters
def custom_color():
	diff = 10
	width = 32*16
	height = 32*9
	key_color = None
	im = ImageGrab.grab(backend="pil", childprocess=False)
	resized_img = im.resize((150, 150), Image.BILINEAR)
	
	result = resized_img.convert('P', palette=Image.ADAPTIVE, colors=1)
	result.save("test.png")
	dominant_color = result.convert('RGB').getpixel((10, 10))
	
	if key_color is None:
		key_color = dominant_color
	else:
		if abs(dominant_color[0] - key_color[0]) < diff\
			and abs(dominant_color[1] - key_color[1]) < diff \
				and abs(dominant_color[2] - key_color[2]) < diff:
				return dominant_color
		else:
			key_color = dominant_color
	return dominant_color

width = 32*16
height = 32*9	
bbox = (0, 0, width, height)
start_time = time.time()
#print(colorz())
img = ImageGrab.grab(bbox=bbox)
print("--- %s seconds ---" % (time.time() - start_time))

print("--- --------------------------------- --- ")
start_time = time.time()
am = colorz(3)
print("--- %s seconds ---" % (time.time() - start_time))

rgb = list(am)[0].lstrip('#')
print(rgb)
print(format( tuple(int(rgb[i:i+2], 16) for i in (0, 2, 4)) ))

print("--- --------------------------------- --- ")
start_time = time.time()
bm = custom_color()
print("--- %s seconds ---" % (time.time() - start_time))
print (list(bm))

