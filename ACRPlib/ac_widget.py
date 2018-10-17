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


class ACTyreWidget(ACGrid):
    def __init__(self, tyre, app, front=False, parent=None):
        super().__init__(parent, 3, 5)

        self.tyre = tyre
        self.app = app
        self.front = front

        self.tyre_temps = [ACLabel("", self.app)] * 4
        for i in range(0, len(self.tyre_temps)):
            self.tyre_temps[i] = ACLabel("", self.app)
            self.tyre_temps[i].background = True

        self.t = None
        self.p = None
        self.w = None
        self.w_state = None

        self.tyre_temp_values = [145, 135, 125, 105, 75, 65, 55]
        self.tyre_temp_colors = [RED, ORANGE, YELLOW, LIME, GREEN, CYAN, BLUE]

        self.tyre_wear_values = [90, 80, 60, 40, 20]
        self.tyre_wear_colors = [GREEN, LIME, YELLOW, ORANGE, RED]

        self.tyre_pressure_values = [35, 32, 29, 26, 23, 20, 17]
        self.tyre_pressure_colors = [RED, ORANGE, YELLOW, LIME, GREEN, CYAN, BLUE]

    def init(self):
        self.updateSize()

        self.t = ACLabel("", self.app)
        self.p = ACLabel("", self.app)
        self.w = ACLabel("", self.app)
        self.w_state = ACProgressBar(self.app)

        self.t.font_size = 12
        self.t.font_bold = 1
        self.t.text_h_alignment = "left"
        self.p.font_size = 12
        self.p.font_bold = 1
        self.p.text_h_alignment = "right"
        self.w.font_size = 12
        self.w.font_bold = 1

        self.w_state.border = 1

        self.addWidget(self.tyre_temps[0], 0, 0, 1, 3)

        if self.front:
            self.addWidget(self.tyre_temps[1], 1, 0)
            self.addWidget(self.tyre_temps[3], 1, 1, 1, 2)
        else:
            self.addWidget(self.tyre_temps[1], 1, 2)
            self.addWidget(self.tyre_temps[3], 1, 0, 1, 2)

        self.addWidget(self.tyre_temps[2], 2, 0, 1, 3)

        self.addWidget(self.t, 0, 3)
        self.addWidget(self.p, 2, 3)
        self.addWidget(self.w_state, 0, 4, 2, 1)
        self.addWidget(self.w, 2, 4, 1, 1)

    def update(self):
        self.t.text = "{:3.0f}°".format(ACCAR.getTyreTemp(self.tyre))
        self.p.text = "{:2.0f}psi".format(ACCAR.getTyrePressure(self.tyre))
        self.w.text = ACCAR.getTyreWearFormated(self.tyre)

        temps = ACCAR.getTyreTemp(self.tyre, "all")

        for i in range(0, len(temps)):
            for j in range(0, len(self.tyre_temp_values)):
                if temps[i] > self.tyre_temp_values[j]:
                    self.t.text_color = self.tyre_temp_colors[j]
                    self.tyre_temps[i].background_color = self.tyre_temp_colors[j]
                    break

        wear = ACCAR.getTyreWear(self.tyre)
        self.w_state.value = wear

        for i in range(0, len(self.tyre_wear_values)):
            if wear > self.tyre_wear_values[i]:
                self.w.text_color = self.tyre_wear_colors[i]
                break

        pressure = ACCAR.getTyrePressure(self.tyre)

        for i in range(0, len(self.tyre_pressure_values)):
            if pressure > self.tyre_pressure_values[i]:
                self.p.text_color = self.tyre_pressure_colors[i]
                break

        dirt = ACCAR.getTyreDirtyLevel(self.tyre)

        if dirt > 0:
            for i in range(0, len(temps)):
                self.tyre_temps[i].background_color = Color(0.7, 0.3, 0.1, max(0.2, 1 - dirt * 0.2))

        super().update()

    def render(self):
        super().render()

        self.w_state.render()


class ACCarModelWidget(ACGrid):
    def __init__(self, app, parent=None):
        super().__init__(parent, 7, 7)

        self.app = app

        self.car_damage = [] * 4
        self.car_damage_values = [80, 60, 40, 20, 0]
        self.car_damage_colors = [RED, ORANGE, YELLOW, LIME, GREEN]

    def init(self):
        for i in range(0, len(self.car_damage)):
            self.car_damage[i] = ACLabel("", self.app)

        self.addWidget(self.car_damage[0], 1, 1, 5, 1)
        self.addWidget(self.car_damage[1], 6, 1, 5, 1)
        self.addWidget(self.car_damage[2], 1, 2, 1, 3)
        self.addWidget(self.car_damage[3], 6, 2, 1, 3)

    def update(self):
        for i in range(0, len(self.car_damage)):
            damage = ACCAR.getCarDamage(i)
            for j in range(0, len(self.car_damage_values)):
                if damage[i] > self.car_damage_values[j]:
                    self.car_damage[i].background_color = self.car_damage_colors[j]
                    break
