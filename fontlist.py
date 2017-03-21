import os

def _styles_contains(font, value):
    for style in font["styles"]:
        if value.lower() in style.lower():
            return True
    return False


class FontList(list):
    def __init__(self, fonts=list()):
        list.__init__(self, fonts)
    def all():
        return FontList(sorted(eval("[" + os.popen(r'''fc-list -f "{\"name\":\"%{family[0]|cescape}\",
        \"path\":\"%{file|cescape}\",
        \"style\":\"%{style[0]|cescape}\",
        \"styles\":\"%{style|cescape}\".split(\",\"),
        \"weight\":%{weight|cescape},
        \"spacing\":%{spacing:-0}},\n"''').read() + "]"),
                               key=lambda font: font["name"]))
    def bold(self):
        return FontList([font for font in self
                         if _styles_contains(font, "Bold")])

    def slanted(self):
        return FontList([font for font in self
                         if (_styles_contains(font, "Italic") or
                             _styles_contains(font, "Oblique") or
                             _styles_contains(font, "Slanted"))])

    def mono(self):
        return FontList([font for font in self
                         if font["spacing"] == 100])

    def regular(self):
        return FontList([font for font in self
                         if font not in self.bold() + self.slanted()])

    def proportional(self):
        return FontList([font for font in self
                         if font not in self.mono()])

    def by_style(self, style):
        return FontList([font for font in self
                         if _styles_contains(font, style)])

    def by_partial_name(self, partial):
        return FontList([font for font in self
                         if partial.lower() in font["name"].lower()])

    def by_weight(self, weight):
        return FontList([font for font in self
                         if font["weight"] == weight])

    def by_spacing(self, spacing):
        return FontList([font for font in self
                         if font["spacing"] == spacing])
    
if __name__ == "__main__":
    print(["%(name)s %(style)s" % font
           for font in FontList.all().by_style("Book")])
    print(["%(name)s %(style)s" % font
           for font in FontList.all().bold().slanted().mono()])
    print(["%(name)s %(style)s" % font
           for font in FontList.all().by_style("Roman")])
    styles = []
    for font in FontList.all():
        styles += font["styles"]
    print(set(styles))
