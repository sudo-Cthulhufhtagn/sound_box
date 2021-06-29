#!/usr/bin/env python3
import rospy, os, sys, rospkg
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass

if __name__ == '__main__':
    rospy.init_node('soundplay_test', anonymous = True)
    soundhandle = SoundClient()

    rospy.sleep(1)

    soundhandle.stopAll()
    
    rospack = rospkg.RosPack()
    to_files=rospack.get_path('sound_box')
    sleep(10)# This delay is needed because when robot wakes up
    rospy.loginfo('Attempt 1')
    soundhandle.playWave(to_files + "/audio/System_initialized.ogg")
    sleep(2)
