#include "robot.h"
#include "iksolver.h"
#include "fksolver.h"
#include "footstep.h"
#include "footstep_planner.h"
#include "stepping_controller.h"
#include "stabilizer.h"

#include <iostream>
#include <iomanip>

using namespace std;
using namespace cnoid;
using namespace cnoid::vnoid;

Timer            timer;
Param            param;
Centroid         centroid;
Base             base;
//vector<Hand>     hand;
vector<Foot>     foot;
//vector<Joint>    joint;
Footstep         footstep;
Footstep         footstep_buffer;

FootstepPlanner     footstep_planner;
SteppingController  stepping_controller;
Stabilizer          stabilizer;

#define _myprint(var) \
    cerr << #var << " : " << var << endl

int main(void)
{
#if 0
    Footstep a, b;
    a.steps.push_back(Step());
    a.steps.push_back(Step());

    Step &as0 = a.steps[0];
    Step &as1 = a.steps[1];

    as0.stride = 0.888;
    _myprint(a.steps[0].stride);

    b.steps.push_back(as0);
    _myprint(b.steps[0].stride);

    b.steps[0].stride = 0.777;
    _myprint(b.steps[0].stride);
    _myprint(a.steps[0].stride);
    return -1;
#endif

    timer.dt = 0.01; //// set dt here
    param.total_mass = 50.0;
    param.com_height =  0.70;
    param.gravity    =  9.8;

    param.trunk_mass = 24.0;
    param.trunk_com = Vector3(0.0, 0.0, 0.166);
    param.zmp_min = Vector3(-0.1, -0.05, -0.1);
    param.zmp_max = Vector3( 0.1,  0.05,  0.1);

    param.Init();

    foot.resize(2);

    centroid.com_pos_ref = Vector3(0.0, 0.0, param.com_height);
    centroid.dcm_ref     = Vector3(0.0, 0.0, param.com_height);
    foot[0].pos_ref = Vector3(0.0, -0.2/2.0, 0.0);
    foot[1].pos_ref = Vector3(0.0,  0.2/2.0, 0.0);

    // init footsteps
    footstep.steps.push_back(Step(0.0, 0.0, 0.2, 0.0, 0.0, 0.5, 0));
    footstep.steps.push_back(Step(0.0, 0.0, 0.2, 0.0, 0.0, 0.5, 1));
    // foot placement and DCM of the initial step must be specified
    footstep.steps[0].foot_pos[0] = foot[0].pos_ref;
    footstep.steps[0].foot_pos[1] = foot[1].pos_ref;
    footstep.steps[0].dcm = centroid.dcm_ref;
    cerr << "00 footstep(pre)" << endl;
    for(int i = 0; i < footstep.steps.size(); i++) {
        cerr << "steps[" << i << "]" << endl;
        printStep(footstep.steps[i]);
    }
    footstep_planner.Plan(param, footstep);
    cerr << "00 footstep(after Plan)" << endl;
    for(int i = 0; i < footstep.steps.size(); i++) {
        cerr << "steps[" << i << "]" << endl;
        printStep(footstep.steps[i]);
    }
    footstep_planner.GenerateDCM(param, footstep);
    cerr << "00 footstep(after GenDCM)" << endl;
    for(int i = 0; i < footstep.steps.size(); i++) {
        cerr << "steps[" << i << "]" << endl;
        printStep(footstep.steps[i]);
    }
    cerr << endl;
    footstep_buffer.steps.push_back(footstep.steps[0]);
    footstep_buffer.steps.push_back(footstep.steps[1]);

    // init stepping controller
    stepping_controller.swing_height = 0.05;
    stepping_controller.swing_tilt   = 0.0;
    stepping_controller.dsp_duration = 0.05;
    stepping_controller.timing_adaptation_weight = 0.1;

    // init stabilizer
    stabilizer.orientation_ctrl_gain_p = 50.0;//100.0;
    stabilizer.orientation_ctrl_gain_d = 5.0;//10.0;
    stabilizer.dcm_ctrl_gain           = 2.0;
    stabilizer.base_tilt_rate          = 0.0;//5.0;
    stabilizer.base_tilt_damping_p     = 0.0;//100.0;
    stabilizer.base_tilt_damping_d     = 0.0;//50.0;

    {
        Step step;
        step.stride   = 0.1; //-max_stride*joystick.getPosition(Joystick::L_STICK_V_AXIS);
        step.turn     = 0.0; //-max_turn  *joystick.getPosition(Joystick::L_STICK_H_AXIS);
        step.spacing  = 0.20;
        step.climb    = 0.0;
        step.duration = 0.5;
        footstep.steps.push_back(step);
        footstep.steps.push_back(step);
        footstep.steps.push_back(step);
        step.stride = 0.0;
        step.turn   = 0.0;
        footstep.steps.push_back(step);

        cerr << "footstep(pre)" << endl;
        for(int i = 0; i < footstep.steps.size(); i++) {
            cerr << "steps[" << i << "]" << endl;
            printStep(footstep.steps[i]);
        }
        //
        footstep_planner.Plan(param, footstep);
        //
        cerr << "footstep(after Plan)" << endl;
        for(int i = 0; i < footstep.steps.size(); i++) {
            cerr << "steps[" << i << "]" << endl;
            printStep(footstep.steps[i]);
        }
        //
        footstep_planner.GenerateDCM(param, footstep);
        //
        cerr << "footstep(after GenDCM)" << endl;
        for(int i = 0; i < footstep.steps.size(); i++) {
            cerr << "steps[" << i << "]" << endl;
            printStep(footstep.steps[i]);
        }
        cerr << endl;
    }

    for(long _i_ = 0; _i_ < 550; _i_++) {

#if 0
    if(timer.count % 10 == 0) {
        while(footstep.steps.size() > 2)
            footstep.steps.pop_back();
        cerr << "add steps : " << timer.count << endl;

        Step step;
        step.stride   = 0.1; //-max_stride*joystick.getPosition(Joystick::L_STICK_V_AXIS);
        step.turn     = 0.0; //-max_turn  *joystick.getPosition(Joystick::L_STICK_H_AXIS);
        step.spacing  = 0.20;
        step.climb    = 0.0;
        step.duration = 0.5;
        footstep.steps.push_back(step);
        footstep.steps.push_back(step);
        footstep.steps.push_back(step);
        step.stride = 0.0;
        step.turn   = 0.0;
        footstep.steps.push_back(step);

        cerr << "footstep(pre)" << endl;
        for(int i = 0; i < footstep.steps.size(); i++) {
            cerr << "steps[" << i << "]" << endl;
            printStep(footstep.steps[i]);
        }
        //
        footstep_planner.Plan(param, footstep);
        //
        cerr << "footstep(after Plan)" << endl;
        for(int i = 0; i < footstep.steps.size(); i++) {
            cerr << "steps[" << i << "]" << endl;
            printStep(footstep.steps[i]);
        }
        //
        footstep_planner.GenerateDCM(param, footstep);
        //
        cerr << "footstep(after GenDCM)" << endl;
        for(int i = 0; i < footstep.steps.size(); i++) {
            cerr << "steps[" << i << "]" << endl;
            printStep(footstep.steps[i]);
        }
    }
#endif
    cerr << "stepping_controller : [" << timer.count << "] : " << fixed << setprecision(4) << timer.time << " (" << timer.dt << ")" << std::endl;
    stepping_controller.Update(timer, param, footstep, footstep_buffer, centroid, base, foot);

    //// stabilizer performs balance feedback
    //stabilizer         .Update(timer, param, /*footstep_buffer,*/ centroid, base, foot);

    //// calc CoM IK
    //ik_solver.Comp(&fk_solver, param, centroid, base, hand, foot, joint);

    timer.Countup();

    } // for _i_

    return 0;
}
