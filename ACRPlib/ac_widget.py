from math import log10
from ACRPlib.ac_gui import *


class ACLapDeltaWidget(ACWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)

        self.delta = 0
        self.delta_color = WHITE

    def update(self):
        super().update()

        self.delta = ACLAP.getLapDeltaTime()

    def render(self):
        super().render()

        x = self.pos[0]
        y = self.pos[1]
        w = self.size[0]
        h = self.size[1]
        w2 = w / 2
        dist = 0
        if self.delta != 0:
            dist = min(max(abs(self.delta) * w2 * 0.1, log10(abs(self.delta)) * w2), w2)

        if self.delta < 0:
            self.delta_color = GOOD
            GL.rect(x + w2 - dist, y, dist, h, self.delta_color, True)
        elif self.delta > 0:
            self.delta_color = BAD
            GL.rect(x + w2, y, dist, h, self.delta_color, True)
        else:
            self.delta_color = WHITE

        GL.rect(x, y, w, h, WHITE, False)
        GL.line(x + w2, y, x + w2, y + h, WHITE)


AC_RPM_STATUS = {
    "rpm": [100, 98, 96, 94, 92],
    "rpm_colors": [RED, ORANGE, YELLOW, LIME, GREEN]
}


class ACRPMWidget(ACWidget):
    def __init__(self, orientation=0, parent=None):
        super().__init__(parent)

        self.rpm_rel = 0
        self.orientation = orientation
        self.color = TRANSPARENT

    def update(self):
        super().update()

        self.rpm_rel = ACCAR.getRPM() / ACCAR.getRPMMax()

    def render(self):
        super().render()

        start = self.pos[0]
        stop = int((self.pos[0] + self.size[0]) * self.rpm_rel)
        bar_w = 2
        bar_d = 4
        offset = 0.2
        size = self.size[0]

        if self.orientation == 1:
            start = (self.pos[1] + self.size[1]) * self.rpm_rel
            stop = self.pos[1] + self.size[1]
            bar_d *= -1

        for pos in range(start, stop, bar_d):
            if pos >= 0.92 * size:
                self.color = RED
            elif pos >= 0.8 * size:
                self.color = ORANGE
            elif pos >= 0.6 * size:
                self.color = YELLOW
            elif pos >= 0.3 * size:
                self.color = LIME
            else:
                self.color = GREEN

            if self.orientation == 0:
                GL.rect(pos, int(self.pos[1] + (self.size[1] * offset)), bar_w, int(self.size[1] * (1 - offset * 2)), self.color, True)
            else:
                GL.rect(self.pos[0], pos, self.size[1], bar_w, self.color, True)


AC_TYRE_STATUS = {
    "tyre_wear": [100, 80, 60, 40, 20],
    "tyre_wear_colors": [GREEN, LIME, YELLOW, ORANGE, RED],
    "tyre_temp": [100, 80, 60, 40, 20],
    "tyre_temp_colors": [GREEN, LIME, YELLOW, ORANGE, RED],
    "tyre_dirt": [100, 80, 60, 40, 20],
    "tyre_dirt_colors": [GREEN, LIME, YELLOW, ORANGE, RED],
    "tyre_pressure": [100, 80, 60, 40, 20],
    "tyre_pressure_colors": [GREEN, LIME, YELLOW, ORANGE, RED]
}


class ACTyreWidget(ACWidget):
    def __init__(self, tyre, app, parent=None):
        super().__init__(parent)

        self.tyre = tyre
        self.widget = ACGrid(app, 3, 4)

        self.t_o = ACLabel("", app)
        self.t_m = ACLabel("", app)
        self.t_c = ACLabel("", app)
        self.t_i = ACLabel("", app)
        self.t = ACLabel("", app)
        self.w = ACLabel("", app)
        self.p = ACLabel("", app)

        self.t_o.background_color = GREEN
        self.t_m.background_color = GREEN
        self.t_c.background_color = GREEN
        self.t_i.background_color = GREEN

        self.widget.addWidget(self.t_o, 0, 0)
        self.widget.addWidget(self.t_m, 1, 0)
        self.widget.addWidget(self.t_c, 1, 1)
        self.widget.addWidget(self.t_i, 2, 0)
        self.widget.addWidget(self.t, 0, 3)
        self.widget.addWidget(self.w, 1, 3)
        self.widget.addWidget(self.p, 2, 3)

    def update(self):
        super().update()

        self.t.text = ACCAR.getTyreTempFormated(self.tyre)
        self.w.text = ACCAR.getTyreWearFormated(self.tyre)
        self.p.text = ACCAR.getTyrePressureFormated(self.tyre)

    def render(self):
        super().render()
