import os

def clear_and_print_header(heading):
    """Clears CLI and displays the heading of any requested section

    Args:
        heading (str): heding to display
    """
    clear_cli()
    print(f"*************************{heading}*************************\n")
    
def clear_cli():
    """Clears the cli window
    """
    os.system('cls' if os.name == 'nt' else 'clear')