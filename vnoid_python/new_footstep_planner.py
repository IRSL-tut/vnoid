import numpy as np
import math
from vnoid_types import Step, Footstep, Param, Ground

eps = 1.0e-10

class FootstepPlanner:
    """歩行ステップの計画"""

    def __init__(self):
        pass

    def Plan(self, param: Param, footstep: Footstep):
        """
        足の配置とサポート足フラグを決定

        Args:
            param: 歩行パラメータ
            footstep: 歩行計画（step[0]の足の配置とDCMは外部で指定される）
        """
        nstep = len(footstep.steps)

        for i in range(nstep - 1):
            st0 = footstep.steps[i]
            st1 = footstep.steps[i + 1]

            sup = st0.side      # サポート足
            swg = 1 - st0.side  # スウィング足

            dtheta = st0.turn
            l = st0.stride
            d = st0.sway
            w = (1.0 if sup == 0 else -1.0) * st0.spacing
            dz = st0.climb

            # スウィング足の相対位置を計算
            if abs(dtheta) < eps:
                dprel = np.array([l, w + d, dz])
            else:
                r = l / dtheta
                dprel = np.array([
                    (r - w / 2.0 - d) * math.sin(dtheta),
                    (r + w / 2.0) - (r - w / 2.0 - d) * math.cos(dtheta),
                    dz
                ])

            # サポート足と スウィング足を交換
            st1.side = 1 - st0.side

            # サポート足の位置は変わらない
            # st1.foot_pos[sup]   = st0.foot_pos[sup].copy()
            # st1.foot_angle[sup] = st0.foot_angle[sup].copy()
            # st1.foot_ori[sup]   = st0.foot_ori[sup]
            st1.foot_coords[sup] = st0.foot_coords[sup].copy()

            # スウィング足の位置が変わる
            # st1.foot_pos[swg]   = st0.foot_pos[sup] + rotate_vector(st0.foot_ori[sup], dprel)
            # st1.foot_angle[swg] = st0.foot_angle[sup] + np.array([0.0, 0.0, dtheta])
            # st1.foot_ori[swg]   = R.from_euler('xyz', st1.foot_angle[swg])
            cds = st0.foot_coords[sup].copy()
            cds.translate(dprel)
            cds.rotate(dtheta, cds.Z)
            st1.foot_coords[swg] = cds

#>    def align_to_ground(self, ground: Ground, footstep: Footstep):
#>        """
#>        地面に足を合わせる
#>
#>        Args:
#>            ground: 地面情報
#>            footstep: 歩行計画
#>        """
#>        # 初期サポート足の中心を基準に回転
#>        pivot = footstep.steps[0].foot_pos[footstep.steps[0].side]
#>
#>        # 地面の法線ベクトル
#>        normal = rotate_vector(ground.ori, np.array([0.0, 0.0, 1.0]))
#>
#>        for k in range(len(footstep.steps)):
#>            st = footstep.steps[k]
#>
#>            for i in range(2):
#>                # Z座標を修正
#>                dp = st.foot_pos[i] - pivot
#>                if abs(normal[2]) > eps:
#>                    dp[2] = -(normal[0] * dp[0] + normal[1] * dp[1]) / normal[2]
#>
#>                st.foot_pos[i][2] = pivot[2] + dp[2]
#>
#>                # 地面法線を足の yaw ローカル座標に変換
#>                yaw = st.foot_angle[i][2]
#>                rot_z_neg = R.from_euler('z', -yaw)
#>                nl = rotate_vector(rot_z_neg, normal)
#>
#>                st.foot_angle[i][0] = np.arcsin(-nl[1])
#>                st.foot_angle[i][1] = np.arctan2(nl[0], nl[2])
#>
#>                # クォータニオンに変換
#>                st.foot_ori[i] = R.from_euler('xyz', st.foot_angle[i])

    def GenerateDCM(self, param: Param, footstep: Footstep):
        """
        参考 DCM と ZMP を生成

        Args:
            param: 歩行パラメータ
            footstep: 歩行計画
        """
        nstep = len(footstep.steps)
        offset = np.array([0.0, 0.0, param.com_height])

        # 最後のステップの状態を設定
        i = nstep - 1
        # ZMP は足の中点
        footstep.steps[i].zmp = (footstep.steps[i].foot_coords[0].pos + footstep.steps[i].foot_coords[1].pos) / 2.0

        # DCM は ZMP から com_height 上
        footstep.steps[i].dcm = (footstep.steps[i].foot_coords[0].pos + footstep.steps[i].foot_coords[1].pos) / 2.0 + offset

        i -= 1

        # N-1 から 0 ステップの状態を計算
        while i >= 0:
            st0 = footstep.steps[i]
            st1 = footstep.steps[i + 1]

            sup = st0.side
            swg = 1 - st0.side

            a = math.exp(-st0.duration / param.T)

            # 初期ステップ: DCM は外部で指定済み、ZMP を決定
            if i == 0:
                st0.zmp = (st0.dcm - a * st1.dcm) / (1.0 - a) - offset
            else:
                # その他のステップ
                eps_local = 1.0e-3

                # スウィング足の位置が変わらない場合はダブルサポート
                if (np.linalg.norm(st0.foot_coords[swg].pos - st1.foot_coords[swg].pos) < eps_local and
                    np.linalg.norm(st0.foot_coords[swg].RPY - st1.foot_coords[swg].RPY) < eps_local):
                    st0.zmp = (st0.foot_coords[sup].pos + st0.foot_coords[swg].pos) / 2.0
                else:
                    # 그렇지 않으면 ZMP をサポート足に設定
                    st0.zmp = st0.foot_coords[sup].pos.copy()

                # DCM を ZMP から決定
                st0.dcm = (1.0 - a) * (st0.zmp + offset) + a * st1.dcm

            # ステップフラグを設定
            eps_local = 1.0e-3
            if (np.linalg.norm(st0.foot_coords[swg].pos - st1.foot_coords[swg].pos) < eps_local and
                np.linalg.norm(st0.foot_coords[swg].RPY - st1.foot_coords[swg].RPY) < eps_local):
                st0.stepping = False
            else:
                st0.stepping = True

            i -= 1


