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

        for key, value in self.niri.outputs.items():
            details = self.niri.get_output_details(key)
            if not details:
                continue

            log_width = details["logical_size"]["width"]
            log_height = details["logical_size"]["height"]

            log_x = details["logical_position"]["x"]
            log_y = details["logical_position"]["y"]

            scaled_width = int(log_width / 10)
            scaled_height = int(log_height / 10)
            scaled_x = int(log_x / 10)
            scaled_y = int(log_y / 10)

            controller: Gtk.GestureDrag = Gtk.GestureDrag.new()
            controller.connect("drag-begin", self.on_begin)
            controller.connect("drag-update", self.on_update)
            controller.connect("drag-end", self.on_end)
            self.controllers.append(controller)

            output = OutputWidget(
                width=scaled_width,
                height=scaled_height,
                make=value["make"],
                model=value["model"],
                name=key,
                x=scaled_x,
                y=scaled_y,
                mode=self._format_mode(value),
                scale=details["scale"],
                transform=details["transform"].lower(),
            )
            output.add_controller(controller)
            self.fixed.put(output, scaled_x, scaled_y)
            self.outputs.append(output)

    def _format_mode(self, output_value):
        current_mode_idx = output_value.get("current_mode")
        modes = output_value.get("modes", [])
        if current_mode_idx is not None and 0 <= current_mode_idx < len(modes):
            m = modes[current_mode_idx]
            # Format as "WxH@REFRESH"
            refresh = m["refresh_rate"] / 1000.0
            return f"{m['width']}x{m['height']}@{refresh:.3f}"
        return ""

    @Gtk.Template.Callback()
    def on_save_clicked(self, _button):
        outputs_data = [
            {
                "name": output.name,
                "x": output.x,
                "y": output.y,
                "mode": output.mode,
                "scale": output.scale,
                "transform": output.transform,
            }
            for output in self.outputs
        ]
        self.niri.save_config(outputs_data)

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
        target = controller.get_widget()
        assert target is not None

        current_pos = self.fixed.get_child_position(target)
        scaled_x = current_pos[0] * 10
        scaled_y = current_pos[1] * 10
        target.update_position(scaled_x, scaled_y)
        print(f"{target.name} at position {target.x}, {target.y}")
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
