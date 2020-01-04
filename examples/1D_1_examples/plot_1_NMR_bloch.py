# -*- coding: utf-8 -*-
"""
Nuclear Magnetic Resonance (NMR) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
#%%
# The following dataset is a :math:`^{13}\mathrm{C}` time-domain NMR Bloch decay
# signal of ethanol.
# Let's load this data file and take a quick look at its data
# structure. We follow the steps described in the previous example.
import csdmpy as cp

filename = "https://osu.box.com/shared/static/2e4fqm8n8bh4i5wgrinbwcavafa8x7y1.csdf"
NMR_data = cp.load(filename)

#%%
print(NMR_data.data_structure)

#%%
# This particular example illustrates two additional attributes of the CSD model,
# namely, the :attr:`~csdmpy.csdm.CSDM.geographic_coordinate` and
# :attr:`~csdmpy.csdm.CSDM.tags`. The `geographic_coordinate` described the
# location where the CSDM file was last serialized. You may access this
# attribute through,

#%%
NMR_data.geographic_coordinate

#%%
# The `tags` attribute is a list of keywords that best describe the dataset.
# The `tags` attribute is accessed through,

#%%
NMR_data.tags

#%%
# You may add additional tags, if so desired, to this list using the `append`
# method of python's list class, for example

#%%
NMR_data.tags.append("Bloch decay")
NMR_data.tags

#%%
# Unlike the previous example, the data structure of an NMR measurement is
# a complex-valued dependent variable. In this example, the values are

#%%
y = NMR_data.dependent_variables
print(y[0].components[0])


#%%
# The coordinates along the dimension are

x = NMR_data.dimensions
x0 = x[0].coordinates
print(x0)

#%%
# In the previous example, we illustrated a matplotlib script for plotting 1D data.
# Here, we use the csdmpy :meth:`~csdmpy.plot` method, which is a supplementary method
# for plotting 1D and 2D datasets only.

cp.plot(NMR_data)
