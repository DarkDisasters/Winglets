#!/user/bin/python
# -*- coding: UTF-8 -*-

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

def measure(loc, scale, size):
     "Measurement model, return two coupled measurements."
     # np.random.normal(loc=0.0, scale=1.0,size=None)
     # loc：分布均值 scale：标准差 size：输出shape

     m1 = np.random.normal(loc=loc, scale=scale, size=size)
     m2 = np.random.normal(loc=-loc, scale=scale, size=size)
     return m1+m2, m1-m2

t1, t2 = measure(2, 3, 300)
c1, c2 = measure(-1, 2, 300)

label = range(0,t1.size+c1.size)
lab = np.array(label)
np.random.shuffle(lab)

raw_x_list = []
raw_y_list = []

while len(raw_x_list)<(t1.size+c1.size):
     v = lab[len(raw_x_list)]
     if(v<t1.size):
          raw_x_list.append(t1[v])
          raw_y_list.append(t2[v])
     else:
          raw_x_list.append(c1[v-t1.size])
          raw_y_list.append(c2[v-t1.size])

raw_x = np.array(raw_x_list)
raw_y = np.array(raw_y_list)

boot_x_list = []
boot_y_list = []

while len(boot_x_list) < 50:
     p = np.random.randint(0, raw_x.size)
     boot_x_list.append(raw_x[p])
     boot_y_list.append(raw_y[p])

boot_x = np.array(boot_x_list)
boot_y = np.array(boot_y_list)

print(raw_x.size)

margin = 0.5

xmin = raw_x.min()-margin
xmax = raw_x.max()+margin
ymin = raw_y.min()-margin
ymax = raw_y.max()+margin

X, Y = np.mgrid[xmin:xmax:300j, ymin:ymax:300j]
positions = np.vstack([X.ravel(), Y.ravel()])

raw_values = np.vstack([raw_x, raw_y])
raw_kernel = stats.gaussian_kde(raw_values)
raw_z = np.reshape(raw_kernel(positions).T, X.shape)

fig, ax = plt.subplots(num=100)

ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])

im = ax.imshow(np.rot90(raw_z), cmap='Blues', extent=[xmin, xmax, ymin, ymax])
plt.colorbar(im)
ax.plot(raw_x, raw_y, 'k.', markersize=2, alpha=0.7)
plt.title('surprise-raw')
# fig.savefig('surprise-raw')

# fig, ax = plt.subplots()
# im = ax.imshow(np.rot90(surprise), cmap=plt.cm.summer, extent=[xmin, xmax, ymin, ymax])

#ax.set_xlim([xmin, xmax])
#ax.set_ylim([ymin, ymax])

#plt.colorbar(im)

#ax.plot(m1, m2, 'k.', markersize=4)
plt.show()
