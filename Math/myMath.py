import math
import cv2
import numpy as np


# 좌표 그리
def draw_point(src, pt, bgr):
    # 좌표 출력
    cv2.rectangle(src, pt, pt, bgr, 3)


# 각도 변환
def rotate_pt(degree, pt):
    x = pt[0]
    y = pt[1]

    rad = degree * (math.pi / 180.0)
    nx = round(math.cos(rad) * x - math.sin(rad) * y)
    ny = round(math.sin(rad) * x + math.cos(rad) * y)
    pt = (nx, ny)
    return pt


# 이미지 생성
img = np.zeros((512, 512, 3), np.uint8)

# 원점
org_pt = (256, 256)
draw_point(img, org_pt, (255, 255, 0))

# 대상좌표
target_pt = [100, 100]

# 좌표 목록
points = []

# 각도 변경
for angle in range(0, 360, 3):
    pt = rotate_pt(angle, target_pt)
    pt_with_org = (pt[0] + org_pt[0], pt[1] + org_pt[1])
    points.append(pt_with_org)
    print('angle :', angle, pt_with_org)

# 좌표 그리기
for point in points:
    draw_point(img, point, (0,0,255))

# 이미지 출력
cv2.imshow('img', img)
cv2.waitKey()
