"""
Timer is used for limit person thinking time
and control the flow of time counter in the scene

The amount of peak (total) time is
easy changed by using change constant.py timer variable
# Time Remaining for Player
START_TIME = 200
By: Abel Yohannes
"""

import time
from checkers.constants import START_TIME


class TimerController:

    def __init__(self):

        self.frame_rate = 30
        self.start_time = START_TIME
        self.total_seconds = 4
        self.counter = 0


    def clock_controller(self, screen, player1Turn , player2Turn ,frame_count, font):

        self.counter = int(frame_count // self.frame_rate)
        self.total_seconds = self.start_time - self.counter

        try:
            _myTimeFormat = str(time.strftime("%M:%S", time.gmtime(self.total_seconds)))


            if player1Turn:
                # Blit to the screen
                clock1 = font.render(str(_myTimeFormat), True, (255, 255, 255))
                clockRect1 = clock1.get_rect(midleft=(43, 172))
                clock2 = font.render(str("Wait"), True, (255, 255, 255))
                clockRect2 = clock2.get_rect(midleft=(42, 441))

                if _myTimeFormat == "00:00":
                    clock1 = font.render(str("Wait"), True, (255, 255, 255))
                    clockRect1 = clock1.get_rect(midleft=(43, 172))
                    clock2 = font.render(str(str(START_TIME)+"sec"), True, (255, 255, 255))
                    clockRect2 = clock2.get_rect(midleft=(42, 441))

                    return True

            elif player2Turn:
                clock1 = font.render(str("Wait"), True, (255, 255, 255))
                clockRect1 = clock1.get_rect(midleft=(43, 172))
                clock2 = font.render(str(_myTimeFormat), True, (255, 255, 255))
                clockRect2 = clock2.get_rect(midleft=(42, 441))

                if _myTimeFormat == "00:00":
                    clock1 = font.render(str(str(START_TIME) + "sec"), True, (255, 255, 255))
                    clockRect1 = clock1.get_rect(midleft=(43, 172))
                    clock2 = font.render(str("Wait"), True, (255, 255, 255))
                    clockRect2 = clock2.get_rect(midleft=(42, 441))
                    return True

            else:
                clock1 = font.render(str("Suspend"), True, (255, 255, 255))
                clockRect1 = clock1.get_rect(midleft=(43, 172))
                clock2 = font.render(str("Suspend"), True, (255, 255, 255))
                clockRect2 = clock2.get_rect(midleft=(42, 441))

            screen.blit(clock1, clockRect1)
            screen.blit(clock2, clockRect2)

        except:
            print("Something wont work")

