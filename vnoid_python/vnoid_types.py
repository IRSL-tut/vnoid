exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())
# coordinates

# import numpy as np
# import math
from dataclasses import dataclass
from typing import List
from typing import ClassVar

@dataclass
class Param:
    """歩行パラメータ"""
    com_height: float = 0.7  # CoM の高さ
    T: float = 1.0           # 時定数
    gravity: float = 9.8     #
    def __post_init__(self):
        self.T = math.sqrt( self.com_height/self.gravity )

@dataclass
class Timer:
    """タイマー情報"""
    time: float = 0.0
    count: int  = 0
    dt: float   = 0.001
    def CountUp(self):
        self.count += 1
        self.time += self.dt

@dataclass
class Ground:
    """地面情報"""
    ori: coordinates = None  # 地面の姿勢

    def __post_init__(self):
        if self.ori is None:
            self.ori = coordinates()

###
@dataclass
class Step:
    """1ステップの情報"""
    right: ClassVar[int] = 0
    left:  ClassVar[int] = 1
    # 足の位置と姿勢（右足[0], 左足[1]）
    #foot_pos: np.ndarray = None      # (2, 3) - 足の位置 [right, left]
    #foot_angle: np.ndarray = None    # (2, 3) - roll, pitch, yaw [right, left]
    #foot_ori: list = None            # (2,) - 回転行列 [right, left]
    foot_coords : List[coordinates] = None # [coordinates, coordinates] [right, left]
    # 足の側（0: 右, 1: 左）
    side: int = 0
    # ステップパラメータ
    stride: float  = 0.2  # 前進距離
    sway: float    = 0.0  # 横揺れ
    turn: float    = 0.0  # 回転角度
    spacing: float = 0.2  # 足の間隔
    climb: float   = 0.0  # 階段登り
    # タイミング情報
    duration: float = 0.8  # ステップの継続時間
    tbegin: float   = 0.0  # ステップ開始時刻
    # DCM と ZMP
    dcm: np.ndarray = None  # Divergent Component of Motion
    zmp: np.ndarray = None  # Zero Moment Point
    # その他
    stepping: bool = True   # ステップするか（サポート交換）
    ## dual support
    def __post_init__(self):
        if self.foot_coords is None:
            self.foot_coords = [coordinates(), coordinates()]
        if self.dcm is None:
            self.dcm = np.array([0.0, 0.0, 0.0])
        if self.zmp is None:
            self.zmp = np.array([0.0, 0.0, 0.0])

    def copy(self):
        return Step(side=self.side, stride=self.stride, sway=self.sway, turn=self.turn, spacing=self.spacing,
                    climb=self.climb, duration=self.duration, tbegin=self.tbegin, stepping=self.stepping,
                    foot_coords=[self.foot_coords[0].copy(), self.foot_coords[1].copy()],
                    dcm=np.array(self.dcm), zmp=np.array(self.zmp) )
@dataclass
class Footstep:
    """複数ステップの歩行計画"""
    steps: List[Step] = None
    def __post_init__(self):
        if self.steps is None:
            self.steps = []

@dataclass
class Centroid:
    """重心情報"""
    dcm_ref: np.ndarray = None       # 参考 DCM
    dcm_target: np.ndarray = None    # 目標 DCM
    zmp_ref: np.ndarray = None       # 参考 ZMP
    zmp_target: np.ndarray = None    # 目標 ZMP
    ####
    force_ref:  np.ndarray = None  #/< reference force
    moment_ref: np.ndarray = None  #/< reference moment
    zmp:        np.ndarray = None  #/< current ZMP
    dcm:        np.ndarray = None  #/< DCM (divergent component of motion)
    com_pos: np.ndarray = None     # 目標? CoM
    com_pos_ref: np.ndarray = None # 参考 CoM
    com_vel_ref: np.ndarray = None #/< reference velocity of CoM
    com_acc_ref: np.ndarray = None #/< reference acceleration of CoMxo

    def __post_init__(self):
        if self.dcm_ref is None:
            self.dcm_ref = np.array([0.0, 0.0, 0.0])
        if self.dcm_target is None:
            self.dcm_target = np.array([0.0, 0.0, 0.0])
        if self.zmp_ref is None:
            self.zmp_ref = np.array([0.0, 0.0, 0.0])
        if self.zmp_target is None:
            self.zmp_target = np.array([0.0, 0.0, 0.0])
        if self.com_pos_ref is None:
            self.com_pos_ref = np.array([0.0, 0.0, 0.0])
        if self.com_vel_ref is None:
            self.com_vel_ref = np.array([0.0, 0.0, 0.0])
        if self.com_acc_ref is None:
            self.com_acc_ref = np.array([0.0, 0.0, 0.0])

@dataclass
class Base:
    """ベース（ボディ）情報"""
    #>angle: np.ndarray = None         # 現在の角度 [roll, pitch, yaw]
    #>angle_ref: np.ndarray = None     # 参考角度
    #>ori: R = None                    # 現在の向き
    #>ori_ref: R = None                # 参考向き
    #>pos:        np.ndarray = None #/< position
    #>pos_ref:    np.ndarray = None #/< reference position
    #
    coords: coordinates  = None #
    coords_ref: coordinates = None
    #
    vel:        np.ndarray = None #/< velocity
    vel_ref:    np.ndarray = None #/< reference velocity
    angvel:     np.ndarray = None #/< current angular velocity
    angvel_ref: np.ndarray = None #/< reference angular velocity
    acc:        np.ndarray = None
    acc_ref:    np.ndarray = None #/< reference acceleration
    angacc:     np.ndarray = None
    angacc_ref: np.ndarray = None #/< reference angular acceleration

    def __post_init__(self):
        if self.coords is None:
            self.coords = coordinates()
        if self.coords_ref is None:
            self.coords_ref = coordinates()

@dataclass
class Foot:
    """足の情報"""
    #>pos_ref: np.ndarray = None     # 参考位置
    #>angle_ref: np.ndarray = None   # 参考角度 [roll, pitch, yaw]
    #>ori_ref: R = None              # 参考向き
    coords_ref: coordinates = None #
    contact_ref: bool = False      # 接触フラグ
#>bool        contact;      ///< current contact state (true if foot is in contact with the ground)
#>bool        contact_ref;  ///< reference contact state
#>double      balance;      ///< current balance ratio [0.0, 1.0].  indicates the ratio of vertical reaction force applied to this foot
#>double      balance_ref;  ///< reference balance ratio [0.0, 1.0]
#>Vector3     pos;          ///< position
#>Vector3     pos_ref;      ///< reference position
#>Quaternion  ori;          ///< orientation in quaternion
#>Quaternion  ori_ref;      ///< reference orientation in quaternion
#>Vector3     angle;        ///< orientation in roll-pitch-yaw
#>Vector3     angle_ref;    ///< reference orientation in roll-pitch-yaw
#>Vector3     vel_ref;      ///< reference velocity
#>Vector3     angvel_ref;   ///< reference angular velocity
#>Vector3     acc_ref;      ///< reference acceleration
#>Vector3     angacc_ref;   ///< reference angular acceleration
#>Vector3     force;        ///< ground reaction force acting on this foot
#>Vector3     force_ref;    ///< reference ground reaction force
#>Vector3     moment;       ///< ground reaction moment acting on this foot
#>Vector3     moment_ref;   ///< reference ground reaction moment
#>Vector3     zmp;          ///< ZMP (i.e., center-of-pressure) of this foot
#>Vector3     zmp_ref;      ///< reference ZMP of this foot

    def __post_init__(self):
        if self.coords_ref is None:
            self.coords_ref = coordinates()

def fmtVec3(vec3):
    return f'({vec3[0]:.6f}, {vec3[1]:.6f}, {vec3[2]:.6f} )'

def printVec3(vec3, prefix=''):
    print(prefix + fmtVec3(vec3))

def printStep(step, prefix='step.'):
    print(f'{prefix}stride:\t{step.stride:.6f}')
    print(f'{prefix}sway:\t{step.sway:.6f}')
    print(f'{prefix}spacing:\t{step.spacing:.6f}')
    print(f'{prefix}turn:\t{step.turn:.6f}')
    print(f'{prefix}climb:\t{step.climb:.6f}')
    print(f'{prefix}duration:\t{step.duration:.6f}')
    print(f'{prefix}side:\t{step.side}')
    #print(f'{prefix}stepping:\t{step.stepping}')
    if step.stepping:
        print(f'{prefix}stepping:\t{1}')
    else:
        print(f'{prefix}stepping:\t{0}')
    print(f'{prefix}tbegin:\t{step.tbegin:.6f}')
    print(f'{prefix}foot_pos[0]:\t' + fmtVec3(step.foot_coords[0].pos))
    print(f'{prefix}foot_pos[1]:\t' + fmtVec3(step.foot_coords[1].pos))
    print(f'{prefix}foot_angle[0]:\t' + fmtVec3(step.foot_coords[0].RPY))
    print(f'{prefix}foot_angle[1]:\t' + fmtVec3(step.foot_coords[1].RPY))
    print(f'{prefix}zmp:\t'+ fmtVec3(step.zmp))
    print(f'{prefix}dcm:\t'+ fmtVec3(step.dcm))

def printFoot(foot, prefix=""):
    if foot.contact_ref:
        print(f'{prefix}contact_ref:\t{1}')
    else:
        print(f'{prefix}contact_ref:\t{0}')
    print(f'{prefix}pos_ref:\t' + fmtVec3(foot.coords_ref.pos))
    print(f'{prefix}angle_ref:\t' + fmtVec3(foot.coords_ref.RPY))
