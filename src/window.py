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
            controller.connect("drag-end", self.on_end)
            self.controllers.append(controller)

            output = OutputWidget(
                width=384,
                height=216,
                make=value["make"],
                model=value["model"],
                name=key,
            )
            output.add_controller(controller)
            self.fixed.put(output, val, 0)
            self.outputs.append(output)

    def on_begin(self, controller: Gtk.GestureDrag, _start_x, _start_y):
        target = controller.get_widget()
        assert target is not None

        current_pos = self.fixed.get_child_position(target)
        px, py = self.get_pointer_position()

        self.diff = (
            current_pos[0] - px,
            current_pos[1] - py,
        )

    def on_update(self, controller: Gtk.GestureDrag, _offset_x, _offset_y):
        snap_threshold = 16.0
        target = controller.get_widget()
        assert target is not None

        px, py = self.get_pointer_position()
        move_x = px + self.diff[0]
        move_y = py + self.diff[1]

        target_width, target_height = target.get_width(), target.get_height()

        best_dx = snap_threshold
        best_dy = snap_threshold

        final_x, final_y = move_x, move_y

        for other in self.outputs:
            if other == target:
                continue

            other_pos = self.fixed.get_child_position(other)
            other_width, other_height = other.get_width(), other.get_height()

            if (
                move_y < other_pos[1] + other_height + snap_threshold
                and move_y + target_height > other_pos[1] - snap_threshold
            ):
                x_edges = [
                    other_pos[0],
                    other_pos[0] + other_width,
                    other_pos[0] - target_width,
                    other_pos[0] + other_width - target_width,
                ]
                for x in x_edges:
                    if (d := abs(move_x - x)) < best_dx:
                        best_dx = d
                        final_x = x

            if (
                move_x < other_pos[0] + other_width + snap_threshold
                and move_x + target_width > other_pos[0] - snap_threshold
            ):
                y_edges = [
                    other_pos[1],
                    other_pos[1] + other_height,
                    other_pos[1] - target_height,
                    other_pos[1] + other_height - target_height,
                ]
                for y in y_edges:
                    if (d := abs(move_y - y)) < best_dy:
                        best_dy = d
                        final_y = y

        max_w = self.fixed.get_width() - target_width
        max_h = self.fixed.get_height() - target_height

        self.fixed.move(
            target, max(0, min(final_x, max_w)), max(0, min(final_y, max_h))
        )

    def on_end(self, controller: Gtk.GestureDrag, offset_x, offset_y):
        # TODO: Add update "real" position for final export to outputs.kdl
        pass

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
