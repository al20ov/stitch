import operator

import gi

from utils.niri import Niri

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gdk, GObject, Gtk

from output_widget import OutputWidget


@Gtk.Template(filename="src/window.ui")
class StitchWindow(Adw.ApplicationWindow):
    __gtype_name__ = "stitch_window"

    fixed: Gtk.Fixed = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        self.niri = Niri()

        self.outputs: list[OutputWidget] = []
        self.controllers: list[Gtk.GestureDrag] = []

        val = 0

        for key, value in self.niri.outputs.items():
            controller: Gtk.GestureDrag = Gtk.GestureDrag.new()
            controller.connect("drag-begin", self.on_begin)
            controller.connect("drag-update", self.on_update)
            self.controllers.append(controller)

            output = OutputWidget(width=100, height=100, output_name=key)
            output.add_controller(controller)
            self.fixed.put(output, val, 0)
            self.outputs.append(output)

    def on_begin(self, controller: Gtk.GestureDrag, start_x, start_y):
        target_widget: Gtk.Widget = controller.get_widget()

        self.diff = tuple(
            map(
                operator.sub,
                self.fixed.get_child_position(target_widget),
                self.get_pointer_position(),
            )
        )

    def on_update(self, controller: Gtk.GestureDrag, offset_x, offset_y):
        target_widget: Gtk.Widget = controller.get_widget()

        move = map(operator.add, self.get_pointer_position(), self.diff)

        max_width = self.fixed.get_width() - target_widget.get_width()
        max_height = self.fixed.get_height() - target_widget.get_height()
        move_x, move_y = map(min, (max_width, max_height), map(max, (0, 0), move))

        self.fixed.move(target_widget, move_x, move_y)

    def get_pointer_position(self):
        pointer: Gdk.Device = self.get_display().get_default_seat().get_pointer()
        _, px, py, _ = (
            self.fixed.get_native().get_surface().get_device_position(pointer)
        )
        return self.translate_coordinates(self.fixed, px, py)
