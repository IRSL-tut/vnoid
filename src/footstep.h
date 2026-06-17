#pragma once

#include "types.h"

#include <deque>
using namespace std;

namespace cnoid{
namespace vnoid{

/**
 Single footstep
 **/
class Step{
public:
	double   stride;    ///< longitudinal step length
    double   sway;      ///< lateral step length
	double   spacing;   ///< lateral spacing between left and right feet
	double   turn;      ///< turning angle in single step
	double   climb;     ///< vertical displacement in single step
	double   duration;  ///< step duration
    
	int      side;      ///< indicates which foot (0: right, 1: left) is the support foot in this step
	bool     stepping;  ///< stepping or standing still
	double   tbegin;    ///< starting time of this step
		
	Vector3     foot_pos   [2];  ///< position of each foot at the beginning of this step
	Vector3     foot_angle [2];
	Quaternion  foot_ori   [2];  ///< orientation of each foot at the beginning of this step
	Vector3     foot_vel   [2];
	Vector3     foot_angvel[2];
    Vector3     zmp;             ///< position of zmp during this step
	Vector3     dcm;             ///< position of dcm at the beginning of this step

    Step(double _stride = 0.0, double _sway = 0.0, double _spacing = 0.0, double _turn = 0.0, double _climb = 0.0, double _duration = 0.5, int _side = 0);
};

#define _printVector3Only(variable)                                   \
    cerr << "(";                                                      \
    cerr << fixed << setprecision(6) << variable.x() << ", ";         \
    cerr << fixed << setprecision(6) << variable.y() << ", ";         \
    cerr << fixed << setprecision(6) << variable.z() << " )" << endl;

#define _printVector3(variable)                 \
    cerr << #variable << ":\t";                 \
    _printVector3Only(variable);

#define _printVector3Prefix(prefix, variable)   \
    cerr << prefix;                             \
    _printVector3Only(variable);

#define _printVarOnly(variable) \
    cerr << fixed << setprecision(6) << variable << endl;

#define _printVar(variable)                               \
    cerr << #variable << ":\t";                           \
    _printVarOnly(variable);

#define _printVarPrefix(prefix, variable)       \
    cerr << prefix;                             \
    _printVarOnly(variable)

#define printStep(step)                           \
    _printVar(step.stride);                       \
    _printVar(step.sway);                         \
    _printVar(step.spacing);                      \
    _printVar(step.turn);                         \
    _printVar(step.climb);                        \
    _printVar(step.duration);                     \
    _printVar(step.side);                         \
    _printVar(step.stepping);                     \
    _printVar(step.tbegin);                       \
    _printVector3(step.foot_pos[0]);              \
    _printVector3(step.foot_pos[1]);              \
    _printVector3(step.zmp);                      \
    _printVector3(step.dcm);

//>#define printFoot(foot)                         \
//>    _printVar(foot.contact);                    \
//>    _printVar(foot.contact_ref);                \
//>    _printVar(foot.balance);                    \
//>    _printVar(foot.balance_ref);                \
//>    _printVector3(foot.pos);                    \
//>    _printVector3(foot.pos_ref);                \
//>    _printVar(foot.ori);                        \
//>    _printVar(foot.ori_ref);                    \
//>    _printVector3(foot.angle);                  \
//>    _printVector3(foot.angle_ref);              \
//>    _printVector3(foot.vel_ref);                \
//>    _printVector3(foot.angvel_ref);             \
//>    _printVector3(foot.acc_ref);                \
//>    _printVector3(foot.angacc_ref);             \
//>    _printVector3(foot.force);                  \
//>    _printVector3(foot.force_ref);              \
//>    _printVector3(foot.moment);                 \
//>    _printVector3(foot.moment_ref);             \
//>    _printVector3(foot.zmp);                    \
//>    _printVector3(foot.zmp_ref);
#define printFoot(foot)                         \
    _printVar(foot.contact_ref);                \
    _printVector3(foot.pos_ref);                \
    _printVector3(foot.angle_ref);

//>	bool        contact;      ///< current contact state (true if foot is in contact with the ground)
//>	bool        contact_ref;  ///< reference contact state
//>	double      balance;      ///< current balance ratio [0.0, 1.0].  indicates the ratio of vertical reaction force applied to this foot
//>	double      balance_ref;  ///< reference balance ratio [0.0, 1.0]
//>	Vector3     pos;          ///< position
//>	Vector3     pos_ref;      ///< reference position
//>	Quaternion  ori;          ///< orientation in quaternion
//>	Quaternion  ori_ref;      ///< reference orientation in quaternion
//>	Vector3     angle;        ///< orientation in roll-pitch-yaw
//>	Vector3     angle_ref;    ///< reference orientation in roll-pitch-yaw
//>	Vector3     vel_ref;      ///< reference velocity
//>	Vector3     angvel_ref;   ///< reference angular velocity
//>	Vector3     acc_ref;      ///< reference acceleration
//>	Vector3     angacc_ref;   ///< reference angular acceleration
//>	Vector3     force;        ///< ground reaction force acting on this foot
//>	Vector3     force_ref;    ///< reference ground reaction force
//>	Vector3     moment;       ///< ground reaction moment acting on this foot
//>	Vector3     moment_ref;   ///< reference ground reaction moment
//>	Vector3     zmp;          ///< ZMP (i.e., center-of-pressure) of this foot
//>	Vector3     zmp_ref;      ///< reference ZMP of this foot

/**
 Footstep sequence
 **/
class Footstep{
public:
    /// series of footsteps
    deque<Step>  steps;
};

}
}
