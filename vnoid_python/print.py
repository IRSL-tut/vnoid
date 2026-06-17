exec(open('walking_control.py').read())

wc=WalkingControl()
wc.setup_controller()

for i in range(600):
    print(f'stepping_controller : {i}')
    wc.step_simulation()
