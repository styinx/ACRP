import ac
import acsys
import sys
import os
import platform
from math import sin, cos, isinf

if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__) + '/../stdlib64'
else:
    sysdir = os.path.dirname(__file__) + '/../stdlib'

sys.path.insert(0, sysdir)
sys.path.insert(0, os.path.dirname(__file__) + '/../third_party')
os.environ['PATH'] = os.environ['PATH'] + ";."

from third_party.sim_info import info


def formatTime(millis):
    millis = int(millis)
    m = int(millis / 60000)
    s = int((millis % 60000) / 1000)
    ms = millis % 1000

    return "{:02d}:{:02d}.{:03d}".format(m, s, ms)


def formatDistance(meters):
    km = int(meters / 1000)
    m = (meters % 1000) / 10

    return "{:2d}.{:02.0f} km".format(km, m)


def formatGear(gear):
    if gear == 0:
        return "R"
    elif gear == 1:
        return "N"
    else:
        return str(gear - 1)


def LOG(msg):
    ac.log(msg)


def CONSOLE(msg):
    ac.console(msg)


class Color:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a


class Font:
    def __init__(self, font_name, italic, bold):
        if ac.initFont(0, font_name, italic, bold) == -1:
            CONSOLE("Error while loading Font: " + font_name)

        self.font_name = font_name
        self.italic = italic
        self.bold = bold


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GL:
    @staticmethod
    def line(x1, y1, x2, y2, color=Color(1, 1, 1, 1)):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        ac.glBegin(1)
        ac.glVertex2f(x1, y1)
        ac.glVertex2f(x2, y2)
        ac.glEnd()

    @staticmethod
    def rect(x, y, w, h, color=Color(1, 1, 1, 1), filled=True):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        if filled:
            ac.glQuad(x, y, w, h)
        else:
            ac.glBegin(1)
            ac.glVertex2f(x, y)
            ac.glVertex2f(x + w, y)
            ac.glVertex2f(x + w, y)
            ac.glVertex2f(x + w, y + h)
            ac.glVertex2f(x + w, y + h)
            ac.glVertex2f(x, y + h)
            ac.glVertex2f(x, y + h)
            ac.glVertex2f(x, y)
            ac.glEnd()

    @staticmethod
    def circle(x, y, radius, color=Color(1, 1, 1, 1), filled=True):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        if filled:
            ac.glBegin(2)
        else:
            ac.glBegin(1)

        start = 0
        stop = 360
        sample = 36 * radius
        while start <= stop:
            rad1 = start
            rad2 = min(start + 1, stop)
            ac.glVertex2f(x + cos(rad1) * radius, y - sin(rad1) * radius)
            ac.glVertex2f(x + cos(rad2) * radius, y - sin(rad2) * radius)
            if filled:
                ac.glVertex2f(x, y)

            start += sample

        ac.glEnd()

    @staticmethod
    def arc(x, y, radius, start=0, stop=360, color=Color(1, 1, 1, 1), filled=True):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        if filled:
            ac.glBegin(2)
        else:
            ac.glBegin(1)

        sample = (stop - start) / (36 * radius)
        while start <= stop:
            rad1 = start
            rad2 = min(start + 1, stop)
            ac.glVertex2f(x + cos(rad1) * radius, y - sin(rad1) * radius)
            ac.glVertex2f(x + cos(rad2) * radius, y - sin(rad2) * radius)
            if filled:
                ac.glVertex2f(x, y)

            start += sample

        ac.glEnd()

    @staticmethod
    def donut(x, y, radius, width, start=0, stop=360, color=Color(1, 1, 1, 1), filled=True):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        if filled:
            ac.glBegin(2)
        else:
            ac.glBegin(1)

        sample = (stop - start) / (36 * radius)
        while start <= stop:
            rad1 = start
            rad2 = min(start + 1, stop)
            ac.glVertex2f(x + cos(rad1) * radius, y - sin(rad1) * radius)
            ac.glVertex2f(x + cos(rad2) * radius, y - sin(rad2) * radius)
            ac.glVertex2f(x + cos(rad1) * (radius - width), y - sin(rad1) * (radius - width))
            ac.glVertex2f(x + cos(rad2) * (radius - width), y - sin(rad2) * (radius - width))
            if filled:
                ac.glVertex2f(x + cos(rad2) * radius, y - sin(rad2) * radius)
                ac.glVertex2f(x + cos(rad1) * (radius - width), y - sin(rad1) * (radius - width))

            start += sample

        ac.glEnd()

    @staticmethod
    def polygon(points, color=Color(1, 1, 1, 1), filled=True):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        if filled:
            ac.glBegin(2)
        else:
            ac.glBegin(1)

        for i in points:
            if isinstance(i, Point):
                ac.glVertex2f(i.x, i.y)

        ac.glEnd()


ACSYS_PROPERTIES = {
    "SpeedMS": {"id": 0, "optional": False, "result": 1},
    "SpeedMPH": {"id": 1, "optional": False, "result": 1},
    "SpeedKMH": {"id": 2, "optional": False, "result": 1},
    "Gas": {"id": 3, "optional": False, "result": 1},
    "Brake": {"id": 4, "optional": False, "result": 1},
    "Clutch": {"id": 5, "optional": False, "result": 1},
    "Gear": {"id": 6, "optional": False, "result": 1},
    "Aero": {"id": 7, "optional": False, "result": 1},
    "BestLap": {"id": 8, "optional": False, "result": 1},
    "CamberRad": {"id": 9, "optional": False, "result": 4},
    "AccG": {"id": 10, "optional": False, "result": 3},
    "CGHeight": {"id": 11, "optional": False, "result": 1},
    "DriftBestLap": {"id": 12, "optional": False, "result": 1},
    "DriftLastLap": {"id": 13, "optional": False, "result": 1},
    "DriftPoints": {"id": 14, "optional": False, "result": 1},
    "DriveTrainSpeed": {"id": 15, "optional": False, "result": 1},
    "DY": {"id": 16, "optional": False, "result": 4},
    "RPM": {"id": 17, "optional": False, "result": 1},
    "Load": {"id": 18, "optional": False, "result": 4},
    "InstantDrift": {"id": 19, "optional": False, "result": 1},
    "IsDriftInvalid": {"id": 20, "optional": False, "result": 1},
    "IsEngineLimiterOn": {"id": 21, "optional": False, "result": 1},
    "LapCount": {"id": 22, "optional": False, "result": 1},
    "LapInvalidated": {"id": 23, "optional": False, "result": 1},
    "LapTime": {"id": 24, "optional": False, "result": 1},
    "LastFF": {"id": 25, "optional": False, "result": 1},
    "LastLap": {"id": 26, "optional": False, "result": 1},
    "LocalAngularVelocity": {"id": 27, "optional": False, "result": 3},
    "LocalVelocity": {"id": 28, "optional": False, "result": 3},
    "Mz": {"id": 29, "optional": False, "result": 4},
    "NdSlip": {"id": 30, "optional": False, "result": 4},
    "NormalizedSplinePosition": {"id": 31, "optional": False, "result": 1},
    "PerformanceMeter": {"id": 32, "optional": False, "result": 1},
    "SlipAngle": {"id": 33, "optional": False, "result": 4},
    "SlipAngleContactPatch": {"id": 34, "optional": False, "result": 4},
    "SlipRatio": {"id": 35, "optional": False, "result": 4},
    "SpeedTotal": {"id": 36, "optional": False, "result": 3},
    "Steer": {"id": 37, "optional": False, "result": 1},
    "SuspensionTravel": {"id": 38, "optional": False, "result": 4},
    "TurboBoost": {"id": 39, "optional": False, "result": 1},
    "TyreDirtyLevel": {"id": 40, "optional": False, "result": 4},
    "TyreContactNormal": {"id": 41, "optional": False, "result": 3},
    "TyreContactPoint": {"id": 42, "optional": False, "result": 3},
    "TyreHeadingVector": {"id": 43, "optional": False, "result": 1},
    "TyreLoadedRadius": {"id": 44, "optional": False, "result": 4},
    "TyreRadius": {"id": 45, "optional": False, "result": 4},
    "TyreRightVector": {"id": 46, "optional": False, "result": 1},
    "TyreSlip": {"id": 47, "optional": False, "result": 4},
    "TyreSurfaceDef": {"id": 48, "optional": False, "result": 1},
    "TyreVelocity": {"id": 49, "optional": False, "result": 1},
    "Velocity": {"id": 50, "optional": False, "result": 3},
    "WheelAngularSpeed": {"id": 51, "optional": False, "result": 4},
    "WorldPosition": {"id": 52, "optional": False, "result": 3},
    "Caster": {"id": 53, "optional": False, "result": 1},
    "CurrentTyresCoreTemp": {"id": 54, "optional": False, "result": 4},
    "LastTyresTemp": {"id": 55, "optional": False, "result": 3},
    "DynamicPressure": {"id": 56, "optional": False, "result": 4},
    "RideHeight": {"id": 57, "optional": False, "result": 2},
    "ToeInDeg": {"id": 58, "optional": False, "result": 1},
    "CamberDeg": {"id": 59, "optional": False, "result": 4},
    "KersCharge": {"id": 60, "optional": False, "result": 1},
    "KersInput": {"id": 61, "optional": False, "result": 1},
    "DrsAvailable": {"id": 62, "optional": False, "result": 1},
    "DrsEnabled": {"id": 63, "optional": False, "result": 1},
    "EngineBrake": {"id": 64, "optional": False, "result": 1},
    "ERSRecovery": {"id": 65, "optional": False, "result": 1},
    "ERSDelivery": {"id": 66, "optional": False, "result": 1},
    "ERSHeatCharging": {"id": 67, "optional": False, "result": 1},
    "ERSCurrentKJ": {"id": 68, "optional": False, "result": 1},
    "ERSMaxJ": {"id": 69, "optional": False, "result": 1},
    "RaceFinished": {"id": 70, "optional": False, "result": 1},
    "P2PStatus": {"id": 71, "optional": False, "result": 1},
    "P2PActivations": {"id": 72, "optional": False, "result": 1},
}


class ACPLAYER:
    @staticmethod
    def getPlayerNickname():
        return info.static.playerNick

    @staticmethod
    def getPlayerFirstname():
        return info.static.playerName

    @staticmethod
    def getPlayerLastname():
        return info.static.playerSurname

    @staticmethod
    def isIdealLineOn():
        return info.graphics.idealLineOn

    @staticmethod
    def isAutoShifterOn():
        return info.physics.autoShifterOn


class ACSESSION:
    @staticmethod
    def getSessionType():
        return info.graphics.session

    @staticmethod
    def getSessionTypeName():
        session = ACSESSION.getSessionType()

        if session == 0:
            return "Training"
        elif session == 1:
            return "Qualifying"
        elif session == 2:
            return "Race"
        elif session == 3:
            return "Hotlap"
        elif session == 4:
            return "Time Attack"
        elif session == 5:
            return "Drift"
        else:
            return "Drag"

    @staticmethod
    def getSessionCount():
        return info.static.numberOfSessions

    @staticmethod
    def getSessionStatus():
        return info.graphics.status

    @staticmethod
    def getSessionStatusName():
        session = ACSESSION.getSessionStatus()

        if session == 0:
            return "Off"
        elif session == 1:
            return "Replay"
        elif session == 2:
            return "Live"
        else:
            return "Pause"

    @staticmethod
    def getFlagType():
        return info.graphics.flag

    @staticmethod
    def getFlagTypeName():
        flag = ACSESSION.getFlagType()

        if flag == 0:
            return ""
        elif flag == 1:
            return "Blue"
        elif flag == 2:
            return "Yellow"
        elif flag == 3:
            return "Black"
        elif flag == 4:
            return "White"
        elif flag == 5:
            return "Checkered"
        elif flag == 1:
            return "Penalty"

    @staticmethod
    def pitWindowStart():
        return info.static.pitWindowStart

    @staticmethod
    def pitWindowEnd():
        return info.static.pitWindowEnd

    @staticmethod
    def isTimedRace():
        return info.static.isTimedRace

    @staticmethod
    def getRaceTimeLeft():
        return info.graphics.sessionTimeLeft

    @staticmethod
    def getRaceTimeLeftFormated():
        time = ACSESSION.getRaceTimeLeft()

        if not isinf(time):
            if ACSESSION.isTimedRace():
                return "time left: " + formatTime(time)
            elif time > 0:
                return "next session in: " + formatTime(time)
        return ""

    @staticmethod
    def getTrackLength():
        return ac.getTrackLength(0)

    @staticmethod
    def getTrackLengthFormated():
        return formatDistance(ACSESSION.getTrackLength())

    @staticmethod
    def getTrackName():
        return ac.getTrackName(0)

    @staticmethod
    def getTrackConfiguration():
        return ac.getTrackConfiguration(0)

    @staticmethod
    def getCarName():
        return ac.getCarName(0)

    @staticmethod
    def getCarsCount():
        return ac.getCarsCount()

    @staticmethod
    def getWindDirection():
        return info.graphics.windDirection

    @staticmethod
    def getWindSpeed():
        return info.graphics.windSpeed

    @staticmethod
    def getSurfaceGrip():
        return info.graphics.surfaceGrip

    @staticmethod
    def getRoadTemp():
        return info.physics.roadTemp

    @staticmethod
    def getAirTemp():
        return info.physics.airTemp

    @staticmethod
    def getAirDensity():
        return info.physics.airDensity


class ACLAP:
    @staticmethod
    def getLapCount():
        return info.graphics.completedLaps

    @staticmethod
    def getCurrentLapTime(car=0):
        return ac.getCarState(car, acsys.CS.LapTime)

    @staticmethod
    def getCurrentLap(car=0):
        time = ac.getCarState(car, acsys.CS.LapTime)
        if time > 0:
            return formatTime(time)
        else:
            return "00:00.000"

    @staticmethod
    def getLastLapTime(car=0):
        return ac.getCarState(car, acsys.CS.LastLap)

    @staticmethod
    def getLastLap(car=0):
        time = ac.getCarState(car, acsys.CS.LastLap)
        if time > 0:
            return formatTime(time)
        else:
            return "00:00.000"

    @staticmethod
    def getBestLapTime(car=0):
        return ac.getCarState(car, acsys.CS.BestLap)

    @staticmethod
    def getBestLap(car=0):
        time = ac.getCarState(car, acsys.CS.BestLap)
        if time > 0:
            return formatTime(time)
        else:
            return "00:00.000"

    @staticmethod
    def getSectorIndex():
        return info.graphics.currentSectorIndex

    @staticmethod
    def getLastSector():
        return info.graphics.lastSectorTime

    @staticmethod
    def getSectorCount():
        return info.static.sectorCount

    @staticmethod
    def getSplit():
        return info.graphics.split

    @staticmethod
    def getSplits(car=0):
        return ac.getLastSplits(car)

    @staticmethod
    def getLap(car=0):
        return ac.getCarState(car, acsys.CS.LapCount) + 1

    @staticmethod
    def getLapDeltaTime(car=0):
        return ac.getCarState(car, acsys.CS.PerformanceMeter)

    @staticmethod
    def getLapDelta(car=0):
        time = ACLAP.getLapDeltaTime() * 1000
        if time != 0:
            if time < 0:
                return "-" + formatTime(abs(time))
            elif time > 0:
                return "+" + formatTime(abs(time))
        else:
            return "-00:00.000"

    @staticmethod
    def isLapInvalidated(car=0):
        return ac.getCarState(car, acsys.CS.LapInvalidated) or ACCAR.getTyresOut() > 2 or ACCAR.isInPit()

    @staticmethod
    def getLaps():
        if info.graphics.numberOfLaps > 0:
            return info.graphics.numberOfLaps
        else:
            return "-"

    @staticmethod
    def lastSectorTime():
        return info.graphics.lastSectorTime

    @staticmethod
    def getSectors():
        return info.static.sectorCount


class ACCAR:
    @staticmethod
    def getFocusedCar():
        return ac.getFocusedCar()

    @staticmethod
    def getTraveledDistance():
        return info.graphics.distanceTraveled

    @staticmethod
    def getCarDamage(loc=0):
        # 0: Front, 1: Rear, 2: Left, 3: Right, 4:?
        return info.physics.carDamage[loc]

    @staticmethod
    def getPrevCarDiffTimeDist():
        time = 0
        dist = 0
        track_len = ACSESSION.getTrackLength()
        lap = ACLAP.getLap(0)
        pos = ACCAR.getLocation(0)

        for car in range(ACSESSION.getCarsCount()):
            if ACCAR.getPosition(car) == ACCAR.getPosition(0) - 1:
                lap_next = ACLAP.getLap(car)
                pos_next = ACCAR.getLocation(car)

                dist = max(0, (pos_next * track_len + lap_next * track_len) - (pos * track_len + lap * track_len))
                time = max(0.0, dist / max(10.0, ACCAR.getSpeed(0, "ms")))
                break
        return time, dist

    @staticmethod
    def getPrevCarDiff():
        time, dist = ACCAR.getPrevCarDiffTimeDist()
        track_len = ACSESSION.getTrackLength()

        if dist > track_len:
            laps = dist / track_len
            if laps > 1.05:
                return "+{:3.1f}".format(laps) + " Laps"
            elif laps < 1.05:
                return "+{:3.0f}".format(laps) + "   Lap"
        else:
            if time > 60:
                minute = time / 60
                if minute > 1.05:
                    return "+{:3.1f}".format(minute) + " Mins"
                elif minute < 1.05:
                    return "+{:3.0f}".format(minute) + "   Min"
            else:
                return "+" + formatTime(int(time * 1000))

    @staticmethod
    def getNextCarDiffTimeDist():
        time = 0
        dist = 0
        track_len = ACSESSION.getTrackLength()
        lap = ACLAP.getLap(0)
        pos = ACCAR.getLocation(0)

        for car in range(ACSESSION.getCarsCount()):
            if ACCAR.getPosition(car) == ACCAR.getPosition(0) + 1:
                lap_next = ACLAP.getLap(car)
                pos_next = ACCAR.getLocation(car)

                dist = max(0.0, (pos * track_len + lap * track_len) - (pos_next * track_len + lap_next * track_len))
                time = max(0.0, dist / max(10.0, ACCAR.getSpeed(car, "ms")))
                break
        return time, dist

    @staticmethod
    def getNextCarDiff():
        time, dist = ACCAR.getNextCarDiffTimeDist()
        track_len = ACSESSION.getTrackLength()

        if dist > track_len:
            laps = dist / track_len
            if laps > 1:
                return "-{:3.1f}".format(laps) + " Laps"
            else:
                return "-{:3.1f}".format(laps) + "   Lap"
        else:
            if time > 60:
                minute = time / 60
                if minute > 1.05:
                    return "-{:3.1f}".format(minute) + " Mins"
                elif minute < 1.05:
                    return "-{:3.0f}".format(minute) + "   Min"
            else:
                return "-" + formatTime(int(time * 1000))

    @staticmethod
    def getGas():
        return info.physics.gas

    @staticmethod
    def getBrake():
        return info.physics.brake

    @staticmethod
    def hasDRS():
        return info.static.hasDRS

    @staticmethod
    def DRSEnabled():
        return info.physics.drsEnabled

    @staticmethod
    def hasERS():
        return info.static.hasERS

    @staticmethod
    def hasKERS():
        return info.static.hasKERS

    @staticmethod
    def ABS():
        return info.physics.abs

    @staticmethod
    def getSpeed(car=0, unit="kmh"):
        if unit == "kmh":
            return ac.getCarState(car, acsys.CS.SpeedKMH)
        elif unit == "mph":
            return ac.getCarState(car, acsys.CS.SpeedMPH)
        elif unit == "ms":
            return ac.getCarState(car, acsys.CS.SpeedMS)

    @staticmethod
    def getGear(car=0):
        return formatGear(ac.getCarState(car, acsys.CS.Gear))

    @staticmethod
    def getRPMValue(car=0):
        return ac.getCarState(car, acsys.CS.RPM)

    @staticmethod
    def getRPM(car=0):
        return int(ACCAR.getRPMValue(car))

    @staticmethod
    def getRPMMax():
        if info.static.maxRpm:
            return info.static.maxRpm
        else:
            return 8000

    @staticmethod
    def getPosition(car=0):
        return ac.getCarRealTimeLeaderboardPosition(car) + 1

    @staticmethod
    def getLocation(car=0):
        return ac.getCarState(car, acsys.CS.NormalizedSplinePosition)

    @staticmethod
    def getPenaltyTime():
        return info.graphics.penaltyTime

    @staticmethod
    def isPitLimiterOn():
        return info.physics.pitLimiterOn

    @staticmethod
    def mandatoryPitStopDone():
        return info.graphics.mandatoryPitDone

    @staticmethod
    def isInPit(car=0):
        return ACCAR.isInPitLine(car) or ACCAR.isInPitBox(car)

    @staticmethod
    def isInPitLine(car=0):
        return ac.isCarInPitline(car)

    @staticmethod
    def isInPitBox(car=0):
        return ac.isCarInPit(car)

    @staticmethod
    def isAIDriven():
        return info.physics.isAIControlled

    @staticmethod
    def getFuel():
        return info.physics.fuel

    @staticmethod
    def getMaxFuel():
        return info.static.maxFuel

    @staticmethod
    def getTyresOut():
        return info.physics.numberOfTyresOut

    @staticmethod
    def getTyreWearValue(tyre=0):
        # 0: FL, 1: FR, 2: RL, 3: RR
        return info.physics.tyreWear[tyre]

    @staticmethod
    def getTyreWear(tyre=0):
        return (ACCAR.getTyreWearValue(tyre) - 94) * 16.6

    @staticmethod
    def getTyreWearFormated(tyre=0):
        return "{:2.1f}%".format((ACCAR.getTyreWearValue(tyre) - 94) * 16.6)

    @staticmethod
    def getTyreDirtyLevel(tyre=0):
        return info.physics.tyreDirtyLevel[tyre]

    @staticmethod
    def getTyreCompund():
        return info.graphics.tyreCompound

    @staticmethod
    def getTyreCompundSymbol():
        compund = info.graphics.tyreCompound
        if compund == "":
            return ""

    @staticmethod
    def getCarModel():
        return info.static.carModel

    @staticmethod
    def getTyreTemp(tyre=0, loc="m"):
        if loc == "i":
            return info.physics.tyreTempI[tyre]
        elif loc == "m":
            return info.physics.tyreTempM[tyre]
        elif loc == "o":
            return info.physics.tyreTempO[tyre]
        elif loc == "c":
            return info.physics.tyreCoreTemperature[tyre]
        elif loc == "all":
            return [info.physics.tyreTempI[tyre],
                    info.physics.tyreTempM[tyre],
                    info.physics.tyreTempO[tyre],
                    info.physics.tyreCoreTemperature[tyre]]

    @staticmethod
    def getTyreTempFormated(tyre=0, loc="m"):
        return "{:2.1f}°".format(ACCAR.getTyreTemp(tyre, loc))

    @staticmethod
    def getTyrePressure(tyre=0):
        return info.physics.wheelsPressure[tyre]

    @staticmethod
    def getTyrePressureFormated(tyre=0):
        return "{:2.1f}psi".format(ACCAR.getTyrePressure(tyre))

    @staticmethod
    def getBrakeTemperature(tyre=0):
        return info.physics.brakeTemp[tyre]

    @staticmethod
    def getBrakeTemperatureFormated(tyre=0):
        return "{:2.1f}°".format(ACCAR.getBrakeTemperature(tyre))
