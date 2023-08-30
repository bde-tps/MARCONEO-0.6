"""
main.py

Entrypoint of the application.
It launches the application.
"""

#------------------------------------------------------------------------------#

from src.marconeo import MarcoNeo

#------------------------------------------------------------------------------#

if __name__ == "__main__":
    print("Starting MarcoNeo...")
    marco = MarcoNeo()
    print("MarcoNeo stopped.")
