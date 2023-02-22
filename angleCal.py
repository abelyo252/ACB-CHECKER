"""
Real Time Angle Calculator Module
By: Abel Yohannes
Internship Project for jimma university
"""
import math
import numpy as np
from math import sin , cos , tan , acos  , asin , atan
import math
import send
l2 = 1
l3 = 1
l4 = 0.5


def todeg(theta):
    return math.degrees(theta)

def torad(theta):
    return math.radians(theta)


def middlepoint(ye, ze, gamma):
    # Angle is measured in radian
    y3 = ye - (l4 * cos(gamma))
    z3 = ze - (l4 * sin(gamma))
    print("Middle Point : ", y3, z3)
    return y3, z3


def alphac(y3, z3):
    upper = y3 * y3 + z3 * z3 - (l2 * l2 + l3 * l3)
    lower = 2 * l2 * l3
    result = (upper / lower)
    print("alpha result : ", result)

    if result < 0:
        try:
            result = result * -1
            alpha = acos(result)
            alpha = math.pi - alpha

        except:
            print("Point given is not in the workspace !")
            return 0


    else:
        try:
            alpha = acos(result)

        except:
            print("Point given is not in the workspace !")
            return 0

    print("Alpha measured : ", alpha)

    return alpha


def betac(y3, z3, alpha):
    upper = l3 * sin(alpha)
    summer = y3 * y3 + z3 * z3
    lower = math.sqrt(summer)

    result = upper / lower
    if result < 0:
        try:
            result = result * -1
            beta = asin(result)
            beta = beta * -1
        except:
            print("Point given is not in the workspace !")
            return 0


    else:
        try:
            beta = asin(result)
        except:
            print("Point given is not in the workspace !")
            return 0

    print("Beta measured : ", beta)
    return beta


def elbow_up(angle, alpha, beta, gamma):
    theta2_b = angle + beta
    # theta3_b = alpha - math.pi
    theta3_b = -alpha
    theta4_b = gamma - theta3_b - theta2_b



    return theta2_b, theta3_b, theta4_b


def inverse_kinematics(posx , posy, posz, gamma):
    y3, z3 = middlepoint(posy, posz, gamma)
    alpha = alphac(y3, z3)
    beta = betac(y3, z3, alpha)

    angle = atan(z3 / y3)


    theta1 = atan(posy/ posx)
    theta2_b, theta3_b, theta4_b = elbow_up(angle, alpha, beta, gamma)
    return theta1 , theta2_b , theta3_b , theta4_b


def find_angle():
    theta1 , theta2_b , theta3_b , theta4_b  = inverse_kinematics(2.109 ,1.538, 0.06, torad(-70))
    print("Elbow up Theta1 : ", todeg(theta1))
    print("Elbow up Theta2 : ", todeg(theta2_b))
    print("Elbow up Theta3 : ", todeg(theta3_b))
    print("Elbow up Theta4 : ", todeg(theta4_b))
    send.sendAngle(theta1 , theta2_b , theta3_b , theta4_b)


def main():
    find_angle()


if __name__ == "__main__":
    main()


