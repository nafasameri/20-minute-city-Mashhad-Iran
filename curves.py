import numpy as np
import pandas as pd
from matplotlib import pyplot as plt



data = pd.read_csv('results.csv')
# print(data.head())
# data = data.transpose()


# percentage = data.iloc[-1]
percentage = data['percentage']
Unnamed = data['Unnamed: 0']
# percentage = percentage.transpose()
# percentage= percentage.astype(str)
print(Unnamed)
print(percentage)
# percentage['percentage'].hist()
plt.hist([Unnamed, percentage])
plt.show()