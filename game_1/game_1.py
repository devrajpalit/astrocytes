from utils import (  # KINECT
    KINECT,
    KINECT_EVENT_STREAM,
    KINECT_FRAME_SIZE,
    NEW_BODY_FRAME_EVENT,
    NEW_BODY_INDEX_FRAME_EVENT)
from utils import (  # PYGAME
    render_player,
    SCREEN,
    SCREEN_SIZE,
    Size)

from math import atan2, degrees, pi
from pykinect2 import PyKinectV2
import pygame
import random


class Game_1:
    def __init__(self):
        self.bg = pygame.image.load('game_1/game_1.jpg')
        self.body_frame = None
        self.body_index_frame = None
        self.solved = True
        self.time_angles = None
        self.threshold = 5  # in degrees

        self.player_size = Size(SCREEN_SIZE.W / 3, SCREEN_SIZE.H / 3)

        KINECT_EVENT_STREAM.subscribe(self.event_handler)

    def event_handler(self, e):
        if e.type == NEW_BODY_FRAME_EVENT:
            self.body_frame = e.body_frame
        elif e.type == NEW_BODY_INDEX_FRAME_EVENT:
            self.body_index_frame = e.body_index_frame

    def generate_arm_angles(self):
        for body in self.body_frame.bodies:
            if not body.is_tracked:
                continue
            joints = body.joints

            arm_angles = []
            for side in ['Left', 'Right']:
                joint0 = eval('PyKinectV2.JointType_Shoulder%s' % (side))
                joint1 = eval('PyKinectV2.JointType_Hand%s' % (side))

                joint0State = joints[joint0].TrackingState
                joint1State = joints[joint1].TrackingState
                jointPoints = KINECT.body_joints_to_color_space(joints)

                (x1, y1) = jointPoints[joint0].x, jointPoints[joint0].y
                (x2, y2) = jointPoints[joint1].x, jointPoints[joint1].y
                dx = x1 - x2
                dy = y1 - y2
                rads = atan2(dy, dx)
                rads = rads % (2 * pi)
                degs = degrees(rads)
                if degs > 180:
                    degs = 360 - degs
                arm_angles.append(degs)
            return arm_angles

    def generate_time_angles(self):
        (hour, minute) = self.generate_time()

        hour_step = 360 / 12
        minute_step = 360 / 60

        hour_angle = hour_step * hour
        minute_angle = minute_step * minute

        if hour_angle > 180:
            hour_angle = 360 - hour_angle
        if minute_angle > 180:
            minute_angle = 360 - minute_angle

        return (hour_angle, minute_angle)

    def generate_time(self):
        hours = [(1 + i) for i in range(12)]
        minutes = [i for i in range(0, 60, 15)]

        hour = random.sample(hours, 1)[0]
        minute = random.sample(minutes, 1)[0]

        print (hour, minute)
        return (hour, minute)

    def render(self):
        SCREEN.blit(pygame.transform.scale(self.bg, (SCREEN_SIZE.W, SCREEN_SIZE.H)), (0, 0))

        if self.solved is True:
            self.solved = False
            self.time_angles = self.generate_time_angles()

        if self.body_index_frame is not None:
            arm_angles = self.generate_arm_angles()
            if arm_angles is not None:
                (hour_angle, minute_angle) = self.time_angles
                (left_arm_angle, rigt_arm_angle) = arm_angles

                print (hour_angle, minute_angle), (left_arm_angle, rigt_arm_angle)
                if ((
                    abs(hour_angle - left_arm_angle) < self.threshold and
                    abs(minute_angle - rigt_arm_angle) < self.threshold
                ) or (
                    abs(hour_angle - rigt_arm_angle) < self.threshold and
                    abs(minute_angle - left_arm_angle) < self.threshold
                )):
                    self.solved = True

            render_player(
                self.body_index_frame,
                self.player_size,
                'bottom right')
