exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())
exec(open('walking_control.py').read())

wc=WalkingControl()
wc.setup_controller()
di = DrawInterface()

for i in range(200):
    wc.step_simulation()
    cleft  = coordinates(wc.feet[0].pos_ref)
    cright = coordinates(wc.feet[1].pos_ref)
    cleft .setRPY(wc.feet[0].angle_ref)
    cright.setRPY(wc.feet[1].angle_ref)
    dcm = coordinates(wc.centroid.dcm_target)
    di.addObject(mkshapes.makeCoords(length=0.1, coords=cleft))
    di.addObject(mkshapes.makeCoords(length=0.1, coords=cright))
    di.addObject(mkshapes.makeCoords(length=0.07, coords=dcm))
