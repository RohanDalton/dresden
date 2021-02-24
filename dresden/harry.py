import cProfile
import datetime
import functools
import os

import gprof2dot
import pydot

__author__ = "Rohan B. Dalton"


def get_temp_dir():
    """Placeholder"""
    return os.path.expanduser("~/tmp")


class Harry(object):
    """
    Class for enabling profiling Python code via decorator or context manager.
    """

    def __init__(self, func_to_profile=None):
        if func_to_profile is not None:
            functools.wraps(func_to_profile)(self)
            # noinspection PyUnresolvedReferences
            self._func = self.__wrapped__
        self._profile = None

    def _start_investigation(self):
        self._profile = cProfile.Profile()
        self._profile.enable()

    def _conclude_investigation(self):
        self._profile.disable()

        # TODO: Snakeviz is just a thin wrapper around Tornado. Write own server, that can run separately.
        # TODO: Directory browsing for comparisons
        # Dump the stats file for use by snakeviz.
        temp_dir = get_temp_dir()
        now = datetime.datetime.now()
        stats_file = "{name}_{now:%Y%m%d_%H%M%S}.stats".format(name=self._func.__name__, now=now)
        stats_path = os.path.join(temp_dir, stats_file)
        self._profile.dump_stats(stats_path)

        parser = gprof2dot.PstatsParser(self._profile)
        parser.stats.sort_stats("time")
        prof = parser.parse()
        prof.prune(0.5 / 100.0, 0.1 / 100.0, None, False)
        dot_file = "{name}_{now:%Y%m%d_%H%M%S}.dot".format(name=self._func.__name__, now=now)
        dot_path = os.path.join(get_temp_dir(), dot_file)
        with open(dot_path, "wt") as fh:
            dot_writer = gprof2dot.DotWriter(fh)
            dot_writer.graph(prof, gprof2dot.TEMPERATURE_COLORMAP)

        png_path = dot_path.replace(".dot", ".png")
        (graph,) = pydot.graph_from_dot_file(dot_path)
        graph.write_png(png_path)

    # noinspection PyUnresolvedReferences
    def __call__(self, *args, **kwargs):
        self._start_investigation()
        try:
            result = self._profile.runcall(self.__wrapped__, *args, **kwargs)
        except Exception as e:
            raise e
        else:
            return result
        finally:
            self._conclude_investigation()

    def __enter__(self):
        self._start_investigation()

    def __exit__(self):
        self._conclude_investigation()


if __name__ == "__main__":
    pass
