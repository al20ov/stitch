import sys

import gi

from window import StitchWindow
from output_widget import OutputWidget

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GObject

from utils.niri import Niri

GObject.type_register(OutputWidget)


class Stitch(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.github.al20ov.stitch")
        self.niri = Niri()

    def do_activate(self):
        window = StitchWindow(application=self)
        window.present()


if __name__ == "__main__":
    app = Stitch()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
