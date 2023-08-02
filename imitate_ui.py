import pygame
import os
import pandas as pd
import cv2
from pygame.locals import *

#bgColor=(255, 204, 255)#背景颜色
bgColor=(255,255,220)#背景颜色
btColor=(215, 252, 252)#按钮颜色

rootpath= 'C:/Users/dengl/Desktop/activity/imitation_video_ui/'

def draw_bg(screen,namelist,rankboard=True):#绘制背景
    pygame.display.set_caption("Imitate Show")#标题

    pygame.draw.aaline(screen,(0,0,0),(720,0),(720,800))#绘制分割线
    pygame.draw.aaline(screen,(0,0,0),(960,0),(960,400))#绘制分割线
    pygame.draw.line(screen,(0,0,0),(1200,0),(1200,800),width=3)#绘制分割线
    d=50
    for i in range(1,10):
        pygame.draw.aaline(screen,(0,0,0),(720,i*d),(1200,i*d))#绘制分割线

    #提示信息
    fontch = pygame.font.SysFont('simHei',22)
    txt = fontch.render("输入视频名称", True, (0,0,0))
    screen.blit(txt, (5,22))
    fontch = pygame.font.SysFont('simHei',22)
    txt = fontch.render("最高纪录", True, (0,0,0))
    screen.blit(txt, (1302,14))
    #设置按钮
    pygame.draw.rect(screen, btColor,((150,10),(145, 50)))

    pygame.draw.rect(screen, btColor,((370,10),(135, 50)))
    fontch = pygame.font.SysFont('simHei',22)
    txt = fontch.render("原始视频", True, (0,0,0))
    screen.blit(txt, (393,24))

    pygame.draw.rect(screen, btColor,((5,70),(135, 50)))
    fontch = pygame.font.SysFont('simHei',22)
    txt = fontch.render("点击录像", True, (0,0,0))
    screen.blit(txt, (28,84))

    pygame.draw.rect(screen, btColor,((370,70),(135, 50)))
    fontch = pygame.font.SysFont('simHei',22)
    txt = fontch.render("查看分数", True, (0,0,0))
    screen.blit(txt, (393,84))

    if rankboard:
        b=300
        n=len(namelist)
        records=pd.read_csv(rootpath+'/records.csv',index_col=0,header=0)
        print(records)
        pygame.draw.aaline(screen,(0,0,0),(1200,50),(1200+b,50))#绘制分割线
        pygame.draw.aaline(screen,(0,0,0),(1200+b//2,50),(1200+b//2,50+50*n))#绘制分割线
        fontch = pygame.font.SysFont('simHei',20)
        for i in range(2,n+2):
            pygame.draw.aaline(screen,(0,0,0),(1200,50*i),(1200+b,50*i))#绘制分割线
            txt = fontch.render(namelist[i-2], True, (0,0,0))
            l=len(namelist[i-2])
            screen.blit(txt, (1200+(150-l*10)//2,50*i-35))
            s='{0:.2f}'.format(records[namelist[i-2]][0])
            txt = fontch.render(s, True, (0,0,0))
            l=len(s)
            screen.blit(txt, (1350+(150-l*10)//2,50*i-35))

        path=rootpath+'/scorepic/'+'logo1.png'
        pic = pygame.image.load(path).convert()
        pic = pygame.transform.scale(pic, (200,200))
        screen.blit(pic, (1250,575))
    
    pygame.display.flip()

    return records

def print_records(screen,namelist,records):
    b=300
    n=len(namelist)
    records.to_csv(rootpath+'/records.csv')
    fontch = pygame.font.SysFont('simHei',20)
    for i in range(2,n+2):
        pygame.draw.rect(screen, bgColor,((1200+b//2+1,50*(i-1)+1),(100, 40)))
        s='{0:.2f}'.format(records[namelist[i-2]][0])
        txt = fontch.render(s, True, (0,0,0))
        l=len(s)
        screen.blit(txt, (1350+(150-l*10)//2,50*i-35))
    
    pygame.display.flip()

def print_score(screen,score,name_score,rhythm_score):#打印
    # if rhythm_score>=0:
    #     name_score.append(['节奏',rhythm_score*100])
    fontch = pygame.font.SysFont('simHei',20)
    for i in range(len(name_score)):
        r=i//2
        c=i%2
        #tp=name_score[i][0]+':  '+str(int(name_score[i][1]*100)/100)
        tp='{0}:{1}{2:.2f}'.format(name_score[i][0],' '*(12-len(name_score[i][0])*2),name_score[i][1])
        txt = fontch.render(tp, True, (0,0,0))
        screen.blit(txt, (730+c*240,15+r*50))
    txt = fontch.render('动作得分:  {0:.2f}'.format(score), True, (0,0,0))
    screen.blit(txt, (730,415))
    if rhythm_score>=0:
        txt = fontch.render('(节奏得分:  {0:.2f})'.format(rhythm_score*100), True, (0,0,0))
        screen.blit(txt, (970,415))
    print('节奏分',rhythm_score.mean())

    fontch = pygame.font.SysFont('simHei',30)
    txt=fontch.render('模仿评级', True, (0,0,0))
    screen.blit(txt, (730,625))
    grade=0
    if score>98:
        grade=4
    elif score>95:
        grade=2
    elif score>90:
        grade=3
    elif score>80:
        grade=1
    elif score>70:
        grade=5
    elif score>60:
        grade=6
    else:
        grade=7
    insert_score(screen,str(grade))
    pygame.display.flip()

def print_duration(screen,dur):
    durs='录制时长 {0} 秒'.format(dur)
    fontch = pygame.font.SysFont('simHei',22)
    txt = fontch.render(durs, True, (255,0,0))
    screen.blit(txt, (510,24))

def insert_picture(screen,name,horizontal=700,vertical=660):#插入图片
    path=rootpath+'/origin_pics/'+name+'.jpg'
    piclist=os.listdir(rootpath+'/origin_pics/')
    if not name+'.jpg' in piclist:
        return
    pic = pygame.image.load(path).convert()
    size=pic.get_size()
    
    delta1=vertical-(horizontal/size[0])*size[1] #按横向放大
    delta2=horizontal-(vertical/size[1])*size[0] #按纵向放大
    if delta1<0:
        sizek=vertical/size[1]
    elif delta2<0:
        sizek=horizontal/size[0]
    elif delta1<delta2:
        sizek=horizontal/size[0]
    else:
        sizek=vertical/size[1]
    sizeh=int(size[0]*sizek)
    sizev=int(size[1]*sizek)
    x=int((horizontal-sizeh)/2)+10
    y=int((vertical-sizev)/2)+130
    pic = pygame.transform.scale(pic, (sizeh,sizev))
    screen.blit(pic, (x,y))
    pygame.display.flip()

def insert_score(screen,name,horizontal=300,vertical=300):#插入图片
    path=rootpath+'\\scorepic\\'+name+'.png'
    pic = pygame.image.load(path).convert()
    size=pic.get_size()
    
    delta1=vertical-(horizontal/size[0])*size[1] #按横向放大
    delta2=horizontal-(vertical/size[1])*size[0] #按纵向放大
    if delta1<0:
        sizek=vertical/size[1]
    elif delta2<0:
        sizek=horizontal/size[0]
    elif delta1<delta2:
        sizek=horizontal/size[0]
    else:
        sizek=vertical/size[1]
    sizeh=int(size[0]*sizek)
    sizev=int(size[1]*sizek)
    x=int((horizontal-sizeh)/2)+875
    y=int((vertical-sizev)/2)+475
    pic = pygame.transform.scale(pic, (sizeh,sizev))
    screen.blit(pic, (x,y))
    pygame.display.flip()

def insert_video(name): #插入视频
    video = cv2.VideoCapture(name)

    # 获得码率及尺寸
    fps = video.get(cv2.CAP_PROP_FPS)
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fNUMS = video.get(cv2.CAP_PROP_FRAME_COUNT)

    # 读帧
    success, frame = video.read()
    while success:
        #frame = cv2.resize(frame, (960, 540)) # 根据视频帧大小进行缩放
        cv2.imshow('Video Preview', frame)  # 显示
        cv2.waitKey(int(1000 / int(fps)))  # 设置延迟时间
        success, frame = video.read()  # 获取下一帧
    video.release()
    cv2.destroyAllWindows()

def reset_ui(screen):
    
    pygame.draw.rect(screen, bgColor,((10,130),(700, 660)))
    pygame.draw.rect(screen, bgColor,((720,0),(480, 800)))
    pygame.draw.rect(screen, bgColor,((510,10),(180, 50)))
    pygame.draw.aaline(screen,(0,0,0),(720,0),(720,800))#绘制分割线
    pygame.draw.aaline(screen,(0,0,0),(960,0),(960,400))#绘制分割线
    d=50
    for i in range(1,10):
        pygame.draw.aaline(screen,(0,0,0),(720,i*d),(1200,i*d))#绘制分割线
    pygame.display.flip()

def input_str(screen,mode=0):#输入
    namestr=''
    flag=1
    while flag:
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key == K_BACKSPACE:#退格
                    if len(namestr)<=1:
                        namestr=''
                    else:
                        namestr = namestr[:-1]
                    #更新界面打印
                    if mode==1:#人数
                        pygame.draw.rect(screen, btColor,((150,10),(145, 50)))
                        fontch = pygame.font.SysFont('simHei',18)
                        txt = fontch.render(namestr, True, (0,0,0))
                        screen.blit(txt, (155,25))
                        pygame.display.flip()
                    elif mode==2:#起始编号
                        pygame.draw.rect(screen, btColor,((515,10),(145, 50)))
                        fontch = pygame.font.SysFont('simHei',18)
                        txt = fontch.render(namestr, True, (0,0,0))
                        screen.blit(txt, (520,252))
                        pygame.display.flip()
                elif event.key==K_RETURN:#回车
                    flag=0
                    if mode==1:
                        pygame.draw.rect(screen, btColor,((150,10),(145, 50)))
                        pygame.display.flip()
                    elif mode==2:
                        pygame.draw.rect(screen, btColor,((515,10),(145, 50)))
                        pygame.display.flip()
                    break
                else:#输入
                    namestr+=event.unicode
                    if mode==1:#人数
                        pygame.draw.rect(screen, btColor,((150,10),(145, 50)))
                        fontch = pygame.font.SysFont('simHei',18)
                        txt = fontch.render(namestr, True, (0,0,0))
                        screen.blit(txt, (155,25))
                        pygame.display.flip()
                    elif mode==2:#起始编号
                        pygame.draw.rect(screen, btColor,((515,10),(145, 50)))
                        fontch = pygame.font.SysFont('simHei',18)
                        txt = fontch.render(namestr, True, (0,0,0))
                        screen.blit(txt, (520,25))
                        pygame.display.flip()

    return namestr
