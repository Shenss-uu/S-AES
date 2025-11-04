from s_aes_gui import SAESGUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = SAESGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()