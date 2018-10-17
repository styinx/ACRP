import ac
from ACRPlib.ac_lib import *

TRANSPARENT = Color(0, 0, 0, 0)
BLACK = Color(0, 0, 0, 1)
BLUE = Color(0, 0, 1, 1)
GREEN = Color(0, 1, 0, 1)
CYAN = Color(0, 1, 1, 1)
RED = Color(1, 0, 0, 1)
WHITE = Color(1, 1, 1, 1)

LIME = Color(0.2, 0.7, 0.1, 1)
YELLOW = Color(0.9, 0.9, 0, 1)
ORANGE = Color(0.9, 0.7, 0, 1)
PURPLE = Color(0.3, 0, 0.7, 1)

GOOD = Color(0, 0.8, 0, 1)
BAD = Color(0.9, 0, 0, 1)

COLORS = {
    "TRANSPARENT": TRANSPARENT
}


class ACGUI:
    text_h_alignment = "center"
    text_v_alignment = "middle"
    text_color = WHITE
    font_size = 10
    font_family = "Roboto Mono"
    italic = 0
    bold = 0


class ACWidget(object):
    def __init__(self, parent=None):
        self._ac_obj = None
        self._child = None
        self._parent = None
        self._pos = (0, 0)
        self._size = (0, 0)
        self._visible = True
        self._background_texture = None
        self._background = False
        self._background_color = Color(0, 0, 0, 0)
        self._background_opacity = 0
        self._border = True
        self._border_color = Color(1, 1, 1, 1)
        self._render_callback = None

        if parent is not None:
            self._parent = parent
            parent._child = self

            self.pos = parent.pos
            self.size = parent.size

    @staticmethod
    def getPosition(obj):
        return ac.getPosition(obj)

    def obj(self):
        return self._ac_obj

    @property
    def child(self):
        return self._child

    @child.setter
    def child(self, child):
        if self._child is not None:
            self._child.parent = None

        self._child = child

        if child is not None:
            child._parent = self

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if self._parent is not None:
            self._parent.child = None

        self._parent = parent

        if parent is not None:
            parent._child = self

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos

        if self._ac_obj is not None:
            ac.setPosition(self._ac_obj, self._pos[0], self._pos[1])

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

        if self._ac_obj is not None:
            ac.setSize(self._ac_obj, self._size[0], self._size[1])

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        self._visible = visible

        if self._ac_obj is not None:
            ac.setVisible(visible)

    @property
    def background_texture(self):
        return self._background_texture

    @background_texture.setter
    def background_texture(self, tex):
        if isinstance(tex, str):
            self._background_texture = ac.newTexture(tex)
        else:
            self._background_texture = tex

        if self._ac_obj is not None:
            ac.setBackgroundTexture(self._ac_obj, self._background_texture)

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, background):
        self._background = background

        if self._ac_obj is not None:
            ac.drawBackground(self._ac_obj, self._background)

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        self._background_color = background_color

        if self._ac_obj is not None:
            col = self._background_color
            ac.setBackgroundColor(self._ac_obj, col.r, col.g, col.b)
            ac.setBackgroundOpacity(self._ac_obj, col.a)

    @property
    def background_opacity(self):
        return self._background_opacity

    @background_opacity.setter
    def background_opacity(self, background_opacity):
        self._background_opacity = background_opacity

        if self._ac_obj is not None:
            ac.setBackgroundOpacity(self._ac_obj, background_opacity)

    @property
    def border(self):
        return self._border

    @border.setter
    def border(self, border):
        if isinstance(border, bool):
            self._border = border

        if self._ac_obj is not None:
            ac.drawBorder(self._ac_obj, self._border)

    @property
    def border_color(self):
        return self._border_color

    @border_color.setter
    def border_color(self, border_color):
        if isinstance(border_color, Color):
            self._border_color = border_color

    def show(self):
        if self._ac_obj is not None:
            ac.setVisible(self._ac_obj, True)

    def hide(self):
        if self._ac_obj is not None:
            ac.setVisible(self._ac_obj, False)

    def update(self):
        if self._child is not None:
            self._child.update()

        if self._background:
            col = self._background_color
            if self._ac_obj is not None:
                ac.setBackgroundColor(self._ac_obj, col.r, col.g, col.b)
                ac.setBackgroundOpacity(self._ac_obj, col.a)

    def render(self):
        if self._child is not None:
            self._child.render()

        if self._border:
            GL.rect(self._pos[0], self._pos[1], self._size[0], self._size[1], self._border_color, False)


class ACMainWidget(ACWidget):
    def __init__(self, app):
        super().__init__()

        self._children = []
        self._app = app
        self.size = self._app.size

    def app(self):
        return self._app

    def attach(self, app):
        self._children.append(app)

        if not app.attached:

            x, y = app.pos
            w, h = app.size

            ax, ay = self._app.pos
            aw, ah = self._app.size

            # horizontal
            if ax - x <= ay - y or ax + aw - x <= ay + ah - y:
                # left
                if x <= ax + aw / 2:
                    app.pos = (ax - w - 1, ay)
                # right
                elif x > ax + aw / 2:
                    app.pos = (ax + aw + 1, ay)
            # vertical
            else:
                # top
                if y <= ay + ah / 2:
                    app.pos = (ax, ay - h - 1)
                # bottom
                elif y > ay + ah / 2:
                    app.pos = (ax, ay + ah + 1)

        app.attached = True

    def dettach(self, app):
        if isinstance(app, ACApp):
            i = 0
        elif isinstance(app, int) and app < len(self._children):
            self._children[app] = None

        app.attached = False

    def update(self):
        pass

    def render(self):
        pass


class ACApp(ACWidget):
    def __init__(self, app_name, x, y, w, h, main=None):
        super().__init__()

        self._ac_obj = ac.newApp(app_name)
        self._main = main
        self.position_changed = False
        self.attached = False
        self._render_callback = None
        self._title = False
        self._title_position = (0, 0)
        self._icon = False
        self._icon_position = (0, 0)

        self._pos = ac.getPosition(self._ac_obj)
        self.size = (int(w), int(h))

        self.update()

    @property
    def main(self):
        return self._main

    @main.setter
    def main(self, main):
        self._main = main

    @property
    def render_callback(self):
        return self._render_callback

    @render_callback.setter
    def render_callback(self, render_callback):
        self._render_callback = render_callback

        if self._ac_obj is not None:
            ac.addRenderCallback(self._ac_obj, self._render_callback)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

        if self._ac_obj is not None:
            ac.setTitle(self._ac_obj, self._title)

    @property
    def title_position(self):
        return

    @title_position.setter
    def title_position(self, title_position):
        self._title_position = title_position

        if self._ac_obj is not None:
            ac.setTitlePosition(self._ac_obj, 0, -10000)

    @property
    def icon(self):
        return

    @icon.setter
    def icon(self, icon):
        self._icon = icon

    @property
    def icon_position(self):
        return self.icon_position

    @icon_position.setter
    def icon_position(self, icon_position):
        self._icon_position = icon_position

        if self._ac_obj is not None:
            ac.setIconPosition(self._ac_obj, 0, -10000)

    def app(self):
        return self._ac_obj

    def hideDecoration(self):
        if self._ac_obj is not None:
            ac.setTitlePosition(self._ac_obj, 0, -10000)
            ac.setIconPosition(self._ac_obj, 0, -10000)

        return self

    def update(self):
        self.position_changed = False
        col = self._background_color

        if self._ac_obj is not None:
            ac.setBackgroundColor(self._ac_obj, col.r, col.g, col.b)
            ac.setBackgroundOpacity(self._ac_obj, col.a)

            x, y = ACWidget.getPosition(self._ac_obj)

            if self._pos[0] != x or self._pos[1] != y:
                self._pos = (x, y)
                self.position_changed = True

    def render(self):
        if self._border:
            GL.rect(0, 0, self._size[0], self._size[1], self._border_color, False)


class ACLayout(ACWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._children = None


class ACBox(ACLayout):
    def __init__(self, parent=None, orientation=0):
        super().__init__(parent)

        self._children = []
        self._children_count = 0
        self._orientation = orientation

    def addWidget(self, widget):
        self._children.append(widget)
        self._children_count += 1

    def update(self):
        super().update()

        for child in self._children:
            child.update()

    def render(self):
        super().render()

        for child in self._children:
            child.render()


class ACHBox(ACBox):
    def __init__(self, parent=None):
        super().__init__(parent, 0)

    def addWidget(self, widget):
        super().addWidget(widget)

        x = self.pos[0]
        w = int(self.size[0] / self._children_count)
        h = int(self.size[1] / self._children_count)

        for c in self._children:
            c.pos = (int(x), int(self.pos[1]))
            c.size = (int(w), int(h))
            x += w


class ACVBox(ACBox):
    def __init__(self, parent=None):
        super().__init__(parent, 1)

    def addWidget(self, widget):
        super().addWidget(widget)

        y = self.pos[1]
        w = self.size[0] / self._children_count
        h = self.size[1] / self._children_count

        for child in self._children:
            child.pos = (int(self.pos[0]), int(y))
            child.size = (int(w), int(h))
            y += h


class ACGrid(ACLayout):
    def __init__(self, parent, cols, rows):
        super().__init__(parent)

        self._children = [x[:] for x in [[0] * cols] * rows]
        self._cols = cols
        self._rows = rows
        self._cell_width = int(self.size[0] / self._cols + 0.5)
        self._cell_height = int(self.size[1] / self._rows + 0.5)

        if isinstance(parent, ACApp):
            self.pos = (0, 0)

    def addWidget(self, widget, x, y, w=1, h=1):
        self._children[y][x] = widget

        widget.pos = (int(self.pos[0] + x * self._cell_width + 0.5), int(self.pos[1] + y * self._cell_height + 0.5))
        widget.size = (int(w * self._cell_width + 0.5), int(h * self._cell_height + 0.5))

    def updateSize(self):
        self._cell_width = int(self.size[0] / self._cols + 0.5)
        self._cell_height = int(self.size[1] / self._rows + 0.5)

    def update(self):
        for row in self._children:
            for cell in row:
                if isinstance(cell, ACWidget):
                    cell.update()

    def render(self):
        for row in self._children:
            for cell in row:
                if isinstance(cell, ACWidget):
                    cell.update()


class ACTextWidget(ACWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._text = ""
        self._text_h_alignment = ACGUI.text_h_alignment
        self._text_v_alignment = ACGUI.text_v_alignment
        self._text_color = ACGUI.text_color
        self._font_size = ACGUI.font_size
        self._font_family = ACGUI.font_family
        self._font_italic = ACGUI.italic
        self._font_bold = ACGUI.bold

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

        if self._ac_obj is not None:
            ac.setText(self._ac_obj, text)

    @property
    def text_h_alignment(self):
        return self._text_h_alignment

    @text_h_alignment.setter
    def text_h_alignment(self, text_h_alignment="left"):
        self._text_h_alignment = text_h_alignment

        if self._ac_obj is not None:
            if text_h_alignment == "left":
                ac.setPosition(self._ac_obj, self.pos[0], self.pos[1])
            elif text_h_alignment == "center":
                ac.setPosition(self._ac_obj, int(self.pos[0] + self.size[0] / 2), self.pos[1])
            elif text_h_alignment == "right":
                ac.setPosition(self._ac_obj, int(self.pos[0] + self.size[0]), self.pos[1])
            ac.setFontAlignment(self._ac_obj, text_h_alignment)

    @property
    def text_v_alignment(self):
        return self._text_v_alignment

    @text_v_alignment.setter
    def text_v_alignment(self, text_v_alignment="top"):
        self._text_v_alignment = text_v_alignment

        if self._ac_obj is not None:
            if text_v_alignment == "top":
                ac.setPosition(self._ac_obj, self.pos[0], self.pos[1])
            elif text_v_alignment == "middle":
                ac.setPosition(self._ac_obj, self.pos[0], self.pos[1] + self.size[1] / 2)
            elif text_v_alignment == "bottom":
                ac.setPosition(self._ac_obj, self.pos[0], self.pos[1] + self.size[1])

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, text_color):
        self._text_color = text_color

        if self._ac_obj is not None:
            ac.setFontColor(self._ac_obj, self._text_color.r, self._text_color.g, self._text_color.b,
                            self._text_color.a)

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        self._font_size = font_size

        if self._ac_obj is not None:
            ac.setFontSize(self._ac_obj, self._font_size)

    @property
    def font_italic(self):
        return self._font_italic

    @font_italic.setter
    def font_italic(self, font_italic):
        self._font_italic = font_italic

        if self._ac_obj is not None:
            ac.setCustomFont(self._ac_obj, self._font_family, self._font_italic, self._font_bold)

    @property
    def font_bold(self):
        return self._font_bold

    @font_bold.setter
    def font_bold(self, font_bold):
        self._font_bold = font_bold

        if self._ac_obj is not None:
            ac.setCustomFont(self._ac_obj, self._font_family, self._font_italic, self._font_bold)

    @property
    def font_family(self):
        return self._font_family

    @font_family.setter
    def font_family(self, font_family):
        if isinstance(font_family, str):
            self._font_family = font_family

            if self._ac_obj is not None:
                ac.setCustomFont(self._ac_obj, self._font_family, self._font_italic, self._font_bold)

        elif isinstance(font_family, Font):
            self._font_family = font_family.font_name

            if self._ac_obj is not None:
                ac.setCustomFont(self._ac_obj, self._font_family, self._font_italic, self._font_bold)

    @staticmethod
    def initOBJ(obj):
        obj.text_h_alignment = ACGUI.text_h_alignment
        obj.text_v_alignment = ACGUI.text_v_alignment
        obj.text_color = ACGUI.text_color
        obj.font_size = ACGUI.font_size
        obj.font_family = ACGUI.font_family
        obj.font_italic = ACGUI.italic
        obj.font_bold = ACGUI.bold


class ACLabel(ACTextWidget):
    def __init__(self, text, app, parent=None):
        super().__init__(parent)

        self._ac_obj = ac.addLabel(app.app(), text)
        self.text = text
        ACTextWidget.initOBJ(self)


class ACProgressBar(ACLabel):
    def __init__(self, app, orientation=0, value=0, min_val=0, max_val=100, parent=None):
        super().__init__("", app, parent)

        self.orientation = orientation
        self.color = self.background_color
        self.margin = 0.2
        self.value = value
        self.min_val = min_val
        self.max_val = max_val

    def render(self):
        if self.orientation == 0:
            ratio = self.size[0] * (self.value / self.max_val)
            margin = self.size[1] * self.margin
            GL.rect(self.pos[0], self.pos[1] + margin, ratio, self.size[1] - 2 * margin, self.color)

            if self._border:
                GL.rect(self.pos[0], self.pos[1] + margin, self.size[0], self.size[1] - 2 * margin, self.border_color, False)
        else:
            ratio = self.size[1] * (self.value / self.max_val)
            margin = self.size[0] * self.margin
            GL.rect(self.pos[0] + margin, self.size[1] - ratio, self.size[0] - 2 * margin, ratio, self.color)

            if self._border:
                GL.rect(self.pos[0] + margin, self.pos[1], self.size[0] - 2 * margin, self.size[1], self.border_color,
                        False)
