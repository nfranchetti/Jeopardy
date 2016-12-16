#!/usr/bin/env python

import numpy as np
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import random

from wordcloud import WordCloud, STOPWORDS

img_list = ['j.jpg', 'e.jpg', 'o.jpg', 'p.jpg', 'a.png', 'r.jpg', 'd.jpg', 'y.jpg']
cluster_list = [1, 2, 3, 4, 24, 6, 7, 8]



# def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
#     return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


def make_jeopardy_clouds(img, cluster):
	d = path.dirname(__file__)

	mask = np.array(Image.open(path.join(d, "images/%s" % img)))

	text = open("clusters/cluster%s.txt" % cluster).read()

	stopwords = set(STOPWORDS)

	wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=10,
	               random_state=1).generate(text)

	default_colors = wc.to_array()
	plt.title("Custom colors")
	plt.imshow(wc.recolor(random_state=3))
	wc.to_file("word_cloud.png")
	plt.axis("off")
	plt.figure()
	plt.title("Default colors")
	plt.imshow(default_colors)
	plt.axis("off")
	plt.show()
	wc.to_file("images/final/%s.png" % img[0])

for i in range(len(img_list)):
	make_jeopardy_clouds(img_list[i], cluster_list[i])