import operator
import os
import sys

import gi

from output_widget import OutputWidget

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GObject, Gtk

from utils.niri import Niri


class Stitch(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.github.al20ov.stitch")
        self.niri = Niri()

    def do_activate(self):
        window = StitchWindow(application=self)
        window.present()


@Gtk.Template(filename="src/window.ui")
class StitchWindow(Adw.ApplicationWindow):
    __gtype_name__ = "stitch_window"

    fixed: Gtk.Fixed = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.output_widget0 = OutputWidget(
            width=200, height=100, output_name="ASUS monitor"
        )
        self.fixed.put(self.output_widget0, 0, 0)

        self.controller: Gtk.GestureDrag = Gtk.GestureDrag()
        self.controller.connect("drag-begin", self.on_begin)
        self.controller.connect("drag-update", self.on_update)
        self.output_widget0.add_controller(self.controller)

        button = Gtk.Button(label="Update")
        button.connect("clicked", self.update_widget)
        self.fixed.put(button, 10, 10)

    def update_widget(self, button):
        self.output_widget0.update_dimensions(300, 200)
        self.output_widget0.set_label_text("Updated!")

    def on_begin(self, controller, start_x, start_y):
        self.diff = tuple(
            map(
                operator.sub,
                self.fixed.get_child_position(self.output_widget0),
                self.get_fixed_pos(),
            )
        )

    def on_update(self, controller, offset_x, offset_y):
        move = map(operator.add, self.get_fixed_pos(), self.diff)

        max_width = self.fixed.get_width() - self.output_widget0.get_width()
        max_height = self.fixed.get_height() - self.output_widget0.get_height()
        move_x, move_y = map(min, (max_width, max_height), map(max, (0, 0), move))

        self.fixed.move(self.output_widget0, move_x, move_y)

    def get_fixed_pos(self):
        pointer = self.get_display().get_default_seat().get_pointer()
        _, px, py, _ = (
            self.fixed.get_native().get_surface().get_device_position(pointer)
        )
        return self.translate_coordinates(self.fixed, px, py)


if __name__ == "__main__":
    app = Stitch()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
