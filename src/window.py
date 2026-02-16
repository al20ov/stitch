import gi

from utils.niri import Niri

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk

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

            output = OutputWidget(
                width=100,
                height=100,
                make=value["make"],
                model=value["model"],
                name=key,
            )
            output.add_controller(controller)
            self.fixed.put(output, val, 0)
            self.outputs.append(output)

    def on_begin(self, controller: Gtk.GestureDrag, _start_x, _start_y):
        target_widget = controller.get_widget()
        assert target_widget is not None

        current_pos = self.fixed.get_child_position(target_widget)
        px, py = self.get_pointer_position()

        self.diff = (
            current_pos[0] - px,
            current_pos[1] - py,
        )

    def on_update(self, controller: Gtk.GestureDrag, _offset_x, _offset_y):
        target_widget = controller.get_widget()
        assert target_widget is not None

        px, py = self.get_pointer_position()

        move_x = px + self.diff[0]
        move_y = py + self.diff[1]

        max_width = self.fixed.get_width() - target_widget.get_width()
        max_height = self.fixed.get_height() - target_widget.get_height()

        final_x = max(0, min(move_x, max_width))
        final_y = max(0, min(move_y, max_height))

        self.fixed.move(target_widget, final_x, final_y)

    def get_pointer_position(self):
        display = self.get_display()
        assert display is not None

        seat = display.get_default_seat()
        assert seat is not None

        pointer = seat.get_pointer()
        assert pointer is not None

        native = self.get_native()
        assert native is not None

        surface = native.get_surface()
        assert surface is not None

        _, px, py, _ = surface.get_device_position(pointer)
        coords = self.translate_coordinates(self.fixed, px, py)
        assert coords is not None

        fx, fy = coords
        return (fx, fy)
