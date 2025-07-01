from prompt_toolkit import PromptSession
from prompt_toolkit.completion import FuzzyWordCompleter
from search import search_files
from utils import colorize

def launch_tui(root, name_pattern, content_pattern, ignore_dirs):
    # pre‐index all matches by name
    matches = [p for p,_,_ in search_files(root, name_pattern, None, ignore_dirs)]
    
    completer = FuzzyWordCompleter(matches)
    session = PromptSession(completer=completer)
    
    while True:
        try:
            text = session.prompt("pyfind> ")
        except KeyboardInterrupt:
            return
        if not text:
            continue
        # preview first 10 content matches
        for path, line, ln in search_files(root, text, content_pattern, ignore_dirs):
            print(colorize(path, style="bold")+" "+f"{ln}:{line.strip()}")
        print()
