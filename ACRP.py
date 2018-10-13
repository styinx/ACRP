from ACRPlib.ac_widget import *

APP = None
APP_X = 0
APP_Y = 0
APP_W = 0
APP_H = 0


def init():
    ROBOTO_MONO = Font("Roboto", 0, 0)
    ROBOTO_MONO = Font("Roboto Mono", 0, 0)
    ROBOTO_MONO_I = Font("Roboto Mono", 1, 0)
    ROBOTO_MONO_B = Font("Roboto Mono", 0, 1)
    ROBOTO_MONO_IB = Font("Roboto Mono", 1, 1)


def rectIntersect(pos1, size1, pos2, size2):
    return not (pos1[0] + size1[0] < pos2[0] or
                pos1[0] > pos2[0] + size2[0] or
                pos1[1] + size1[1] < pos2[1] or
                pos1[1] > pos2[1] + size2[1])


'''
# AC Main Functions
'''


def acMain(ac_version):
    global panel_main, panel_standing, panel_time, panel_car, main_widget
    global APP, APP_X, APP_Y

    init()

    panel_main = ACApp("ACRP", 0, 0, 300, 100).hideDecoration()
    panel_standing = ACApp("ACRP Standings", 0, 0, 300, 100).hideDecoration()
    panel_time = ACApp("ACRP Times", 0, 0, 300, 100).hideDecoration()
    panel_car = ACApp("ACRP Car", 0, 0, 300, 100).hideDecoration()
    main_widget = ACMainWidget(panel_main)

    panel_main.background_color = BLACK
    panel_main.background_opacity = 1
    panel_standing.background_color = BLACK
    panel_standing.background_opacity = 0

    guiMain()
    guiStanding()
    guiTimes()
    guiCar()

    panel_main.render_callback = renderMain
    panel_standing.render_callback = renderStanding
    panel_time.render_callback = renderTime
    panel_car.render_callback = renderCar

    return "ACRP"


def acUpdate(delta):
    global panel_main, panel_standing, panel_time, panel_car, main_widget

    panel_main.update()
    panel_standing.update()
    panel_time.update()
    panel_car.update()

    if panel_standing.position_changed:
        main_widget.dettach(panel_standing)

    if not panel_standing.attached:
        if rectIntersect(panel_main.pos, panel_main.size, panel_standing.pos, panel_standing.size):
            main_widget.attach(panel_standing)

    updateMain()
    updateStanding()
    updateTimes()
    updateCar()


def acRender(delta):
    global panel_main, panel_standing, panel_time, panel_car

    panel_main.render()
    panel_standing.render()
    panel_time.render()
    panel_car.render()

    renderMain()
    renderStanding()
    renderTime()
    renderCar()


'''
# GUI Setup
'''


def guiMain():
    global panel_main
    global main_grid, gear, speed, rpm, rpm_widget

    main_grid = ACGrid(panel_main, 3, 3)
    gear = ACLabel("", panel_main)
    speed = ACLabel("", panel_main)
    rpm = ACLabel("", panel_main)
    rpm_widget = ACRPMWidget()

    gear.font_bold = 1
    gear.font_size = 60
    gear.text_h_alignment = "right"

    speed.font_size = 40
    speed.text_h_alignment = "right"
    speed.text_v_alignment = "top"

    rpm.font_size = 15
    rpm.text_h_alignment = "right"
    rpm.text_v_alignment = "bottom"

    main_grid.addWidget(gear, 0, 0, 1, 2)
    main_grid.addWidget(speed, 1, 0, 2, 1)
    main_grid.addWidget(rpm, 1, 1, 2, 1)
    main_grid.addWidget(rpm_widget, 0, 2, 3, 1)


def guiStanding():
    global panel_standing
    global standing_grid, lap, position, next_car, prev_car

    standing_grid = ACGrid(panel_standing, 4, 4)
    lap = ACLabel("", panel_standing)
    position = ACLabel("", panel_standing)
    next_car = ACLabel("", panel_standing)
    prev_car = ACLabel("", panel_standing)

    lap.font_bold = 1
    lap.font_italic = 1
    lap.font_size = 18

    position.font_bold = 1
    position.font_italic = 1
    position.font_size = 18

    next_car.font_bold = 1
    next_car.text_color = GOOD
    next_car.font_size = 14

    prev_car.font_bold = 1
    prev_car.text_color = BAD
    prev_car.font_size = 14

    standing_grid.addWidget(lap, 0, 0, 2, 1)
    standing_grid.addWidget(position, 2, 0, 2, 1)
    standing_grid.addWidget(next_car, 0, 2, 2, 1)
    standing_grid.addWidget(prev_car, 2, 2, 2, 1)


def guiTimes():
    global panel_time
    global time_grid, delta_widget, delta_label, current, last, best

    time_grid = ACGrid(panel_time, 6, 4)
    delta_widget = ACLapDeltaWidget(panel_time)
    delta_label = ACLabel("", panel_time)

    delta_label.font_bold = 1
    delta_label.text_color = WHITE
    delta_label.font_size = 16

    time_grid.addWidget(delta_widget, 0, 0, 6, 1)
    time_grid.addWidget(delta_label, 0, 2, 6, 1)


def guiCar():
    global panel_car


'''
# GUI Update
'''


def updateMain(delta=0):
    global gear, speed, rpm, rpm_widget

    gear.text = ACCAR.getGear()
    speed.text = "{:3.0f} km/h".format(ACCAR.getSpeed())
    rpm.text = "{:5.0f} rpm".format(ACCAR.getRPM())
    rpm_widget.update()


def updateStanding(delta=0):
    global lap, position, next_car, prev_car

    lap.text = "Lap: " + str(ACLAP.getLap()) + "/" + str(ACLAP.getLaps())
    position.text = "Pos: " + str(ACCAR.getPosition()) + "/" + str(ACSESSION.getCarsCount())
    next_car.text = "Next: " + ACCAR.getNextCarDiff()
    prev_car.text = "Prev: " + ACCAR.getPrevCarDiff()


def updateTimes(delta=0):
    global time_grid, delta_widget, delta_label, current, last, best

    delta_widget.update()
    delta_label.text = ACLAP.getLapDelta()
    delta_label.text_color = delta_widget.delta_color


def updateCar(delta=0):
    i = 0


'''
# GUI Render
'''


def renderMain(delta=0):
    global panel_main
    global rpm_widget

    panel_main.render()
    rpm_widget.render()


def renderStanding(delta=0):
    global panel_standing

    panel_standing.render()


def renderTime(delta=0):
    global panel_time
    global delta_widget

    panel_time.render()
    delta_widget.render()


def renderCar(delta=0):
    global panel_car

    panel_car.render()
