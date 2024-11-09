import seaborn as sns
import matplotlib.pyplot as plt
import os


class Boxplot:
    def __init__(
        self,
        df,
        x=None,
        y=None,
        hue=None,
        order=None,
        hue_order=None,
        orient=None,
        color=None,
        palette=None,
        saturation=0.75,
        width=0.8,
        dodge=True,
        fliersize=5,
        linewidth=None,
        whis=1.5,
        ax=None,
        title=None,
        **kwargs
    ):
        """
        This is used to create boxplot figures using seaborn.

        Parameters:
        -----------
        df (pandas.DataFrame):
            The dataframe containing the data to plot.
        x, y (str):
            The names of two columns in df. The box plots will be for the y column grouped by x column values.
        hue (str, optional):
            Column name for grouping the data by color/hue.
        order, hue_order (list, optional):
            Order to plot the categorical levels in.
        orient (str, optional):
            Orientation of the plot. 'v' or 'h'.
        color (str, optional):
            Color for all of the elements.
        palette (str, optional):
            Colors to use for the different levels of the hue variable.
        saturation (float, optional):
            Proportion of the original saturation to draw colors.
        width (float, optional):
            Width of a full element when not using hue nesting, or width of all the elements for one
            level of the major grouping variable.
        dodge (bool, optional):
            When hue nesting is used, whether elements should be shifted along the categorical axis.
        fliersize (float, optional):
            Size of the markers used to indicate outlier observations.
        linewidth (float, optional):
            Line width of the box outlines.
        whis (float, optional):
            Proportion of the IQR past the low and high quartiles to extend the plot whiskers.
        ax (matplotlib.axes, optional):
            Pre-existing axes for the plot. Otherwise, a new one is created.
        title (str, optional):
            Title for the plot.
        **kwargs:
            Additional keyword arguments are passed to the underlying seaborn boxplot function.
            Other keyword arguments are passed through to matplotlib.axes.Axes.boxplot().

        Return:
        -------
        None
        """
        self.__df = df
        self.__x = x
        self.__y = y
        self.__hue = hue
        self.__order = order
        self.__hue_order = hue_order
        self.__orient = orient
        self.__color = color
        self.__palette = palette
        self.__saturation = saturation
        self.__width = width
        self.__dodge = dodge
        self.__fliersize = fliersize
        self.__linewidth = linewidth
        self.__whis = whis
        self.__ax = ax
        self.__title = title
        self.__kwargs = kwargs

        self.__plot()

    def __plot(self):
        """
        This is a private method used to create the boxplot.

        """
        sns.boxplot(
            x=self.__x,
            y=self.__y,
            hue=self.__hue,
            data=self.__df,
            order=self.__order,
            hue_order=self.__hue_order,
            orient=self.__orient,
            color=self.__color,
            palette=self.__palette,
            saturation=self.__saturation,
            width=self.__width,
            dodge=self.__dodge,
            fliersize=self.__fliersize,
            linewidth=self.__linewidth,
            whis=self.__whis,
            ax=self.__ax,
            **self.__kwargs
        )

        if self.__title:
            plt.title(self.__title)

    def save_plot(self, file_name, folder=None, size=(10, 6)):
        """
        This method saves the created plot in the specified directory.

        Args:
            file_name (str): Name of the file
            folder (str, optional): Name of the directory. If not available, it creates one.
            size (tuple, optional): Size of the figure in inches (width, height). Default is (10, 6).

        """
        if folder:
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_name = os.path.join(folder, file_name)

        fig = plt.figure(figsize=size)
        self.__plot()
        plt.savefig(file_name)
        plt.close(fig)  # prevent figure to pop up in the notebook
        plt.ion()  # turns the display of the plot back on


class DensityPlot:
    def __init__(
        self,
        df,
        x=None,
        y=None,
        hue=None,
        weights=None,
        palette=None,
        hue_order=None,
        hue_norm=None,
        fill=False,
        color=None,
        multiple="layer",
        common_norm=True,
        common_grid=False,
        cumulative=False,
        bw_method="scott",
        bw_adjust=1,
        warn_singular=True,
        log_scale=None,
        levels=10,
        thresh=0.05,
        gridsize=200,
        cut=3,
        clip=None,
        legend=True,
        cbar=False,
        cbar_ax=None,
        cbar_kws=None,
        ax=None,
        title=None,
        **kwargs
    ):
        """
        This is used to create densityPlot figures using seaborn.

        Parameters:
        -----------
        df : Pandas dataframe
            Data for the plot.
        x, y : str, optional
            Variables to map to the x and y axes.
        hue : str, optional
            Variable to map to color.
        weights : str, optional
            Variable to map to size.
        palette : str or dict, optional
            Palette for the plot
        hue_order : list of strings, optional
            Order to plot the categorical levels in.
        hue_norm : tuple or matplotlib.colors.Normalize, optional
            Either a pair of values that set the normalization range in data units or an object that will map from data units into a [0, 1] interval.
        fill : boolean, default=False
            If True, fill the area under the KDE curve.
        color : matplotlib color, optional
            Color for all elements, or seed for a gradient palette.
        multiple : {“layer”, “stack”, “fill”}, optional
            Approach to resolving multiple elements when semantic mapping creates subsets.
        common_norm : boolean, default=True
            If False, normalization within each subset is computed independently.
        common_grid : boolean, default=False
            If True, the grid of evaluation points is the same for each subset.
        cumulative : boolean, default=False
            If True, plot the cumulative distribution.
        bw_method : {‘scott’, ‘silverman’, scalar, pair of scalars }, optional
            Either the name of a reference rule or the scale factor to use when computing the kernel bandwidth.
        bw_adjust : float, optional
            Factor to multiply the default bandwidth by.
        warn_singular : boolean, default=True
            If True, issue a warning when the KDE computation is singular.
        log_scale : boolean, tuple, or number(s), optional
            Set a log scale on the data axis (or axes) with the given base (default 10), and evaluate the KDE in log space.
        levels : int, optional
            Number of contour levels to draw when fill=False.
        thresh : float, optional
            Contours with values lower than this level will not be drawn.
        gridsize : int, optional
            Number of evaluation points.
        cut : float, optional
            Extent of the plot past the extreme data points.
        clip : tuple, optional
            Lower and upper bounds for datapoints used to fit KDE. Can improve aesthetics and reduce computational load.
        legend : boolean, default=True
            If True, draw a legend.
        cbar : boolean, default=False
            If True, draw a colorbar.
        cbar_ax : matplotlib axes, optional
            Existing axes to draw the colorbar onto, otherwise space is taken from the main axes.
        cbar_kws : dict
            Keyword arguments for `fig.colorbar`.
        ax : matplotlib axes, optional
            Axes onto which the plot will be drawn.
        title : str, optional
            The title of the plot.
        **kwargs:
            matplotlib.axes.Axes.plot() (univariate, fill=False),
            matplotlib.axes.Axes.fill_between() (univariate, fill=True),
            matplotlib.axes.Axes.contour() (bivariate, fill=False),
            matplotlib.axes.contourf() (bivariate, fill=True).

        Return:
        -------
        None
        """

        self.__df = df
        self.__x = x
        self.__y = y
        self.__hue = hue
        self.__weights = weights
        self.__palette = palette
        self.__hue_order = hue_order
        self.__hue_norm = hue_norm
        self.__fill = fill
        self.__color = color
        self.__multiple = multiple
        self.__common_norm = common_norm
        self.__common_grid = common_grid
        self.__cumulative = cumulative
        self.__bw_method = bw_method
        self.__bw_adjust = bw_adjust
        self.__warn_singular = warn_singular
        self.__log_scale = log_scale
        self.__levels = levels
        self.__thresh = thresh
        self.__gridsize = gridsize
        self.__cut = cut
        self.__clip = clip
        self.__legend = legend
        self.__cbar = cbar
        self.__cbar_ax = cbar_ax
        self.__cbar_kws = cbar_kws
        self.__ax = ax
        self.__title = title
        self.__kwargs = kwargs

        self.__plot()

    def __plot(self):
        """
        This is a private method used to create the densityplot.

        """
        sns.kdeplot(
            data=self.__df,
            x=self.__x,
            y=self.__y,
            hue=self.__hue,
            weights=self.__weights,
            palette=self.__palette,
            hue_order=self.__hue_order,
            hue_norm=self.__hue_norm,
            fill=self.__fill,
            color=self.__color,
            multiple=self.__multiple,
            common_norm=self.__common_norm,
            common_grid=self.__common_grid,
            cumulative=self.__cumulative,
            bw_method=self.__bw_method,
            bw_adjust=self.__bw_adjust,
            warn_singular=self.__warn_singular,
            log_scale=self.__log_scale,
            levels=self.__levels,
            thresh=self.__thresh,
            gridsize=self.__gridsize,
            cut=self.__cut,
            clip=self.__clip,
            legend=self.__legend,
            cbar=self.__cbar,
            cbar_ax=self.__cbar_ax,
            cbar_kws=self.__cbar_kws,
            ax=self.__ax,
            **self.__kwargs
        )

        if self.__title:
            plt.title(self.__title)

    def save_plot(self, file_name, folder=None, size=(10, 6)):
        """
        This method saves the created plot in the specified directory.

        Args:
            file_name (str): Name of the file
            folder (str, optional): Name of the directory. If not available, it creates one.
            size (tuple, optional): Size of the figure in inches (width, height). Default is (10, 6).

        """
        if folder:
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_name = os.path.join(folder, file_name)

        fig = plt.figure(figsize=size)
        self.__plot()
        plt.savefig(file_name)
        plt.close(fig)  # prevent figure to pop up in the notebook
        plt.ion()  # turns the display of the plot back on


class Violinplot:
    def __init__(
        self,
        df,
        x=None,
        y=None,
        hue=None,
        order=None,
        hue_order=None,
        bw="scott",
        cut=2,
        scale="area",
        scale_hue=True,
        gridsize=100,
        width=0.8,
        inner="box",
        split=False,
        dodge=True,
        orient=None,
        linewidth=None,
        color=None,
        palette=None,
        saturation=0.75,
        ax=None,
        title=None,
        **kwargs
    ):
        """
        This is used to create violinplot figures using seaborn.

        Parameters:
        -----------
        df (pandas.DataFrame or array-like):
            The data to plot. DataFrame preferred.
        x, y (str, array-like, optional):
            Variables to use for plotting. Should be in `data` if it is a DataFrame.
        hue (str or array-like, optional):
            Grouping variable that will produce different violins with different colors.
        order, hue_order (list of strings, optional):
            Order to plot the categorical levels in.
        bw ({‘scott’, ‘silverman’, float}, optional):
            Method to use for calculating bandwidth.
        cut (float, optional):
            Distance in units of bandwidth size to extend the density past the extreme datapoints.
        scale ({“area”, “count”, “width”}, optional):
            The method used to scale the width of each violin.
        scale_hue (bool, optional):
            When using hue nesting, the coloring of the violins are scaled.
        gridsize (int, optional):
            Number of points in the discrete grid for the KDE computation.
        width (float, optional):
            Width of a full element when not using hue nesting, or width of all the elements for one
            level of the major grouping variable.
        inner ({“box”, “quartile”, “point”, “stick”, None}, optional):
            The representation of the datapoints in the violin.
        split (bool, optional):
            When using hue nesting with a binary variable split violins.
        dodge (bool, optional):
            When hue nesting is used, whether elements should be shifted along the categorical axis.
        orient (str, optional):
            Orientation of the plot. 'v' or 'h'.
        linewidth (float, optional):
            Line width of the violin outlines.
        color (Matplotlib color, optional):
            Color for all of the elements.
        palette (seaborn color palatte or dict, optional):
            Colors to use for the different levels of the hue variable.
        saturation (float, optional):
            Proportion of the original saturation to draw colors.
        ax (matplotlib.axes, optional):
            Pre-existing axes for the plot. Otherwise, a new one is created.
        title (str, optional):
            Title for the plot.
        **kwargs:
            Additional keyword arguments are passed to the underlying seaborn boxplot function.
            Other keyword arguments are passed through to matplotlib.axes.Axes.boxplot().

        Return:
        -------
        None
        """
        self.__df = df
        self.__x = x
        self.__y = y
        self.__hue = hue
        self.__order = order
        self.__hue_order = hue_order
        self.__bw = bw
        self.__cut = cut
        self.__scale = scale
        self.__scale_hue = scale_hue
        self.__gridsize = gridsize
        self.__width = width
        self.__inner = inner
        self.__split = split
        self.__dodge = dodge
        self.__orient = orient
        self.__linewidth = linewidth
        self.__color = color
        self.__palette = palette
        self.__saturation = saturation
        self.__ax = ax
        self.__title = title
        self.__kwargs = kwargs

        self.__plot()

    def __plot(self):
        """
        This is a private method used to create the violinplot.

        """
        plots = sns.violinplot(
            x=self.__x,
            y=self.__y,
            hue=self.__hue,
            data=self.__df,
            order=self.__order,
            hue_order=self.__hue_order,
            bw=self.__bw,
            cut=self.__cut,
            scale=self.__scale,
            scale_hue=self.__scale_hue,
            gridsize=self.__gridsize,
            width=self.__width,
            inner=self.__inner,
            split=self.__split,
            dodge=self.__dodge,
            orient=self.__orient,
            linewidth=self.__linewidth,
            color=self.__color,
            palette=self.__palette,
            saturation=self.__saturation,
            ax=self.__ax,
            **self.__kwargs
        )

        if self.__title:
            plt.title(self.__title)

    def save_plot(self, file_name, folder=None, size=(10, 6)):
        """
        This method saves the created plot in the specified directory.

        Args:
            file_name (str): Name of the file
            folder (str, optional): Name of the directory. If not available, it creates one.
            size (tuple, optional): Size of the figure in inches (width, height). Default is (10, 6).

        """
        if folder:
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_name = os.path.join(folder, file_name)

        fig = plt.figure(figsize=size)
        self.__plot()
        plt.savefig(file_name)
        plt.close(fig)  # prevent figure to pop up in the notebook
        plt.ion()  # turns the display of the plot back on


class ConnectedScatterPlot:
    def __init__(
        self,
        df,
        x=None,
        y=None,
        plots=None,
        ax=None,
        title=None,
        default_style=None,
        **kwargs
    ):
        """
        This is used to create one or more connected scatter plots using matplotlib.

        Parameters:
        -----------
        df (pandas.DataFrame):
            The data to plot. DataFrame preferred.
        x, y (str or array-like, optional):
            Variables to use for a basic single plot.
        plots (list of dict, optional):
            List of dictionaries where each dictionary contains parameters for individual plots.
        ax (matplotlib.axes.Axes, optional):
            Pre-existing axes for the plot. Otherwise, a new one is created.
        title (str, optional):
            Title for the plot.
        default_style (dict, optional):
            Default styling options for the plots like 'linestyle', 'marker', 'color', etc.
        **kwargs:
            Additional keyword arguments passed to the underlying `plot` function for default style.

        Each dictionary in `plots` should contain:
            - 'x': Column name or array-like for x-axis data.
            - 'y': Column name or array-like for y-axis data.
            - 'linestyle': Style of the line connecting data points.
            - 'marker': Style of the markers on data points.
            - 'color': Color for the line and markers.
            - 'linewidth': Width of the lines connecting points.
            - 'label': Label for the plot (optional for legend).

        Return:
        -------
        None
        """
        self.__df = df
        self.__plots = plots or []
        self.__ax = ax
        self.__title = title
        self.__default_style = default_style or {}

        if x and y:
            # If x and y are provided for a basic single plot
            self.__plots = [{"x": x, "y": y, **self.__default_style, **kwargs}]

        self.__plot()

    def __plot(self):
        """
        This is a private method used to create the connected scatter plots.
        """
        if self.__ax is None:
            self.__ax = plt.gca()

        for plot in self.__plots:
            # Extract x and y to use as positional arguments
            x = plot.pop("x")
            y = plot.pop("y")

            # Pass the rest of the dictionary as keyword arguments
            self.__ax.plot(self.__df[x], self.__df[y], **plot)

        if self.__title:
            self.__ax.set_title(self.__title)

        self.__ax.legend()

    def save_plot(self, file_name, folder=None, size=(10, 6)):
        """
        This method saves the created plot in the specified directory.

        Args:
            file_name (str): Name of the file
            folder (str, optional): Name of the directory. If not available, it creates one.
            size (tuple, optional): Size of the figure in inches (width, height). Default is (10, 6).

        """
        if folder:
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_name = os.path.join(folder, file_name)

        fig, ax = plt.subplots(figsize=size)
        self.__ax = ax  # Use the new axis for plotting
        self.__plot()
        plt.savefig(file_name)
        plt.close(fig)  # prevent figure from popping up in the notebook
        plt.ion()  # turns the display of the plot back on


class ScatterPlot:
    def __init__(
        self,
        df,
        x=None,
        y=None,
        plots=None,
        style="scatter",
        ax=None,
        title=None,
        default_style=None,
        **kwargs
    ):
        """
        This is used to create one or more scatter plots, optionally with regression lines, using Seaborn.

        Parameters:
        -----------
        df (pandas.DataFrame):
            The data to plot. DataFrame preferred.
        x (str, optional):
            Column name for x-axis data.
        y (str, optional):
            Column name for y-axis data.
        plots (list of dict, optional):
            List of dictionaries where each dictionary contains parameters for individual plots.
        style (str, optional):
            Determines the type of plot: 'scatter', 'lm', or 'reg'.
        ax (matplotlib.axes.Axes, optional):
            Pre-existing axes for the plot. Otherwise, a new one is created.
        title (str, optional):
            Title for the plot.
        default_style (dict, optional):
            Default styling options for the plots, applicable unless overridden in `plot` config.
        **kwargs:
            Additional keyword arguments passed to the underlying plotting functions.

        Each dictionary in `plots` should contain:
            - 'x': Column name for x-axis data.
            - 'y': Column name for y-axis data.
            - 'hue': Variable in `df` for color encoding.
            - Additional Seaborn plot-specific keys like 'col', 'row', 'palette', etc.

        Return:
        -------
        None
        """
        self.__df = df
        self.__plots = plots or []
        self.__style = style
        self.__ax = ax
        self.__title = title
        self.__default_style = default_style or {}

        if x and y:
            # If x and y are provided for a basic single plot
            self.__plots = [{"x": x, "y": y, **self.__default_style, **kwargs}]

        self.__plot()

    def __plot(self):
        """
        This is a private method used to create the scatter plots.
        """
        sns.set_style("darkgrid")

        for plot in self.__plots:
            # Extract the necessary plot configuration
            x = plot.pop("x")
            y = plot.pop("y")

            if self.__style == "lm":
                sns.lmplot(x=x, y=y, data=self.__df, **plot)
            else:
                # Use plt.subplots for regplot and scatterplot to handle ax if provided
                if self.__style == "reg":
                    sns.regplot(x=self.__df[x], y=self.__df[y], ax=self.__ax, **plot)
                else:
                    sns.scatterplot(
                        x=self.__df[x], y=self.__df[y], ax=self.__ax, **plot
                    )

        if self.__title:
            if self.__style in ["scatter", "reg"] and self.__ax:
                self.__ax.set_title(self.__title)

    def save_plot(self, file_name, folder=None, size=(10, 6)):
        """
        This method saves the created plot in the specified directory.

        Args:
            file_name (str): Name of the file
            folder (str, optional): Name of the directory. If not available, it creates one.
            size (tuple, optional): Size of the figure in inches (width, height). Default is (10, 6).
        """
        if folder:
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_name = os.path.join(folder, file_name)

        # Set the figure size and save the plot
        plt.gcf().set_size_inches(size)
        plt.savefig(file_name)
        plt.close()  # Prevent the figure from popping up
        plt.ion()  # Turn the interactive mode back on
