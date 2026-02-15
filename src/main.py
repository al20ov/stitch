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

    fixed = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.fixed.put(Gtk.Label(label="hello"), 0, 0)


if __name__ == "__main__":
    app = Stitch()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
