#!/usr/bin/python

from __future__ import print_function
import rospy
import rospkg
import std_msgs
import os

from jrk_motor_service.srv import JrkCmd, JrkCmdResponse, JrkCmdRequest

max_bound = 0.27
exe_path = ''
def handle_jrk_srv(req):
    
    target = int(round((-req.target_value*max_bound) * 2047 + 2048))
    if target > 4096:
        target = 4095
    if target < 0:
        target = 0
    p = os.system(exe_path + ' --target ' + str(target))
    print ('request target:', req.target_value, 'raw_data:', target, 'return:', p)
    res = JrkCmdResponse()
    res.is_succeed = True

    return res
	

if __name__ == "__main__":
    rospy.init_node('jrk_server')
    rospack = rospkg.RosPack()
    package_path = rospack.get_path('jrk_motor_service')
    bin_path = package_path + '/bin/'
    exe_path = bin_path + 'JrkCmd'
    s = rospy.Service('/jrk_cmd', JrkCmd, handle_jrk_srv)
    print (os.system(exe_path + ' --target 2048'))
    print (os.system(exe_path + ' --run'))
    print ("Ready to set target.")
    rospy.spin()
    print (os.system(exe_path + ' --stop'))