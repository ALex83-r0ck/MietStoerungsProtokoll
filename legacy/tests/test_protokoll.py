import numpy as np
from kivy.app import App
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


class PlotWidget(Widget):
    def __init__(self, **kwargs):
        super(PlotWidget, self).__init__(**kwargs)
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas_agg = FigureCanvasAgg(self.figure)
        self.texture = None
        self.bind(size=self.on_size)
        self.on_size()  # Initialer Aufruf, um sicherzustellen, dass alles vorbereitet wird

    def on_size(self, *args):
        # Sicherstellen, dass die Größe gültig ist
        if self.size[0] <= 0 or self.size[1] <= 0:
            print(f"Invalid size: {self.size}, skipping initialization")
            return

        # Initialisierung der Textur bei Größenänderung
        if not self.texture:
            print("Initializing texture for the first time")
            self.texture = Texture.create(
                size=(int(self.size[0]), int(self.size[1])), colorfmt="rgba"
            )

        # Matplotlib-Plot aktualisieren
        self.update_plot()

    def update_plot(self, *args):
        if not self.texture:
            print("Texture is not initialized yet, skipping update_plot")
            return

        print("Updating plot")
        self.ax.clear()  # Vorherige Plots löschen
        self.ax.plot([1, 2, 3], [4, 5, 6])  # Beispiel-Plot
        self.canvas_agg.draw()

        buf = np.frombuffer(self.canvas_agg.buffer_rgba(), dtype=np.uint8)
        buf = buf.reshape(self.canvas_agg.get_width_height()[::-1] + (4,))

        self.texture.blit_buffer(buf.flatten(), colorfmt="rgba", bufferfmt="ubyte")

        with self.canvas:
            self.canvas.clear()
            Rectangle(texture=self.texture, pos=self.pos, size=self.size)


class MyApp(App):
    def build(self):
        return PlotWidget()


if __name__ == "__main__":
    MyApp().run()
