from ACRPlib.ac_widget import *

APP = None
APP_X = 0
APP_Y = 0
APP_W = 0
APP_H = 0
first_update = 0

GLOBAL = {
    "CARS": [{"Lap_Invalid", "current_sectors", "Lap"}],
    "Fastest_Lap": 0,
    "Fastest_Sectors": [0, 0, 0]
}


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
    global panel_main, panel_standing, panel_time, panel_tyres, panel_car, panel_session, main_widget
    global APP, APP_X, APP_Y

    init()

    panel_main = ACApp("ACRP", 0, 0, 300, 100).hideDecoration()
    panel_standing = ACApp("ACRP Standings", 0, 0, 300, 100).hideDecoration()
    panel_time = ACApp("ACRP Times", 0, 0, 300, 200).hideDecoration()
    panel_tyres = ACApp("ACRP Tyres", 0, 0, 210, 250).hideDecoration()
    panel_car = ACApp("ACRP Car", 0, 0, 120, 200).hideDecoration()
    panel_session = ACApp("ACRP Session", 0, 0, 300, 100).hideDecoration()
    main_widget = ACMainWidget(panel_main)

    panel_main.background_color = BLACK
    panel_main.background_opacity = 1
    panel_standing.background_color = BLACK
    panel_standing.background_opacity = 1
    panel_time.background_color = BLACK
    panel_time.background_opacity = 1
    panel_tyres.background_color = BLACK
    panel_tyres.background_opacity = 1
    panel_car.background_color = BLACK
    panel_car.background_opacity = 1
    panel_session.background_color = BLACK
    panel_session.background_opacity = 1

    guiMain()
    guiStanding()
    guiTimes()
    guiTyres()
    guiCar()
    guiSession()

    panel_main.render_callback = renderMain
    panel_standing.render_callback = renderStanding
    panel_time.render_callback = renderTime
    panel_tyres.render_callback = renderTyres
    panel_car.render_callback = renderCar
    panel_session.render_callback = renderSession

    return "ACRP"


def acUpdate(delta):
    global first_update, c_lap_fuel, c_dist_fuel
    global panel_main, panel_standing, panel_time, panel_tyres, panel_car, panel_session, main_widget

    if first_update == 0:
        c_lap_fuel = ACCAR.getFuel()
        c_dist_fuel = c_lap_fuel
        first_update += 1

    panel_main.update()
    panel_standing.update()
    panel_time.update()
    panel_tyres.update()
    panel_car.update()
    panel_session.update()

    if panel_standing.position_changed:
        main_widget.dettach(panel_standing)

    if not panel_standing.attached:
        if rectIntersect(panel_main.pos, panel_main.size, panel_standing.pos, panel_standing.size):
            main_widget.attach(panel_standing)

    updateMain()
    updateStanding()
    updateTimes()
    updateTyres()
    updateCar()
    updateSession()


def acRender(delta):
    global panel_main, panel_standing, panel_time, panel_tyres, panel_car, panel_session

    panel_main.render()
    panel_standing.render()
    panel_time.render()
    panel_tyres.render()
    panel_car.render()
    panel_session.render()

    renderMain()
    renderStanding()
    renderTime()
    renderTyres()
    renderCar()
    renderSession()


'''
# GUI Setup
'''


def guiMain():
    global panel_main
    global main_grid, gear, speed, rpm, rpm_widget

    main_grid = ACGrid(panel_main, 3, 4)
    gear = ACLabel("", panel_main)
    speed = ACLabel("", panel_main)
    rpm = ACLabel("", panel_main)
    rpm_widget = ACRPMWidget()

    main_grid.background = 1

    gear.font_bold = 1
    gear.font_size = 60

    speed.font_size = 40
    speed.text_h_alignment = "right"

    rpm.font_size = 20
    rpm.text_h_alignment = "right"
    rpm.text_v_alignment = "top"

    main_grid.addWidget(gear, 0, 0, 1, 3)
    main_grid.addWidget(speed, 1, 0, 2, 2)
    main_grid.addWidget(rpm, 1, 2, 2, 1)
    main_grid.addWidget(rpm_widget, 0, 3, 3, 1)


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
    global time_grid, delta_widget, delta_label, current_sectors, current, last_sectors, last, best, valid
    global current_sector_num, current_sector_value, current_sector_text, current_sector

    time_grid = ACGrid(panel_time, 6, 8)
    delta_widget = ACLapDeltaWidget(panel_time)
    delta_label = ACLabel("", panel_time)
    current_sectors = ACLabel("", panel_time)
    current = ACLabel("", panel_time)
    last_sectors = ACLabel("", panel_time)
    last = ACLabel("", panel_time)
    best = ACLabel("", panel_time)
    current_sector = ACLabel("", panel_time)
    current_sector_num = -1
    current_sector_value = 0
    current_sector_text = ""
    valid = True

    delta_label.font_bold = 1
    delta_label.font_size = 16

    current_sector.font_size = 12
    current.font_size = 16

    last_sectors.font_size = 12
    last.font_size = 16

    best.font_size = 16

    time_grid.addWidget(delta_widget, 0, 0, 6, 1)
    time_grid.addWidget(delta_label, 0, 2, 6, 1)
    time_grid.addWidget(current_sector, 0, 3, 6, 1)
    time_grid.addWidget(current, 0, 4, 6, 1)
    time_grid.addWidget(last_sectors, 0, 5, 6, 1)
    time_grid.addWidget(last, 0, 6, 6, 1)
    time_grid.addWidget(best, 0, 7, 6, 1)


def guiTyres():
    global panel_tyres
    global tyre_grid, tyre_FL, tyre_FR, tyre_RL, tyre_RR

    tyre_grid = ACGrid(panel_tyres, 7, 7)

    tyre_FL = ACTyreWidget(0, panel_tyres, True)
    tyre_FR = ACTyreWidget(1, panel_tyres, True)
    tyre_RL = ACTyreWidget(2, panel_tyres)
    tyre_RR = ACTyreWidget(3, panel_tyres)

    tyre_grid.addWidget(tyre_FL, 0, 0, 3, 3)
    tyre_grid.addWidget(tyre_FR, 4, 0, 3, 3)
    tyre_grid.addWidget(tyre_RL, 0, 4, 3, 3)
    tyre_grid.addWidget(tyre_RR, 4, 4, 3, 3)

    tyre_FL.init()
    tyre_FR.init()
    tyre_RL.init()
    tyre_RR.init()


def guiCar():
    global car_grid, panel_car
    global car_widget, fuel, fuel_rate_p_l, fuel_rate_p_km, c_lap, c_lap_fuel, c_dist, c_dist_fuel, fuel_bar

    car_grid = ACGrid(panel_car, 3, 7)
    car_widget = ACCarModelWidget(panel_car)
    fuel = ACLabel("", panel_car)
    fuel_bar = ACProgressBar(panel_car, 1)
    fuel_rate_p_l = ACLabel("", panel_car)
    fuel_rate_p_km = ACLabel("", panel_car)

    fuel.font_size = 12
    fuel.font_bold = 12
    fuel.text_h_alignment = "left"
    fuel_rate_p_l.font_size = 12
    fuel_rate_p_l.text = "0.0 l / lap"
    fuel_rate_p_l.text_h_alignment = "left"
    fuel_rate_p_km.font_size = 12
    fuel_rate_p_km.text = "0.0 l / km"
    fuel_rate_p_km.text_h_alignment = "left"

    c_lap = 0
    c_lap_fuel = ACCAR.getFuel()
    c_dist = 0
    c_dist_fuel = c_lap_fuel

    car_grid.addWidget(car_widget, 0, 0, 3, 4)
    car_grid.addWidget(fuel, 0, 4, 2, 1)
    car_grid.addWidget(fuel_rate_p_l, 0, 5, 2, 1)
    car_grid.addWidget(fuel_rate_p_km, 2, 6, 2, 1)
    car_grid.addWidget(fuel_bar, 0, 4, 1, 3)

    car_widget.init()


def guiSession():
    global panel_session
    global session_grid, session_state, session_time, track_info, lap_progress

    session_grid = ACGrid(panel_session, 4, 4)
    session_state = ACLabel("", panel_session)
    session_time = ACLabel("", panel_session)
    track_info = ACLabel("", panel_session)
    lap_progress = ACProgressBar(panel_session)

    session_state.font_size = 14
    session_time.font_size = 14
    session_time.text_h_alignment = "left"
    track_info.font_size = 14
    track_info.text_h_alignment = "left"
    lap_progress.color = CYAN

    session_grid.addWidget(session_state, 0, 0, 4, 1)
    session_grid.addWidget(session_time, 0, 1, 4, 1)
    session_grid.addWidget(track_info, 0, 2, 4, 1)
    session_grid.addWidget(lap_progress, 0, 3, 4, 1)


'''
# GUI Update
'''


def updateMain(delta=0):
    global panel_main
    global main_grid, gear, speed, rpm, rpm_widget

    gear.text = ACCAR.getGear()
    speed.text = "{:3.0f} kmh".format(ACCAR.getSpeed())
    rpm.text = "{:5.0f} rpm".format(ACCAR.getRPM())
    rpm_widget.update()

    if rpm_widget.rpm_rel >= 0.94:
        panel_main.background_color = Color(1, 1, 0, 0.5)
    else:
        panel_main.background_color = BLACK

    main_grid.update()


def updateStanding(delta=0):
    global standing_grid, lap, position, next_car, prev_car

    lap.text = "Lap: " + str(ACLAP.getLap()) + "/" + str(ACLAP.getLaps())
    position.text = "Pos: " + str(ACCAR.getPosition()) + "/" + str(ACSESSION.getCarsCount())
    next_car.text = "Next: " + ACCAR.getNextCarDiff()
    prev_car.text = "Prev: " + ACCAR.getPrevCarDiff()

    standing_grid.update()


def updateTimes(delta=0):
    global time_grid, delta_widget, delta_label, current_sectors, current, last_sectors, last, best, valid
    global current_sector_num, current_sector_value, current_sector_text, current_sector

    time_grid.update()
    delta_widget.update()

    delta_label.text = ACLAP.getLapDelta()
    delta_label.text_color = delta_widget.delta_color

    # current splits

    if ACCAR.getTyresOut() == 4:
        valid = False

    if valid:
        current.text = "CUR:" + ACLAP.getCurrentLap()
    else:
        current.text = "CUR:" + ACLAP.getCurrentLap() + " [INVALID]"
    if ACLAP.getLapDeltaTime() < 0:
        current.text_color = GOOD
    elif ACLAP.getLapDeltaTime() > 0:
        current.text_color = BAD
    else:
        current.text_color = WHITE

    last_sector_text = ""
    last_sector_values = ACLAP.getSplits()
    for i in range(0, len(last_sector_values)):
        last_sector_text += formatTime(last_sector_values[i]) + " | "
    last_sectors.text = last_sector_text[:-3]

    last.text = "LST:" + ACLAP.getLastLap()
    if ACLAP.getLastLapTime() == ACLAP.getBestLapTime() and ACLAP.getLastLapTime() != 0:
        last.text_color = GOOD
    else:
        last.text_color = WHITE

    best.text = "BST:" + ACLAP.getBestLap()
    if ACLAP.getBestLapTime() != 0:
        best.text_color = GOOD
    else:
        best.text_color = WHITE


def updateTyres(delta=0):
    global tyre_grid
    global tyre_FL, tyre_FR, tyre_RL, tyre_RR

    tyre_grid.update()

    tyre_FL.update()
    tyre_FR.update()
    tyre_RL.update()
    tyre_RR.update()


def updateCar(delta=0):
    global car_grid
    global car_widget, fuel, fuel_rate_p_l, fuel_rate_p_km, c_lap, c_lap_fuel, c_dist, c_dist_fuel, fuel_bar

    fuel_bar.value = ACCAR.getFuel() / ACCAR.getMaxFuel()

    if ACLAP.getLap() > c_lap:
        fuel_rate_p_l.text = "{:3.1f} l / lap".format(max(0, c_lap_fuel - ACCAR.getFuel()))
        c_lap_fuel = ACCAR.getFuel()
        c_lap = ACLAP.getLap()
    if int(ACCAR.getTraveledDistance() / 1000) > c_dist:
        fuel_rate_p_km.text = "{:3.1f} l / km".format(max(0, c_dist_fuel - ACCAR.getFuel()))
        c_dist_fuel = ACCAR.getFuel()
        c_dist = int(ACCAR.getTraveledDistance() / 1000)

    fuel.text = "{:3.1f} l".format(ACCAR.getFuel())
    fuel_rate_p_l.text = fuel_rate_p_l.text
    fuel_rate_p_km.text = fuel_rate_p_km.text

    car_grid.update()
    car_widget.update()


def updateSession(delta=0):
    global session_grid, session_state, session_time, track_info, lap_progress

    session_grid.update()

    session_state.text = ACSESSION.getSessionTypeName() + " (" + ACSESSION.getSessionStatusName() + ")"
    session_time.text = ACSESSION.getRaceTimeLeftFormated()
    track_info.text = "Track distance: " + str(ACSESSION.getTrackLengthFormated())
    lap_progress.value = ACCAR.getLocation()


'''
# GUI Render
'''


def renderMain(delta=0):
    global panel_main
    global main_grid, rpm_widget

    panel_main.render()
    main_grid.render()
    rpm_widget.render()


def renderStanding(delta=0):
    global panel_standing
    global standing_grid

    standing_grid.render()
    panel_standing.render()


def renderTime(delta=0):
    global panel_time
    global time_grid, delta_widget

    panel_time.render()
    time_grid.render()
    delta_widget.render()


def renderTyres(delta=0):
    global panel_tyres
    global tyre_grid
    global tyre_FL, tyre_FR, tyre_RL, tyre_RR

    panel_tyres.render()
    tyre_grid.render()

    tyre_FL.render()
    tyre_FR.render()
    tyre_RL.render()
    tyre_RR.render()


def renderCar(delta=0):
    global panel_car
    global car_widget
    global car_grid

    panel_car.render()
    car_grid.render()
    car_widget.render()


def renderSession(delta=0):
    global panel_session
    global session_grid

    panel_session.render()
    session_grid.render()
