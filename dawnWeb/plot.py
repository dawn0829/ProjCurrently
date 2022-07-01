
# df = pd.read_csv('/home/user/Desktop/ProjCurrently/dawnWeb/ECGRecord/dawn/2022-05-25 02:48:08.944683.csv')
# print(df)
# print(df[1:])
# x=list(range(len(df)))
# y=df
# plt.plot(x,y[:])
# plt.show()
# x=[]
# y=[]
# for i in range(10):
#     x.append(i)

# for i in range(10):
#     y.append(i)
# plt.plot(x,y,marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")
# plt.show()

import scipy.signal
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 256, endpoint=False)
y = np.cos(-x**2/6.0)
yre = scipy.signal.resample(y,20)
xre = np.linspace(0, 10, len(yre), endpoint=False)
plt.plot(x,y,'b', xre,yre,'or-')
plt.show()