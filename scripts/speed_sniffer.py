#!/usr/bin/env python3
import rospy, os, sys, rospkg, time
from math import sqrt
from sound_play.msg import SoundRequest
from geometry_msgs.msg import Twist
from sound_play.libsoundplay import SoundClient

first_sec=time.time()
player_dic={'Moving':[first_sec, True, 0], 'Maximum speed':[first_sec, True,0]} # last call time, speed was zero, playing recording number

def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass

def callback(data):
    global player
    speeds=[data.linear.x, data.linear.y, data.linear.z]
    i=sqrt(data.linear.x**2 + data.linear.y**2 + data.linear.z**2)
    if i!=0:
        print(abs(i), player_dic['Maximum speed'][1], time.time()-player_dic['Maximum speed'][0])
        
        if player_dic['Moving'][1] and (time.time()-player_dic['Moving'][0]>10):
            if player_dic['Moving'][2]<2:
                if player_dic['Moving'][2]==0:
                    player("Moving.ogg")
                if player_dic['Moving'][2]==1:
                    player("Rolling_out.ogg")
                player_dic['Moving'][2]+=1
            else:
                player_dic['Moving'][2]=0
                player("Engaging.ogg")
            
            player_dic['Moving'][0]=time.time()

        if i>=3 and player_dic['Maximum speed'][1] and (time.time()-player_dic['Maximum speed'][0]>5):
            player("Maximum_speed_achieved.ogg")
            player_dic['Maximum speed'][0]=time.time()

        player_dic['Moving'][2]=False
        player_dic['Maximum speed'][2]=False

    else:
        player_dic['Moving'][2]=True
        player_dic['Maximum speed'][2]=True

def player(melody_name):
    global to_files, soundhandle
    soundhandle.stopAll()
    soundhandle.playWave(to_files + melody_name)
    sleep(2)



if __name__ == '__main__':
    rospy.init_node('soundplay_test', anonymous = True)
    global soundhandle
    soundhandle = SoundClient()

    rospy.sleep(1)

    soundhandle.stopAll()
    global to_files
    rospack = rospkg.RosPack()
    to_files=rospack.get_path('music_box')+'/audio/'
    sleep(2)
    rospy.Subscriber("cmd_vel", Twist, callback)
    rospy.spin()
