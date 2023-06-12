import cv2
import math
from classes.Constants import *


def dist1(ax, ay, bx, by):
    return math.sqrt((ax-bx)**2 + (ay-by)**2)


def dist2(a, b):
    return math.sqrt((a['x']-b['x'])**2 + (a['y']-b['y'])**2)


def rounded_rectangle(src, top_left, bottom_right, radius=1, color=255, thickness=1, line_type=cv2.LINE_AA):
    #  corners:
    #  p1 - p2
    #  |     |
    #  p4 - p3
    p1 = top_left
    p2 = (bottom_right[1], top_left[1])
    p3 = (bottom_right[1], bottom_right[0])
    p4 = (top_left[0], bottom_right[0])
    height = abs(bottom_right[0] - top_left[1])

    if radius > 1:
        radius = 1

    corner_radius = int(radius * (height/2))

    if thickness < 0:
        # big rect
        top_left_main_rect = (int(p1[0] + corner_radius), int(p1[1]))
        bottom_right_main_rect = (int(p3[0] - corner_radius), int(p3[1]))

        top_left_rect_left = (p1[0], p1[1] + corner_radius)
        bottom_right_rect_left = (p4[0] + corner_radius, p4[1] - corner_radius)

        top_left_rect_right = (p2[0] - corner_radius, p2[1] + corner_radius)
        bottom_right_rect_right = (p3[0], p3[1] - corner_radius)

        all_rects = [
            [top_left_main_rect, bottom_right_main_rect],
            [top_left_rect_left, bottom_right_rect_left],
            [top_left_rect_right, bottom_right_rect_right]]

        [cv2.rectangle(src, rect[0], rect[1], color, thickness)
         for rect in all_rects]

    # draw straight lines
    cv2.line(src, (p1[0] + corner_radius, p1[1]), (p2[0] -
             corner_radius, p2[1]), color, abs(thickness), line_type)
    cv2.line(src, (p2[0], p2[1] + corner_radius), (p3[0],
             p3[1] - corner_radius), color, abs(thickness), line_type)
    cv2.line(src, (p3[0] - corner_radius, p4[1]), (p4[0] +
             corner_radius, p3[1]), color, abs(thickness), line_type)
    cv2.line(src, (p4[0], p4[1] - corner_radius), (p1[0],
             p1[1] + corner_radius), color, abs(thickness), line_type)

    # draw arcs
    cv2.ellipse(src, (p1[0] + corner_radius, p1[1] + corner_radius),
                (corner_radius, corner_radius), 180.0, 0, 90, color, thickness, line_type)
    cv2.ellipse(src, (p2[0] - corner_radius, p2[1] + corner_radius),
                (corner_radius, corner_radius), 270.0, 0, 90, color, thickness, line_type)
    cv2.ellipse(src, (p3[0] - corner_radius, p3[1] - corner_radius),
                (corner_radius, corner_radius), 0.0, 0, 90,   color, thickness, line_type)
    cv2.ellipse(src, (p4[0] + corner_radius, p4[1] - corner_radius),
                (corner_radius, corner_radius), 90.0, 0, 90,  color, thickness, line_type)
    return src


def overlay_circle(img, loc, r, fill, stroke, alpha=0.6):
    overlay = img.copy()
    cv2.circle(overlay, loc, r, fill, cv2.FILLED, cv2.LINE_AA)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    cv2.circle(img, loc, r, stroke, 1, cv2.LINE_AA)


def overlay_text_circle(img, string, loc, r, alpha=0.6):
    overlay = img.copy()
    cv2.circle(overlay, loc, r, C_BLACK, cv2.FILLED, cv2.LINE_AA)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    cv2.circle(img, loc, r, C_WHITE, 1, cv2.LINE_AA)
    cv2.putText(img, string, (loc[0]-10, loc[1]+7),
                cv2.FONT_HERSHEY_PLAIN, 1, C_YELLOW, 2, cv2.LINE_AA)


def overlay_text_box(img, string, loc, w, h, c, alpha=0.6):
    overlay = img.copy()
    rounded_rectangle(
        overlay, loc, (loc[1]+h, loc[0]+w), 0.1, C_BLACK, cv2.FILLED)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    rounded_rectangle(img, loc, (loc[1]+h, loc[0]+w), 0.1, C_WHITE, 1)
    cv2.putText(img, string, (loc[0]+20, loc[1]+h//2+15),
                cv2.FONT_HERSHEY_PLAIN, 3, c, 2, cv2.LINE_AA)


def text_box(img, string, loc, w, h, r, fill, stroke, size, c):
    rounded_rectangle(img, loc, (loc[1]+h, loc[0]+w), r, fill, cv2.FILLED)
    rounded_rectangle(img, loc, (loc[1]+h, loc[0]+w), r, stroke, 1)
    substr = string[:]
    offset = 0
    thres = 45
    while len(substr) > thres:
        cv2.putText(img, substr[:thres], (loc[0]+10, loc[1]+20+offset),
                    cv2.FONT_HERSHEY_PLAIN, size, c, 1, cv2.LINE_AA)
        substr = substr[thres:]
        offset += 18
    cv2.putText(img, substr, (loc[0]+10, loc[1]+20+offset),
                cv2.FONT_HERSHEY_PLAIN, size, c, 1, cv2.LINE_AA)
