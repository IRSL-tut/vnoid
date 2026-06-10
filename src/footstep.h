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

#define _printVector3(variable) \
    std::cerr << #variable ;           \
    std::cerr << ":\t( ";                 \
    std::cerr << variable.x() << ", "; \
    std::cerr << variable.y() << ", "; \
    std::cerr << variable.z() << " )" << std::endl;

#define _printVar(variable)                     \
    std::cerr << #variable << " :\t";           \
    std::cerr << variable << std::endl;

#define printStep(step)                           \
    std::cerr << "Step: " << #step << std::endl;  \
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
