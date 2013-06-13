# -*- coding: utf-8 -*-
#!/usr/bin/env python

def plot(image, users):
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    from scipy import stats
    n = []
    p = []
    c = 0
    for u in users:
        n.append(u.name)
        p.append(u.progress)
        c += 1
    matplotlib.use('Agg')

    ind = np.arange(c)+0.10
    width = 0.35
    fig = plt.figure(figsize=(5, 4), dpi=72)
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, p, width, color="b")
    plt.ylim((0, 100))
    ax.set_ylabel('Percentage')
    ax.set_title('Users Percentage Progress Completed')
    ax.set_xticks(ind+0.15)
    ax.set_xticklabels(n)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height), ha='center', va='bottom')

    autolabel(rects1)

    plt.savefig(image, format='png', dpi=72)
