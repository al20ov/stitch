import os
import sys

import gi

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

    main_text = GObject.Property(type=str, default="Default Text")


if __name__ == "__main__":
    app = Stitch()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
