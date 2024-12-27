from src.gui import App
import tkinter as tk
from src.logging_config import configure_logging

configure_logging()

if __name__ == "__main__":
    # Create the Tkinter root window
    root = tk.Tk()

    # Launch the application
    app = App(root)

    # Start the main interface loop
    root.mainloop()
