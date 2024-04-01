import random

import panda3d.core as p3d
from direct.showbase.ShowBase import ShowBase
import complexpbr


class Game(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.set_frame_rate_meter(True)
        self.cam_controller = CameraController(self)

        dlight = p3d.DirectionalLight('dlight')
        dlight.setColor(p3d.Vec4(0.8, 0.8, 0.5, 1)*50)
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setPos(-10, 0, 10)
        dlnp.lookAt(self.render)
        self.render.setLight(dlnp)

        self.water_model = self.loader.loadModel("water_plane.blend")
        self.water_model.reparentTo(self.render)

        # Load the skybox
        self.skybox = self.loader.loadModel("skybox.blend")
        self.skybox.setScale(200)
        self.skybox.reparentTo(self.render)
        self.skybox.setShaderOff()
        self.skybox.setBin('background', 0)
        self.skybox.setDepthWrite(0)
        self.skybox.setLightOff()

        complexpbr.apply_shader(self.render, env_cam_pos=p3d.Vec3(0))
        complexpbr.screenspace_init()

        self.generate_wave_data(.04)

    def generate_wave_data(self, amplitude_scale=0.2):
        def rand_float():
            return (random.random() - 0.5)*2

        def rotate_vec(vec: p3d.Vec3, angle: int) -> p3d.LVecBase3:
            axis = p3d.Vec3(0, 0, 1)
            # the axis vector must be unit length
            axis.normalize()
            # the angle is given in degrees
            quat = p3d.Quat()
            quat.setFromAxisAngle(angle, axis)
            rotated_vec = quat.xform(vec)
            return rotated_vec

        self.amplitude_list = []
        self.wavelength_list = []
        self.phase_list = []
        self.direction_list = []
        self.circular_list = []
        num_waves = 256
        # amp = 1
        # wave = 1
        length = 4
        speed = 5
        wind_direction = p3d.Vec3(.6, .2, 0)

        for wave in range(num_waves):
            x = 10/num_waves*(wave + 1)
            # amp = (-x**0.7 + 5)
            # amp = math.e**(-x)*6
            # amp = x**(-0.8)
            direction = rotate_vec(p3d.Vec3(wind_direction), random.randint(-30, 30))
            wave = (9.82 * 2 * 3.14 / length)**(1 / 2) * 2 * (random.random() + 0.5)
            phase = speed * 2 / length
            self.amplitude_list.append(wave * amplitude_scale)
            self.wavelength_list.append(wave)
            self.phase_list.append(phase)
            self.direction_list.append((direction[0], direction[1]))
            self.circular_list.append(False)

        self.water_model.setShaderInputs(
            amplitude=self.amplitude_list,
            wavelength=self.wavelength_list,
            phase=self.phase_list,
            direction=self.direction_list,
            circular=self.circular_list
        )


class CameraController:
    """Class for handling camera movement.

    Use 'w', 'a', 's', 'd' for moving the camera.
    Use mouse wheel for zooming in and out.
    Press mouse wheel and drag to rotate the camera view.
    """

    def __init__(self, game: ShowBase):
        self.game = game
        self.tasks = []
        self.camera = game.camera
        self.camera_node = p3d.NodePath("camera_node")  # used to rotate camera
        self._setup_camera()

        self.zoom_speed = 1  # adjust to change how fast to zoom

        # data for which keys are pressed
        self.key_map = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "free_rot": False
        }

        # dict of what inputs are bound to the controls (feel free to change these)
        self.key_binds = {
            "up": "w",
            "down": "s",
            "left": "a",
            "right": "d",
            "zoom_in": "wheel_up",
            "zoom_out": "wheel_down",
            "free_rot": "mouse2"  # 'mouse1' should work for trackpads
        }

        self._setup_key_map_and_mouse_inputs()
        self.reset_camera_pos()

    def reset_camera_pos(self):
        """Set the camera position and rotation to its initial values."""
        self.camera_node.setPos(0, 0, 0)
        self.camera_node.setHpr(0, 45, 0)
        self.camera.setHpr(0, 270, 0)
        self.camera.setPos(0, 0, 0)
        self.camera.setPos(self.camera, 0, -10, 0)

    def _setup_camera(self):
        self.camera_node.reparentTo(self.game.render)
        self.camera.reparentTo(self.camera_node)
        self.tasks.append(self.game.taskMgr.add(self._update_camera_position, "_update_camera_position"))

    def _setup_key_map_and_mouse_inputs(self):
        """Set up key binds for player inputs."""

        # setup basic interactions
        for key, value in self.key_binds.items():
            if key == "zoom" or key == "free_rot":
                break
            self.game.accept(value, self._update_key_map, [key, True])
            self.game.accept(value + "-up", self._update_key_map, [key, False])

        self.game.accept(self.key_binds["zoom_in"], self._update_zoom, [1])
        self.game.accept(self.key_binds["zoom_out"], self._update_zoom, [-1])

        self.game.accept(f"{self.key_binds['free_rot']}", self._update_rotation_values, [True])
        self.game.accept(f"{self.key_binds['free_rot']}-up", self._update_rotation_values, [False])
        self.tasks.append(self.game.taskMgr.add(self._update_rotate))

    def _update_rotate(self, task):
        """Update rotation depending on mouse movement."""
        if not self.key_map["free_rot"]:
            return task.cont

        if not self.game.mouseWatcherNode.hasMouse():
            return task.cont

        m_pos = self.game.mouseWatcherNode.getMouse()

        rel_pos = (self._last_mouse_pos - m_pos) * 100
        new_rot = self._last_cam_node_hpr + p3d.Vec3(rel_pos.x, -rel_pos.y, 0)
        self.camera_node.setHpr(new_rot)

        return task.cont

    def _update_camera_position(self, task):
        """Update the camera position depending on keyboard input."""
        dt = self.game.clock.getDt()
        move_speed = -self.camera.getPos().length() * 0.5

        # Move left or right
        speed = move_speed * (self.key_map["left"] - self.key_map["right"]) * dt
        self.camera.setPos(self.camera, speed, 0, 0)

        # Move up or down
        speed = move_speed * (-self.key_map["up"] + self.key_map["down"]) * dt
        self.camera.setPos(self.camera, 0, 0, speed)

        return task.cont

    def _update_zoom(self, value):
        """Zoom in or out when scrolling the mouse wheel."""
        dt = self.game.clock.getDt()
        z = self.camera.getZ()
        self.camera.setPos(self.camera, 0, z * value * dt * 20 * self.zoom_speed, 0)

        # self.camera.setZ(max(1, min(self.camera.getZ(), 400)))

    def _update_rotation_values(self, value: bool):
        """Update key_map and other values needed for camera rotation."""
        self.key_map["free_rot"] = value
        if self.game.mouseWatcherNode.hasMouse():
            self._last_mouse_pos = p3d.Point2(self.game.mouseWatcherNode.getMouse())

        self._last_cam_node_hpr = p3d.Vec3(self.camera_node.getHpr())

    def _update_key_map(self, control_name, control_state):
        """Updates the key_map when a map_button is pressed."""
        self.key_map[control_name] = control_state


if __name__ == '__main__':
    game = Game()
    game.run()
