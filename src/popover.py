gi.require_version("Gtk", "4.0")

from gi.repository import Gtk


@Gtk.Template(filename="src/popover.ui")
class OutputPopover(Gtk.Popover):
    __gtype_name__ = "output_popover"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
