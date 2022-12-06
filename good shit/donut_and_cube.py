"""
Prototype mathematics in rubato
"""

import rubato as rb

rb.init(res=(500, 500), maximize=True, target_fps=60)
rb.Game.show_fps = True

import cube, donut, sprinkles


def custom_update():
    donut.roll += 0.0704
    donut.pitch += 0.0352
    cube.roll += 0.0704
    cube.pitch += 0.0352
    cube.yaw += 0.0176
    sprinkles.roll_donut += 0.0704
    sprinkles.pitch_donut += 0.0352
    # Updates the roll and yaw in radians


def custom_draw():
    offset = 125
    

    rb.Draw.queue_surface(donut.donut_surf(), (offset, -offset))
    
    rb.Draw.queue_surface(cube.cube_surf(), (-offset, -offset))

    rb.Draw.queue_surface(sprinkles.sprinkles_surf(), (0, offset))


rb.Game.update = custom_update
rb.Game.draw = custom_draw
rb.begin()
