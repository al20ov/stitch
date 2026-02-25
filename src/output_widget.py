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
    mode_dropdown: Gtk.DropDown = Gtk.Template.Child()

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
        modes_data = kwargs.pop("modes", [])
        current_mode_idx = kwargs.pop("current_mode_index", 0)

        super().__init__(**kwargs)
        self.init_template()

        self.modes_list = Gtk.StringList.new([m["formatted"] for m in modes_data])
        self.mode_dropdown.set_model(self.modes_list)
        if len(modes_data) > 0:
            self.mode_dropdown.set_selected(current_mode_idx)

        self.popover.set_autohide(True)

        self.set_cursor(Gdk.Cursor.new_from_name("grab", None))

        click_gesture = Gtk.GestureClick.new()
        click_gesture.set_button(3)  # Right click
        click_gesture.connect("pressed", self.on_click)
        self.add_controller(click_gesture)

    @Gtk.Template.Callback()
    def on_mode_selected(self, dropdown, _pspec):
        selected_item = dropdown.get_selected_item()
        if selected_item:
            self.mode = selected_item.get_string()

    def on_click(self, _gesture, _n_press, _x, _y):
        rect = Gdk.Rectangle()
        rect.x = 0
        rect.y = self.get_allocated_height()
        rect.width = self.get_allocated_width()
        rect.height = 1
        self.popover.set_pointing_to(rect)
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
