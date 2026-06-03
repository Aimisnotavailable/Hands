from direct.showbase.ShowBase import ShowBase
from panda3d.core import getModelPath, Point3

class GltfViewer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        getModelPath().appendDirectory("MODEL")

        self.model = self.loader.loadModel("MODEL/scene.gltf", noCache=True)

        bounds = self.model.getTightBounds()
        if bounds:
            centre = (bounds[0] + bounds[1]) * 0.5
            size = (bounds[1] - bounds[0]).length()
            self.model_radius = size * 0.5
        else:
            centre = Point3(0, 0, 0)
            self.model_radius = 1.0

        self.pivot = self.render.attachNewNode("model_pivot")
        self.model.reparentTo(self.pivot)
        self.model.setPos(-centre)

        self.disableMouse()

        # ---- Camera setup ----
        self.cam_distance = self.model_radius * 3.0
        self.cam_target = Point3(0, 0, 0)
        self.camera.setPos(0, -self.cam_distance, 0)
        self.camera.lookAt(self.cam_target)

        # ---- Zoom limits ----
        self.min_distance = self.model_radius * 1.1
        self.max_distance = self.model_radius * 20.0

        self.rotate_speed = 90.0
        self.zoom_speed = 5.0

        self.accept("wheel_up", self.zoom_wheel, [1])
        self.accept("wheel_down", self.zoom_wheel, [-1])

        self.taskMgr.add(self.updateControls, "updateControls")

    def zoom_wheel(self, direction):
        self.cam_distance -= direction * self.model_radius * 0.5
        # Clamp camera distance
        self.cam_distance = max(self.min_distance, min(self.cam_distance, self.max_distance))
        self.update_camera_position()

    def updateControls(self, task):
        dt = globalClock.getDt()
        is_down = self.mouseWatcherNode.is_button_down if self.mouseWatcherNode else None
        if is_down:
            if is_down("arrow_left") or is_down("a"):
                self.pivot.setH(self.pivot.getH() - self.rotate_speed * dt)
            if is_down("arrow_right") or is_down("d"):
                self.pivot.setH(self.pivot.getH() + self.rotate_speed * dt)
            if is_down("arrow_up") or is_down("w"):
                self.pivot.setP(self.pivot.getP() + self.rotate_speed * dt)
            if is_down("arrow_down") or is_down("s"):
                self.pivot.setP(self.pivot.getP() - self.rotate_speed * dt)
            if is_down("q"):
                self.pivot.setR(self.pivot.getR() - self.rotate_speed * dt)
            if is_down("e"):
                self.pivot.setR(self.pivot.getR() + self.rotate_speed * dt)

            if is_down("page_up"):
                self.cam_distance -= self.zoom_speed * dt
            if is_down("page_down"):
                self.cam_distance += self.zoom_speed * dt

            # Clamp camera distance
            self.cam_distance = max(self.min_distance, min(self.cam_distance, self.max_distance))
            self.update_camera_position()

        return task.cont

    def update_camera_position(self):
        # Place camera at current distance, always looking at the model centre
        self.camera.setPos(0, -self.cam_distance, 0)
        self.camera.lookAt(self.cam_target)

app = GltfViewer()
app.run()