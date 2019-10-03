import tempfile
from contextlib import contextmanager


def flatten(d, parent_key=""):
    items = []
    for k, v in d.items():
        new_key = parent_key + "_" + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)


@contextmanager
def TemporaryConfigFiles(n_files=1, suffix=".yaml", mode="w", **kwargs):
    try:
        files = [
            tempfile.NamedTemporaryFile(suffix=suffix, mode=mode, **kwargs)
            for _ in range(n_files)
        ]
        yield files if len(files) > 1 else files[0]
    finally:
        for f in files:
            f.close()
