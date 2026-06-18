exec(open('walking_control.py').read())

wc=WalkingControl()
wc.setup_controller()
wc.no_dcm_gain=True
wc.no_dcm_derivative=True

for i in range(360):
    print(f'stepping_controller : [{wc.timer.count}] : {wc.timer.time:.4f} ({wc.timer.dt:.4f})')
    wc.step_simulation()
