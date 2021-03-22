from click import echo, style
from esccol_map_renderer import EsccolMapRenderer
from PIL import Image
import numpy as np
from glob import glob
from argparse import ArgumentParser

echo(style('importing TensorFlow...', fg='bright_green'))
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow import keras


class LazyObject:
    def __init__(self, creator):
        self._object = None
        self._creator = creator

    def get(self):
        if self._object is None:
            self._object = self._creator()
        return self._object


def create_model():
    return keras.models.load_model('esccol_model')


model_lazyobject = LazyObject(creator=create_model)


def load_image(fp: str, longer_size: int) -> np.ndarray:
    img: Image.Image = Image.open(fp)
    width, height = img.size
    r = min(longer_size / width, longer_size / height)
    img: Image.Image = img.resize((int(width * r), int(height * r)), resample=Image.HAMMING)
    img: np.ndarray = np.asarray(img, dtype=np.float) / 255.
    return img


class ImageRenderer:
    def __init__(self, longer_size: int = 50):
        self._esccol_map_renderer: EsccolMapRenderer = EsccolMapRenderer()
        self._longer_size: int = longer_size
        self._model: keras.Model = model_lazyobject.get()

    def prepare(self, fp: str, verbose: bool = False):
        img: np.ndarray = load_image(fp=fp, longer_size=self._longer_size)
        H, W, channels = img.shape
        assert channels == 3
        rgb_colors: np.ndarray = img.reshape((H * W, 3))
        esccol_number_confidences: tf.Tensor = self._model.predict(rgb_colors)
        esccol_numbers: tf.Tensor = tf.math.argmax(esccol_number_confidences, axis=1)
        esccol_number_map: tf.Tensor = tf.reshape(tensor=esccol_numbers, shape=(H, W))
        self._esccol_map_renderer.prepare(esccol_number_map)
        if verbose: echo(style(f'読み込み完了:{fp}', fg='green'))

    def render(self):
        self._esccol_map_renderer.render()


if __name__ == '__main__':
    parser = ArgumentParser(description='画像を表示する')
    parser.add_argument('fp', help='画像ファイルパス', type=str)
    parser.add_argument('--s',help='画像の長い方の一辺のピクセル数',type=int,default=50)
    args = parser.parse_args()
    renderer = ImageRenderer(longer_size=args.s)
    renderer.prepare(args.fp)
    renderer.render()
