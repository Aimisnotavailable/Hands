from direct.showbase.ShowBase import ShowBase
from panda3d.core import getModelPath

class GltfViewer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        getModelPath().appendDirectory("MODEL")
        # Use noCache=True to ignore any cached .bam for this load
        model = self.loader.loadModel("MODEL/scene.gltf", noCache=True)
        model.reparentTo(self.render)

app = GltfViewer()
app.run()