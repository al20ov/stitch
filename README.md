# Stitch

Output management for Niri similar to `nwg-displays`.

<img width="954" height="625" alt="image" src="https://github.com/user-attachments/assets/4a996acd-befc-4feb-acec-7c9c1bd7231b" />

## Dependencies

### Void Linux

- python3
- python3-gobject
- python3-Jinja2
- ...

## Loose description of how it works

The first thing this program does is get a list of outputs from Niri over its UNIX domain socket (path in $NIRI_SOCKET) by sending "Outputs" (with the quotes). That gives us a JSON array (see `printf '"Outputs"' | socat STDIO $NIRI_SOCKET | jq .` for pretty format).

Then, that array is loaded and each output/display becomes a Gtk.Box that you can drag within a Gtk.Fixed with a Gtk.GestureDrag to arrange your displays.

TODO: Click on a display's Gtk.Box and it brings up a Gtk.Popover where you can change the display's properties such as resolution, scale, rotation, etc...

When you're done, you can save the layout, which will then generate a piece of Niri config in KDL format and write it to `~/.config/niri/outputs.kdl`. If that file is included in the main `~/.config/niri/config.kdl`, Niri should reload its config and apply it if it's considered valid.

## Useful resources

1. Blueprint documentation: https://gnome.pages.gitlab.gnome.org/blueprint-compiler/index.html

2. GTK 4 PyGObject classes: https://api.pygobject.gnome.org/Gtk-4.0/classes.html

3. GTK 4 CSS properties: https://docs.gtk.org/gtk4/css-properties.html

4. libadwaita widget gallery: https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1.7/widget-gallery.html

5. GTK 4 widget gallery: https://docs.gtk.org/gtk4/visual_index.html

6. libadwaita built-in CSS classes: https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1.3/style-classes.html
