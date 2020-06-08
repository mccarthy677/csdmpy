# -*- coding: utf-8 -*-
import csdmpy as cp

filename = cp.tests.test01  # replace this with your file's name.
testdata1 = cp.load(filename)
testdata1.description

# Accessing dimensions and dependent variables of the dataset
x = testdata1.dimensions
y = testdata1.dependent_variables
x[0].description
y[0].description

# Coordinates along the dimension
x[0].coordinates
x[0].coordinates.value

# Components of the dependent variable¶
y[0].components
y[0].components.shape

import matplotlib.pyplot as plt

plt.figure(figsize=(5, 3.5))
plt.plot(x[0].coordinates, y[0].components[0])
plt.xlabel(x[0].axis_label)
plt.ylabel(y[0].axis_label[0])
plt.title(y[0].name)
plt.tight_layout()
plt.show()
