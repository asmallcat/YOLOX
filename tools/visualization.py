import cv2
import os
import xml.etree.ElementTree as ET

# name = 'MVI_40742'
name = 'MVI_40864'

annotation_file = '/home/lxz-2/CZ/project/CenterNet/data/UA-Detrac/DETRAC-Test-Annotations-XML/{}.xml'.format(name)
xml_file = ET.parse(annotation_file).getroot()
img_dir = '/home/lxz-2/CZ/project/CenterNet/outputs/{}_all_model'.format(name)
# img_dir = '/home/lxz-2/CZ/project/CenterNet/outputs/{}'.format(name)

num = 0

for frame in xml_file:

    if frame.tag == 'frame':
        frame_num = frame.attrib['num']
        img_file = os.path.join(img_dir, '{}ctdet.png'.format(int(frame_num) - 1))
        img = cv2.imread(img_file)
        target_list = frame[0]
        for target in target_list:
            if target.tag == 'target':
                box = target[0]
                x1, y1 = int(round(float(box.attrib['left']))), int(round(float(box.attrib['top'])))
                x2, y2 = x1 + int(round(float(box.attrib['width']))), y1 + int(round(float(box.attrib['height'])))
                if x1 > x2:
                    temp = x1
                    x1 = x2
                    x2 = temp
                if y1 > y2:
                    temp = y1
                    y1 = y2
                    y2 = temp
                if x1 < 0:
                    x1 = 0
                if x2 > 960:
                    x2 = 960
                if y1 < 0:
                    y1 = 0
                if y2 > 540:
                    y2 = 540

                classes = target[1].attrib['vehicle_type']  # 'object'

                color = (0, 0, 255)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, classes, (x2, y2 - 7), font, 0.5, color, 1)
        cv2.imshow('img', img)
        cv2.waitKey(0)
        # cv2.imwrite(img_file, img)
cv2.destroyAllWindows()
