from colorama import Fore, Style

def colorize(text, color="green", style=None):
    col = getattr(Fore, color.upper(), "")
    st  = getattr(Style, style.upper(), "") if style else ""
    return f"{col}{st}{text}{Style.RESET_ALL}"
