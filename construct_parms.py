import numpy as np
from solver_equation import closestDistanceBetweenLines
from copy import deepcopy
import math

def read_from_configure_file(file_dir='config.txt'):
#从配置文件中读取数据
    comment=['#','[',';']
    with open(file_dir,'r',encoding='utf-8') as f:
        content=f.readlines()
        content=[c for c in content if c[0] not in comment]
        content=[c.strip() for c in content if c!='\n']
        content=[c.strip('\n').split('=') for c in content]
        print(content)
    var=dict()
#gp,gs  是用分数给出的，不能全读成float型
    for key,num in content:
        var[key]=num
    print(var)
    return var

var=read_from_configure_file('config.txt')
N=int(var['N'])
#架构高度Hjg
Hjg=float(var['Hjg'])
#杆塔呼高Hgt
Hgt=float(var['Hgt'])
#架构挂点间距D_hook
Dh=float(var['Dh'])
#（双回）杆塔中下相间距D_medium_bottom
Dmb=float(var['Dmb'])
#（双回）杆塔中上相间距D_medium_top
Dmt=float(var['Dmt'])
#（单回）杆塔中下间距D_top_bottom
Dtb=float(var['Dtb'])
#（双回）杆塔下横担长度L_bottom，横担方向在y轴正方向为正，负方向为负
#（单回）杆塔下横担长度，表示y轴正方向
Lb=float(var['Lb'])
#（单回）杆塔下横担长度L_bottom，y轴负方向侧
Lb1=float(var['Lb1'])
#杆塔中横担长度L_medium
Lm=float(var['Lm'])
#杆塔下横担长度L_top
Lt=float(var['Lt'])
#杆塔中心距架构中间相水平距离L_hor(x轴方向距离)
Lh=float(var['Lh'])
#杆塔中心距架构中间相垂直距离L_vert
Lv=float(var['Lv'])
#杆塔横担方向与架构平面夹角th,由角度转为弧度
th=float(var['th'])/180*math.pi

#以杆塔中心到架构平面的垂线为x轴，正方向为由架构指向杆塔
#以架构挂点所在直线为y轴，正方向为面向架构方向自右向左
#以竖直向上为z轴及正方向

#匹配方法，架构自右向左（即沿y轴正方向）分别编号0,1,2
#对于双回杆塔，杆塔自下向上（沿z轴正方向）分别编号0,1,2
#对于单回塔，杆塔下横担y轴负向侧为0，正向侧为1，上横担挂点为2
#根据连接点排布，分别在connect_seq_jg与connect_seq_gt中填入对应编号
#比如connect_seq_jg[2,1,0] & connect_seq_gt[0,1,2]代表最左边架构挂点接下相，中间挂点接中相
connect_seq_jg=var['connect_seq_jg'].split(',')
connect_seq_jg=[int(i) for i in connect_seq_jg]
connect_seq_gt=var['connect_seq_gt'].split(',')
connect_seq_gt=[int(i) for i in connect_seq_gt]
# print(connect_seq_jg)


points_down_to_up=[]
points_right_to_left=[]
if(N==2):
    #下横担挂点坐标
    point_gt_bottom=np.array([Lv-Lb*math.sin(th),Lb*math.cos(th),Hgt])
    #中横担挂点坐标
    point_gt_medium=np.array([Lv-Lm*math.sin(th),Lm*math.cos(th),Hgt+Dmb])
    #上横担挂点坐标
    point_gt_top=np.array([Lv-Lt*math.sin(th),Lt*math.cos(th),Hgt+Dmb+Dmt])
if(N==1):
    #下横担0号（y轴负方向）挂点坐标
    point_gt_bottom=np.array([Lv+Lb1*math.sin(th),Lb1*math.cos(th),Hgt])
    #下横担1号（y轴正方向）挂点坐标
    point_gt_medium=np.array([Lv-Lb*math.sin(th),Lb*math.cos(th),Hgt])
    #上横担挂点坐标
    point_gt_top=np.array([Lv-Lt*math.sin(th),Lt*math.cos(th),Hgt+Dtb])
   

#架构最右侧挂点坐标,y坐标最小侧
point_jg_right=np.array([0,Lh-Dh,Hjg])
#架构中间挂点坐标
point_jg_medium=np.array([0,Lh,Hjg])
#架构最左侧挂点坐标
point_jg_left=np.array([0,Lh+Dh,Hjg])

#双回塔单侧导线自下而上排列
if (N==2) :
    points_down_to_up.append(point_gt_bottom)
    points_down_to_up.append(point_gt_medium)
    points_down_to_up.append(point_gt_top)
#单回塔导线自下而上，自y轴负向——>正向
if (N==1) :
    points_down_to_up.append(point_gt_bottom)
    points_down_to_up.append(point_gt_medium)
    points_down_to_up.append(point_gt_top)

#架构自右向左排列，y轴负向——>正向
points_right_to_left.append(point_jg_right)
points_right_to_left.append(point_jg_medium)
points_right_to_left.append(point_jg_left)

lines=[]
for i,j in zip(connect_seq_jg,connect_seq_gt):
    lines.append([points_right_to_left[i],points_down_to_up[j]])

line0=lines[0]
line1=lines[1]
line2=lines[2]

# print(line0)
# print(line1)
# print(line2)


line_to_line=[]
line_to_line.append(line0+line1)
line_to_line.append(line0+line2)
line_to_line.append(line1+line2)

print(line_to_line)

def cal():
    import csv
    with open('output_straight.csv','w') as f:
        writer=csv.writer(f)
        writer.writerow(['距离','A点坐标','B点坐标'])
        for i in line_to_line:
        #print(i)
            writer.writerow(closestDistanceBetweenLines(*i))
            print(closestDistanceBetweenLines(*i))

cal()