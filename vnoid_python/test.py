exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())
exec(open('walking_control.py').read())

wc=WalkingControl()
wc.setup_controller()
wc.stepping_controller.debug = 0
wc.no_dcm_gain=True
wc.no_dcm_derivative=True

di=DrawInterface()

for i in range(360):
    ##
    print(f'stepping_controller : [{wc.timer.count}] : {wc.timer.time:.4f} ({wc.timer.dt:.4f})')
    wc.step_simulation()
    cleft  = coordinates(wc.feet[0].pos_ref)
    cright = coordinates(wc.feet[1].pos_ref)
    cleft .setRPY(wc.feet[0].angle_ref)
    cright.setRPY(wc.feet[1].angle_ref)
    ##
    o_dcm = mkshapes.makeCross(color=[1, 0, 1], lineWdith=1, length=0.02)
    o_dcm.locate(wc.centroid.dcm_ref)
    o_zmp = mkshapes.makeCross(color=[0, 1, 1], lineWdith=1, length=0.02)
    o_zmp.locate(wc.centroid.zmp_ref)
    o_com = mkshapes.makeCross(color=[0, 1, 0], lineWdith=1, length=0.02)
    o_com.locate(wc.centroid.com_pos_ref)
    di.addObjects((mkshapes.makeCoords(length=0.07, coords=cleft),
                   mkshapes.makeCoords(length=0.07, coords=cright),
                   o_dcm, o_zmp, o_com))

# ax=mkshapes.makeLineAxis(fv(0, 0, 0), fv(1, 1, 1), axis_length=0.2)
def drawFoot(center, length=0.2, width=0.1, coords=None, **kwargs):
    coords = coordinates() if coords is None else coords.copy()
    coords.pos = center
    lst = [ coords.transform_vector(fv( length*0.5,  width*0.5, 0)),
            coords.transform_vector(fv(-length*0.5,  width*0.5, 0)),
            coords.transform_vector(fv(-length*0.5, -width*0.5, 0)),
            coords.transform_vector(fv( length*0.5, -width*0.5, 0)) ]
    return mkshapes.makeLines(lst, [[0,1], [1,2], [2,3], [3, 0]], **kwargs)

# mkshape.makeLines(cent
def printFootstep(footstep, length=0.07, lineWidth=5):
    for idx, step in enumerate(footstep.steps):
        print(f'steps[{idx}]')
        printStep(step, f'footstep.steps[{idx}].')
        #
        c_dcm=mkshapes.makeCoords(length=length, lineWidth=lineWidth)
        c_dcm=c_dcm.locate(step.dcm)
        #
        c_zmp=mkshapes.makeCoords(length=length, lineWidth=lineWidth)
        c_zmp=c_zmp.locate(step.zmp)
        #
        di.addObjects((c_dcm, c_zmp))
        swg=step.side
        sup=1-swg
        ax=mkshapes.makeLineAxis(step.foot_pos[sup], step.foot_pos[swg], axis_length=length*0.5, lineWidth=lineWidth*0.5)
        di.addObjects(ax)
