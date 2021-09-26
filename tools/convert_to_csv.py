import xml.etree.ElementTree
import os

# python src/tools/convert_to_csv.py

# balanced weather conditions
VAL_SETS = ['MVI_40204', 'MVI_39861', 'MVI_63521', 'MVI_20011', 'MVI_40244', 'MVI_40992', 'MVI_20051']


# 7个验证集：多云 夜晚 雨天 晴天 多云 夜晚 晴天


def this_is_a_function(annotation_source, image_source, csv_name, set):
    detections = []
    for annotation_file in os.listdir(annotation_source):
        xml_file = xml.etree.ElementTree.parse(os.path.join(annotation_source, annotation_file)).getroot()

        sequence = xml_file.attrib['name']

        for frame in xml_file:
            if frame.tag == 'frame':
                frame_num = frame.attrib['num']

                # decimate training set
                # if int(frame_num) % 10 != 0:  # and set != 'test'
                #     continue
                # 划分数据集修改在main函数中设置
                # split val / training
                if (set == 'val' and sequence not in VAL_SETS) or (set != 'val' and sequence in VAL_SETS):
                    continue

                # 构建图片路径
                file_name = os.path.join(image_source, sequence, 'img' + frame_num.zfill(5) + '.jpg')

                target_list = frame[0]
                for target in target_list:
                    if target.tag == 'target':
                        box = target[0]
                        x1, y1 = int(round(float(box.attrib['left']))), int(round(float(box.attrib['top'])))
                        x2, y2 = x1 + int(round(float(box.attrib['width']))), y1 + int(
                            round(float(box.attrib['height'])))

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

                        classes = target[1].attrib['vehicle_type']  # 'object'  #

                        detections.append((file_name, x1, y1, x2, y2, classes))

    the_file = open(csv_name, 'w')
    for detection in detections:
        print(str(detection)[1:-1].translate(str.maketrans('', '', '\' ')), file=the_file)
    print("{} Finished！".format(csv_name))


# this_is_a_function('/home/lxz-2/CZ/project/CenterNet/data/UA-Detrac/DETRAC-Train-Annotations-XML',
#                    '/home/lxz-2/CZ/project/CenterNet/data/UA-Detrac/train',
#                    '/home/lxz-2/CZ/project/CenterNet/data/UA-Detrac/train10.csv',
#                    set='train')
#
this_is_a_function('/home/lxz-2/CZ/project/CenterNet/data/UA-Detrac/DETRAC-Train-Annotations-XML',
                   '/home/lxz-2/CZ/project/CenterNet/data/UA-Detrac/train',
                   '/home/lxz-2/CZ/project/CenterNet/data/UA-Detrac/val_all.csv',
                   set='val')
#
# this_is_a_function('/home/lxz-2/CZ/project/CenterNet/data/UA-Detrac/DETRAC-Test-Annotations-XML',
#                    '/home/lxz-2/CZ/project/CenterNet/data/UA-Detrac/test',
#                    '/home/lxz-2/CZ/project/CenterNet/data/UA-Detrac/test10.csv',
#                    set='test')

# this_is_a_function('/home/lxz-2/CZ/project/CenterNet/data/UA-Detrac/DETRAC-Train-Annotations-XML',
#                    '/home/lxz-2/CZ/project/CenterNet/data/UA-Detrac/train',
#                    '/home/lxz-2/CZ/project/CenterNet/data/UA-Detrac/train10all.csv',
#                    set='train')
