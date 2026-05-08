"""
plotify.categorical.word_cloud
==============================

Word cloud chart. Plotly has no native word cloud primitive, so only the
Seaborn/Matplotlib backend is implemented; asking for ``backend="plotly"``
raises :class:`ValueError` at construction time.
"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from plotify.base import BasePlot


class WordCloudPlot(BasePlot):
    """
    Word cloud chart.

    Accepts either (a) a single string of text via ``text``, or (b) a mapping
    of word → frequency via ``frequencies``. Exactly one must be provided.
    """

    # Override: this class does not support the Plotly backend. The base
    # class's __init__ will raise ValueError if the caller requests it.
    SUPPORTED_BACKENDS = ("seaborn",)

    def __init__(
        self,
        text=None,
        frequencies=None,
        width=800,
        height=400,
        background_color="white",
        colormap="viridis",
        max_words=200,
        title=None,
        backend="seaborn",
        **kwargs,
    ):
        """
        This is used to create a word cloud.

        Parameters
        ----------
        text : str, optional
            Raw text from which the cloud is generated. Mutually exclusive
            with ``frequencies``.
        frequencies : dict[str, float], optional
            Precomputed word → frequency mapping.
        width, height : int, default=(800, 400)
            Canvas size of the word cloud bitmap in pixels.
        background_color : str, default="white"
            Background colour of the canvas.
        colormap : str, default="viridis"
            Matplotlib colormap used for the words.
        max_words : int, default=200
            Maximum number of words to include in the cloud.
        title : str, optional
            Plot title.
        backend : {"seaborn"}
            Only the Seaborn/Matplotlib backend is supported.
        **kwargs :
            Forwarded to :class:`wordcloud.WordCloud`.

        Returns
        -------
        None
        """
        if (text is None) == (frequencies is None):
            raise ValueError("Provide exactly one of `text` or `frequencies`.")

        self.__text = text
        self.__frequencies = frequencies
        self.__width = width
        self.__height = height
        self.__background_color = background_color
        self.__colormap = colormap
        self.__max_words = max_words
        self.__kwargs = kwargs

        super().__init__(backend=backend, title=title)
        self._render()

    def _plot_seaborn(self):
        """Build a WordCloud bitmap and render it via ``imshow``."""
        wc = WordCloud(
            width=self.__width,
            height=self.__height,
            background_color=self.__background_color,
            colormap=self.__colormap,
            max_words=self.__max_words,
            **self.__kwargs,
        )
        # Two construction paths — pick based on which input the caller gave us.
        if self.__text is not None:
            cloud = wc.generate(self.__text)
        else:
            cloud = wc.generate_from_frequencies(self.__frequencies)

        plt.imshow(cloud, interpolation="bilinear")
        plt.axis("off")
        if self._title:
            plt.title(self._title)
