import cProfile
import pstats
from tqdm import tqdm

def check_profile(n_lines):
    def check_profile(func):
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            result = profiler.runcall(func, *args, **kwargs)
            stats = pstats.Stats(profiler)
            stats.sort_stats("tottime")
            stats.print_stats(n_lines)
            return result
        return wrapper
    return check_profile
