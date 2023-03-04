class Angles:
    def __init__(self, servo_pin):
        print(f"init Angle: {servo_pin}")

    def set_angle(self, angle):
        print(f"angle to set {angle}")


class Measure:
    def __init__(self, trig, echo):
        print(f"init measure {trig}, {echo}")

    def distance_read(self):
        from random import randint
        ran = randint(0, 34)
        # print(f"r_distance: {ran}")
        return ran
