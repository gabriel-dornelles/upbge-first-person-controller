# license: GPL-v2-or-later
# author: Gabriel Dornelles
# last-modified: 26/10/2025

import bge
import collections
import math
import mathutils
import sys

# why we need this? to know when we're in game engine and not in blender itself.
if hasattr(bge, "logic"):
    # add scripts folder to sys path, so python can find our module
    # you also can use an empty .blend as lib and then pack the lib in your .blend
    sys.path.append(bge.logic.expandPath('//scripts'))
    
    # we just need this
    from PyMouse import mouse
    
    # -- ignore this code -- #
    # this should be created in another place
    # for better organization
    
    clamp = lambda x,y,z : max(y, min(x,z))
    odt = bge.logic.getFrameTime()
    dt = 0.0
    
    keyboard = bge.logic.keyboard
    
    g_mouse_sens = 1.0
    
    inputs = {
        'forward': keyboard.inputs[bge.events.WKEY],
        'back'   : keyboard.inputs[bge.events.SKEY],
        'left'   : keyboard.inputs[bge.events.AKEY],
        'right'  : keyboard.inputs[bge.events.DKEY],
        'sprint' : keyboard.inputs[bge.events.LEFTSHIFTKEY],
        'jump'   : keyboard.inputs[bge.events.SPACEKEY],
    }

class PlayerComponent(bge.types.KX_PythonComponent):
    args = collections.OrderedDict([
    ])

    def start(self, args):
        # hardcoded values, why not
        self.__move_speed = 2.5
        
        self.__character = bge.constraints.getCharacter(self.object)
        self.__camera = self.object.childrenRecursive['player_camera']
    
    def update(self):
        self.__delta()
        self.__mouse_look()
        self.__movements()
    
    # also ignore, just delta time
    def __delta(self):
        global dt, odt
        
        c = bge.logic.getFrameTime()
        dt = c - odt
        odt = c
    
    # these functions are self explain...
    
    def __movements(self):
        f = inputs['forward'].active - inputs['back'].active
        s = inputs['right'].active - inputs['left'].active
        
        move_dir = mathutils.Vector((s,f,0)).normalized()
        move_dir *= self.__move_speed if not inputs['sprint'].active else self.__move_speed * 2.0
        
        if inputs['jump'].active:
            self.__character.jump()
        
        self.__character.walkDirection = self.object.worldOrientation * move_dir * dt
    
    def __mouse_look(self):
        if mouse.visible:
            mouse.visible = False
        
        # this is how we can access the delta position
        # -> mouse.deltaPosition
        x, y = mouse.deltaPosition
        
        x *= g_mouse_sens
        y *= g_mouse_sens
        
        # clamp camera X angle (pitch) 90d
        eul   = self.__camera.localOrientation.to_euler()
        eul.x = clamp(eul.x + y, math.radians(-90), math.radians(90))
        self.__camera.localOrientation = eul.to_matrix()
        
        self.object.applyRotation((0,0,x),True)
        
        # same name as RanGE, to make things easier
        mouse.reCenter()

# 100