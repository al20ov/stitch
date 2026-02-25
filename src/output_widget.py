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
    scale_spin: Gtk.SpinButton = Gtk.Template.Child()

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
        self._modes = kwargs.pop("modes", [])
        current_mode_idx = kwargs.pop("current_mode_index", 0)

        super().__init__(**kwargs)
        self.init_template()

        self.modes_list = Gtk.StringList.new([m["formatted"] for m in self._modes])
        self.mode_dropdown.set_model(self.modes_list)
        if len(self._modes) > 0:
            self.mode_dropdown.set_selected(current_mode_idx)

        self.popover.set_autohide(True)

        self.set_cursor(Gdk.Cursor.new_from_name("grab", None))

        click_gesture = Gtk.GestureClick.new()
        click_gesture.set_button(3)  # Right click
        click_gesture.connect("pressed", self.on_click)
        self.add_controller(click_gesture)

        self.connect("notify::scale", self._on_scale_changed)
        self.connect("notify::transform", self._on_transform_changed)

        self._update_logical_size()

    def _update_logical_size(self):
        selected_idx = self.mode_dropdown.get_selected()
        if selected_idx != Gtk.INVALID_LIST_POSITION and selected_idx < len(
            self._modes
        ):
            m = self._modes[selected_idx]

            w, h = m["width"], m["height"]
            if self.transform in ["90", "270", "flipped-90", "flipped-270"]:
                w, h = h, w

            self.width = int((w / self.scale) / 10)
            self.height = int((h / self.scale) / 10)

            if self.popover.get_visible():
                self._update_popover_position()
                self.popover.present()

    def _update_popover_position(self):
        rect = Gdk.Rectangle()
        rect.x = 0
        rect.y = self.height
        rect.width = self.width
        rect.height = 1
        self.popover.set_pointing_to(rect)

    def _on_scale_changed(self, _obj, _pspec):
        self._update_logical_size()

    def _on_transform_changed(self, _obj, _pspec):
        self._update_logical_size()

    @Gtk.Template.Callback()
    def on_mode_selected(self, dropdown, _pspec):
        selected_item = dropdown.get_selected_item()
        if selected_item:
            self.mode = selected_item.get_string()
            self._update_logical_size()

    def on_click(self, _gesture, _n_press, _x, _y):
        self._update_popover_position()
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
