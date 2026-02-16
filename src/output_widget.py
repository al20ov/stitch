import gi

gi.require_version("Gtk", "4.0")

from gi.repository import GObject, Gtk


@Gtk.Template(filename="src/output_widget.ui")
class OutputWidget(Gtk.Box):
    __gtype_name__ = "output_widget"

    make = GObject.Property(type=str, default="")
    model = GObject.Property(type=str, default="")
    name = GObject.Property(type=str, default="")
    width = GObject.Property(type=int, default=100)
    height = GObject.Property(type=int, default=100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

    def update_dimensions(self, width, height):
        self.width = width
        self.height = height

    def set_make(self, make):
        self.make = make

    def set_model(self, model):
        self.model = model

    def set_name(self, name):
        self.name = name
