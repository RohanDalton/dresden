import cProfile
import datetime
import functools
import logging
import os

import gprof2dot
import pydot

__author__ = "Rohan B. Dalton"


def get_temp_dir():
    """Placeholder"""
    return os.getcwd()
    # return os.path.expanduser("~/tmp")


class Harry(object):
    """
    Class for enabling profiling Python code via decorator or context manager.
    """

    def __init__(self, func_to_profile=None):
        if func_to_profile is not None:
            functools.wraps(func_to_profile)(self)
        else:
            pass

        self._profile = None

    def _start_investigation(self):
        logging.debug("Starting profiler.")
        self._profile = cProfile.Profile()
        self._profile.enable()

    def _conclude_investigation(self):
        logging.info("Disabling profiler")
        self._profile.disable()

        # TODO: Snakeviz is just a thin wrapper around Tornado. Write own server, that can run separately.
        # TODO: Directory browsing for comparisons
        # Dump the stats file for use by snakeviz.

        temp_dir = get_temp_dir()
        now = datetime.datetime.now()
        file_base = f"dresden_{now:%Y%m%d_%H%M%S}"
        output_path = os.path.join(temp_dir, file_base)

        stats_path = f"{output_path}.stats"
        logging.info(f"Writing stats file to {stats_path}")
        self._profile.dump_stats(stats_path)

        parser = gprof2dot.PstatsParser(self._profile)
        parser.stats.sort_stats("time")
        prof = parser.parse()
        prof.prune(0.5 / 100.0, 0.1 / 100.0, None, False)
        dot_path = f"{output_path}.dot"
        logging.debug(f"Writing dot file to {dot_path}")
        with open(dot_path, "wt") as fh:
            dot_writer = gprof2dot.DotWriter(fh)
            dot_writer.graph(prof, gprof2dot.TEMPERATURE_COLORMAP)

        png_path = f"{output_path}.png"
        (graph,) = pydot.graph_from_dot_file(dot_path)
        logging.info(f"Writing png file to {png_path}")
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
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conclude_investigation()


if __name__ == "__main__":
    pass
