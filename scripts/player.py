# license: GPL-v2-or-later
# author: Gabriel Dornelles

import bge
import collections
import math
import mathutils
import sys

import pyhelper
pyhelper.init()

if hasattr(bge, "logic"):
    sys.path.append(bge.logic.expandPath('//scripts'))

    # this should be in a more appropriate location
    settings = {
        "mouse_sensitivity" : 1.0,
        "inputs" : {
            'forward': bge.logic.pykeyboard.WKEY,
            'back'   : bge.logic.pykeyboard.SKEY,
            'left'   : bge.logic.pykeyboard.AKEY,
            'right'  : bge.logic.pykeyboard.DKEY,
            'sprint' : bge.logic.pykeyboard.LEFTSHIFTKEY,
            'jump'   : bge.logic.pykeyboard.SPACEKEY,
        }
    }

class PlayerComponent(bge.types.KX_PythonComponent):
    args = collections.OrderedDict([
    ])

    def __init__(self, ob):
        ...

    def start(self, args):
        self.__character = bge.constraints.getCharacter(self.object)
        self.__camera = self.object.childrenRecursive['player_camera']
        self.__move_speed = 2.5
        self.__dt = 0.0
    
    def update(self):
        self.__dt = bge.logic.deltaTime()
        self.__mouse_look()
        self.__movements()

    def __movements(self):
        f = settings['inputs']['forward'].active - settings['inputs']['back'].active
        s = settings['inputs']['right'].active - settings['inputs']['left'].active
        
        move_dir = mathutils.Vector((s,f,0)).normalized()
        move_dir *= self.__move_speed if not settings['inputs']['sprint'].active else self.__move_speed * 2.0
        
        if settings['inputs']['jump'].active:
            self.__character.jump()
        
        self.__character.walkDirection = self.object.worldOrientation * move_dir * self.__dt
    
    def __mouse_look(self):
        mouse = bge.logic.pymouse

        if mouse.visible:
            mouse.visible = False

        x = mouse.deltaPosition.x * settings['mouse_sensitivity']
        y = mouse.deltaPosition.y * settings['mouse_sensitivity']

        camEul = self.__camera.localOrientation.to_euler()
        camEul.x = pyhelper.utils.clamp(camEul.x + y, math.radians(-90.0), math.radians(90.0))
        self.__camera.localOrientation = camEul.to_matrix()
        
        self.object.applyRotation((0,0,x),True)

        mouse.reCenter()
