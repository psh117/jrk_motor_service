#!/usr/bin/python

from __future__ import print_function
import rospy
import rospkg
import std_msgs
import os

from jrk_motor_service.srv import JrkCmd, JrkCmdResponse, JrkCmdRequest

max_bound = 1.0
exe_path = ''

name_serial_dict = {'right_long' : '00281975', 'top_long': '00296377', 'top_short':'00282035'}
def handle_jrk_srv(req):
    if req.name == '':
        req.name = 'right_long'
    seiral = name_serial_dict[req.name]
    target = int(round((req.target_value*max_bound) * 2047 + 2048))
    if target > 4096:
        target = 4095
    if target < 0:
        target = 0
    p = os.system(exe_path + ' --target ' + str(target) + ' -d ' + serial)
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
    for name in name_serial_dict:
        serial = name_serial_dict[name]
        print (os.system(exe_path + ' --target 2048 -d ' + serial))
        print (os.system(exe_path + ' --run -d ' + serial))
    print ("Ready to set target.")
    rospy.spin()
    for name in name_serial_dict:
        serial = name_serial_dict[name]
        print (os.system(exe_path + ' --stop -d ' + serial))