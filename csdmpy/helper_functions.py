# -*- coding: utf-8 -*-
"""Helper functions."""
from copy import deepcopy
from warnings import warn

import matplotlib.projections as proj
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import NonUniformImage


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"

scalar = ["scalar", "vector_1", "pixel_1", "matrix_1_1", "symmetric_matrix_1"]


def _get_label_from_dv(dv, i):
    """Return label along with the unit of the dependent variable

    Args:
        dv: DependentVariable object.
        i: integer counter.
    """
    name, unit = dv.name, dv.unit
    name = name if name != "" else str(i)
    label = f"{name} / ({unit})" if unit != "" else name
    return label


class CSDMAxes(plt.Axes):
    """A custom CSDM data plot axes."""

    name = "csdm"

    def plot(self, csdm, **kwargs):
        """Produce a figure using the `plot` method from the matplotlib library.

        Apply to all 1D datasets with single-component dependent-variables. For
        multiple dependent variables, the data from individual dependent-variables are
        plotted on the same figure.

        Args:
            csdm: A CSDM object of a one-dimensional dataset.
            kwargs: Additional keyword arguments for the matplotlib plot() method.

        Example
        -------

        >>> ax = plt.subplot(projection='csdm') # doctest: +SKIP
        >>> ax.plot(csdm_object) # doctest: +SKIP
        >>> plt.show() # doctest: +SKIP

        """
        x, y = csdm.dimensions, csdm.dependent_variables

        message = (
            "The function requires a 1D dataset with single-component dependent "
            "variables. For multiple dependent-variables, the data from all the "
            "dependent variables are ploted on the same figure."
        )
        if len(x) != 1:
            raise Exception(message)
        for y_ in y:
            if len(y_.components) != 1:
                raise Exception(message)

        z = csdm.split()
        one = True if len(z) == 1 else False

        for i, item in enumerate(z):
            x_, y_ = item.to_list()
            # dv will always be at index 0 because we called the object.split() before.
            dv = item.dependent_variables[0]

            kwargs_ = deepcopy(kwargs)
            # add a default label if not provided by the user.
            if "label" not in kwargs_.keys():
                kwargs_["label"] = dv.name if one else _get_label_from_dv(dv, i)

            r_plt = super().plot(x_, y_, **kwargs_)
        self.set_xlim(x[0].coordinates.value.min(), x[0].coordinates.value.max())
        self.set_xlabel(f"{x[0].axis_label} - 0")

        ylabel = dv.axis_label[0] if one else "dimensionless"
        self.set_ylabel(ylabel)
        self.grid(color="gray", linestyle="--", linewidth=0.5)
        self.legend()

        return r_plt

    def imshow(self, csdm, origin="lower", **kwargs):
        """Produce a figure using the `imshow` method from the matplotlib library.

        Apply to all 2D datasets with either single-component (scalar),
        three-components (pixel_3), or four-components (pixel_4) dependent-variables.
        For single-component (scalar) dependent-variable, grayscale image is produced.
        For three-components (pixel_3) dependent-variable, an RGB image is produced.
        For four-components (pixel_4) dependent-variable, an RGBA image is produced.

        For multiple dependent variables, the data from individual dependent-variables
        are plotted on the same figure.

        Args:
            csdm: A CSDM object of a two-dimensional dataset with scalar, pixel_3, or
                pixel_4 quantity_type dependent variable.
            origin: The matplotlib `origin` argument. In matplotlib, the default is
                'upper'. In csdmpy, however, we set the default to 'lower'.
            kwargs: Additional keyword arguments for the matplotlib imshow() method.

        Example
        -------

        >>> ax = plt.subplot(projection='csdm') # doctest: +SKIP
        >>> ax.imshow(csdm_object) # doctest: +SKIP
        >>> plt.show() # doctest: +SKIP

        """
        x, y = csdm.dimensions, csdm.dependent_variables

        message = (
            "The function requires a 2D dataset with a single-component (scalar), "
            "three components (pixel_3), or four components (pixel_4) dependent "
            "variables. The pixel_3 produces an RGB image while pixel_4, a RGBA image."
        )
        if len(x) != 2:
            raise Exception(message)
        for y_ in y:
            if len(y_.components) not in [1, 3, 4]:
                raise Exception(message)

        if x[0].type == "linear" and x[1].type == "linear":
            return self._call_uniform_2D(csdm, origin=origin, **kwargs)

    def _call_uniform_2D(self, csdm, **kwargs):

        kw_keys = kwargs.keys()

        # set extent
        x = csdm.dimensions
        x0, x1 = x[0].coordinates.value, x[1].coordinates.value
        extent = [x0[0], x0[-1], x1[0], x1[-1]]
        if kwargs["origin"] == "upper":
            extent = [x0[0], x0[-1], x1[-1], x1[0]]
        if "extent" not in kw_keys:
            kwargs["extent"] = extent

        # add cmap for multiple dependent variables.
        cmaps_bool = False
        if "cmaps" in kw_keys:
            cmaps_bool = True
            cmaps = kwargs.pop("cmaps")

        one = True if len(csdm.dependent_variables) == 1 else False

        for i, dv in enumerate(csdm.dependent_variables):
            y = dv.components
            if dv.quantity_type == "scalar":
                if cmaps_bool:
                    kwargs["cmap"] = cmaps[i]

                r_plt = super().imshow(y[0], **kwargs)

                label = dv.axis_label[0] if one else f"{dv.name} - {dv.axis_label[0]}"
                cbar = plt.gcf().colorbar(r_plt, ax=self)
                cbar.ax.minorticks_off()
                cbar.set_label(label)

            if dv.quantity_type == "pixel_3":
                r_plt = super().imshow(np.moveaxis(y.copy(), 0, -1), **kwargs)

            if dv.quantity_type == "pixel_4":
                r_plt = super().imshow(np.moveaxis(y.copy(), 0, -1), **kwargs)

        self.set_xlabel(f"{x[0].axis_label} - 0")
        self.set_ylabel(f"{x[1].axis_label} - 0")
        if one:
            self.set_title(dv.name)
        self.grid(color="gray", linestyle="--", linewidth=0.5)

        return r_plt


proj.register_projection(CSDMAxes)


def _preview(data, reverse_axis=None, range_=None, **kwargs):
    """Quick display of the data."""
    if reverse_axis is not None:
        kwargs["reverse_axis"] = reverse_axis

    if range_ is None:
        range_ = [[None, None], [None, None]]

    x = data.dimensions
    y = data.dependent_variables
    y_len = len(y)
    y_grid = int(y_len / 2) + 1

    if len(x) == 0:
        raise NotImplementedError(
            "Preview of zero dimensional datasets is not implemented."
        )

    if len(x) > 2:
        raise NotImplementedError(
            "Preview of three or higher dimensional datasets " "is not implemented."
        )

    if np.any([x[i].type == "labeled" for i in range(len(x))]):
        raise NotImplementedError("Preview of labeled dimensions is not implemented.")

    fig = plt.gcf()
    if y_len <= 2:
        ax = fig.subplots(y_grid)
        ax = [[ax]] if y_len == 1 else [ax]
    else:
        ax = fig.subplots(y_grid, 2)

    if len(x) == 1:
        one_d_plots(ax, x, y, range_, **kwargs)

    if len(x) == 2:
        two_d_plots(ax, x, y, range_, **kwargs)

    return fig


def one_d_plots(ax, x, y, range_, **kwargs):
    """A collection of possible 1D plots."""
    for i, y_item in enumerate(y):
        i0 = int(i / 2)
        j0 = int(i % 2)
        ax_ = ax[i0][j0]

        if y_item.quantity_type in scalar:
            oneD_scalar(x, y_item, ax_, range_, **kwargs)
        if "vector" in y_item.quantity_type:
            vector_plot(x, y_item, ax_, range_, **kwargs)
        # if "audio" in y_item.quantity_type:
        #     audio(x, y, i, fig, ax, **kwargs)


def two_d_plots(ax, x, y, range_, **kwargs):
    """A collection of possible 2D plots."""
    for i, y_item in enumerate(y):
        i0 = int(i / 2)
        j0 = int(i % 2)
        ax_ = ax[i0][j0]

        if y_item.quantity_type == "pixel_3":
            warn("This method interprets the `pixel_3` dataset as an RGB image.")
            RGB_image(x, y_item, ax_, range_, **kwargs)

        if y_item.quantity_type in scalar:
            twoD_scalar(x, y_item, ax_, range_, **kwargs)

        if "vector" in y_item.quantity_type:
            vector_plot(x, y_item, ax_, range_, **kwargs)


def oneD_scalar(x, y, ax, range_, **kwargs):
    reverse = [False]
    if "reverse_axis" in kwargs.keys():
        reverse = kwargs["reverse_axis"]
        kwargs.pop("reverse_axis")

    components = y.components.shape[0]
    for k in range(components):
        ax.plot(x[0].coordinates, y.components[k], **kwargs)
        ax.set_xlim(x[0].coordinates.value.min(), x[0].coordinates.value.max())
        ax.set_xlabel(f"{x[0].axis_label} - 0")
        ax.set_ylabel(y.axis_label[0])
        ax.set_title("{0}".format(y.name))
        ax.grid(color="gray", linestyle="--", linewidth=0.5)

    ax.set_xlim(range_[0])
    ax.set_ylim(range_[1])

    if reverse[0]:
        ax.invert_xaxis()


def twoD_scalar(x, y, ax, range_, **kwargs):
    reverse = [False, False]
    if "reverse_axis" in kwargs.keys():
        reverse = kwargs["reverse_axis"]
        kwargs.pop("reverse_axis")

    x0 = x[0].coordinates.value
    x1 = x[1].coordinates.value
    y00 = y.components[0]
    extent = [x0[0], x0[-1], x1[0], x1[-1]]
    if "extent" not in kwargs.keys():
        kwargs["extent"] = extent

    if x[0].type == "linear" and x[1].type == "linear":
        if "origin" not in kwargs.keys():
            kwargs["origin"] = "lower"
        if "aspect" not in kwargs.keys():
            kwargs["aspect"] = "auto"

        cs = ax.imshow(y00, **kwargs)
    else:
        if "interpolation" not in kwargs.keys():
            kwargs["interpolation"] = "nearest"

        cs = NonUniformImage(ax, **kwargs)
        cs.set_data(x0, x1, y00)
        ax.images.append(cs)

    cbar = ax.figure.colorbar(cs, ax=ax)
    cbar.ax.minorticks_off()
    cbar.set_label(y.axis_label[0])
    ax.set_xlim([extent[0], extent[1]])
    ax.set_ylim([extent[2], extent[3]])
    ax.set_xlabel(f"{x[0].axis_label} - 0")
    ax.set_ylabel(f"{x[1].axis_label} - 1")
    ax.set_title("{0}".format(y.name))
    ax.grid(color="gray", linestyle="--", linewidth=0.5)

    ax.set_xlim(range_[0])
    ax.set_ylim(range_[1])

    if reverse[0]:
        ax.invert_xaxis()
    if reverse[1]:
        ax.invert_yaxis()


def vector_plot(x, y, ax, range_, **kwargs):
    reverse = [False, False]
    if "reverse_axis" in kwargs.keys():
        reverse = kwargs["reverse_axis"]
        kwargs.pop("reverse_axis")

    x0 = x[0].coordinates.value
    if len(x) == 2:
        x1 = x[1].coordinates.value
    else:
        x1 = np.zeros(1)

    x0, x1 = np.meshgrid(x0, x1)
    u1 = y.components[0]
    v1 = y.components[1]

    if "pivot" not in kwargs.keys():
        kwargs["pivot"] = "middle"
    ax.quiver(x0, x1, u1, v1, **kwargs)
    ax.set_xlabel(f"{x[0].axis_label} - 0")
    ax.set_xlim(x[0].coordinates.value.min(), x[0].coordinates.value.max())
    if len(x) == 2:
        ax.set_ylim(x[1].coordinates.value.min(), x[1].coordinates.value.max())
        ax.set_ylabel(f"{x[1].axis_label} - 1")
        if reverse[1]:
            ax.invert_yaxis()
    else:
        ax.set_ylim([-y.components.max(), y.components.max()])
    ax.set_title("{0}".format(y.name))
    ax.grid(color="gray", linestyle="--", linewidth=0.5)

    ax.set_xlim(range_[0])
    ax.set_ylim(range_[1])

    if reverse[0]:
        ax.invert_xaxis()


def RGB_image(x, y, ax, range_, **kwargs):
    reverse = [False, False]
    if "reverse_axis" in kwargs.keys():
        reverse = kwargs["reverse_axis"]
        kwargs.pop("reverse_axis")

    y0 = y.components
    ax.imshow(np.moveaxis(y0 / y0.max(), 0, -1), **kwargs)
    ax.set_title("{0}".format(y.name))

    ax.set_xlim(range_[0])
    ax.set_ylim(range_[1])

    if reverse[0]:
        ax.invert_xaxis()
    if reverse[1]:
        ax.invert_yaxis()


# def audio(x, y, i0, fig, ax):
#     try:
#         SOUND = 1
#         import sounddevice as sd
#     except ImportError:
#         SOUND = 0
#         string = (
#             "Module 'sounddevice' is not installed. All audio data files will "
#             "not be played. To enable audio files, install 'sounddevice' using"
#             " 'pip install sounddevice'."
#         )
#         warn(string)

#     plot1D(x, y, i0, ax)
#     if SOUND == 1:
#         data_max = y[i0].components.max()
#         sd.play(0.9 * y[i0].components.T / data_max, 1 / x[0].increment.to("s").value)
