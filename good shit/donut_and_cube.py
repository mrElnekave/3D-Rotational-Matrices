"""
Prototype mathematics in rubato
"""

import rubato as rb

rb.init(res=(500, 500), maximize=True, target_fps=60)
rb.Game.show_fps = True

import cube, donut, sprinkles

granularity = 2

def custom_update():
    donut.roll += 0.0704 * granularity
    donut.pitch += 0.0352 * granularity
    cube.roll += 0.0704 * granularity
    cube.pitch += 0.0352 * granularity
    cube.yaw += 0.0176 * granularity
    sprinkles.roll_donut += 0.0704 * granularity
    sprinkles.pitch_donut += 0.0352 * granularity
    # Updates the roll and yaw in radians


def custom_draw():
    offset = 125
    

    rb.Draw.queue_surface(donut.donut_surf(), (offset, -offset))
    
    rb.Draw.queue_surface(cube.cube_surf(), (-offset, -offset))

    rb.Draw.queue_surface(sprinkles.sprinkles_surf(), (0, offset))


rb.Game.update = custom_update
rb.Game.draw = custom_draw
rb.begin()
