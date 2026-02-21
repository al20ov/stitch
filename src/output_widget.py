from enum import Enum

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gdk, GObject, Gtk


# TODO
class VariableRefreshRate(Enum):
    OFF = 0
    ON = 1
    ON_DEMAND = 2


@Gtk.Template(filename="src/output_widget.ui")
class OutputWidget(Gtk.Box):
    __gtype_name__ = "output_widget"

    popover: Gtk.Popover = Gtk.Template.Child()

    make = GObject.Property(type=str, default="")
    model = GObject.Property(type=str, default="")
    name = GObject.Property(type=str, default="")
    width = GObject.Property(type=int, default=100)
    height = GObject.Property(type=int, default=100)

    x = GObject.Property(type=int, default=0)
    y = GObject.Property(type=int, default=0)

    mode = GObject.Property(type=str, default="")
    scale = GObject.Property(type=float, default=1.0)
    transform = GObject.Property(type=str, default="normal")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        self.set_cursor(Gdk.Cursor.new_from_name("grab", None))

        click_gesture = Gtk.GestureClick.new()
        click_gesture.set_button(3)  # Right click
        click_gesture.connect("pressed", self.on_click)
        self.add_controller(click_gesture)

    def on_click(self, _gesture, _n_press, _x, _y):
        self.popover.popup()

    def update_dimensions(self, width, height):
        self.width = width
        self.height = height

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def set_make(self, make):
        self.make = make

    def set_model(self, model):
        self.model = model

    def set_name(self, name):
        self.name = name
