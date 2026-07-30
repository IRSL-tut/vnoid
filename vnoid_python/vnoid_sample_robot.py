import os
exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())

class VnoidSampleRobot(ru.ImportedRobotModel):
    def __init__(self, robot=None, item=True, world=False, **kwargs):
        super().__init__(robot=robot, item=item, world=world, **kwargs)
    def _init_ending(self, **kwargs): ## override
        self.registerEndEffector('lleg', ## end-effector
                                 'L_FOOT_R', ## tip-link
                                 tip_link_to_eef = coordinates(fv(0, 0, -0.05)),
                                 joint_tuples = (('L_UPPERLEG_Y',  'hip-y'),
                                                 ('L_UPPERLEG_R',  'hip-r'),
                                                 ('L_UPPERLEG_P',  'hip-p'),
                                                 ('L_LOWERLEG_P',  'knee-p'),
                                                 ('L_FOOT_P',      'ankle-p'),
                                                 ('L_FOOT_R',      'ankle-r'),
                                                 )
                                 )
        self.registerEndEffector('rleg', ## end-effector
                                 'R_FOOT_R', ## tip-link
                                 tip_link_to_eef = coordinates(fv(0, 0, -0.05)),
                                 joint_tuples = (('R_UPPERLEG_Y', 'hip-y'),
                                                 ('R_UPPERLEG_R', 'hip-r'),
                                                 ('R_UPPERLEG_P', 'hip-p'),
                                                 ('R_LOWERLEG_P', 'knee-p'),
                                                 ('R_FOOT_P',     'ankle-p'),
                                                 ('R_FOOT_R',     'ankle-r'),
                                                 )
                                 )
        self.registerEndEffector('larm', ## end-effector
                                 'L_HAND_R', ## tip-link
                                 tip_link_to_eef = coordinates(fv(0, 0, -0.12)),
                                 joint_tuples = (('L_UPPERARM_P', 'shoulder-p'),
                                                 ('L_UPPERARM_R', 'shoulder-r'),
                                                 ('L_UPPERARM_Y', 'shoulder-y'),
                                                 ('L_LOWERARM_P', 'elbow-p'),
                                                 ('L_LOWERARM_Y', 'wrist-y'),
                                                 ('L_HAND_P',     'wrist-p'),
                                                 ('L_HAND_R',     'wrist-r'),
                                                 )
                                 )
        self.registerEndEffector('rarm', ## end-effector
                                 'R_HAND_R', ## tip-link
                                 tip_link_to_eef = coordinates(fv(0, 0, -0.12)),
                                 joint_tuples = (('R_UPPERARM_P', 'shoulder-p'),
                                                 ('R_UPPERARM_R', 'shoulder-r'),
                                                 ('R_UPPERARM_Y', 'shoulder-y'),
                                                 ('R_LOWERARM_P', 'elbow-p'),
                                                 ('R_LOWERARM_Y', 'wrist-y'),
                                                 ('R_HAND_P',     'wrist-p'),
                                                 ('R_HAND_R',     'wrist-r'),
                                                 )
                                 )
        self.registerNamedPose('default', ## CoM = 0, 0, xxx
                               [0, 0,
                                0, 0,
                                0.48664308, -1.1411487 ,  0.88348299, -1.3961557 , -1.33181124,  0.19606474, -0.16294286,
                                0.48664308,  1.1411487 , -0.88348299, -1.3961557 ,  1.33181124,  0.19606474,  0.16294286,
                                0, 0, -0.6005, 1.011, -0.4105, 0,
                                0, 0, -0.6005, 1.011, -0.4105, 0,
                                ],
                               ru.make_coordinates( {'pos': [0.0, 0.0, 0.764285 ]} )
                               )

VnoidSampleRobot.model_file = f'{os.path.dirname(__file__)}/../model/sample_robot/sample_robot_ver2.body'

robot_class = VnoidSampleRobot

### makeRobot(robot=None, **kwargs):
def makeRobot(robot=None, item=True, world=True, **kwargs):
    return robot_class(robot, item=item, world=world, **kwargs)
