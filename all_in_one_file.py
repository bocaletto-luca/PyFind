#!/usr/bin/env python3
"""
pyfind.py – Powerful file finder & content grepping in one script.

Features:
- Name-based search (glob or regex)
- Content search with regex
- Exclude dirs (e.g. .git, venv)
- Colored output via colorama
- Parallel filesystem walk with ThreadPoolExecutor
- Interactive fuzzy mode with preview using prompt_toolkit
"""

import os
import fnmatch
import regex
import argparse
import pathlib
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init as colorama_init

# optional interactive
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import FuzzyWordCompleter
    HAS_TUI = True
except ImportError:
    HAS_TUI = False

# initialize ANSI colors
colorama_init(autoreset=True)

def colorize(text, color="GREEN", style=None):
    col = getattr(Fore, color.upper(), "")
    st  = getattr(Style, style.upper(), "") if style else ""
    return f"{col}{st}{text}{Style.RESET_ALL}"

def walk(root, ignore_dirs):
    """Yield all file paths under root, skipping ignore_dirs."""
    for dirpath, dirs, files in os.walk(root):
        # filter directories in-place
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            yield os.path.join(dirpath, f)

def search_files(root, name_pattern, content_pattern=None, ignore_dirs=None):
    """Generator yielding (path, line, lineno) or (path, None, None)."""
    ignore_dirs = ignore_dirs or []
    is_glob = any(ch in name_pattern for ch in "*?[]")
    if not is_glob:
        name_re = regex.compile(name_pattern)
    else:
        name_re = None

    def match_path(path):
        name = os.path.basename(path)
        if is_glob:
            ok = fnmatch.fnmatch(name, name_pattern)
        else:
            ok = bool(name_re.search(name))
        if not ok:
            return None
        if content_pattern:
            cre = regex.compile(content_pattern)
            try:
                with open(path, errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        if cre.search(line):
                            return (path, line.rstrip("\n"), i)
            except Exception:
                return None
            return None
        return (path, None, None)

    with ThreadPoolExecutor() as pool:
        for res in pool.map(match_path, walk(root, ignore_dirs)):
            if res:
                yield res

def launch_tui(root, name_pattern, content_pattern, ignore_dirs):
    """Fuzzy interactive search & preview."""
    print(colorize("Entering interactive fuzzy mode (Ctrl-C to exit)...", "CYAN"))
    # pre-index file paths
    paths = [p for p,_,_ in search_files(root, name_pattern, None, ignore_dirs)]
    completer = FuzzyWordCompleter(paths, WORD=True)
    session = PromptSession(completer=completer)
    while True:
        try:
            query = session.prompt("pyfind> ")
        except KeyboardInterrupt:
            break
        if not query.strip():
            continue
        # preview up to 10 matches
        count = 0
        for path, line, lineno in search_files(root, query, content_pattern, ignore_dirs):
            path_col = colorize(path, "YELLOW")
            if line is not None:
                print(f"{path_col}:{lineno}: {line}")
            else:
                print(path_col)
            count += 1
            if count >= 10:
                break
        if count == 0:
            print(colorize("No matches found.", "RED"))
        print()

def main():
    p = argparse.ArgumentParser(
        description="pyfind: fast name & content search, optional fuzzy TUI"
    )
    p.add_argument("pattern", help="name pattern (glob or regex)")
    p.add_argument("-c", "--content", help="search inside files (regex)")
    p.add_argument("-i", "--interactive", action="store_true",
                   help="fuzzy interactive mode (requires prompt_toolkit)")
    p.add_argument("--ignore", nargs="*", default=[".git", ".venv"],
                   help="directories to skip")
    p.add_argument("-r", "--root", default=".",
                   help="root directory to search (default: current)")
    args = p.parse_args()

    if args.interactive:
        if not HAS_TUI:
            print("Error: prompt_toolkit not installed. Install with `pip install prompt_toolkit`.")
            return
        launch_tui(args.root, args.pattern, args.content, args.ignore)
    else:
        for path, line, lineno in search_files(
                args.root, args.pattern, args.content, args.ignore):
            path_col = colorize(path, "GREEN")
            if line:
                print(f"{path_col}:{lineno}: {line}")
            else:
                print(path_col)

if __name__ == "__main__":
    main()
