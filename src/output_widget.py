import gi

gi.require_version("Gtk", "4.0")

from gi.repository import GObject, Gtk


@Gtk.Template(filename="src/output_widget.ui")
class OutputWidget(Gtk.Box):
    __gtype_name__ = "output_widget"

    output_name = GObject.Property(type=str, default="Text")
    width = GObject.Property(type=int, default=100)
    height = GObject.Property(type=int, default=100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

    def update_dimensions(self, width, height):
        self.width = width
        self.height = height

    def set_label_text(self, text):
        self.output_name = text
