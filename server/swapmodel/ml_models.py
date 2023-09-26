import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image


class FaceSwapModel:
    def __init__(self):
        self.app = FaceAnalysis(name='buffalo_l')
        self.swapper = insightface.model_zoo.get_model('swapmodel/inswapper_128.onnx',
                                                       download=False,
                                                       download_zip=False)
        self.app.prepare(ctx_id=0, det_size=(640,640))

    def face_detection(self, img):
        faces = self.app.get(img)
        return faces

    def face_swapping(self,
                      target_img,
                      source_faces,
                      target_faces,
                      target_idx,
                      source_idx):

        img_copied = target_img.copy()
        target_face = target_faces[target_idx]
        source_face = source_faces[source_idx]

        result = self.swapper.get(img_copied, target_face, source_face, paste_back=True)

        return result
