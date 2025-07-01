import os, fnmatch, regex
from concurrent.futures import ThreadPoolExecutor

def walk(root, ignore_dirs):
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for fname in files:
            yield os.path.join(dirpath, fname)

def search_files(root, name_pattern, content_pattern=None, ignore_dirs=None):
    ignore_dirs = ignore_dirs or []
    is_glob = any(ch in name_pattern for ch in "*?[]")
    name_re = regex.compile(fnmatch.translate(name_pattern)) \
              if not is_glob else None

    def matcher(path):
        fn = os.path.basename(path)
        ok = fnmatch.fnmatch(fn, name_pattern) if is_glob else bool(name_re.match(fn))
        if not ok:
            return None
        if content_pattern:
            cre = regex.compile(content_pattern, regex.IGNORECASE)
            with open(path, errors="ignore") as f:
                for i, l in enumerate(f,1):
                    if cre.search(l):
                        return (path, l, i)
            return None
        return (path, None, None)

    with ThreadPoolExecutor() as ex:
        for res in ex.map(matcher, walk(root, ignore_dirs)):
            if res:
                yield res
