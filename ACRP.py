from ACRPlib.ac_widget import *

APP = None
APP_X = 0
APP_Y = 0
APP_W = 0
APP_H = 0

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
    global panel_main, panel_standing, panel_time, panel_car, panel_player, main_widget
    global APP, APP_X, APP_Y

    init()

    panel_main = ACApp("ACRP", 0, 0, 300, 100).hideDecoration()
    panel_standing = ACApp("ACRP Standings", 0, 0, 300, 100).hideDecoration()
    panel_time = ACApp("ACRP Times", 0, 0, 300, 200).hideDecoration()
    panel_car = ACApp("ACRP Car", 0, 0, 200, 300).hideDecoration()
    panel_player = ACApp("ACRP Player", 0, 0, 300, 100).hideDecoration()
    main_widget = ACMainWidget(panel_main)

    panel_main.background_color = BLACK
    panel_main.background_opacity = 1
    panel_standing.background_color = BLACK
    panel_standing.background_opacity = 1
    panel_time.background_color = BLACK
    panel_time.background_opacity = 1
    panel_car.background_color = BLACK
    panel_car.background_opacity = 1
    panel_player.background_color = BLACK
    panel_player.background_opacity = 1

    guiMain()
    guiStanding()
    guiTimes()
    guiCar()
    guiPlayer()

    panel_main.render_callback = renderMain
    panel_standing.render_callback = renderStanding
    panel_time.render_callback = renderTime
    panel_car.render_callback = renderCar
    panel_player.render_callback = renderPlayer

    return "ACRP"


def acUpdate(delta):
    global panel_main, panel_standing, panel_time, panel_car, panel_player, main_widget

    panel_main.update()
    panel_standing.update()
    panel_time.update()
    panel_car.update()
    panel_player.update()

    if panel_standing.position_changed:
        main_widget.dettach(panel_standing)

    if not panel_standing.attached:
        if rectIntersect(panel_main.pos, panel_main.size, panel_standing.pos, panel_standing.size):
            main_widget.attach(panel_standing)

    updateMain()
    updateStanding()
    updateTimes()
    updateCar()
    updatePlayer()


def acRender(delta):
    global panel_main, panel_standing, panel_time, panel_car, panel_player

    panel_main.render()
    panel_standing.render()
    panel_time.render()
    panel_car.render()
    panel_player.render()

    renderMain()
    renderStanding()
    renderTime()
    renderCar()
    renderPlayer()


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
    global time_grid, delta_widget, delta_label, current_sectors, current, last_sectors, last, best
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
    current_sector_num = 0
    current_sector_value = 0
    current_sector_text = ""

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


def guiCar():
    global car_grid, panel_car
    global tyre_FL, tyre_FR, tyre_RL, tyre_RR

    car_grid = ACGrid(panel_car, 5, 5)

    tyre_FL = ACTyreWidget(0, panel_car)
    tyre_FR = ACTyreWidget(1, panel_car, True)
    tyre_RL = ACTyreWidget(2, panel_car)
    tyre_RR = ACTyreWidget(3, panel_car, True)

    car_grid.addWidget(tyre_FL, 0, 0, 2, 2)
    car_grid.addWidget(tyre_FR, 0, 3, 2, 2)
    car_grid.addWidget(tyre_RL, 3, 0, 2, 2)
    car_grid.addWidget(tyre_RR, 3, 3, 2, 2)

    # tyre_FL.init()
    # tyre_FR.init()
    # tyre_RL.init()
    # tyre_RR.init()


def guiPlayer():
    global panel_player
    global player_grid, player_name, session_info, session_time, track_info

    player_grid = ACGrid(panel_player, 4, 3)
    player_name = ACLabel("", panel_player)
    session_info = ACLabel("", panel_player)
    session_time = ACLabel("", panel_player)
    track_info = ACLabel("", panel_player)

    player_grid.addWidget(player_name, 0, 0, 4, 1)
    player_grid.addWidget(session_info, 0, 1, 2, 1)
    player_grid.addWidget(session_time, 2, 1, 2, 1)
    player_grid.addWidget(track_info, 0, 2, 2, 1)


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

    if rpm_widget.rpm_rel >= 0.96:
        main_grid.background_color = YELLOW
    else:
        main_grid.background_color = TRANSPARENT

    main_grid.update()


def updateStanding(delta=0):
    global lap, position, next_car, prev_car

    lap.text = "Lap: " + str(ACLAP.getLap()) + "/" + str(ACLAP.getLaps())
    position.text = "Pos: " + str(ACCAR.getPosition()) + "/" + str(ACSESSION.getCarsCount())
    next_car.text = "Next: " + ACCAR.getNextCarDiff()
    prev_car.text = "Prev: " + ACCAR.getPrevCarDiff()


def updateTimes(delta=0):
    global time_grid, delta_widget, delta_label, current_sectors, current, last_sectors, last, best
    global current_sector_num, current_sector_value, current_sector_text, current_sector

    delta_widget.update()

    delta_label.text = ACLAP.getLapDelta()
    delta_label.text_color = delta_widget.delta_color

    split = ACLAP.getSplit()
    if current_sector_value != split and split != '':
        CONSOLE("change " + str(split))
        current_sector_value = split
        current_sector_text += current_sector_value + " | "
        current_sector_num += 1

        if current_sector_num == ACLAP.getSectors() + 1:
            CONSOLE("reset " + str(split))
            current_sector_num = 0
            current_sector_text = ""
        current_sector.text = current_sector_text

    current.text = "CUR:" + ACLAP.getCurrentLap()
    if ACLAP.getLapDeltaTime() < 0:
        current.text_color = GOOD
    if ACLAP.getLapDeltaTime() > 0:
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


def updateCar(delta=0):
    global car_grid

    car_grid.update()


def updatePlayer(delta=0):
    global player_grid, player_name, session_info, session_time, track_info

    if ACCAR.isAIDriven():
        player_name.text = ACPLAYER.getPlayerNickname() + " [" + ACSESSION.getCarName() + "] (AI)"
    else:
        player_name.text = ACPLAYER.getPlayerNickname() + " [" + ACSESSION.getCarName() + "]"

    session_info.text = ACSESSION.getSessionTypeName() + " (" + ACSESSION.getSessionStatusName() + ")"
    session_time.text = ACSESSION.getRaceTimeLeftFormated()
    track_info.text = str(ACSESSION.getTrackName()) + "[" + str(ACSESSION.getTrackConfiguration()) + "] " + str(ACSESSION.getTrackLengthFormated())


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

    panel_standing.render()


def renderTime(delta=0):
    global panel_time
    global delta_widget

    panel_time.render()
    delta_widget.render()


def renderCar(delta=0):
    global panel_car
    global car_grid

    panel_car.render()
    car_grid.render()


def renderPlayer(delta=0):
    global panel_player

    panel_player.render()
