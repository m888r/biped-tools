import math, cv2, time
import numpy as np

GREEN = (0,255,0)
RED = (0,0,255)
BLUE = (255,0,0)
WHITE = (255,255,255)
TEAL = (255,255,0)

WDT,HGT = 640,480
points = list(range(8))
cube_size = 0.8

points[0] = [[-cube_size],[-cube_size],[cube_size]]
points[1] = [[+cube_size],[-cube_size],[cube_size]]
points[2] = [[+cube_size],[+cube_size],[cube_size]]
points[3] = [[-cube_size],[+cube_size],[cube_size]]
points[4] = [[-cube_size],[-cube_size],[-cube_size]]
points[5] = [[+cube_size],[-cube_size],[-cube_size]]
points[6] = [[+cube_size],[+cube_size],[-cube_size]]
points[7] = [[-cube_size],[+cube_size],[-cube_size]]

def draw_line(img, i,j,k,color):
    a,b = k[i],k[j]
    cv2.line(img, (a[0],a[1]),(b[0],b[1]), color, 2)

black = np.zeros(shape=(480,640,3), dtype=np.uint8)
x_angle, y_angle, z_angle = 0,0,0
angle_speed = 120
scale = 600

delta_radian = 0.0157

while True:
    img = np.copy(black)
    projected_points = [j for j in range(len(points))]
    # x_angle += delta_radian
    # y_angle += delta_radian
    # z_angle += delta_radian
    # angle = int(math.degrees(x_angle))
    x_angle = 0;
    y_angle = 0;
    z_angle = 0;
    if x_angle > math.pi*1.99: x_angle = 0
    if y_angle > math.pi*1.99: y_angle = 0
    if z_angle > math.pi*1.99: z_angle = 0

    rotation_x = [
        [1, 0,  0],
        [0, math.cos(x_angle), -math.sin(x_angle)],
        [0, math.sin(x_angle), math.cos(x_angle)]
        ]
    rotation_y = [
        [math.cos(y_angle), 0, -math.sin(y_angle)],
        [0, 1,  0],
        [math.sin(y_angle), 0,  math.cos(y_angle)]
        ]
    rotation_z = [
        [math.cos(z_angle), -math.sin(z_angle), 0],
        [math.sin(z_angle), math.cos(z_angle), 0],
        [0, 0,  1],
        ]
    index = 0
    for point in points:
        rotated_2d = np.matmul(rotation_y, point)
        rotated_2d = np.matmul(rotation_x, rotated_2d)
        rotated_2d = np.matmul(rotation_z, rotated_2d)
        distance = 5
        z = 1/(distance - rotated_2d[2][0])
        projection_matrix = [[z,0,0],[0,z,0]]
        projected_2d = np.matmul(projection_matrix, rotated_2d)
        x = int(projected_2d[0][0] * scale) + WDT//2
        y = int(projected_2d[1][0] * scale) + HGT//2
        projected_points[index] = [x,y]
        cv2.circle(img, (x,y), 5, WHITE, 2)
        cv2.circle(img, (WDT//2, HGT//2), 4, TEAL, cv2.FILLED)
        index += 1

    for m in range(4):
        draw_line(img, m, (m+1)%4, projected_points, GREEN)
        draw_line(img, m+4, (m+1)%4+4, projected_points, RED)
        draw_line(img, m, m+4, projected_points, BLUE)
    
    cv2.imshow("", img)
    time.sleep(1/angle_speed)
    if cv2.waitKey(1) == ord('q'):
        break
