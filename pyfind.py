#!/usr/bin/env python3
import argparse
from search import search_files
from tui import launch_tui

def main():
    p = argparse.ArgumentParser(prog="pyfind")
    p.add_argument("pattern", help="file‐name glob or regex")
    p.add_argument("-c","--content", help="search inside files (regex)")
    p.add_argument("-i","--interactive", action="store_true",
                   help="fuzzy interactive mode")
    p.add_argument("--ignore", nargs="*", default=[".git",".venv"],
                   help="dirs to skip")
    args = p.parse_args()

    if args.interactive:
        launch_tui(root=".", name_pattern=args.pattern,
                   content_pattern=args.content,
                   ignore_dirs=args.ignore)
    else:
        for path, line, lineno in search_files(
            root=".", name_pattern=args.pattern,
            content_pattern=args.content,
            ignore_dirs=args.ignore
        ):
            if line:
                print(f"{path}:{lineno}: {line.strip()}")
            else:
                print(path)

if __name__=="__main__":
    main()
