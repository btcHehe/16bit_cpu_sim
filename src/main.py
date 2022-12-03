from gui import App
from constants import WIN_H, WIN_W

if __name__ == '__main__':
    app = App(WIN_W, WIN_H)
    app.spawnWidgets()
    app.mainloop()
