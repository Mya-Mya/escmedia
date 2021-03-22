from img_renderer import ImageRenderer
from argparse import ArgumentParser
from time import sleep, time
from glob import glob
from typing import List
import os
from click import style, echo, clear, confirm
from concurrent.futures import ThreadPoolExecutor
from subprocess import call

MOVIE_EXTS = ['mov', 'mp4', 'gif']
CURRENT_DIRECTORY = os.path.abspath(os.path.split(__file__)[0])


def is_movie(fp: str):
    ext = os.path.splitext(fp)[1][1:].lower()
    return ext in MOVIE_EXTS


def movie2images(movie_path: str, fps: int, update: bool = False):
    directory, basename = os.path.split(movie_path)
    name, ext = os.path.splitext(basename)
    dst_directory = os.path.join(directory, name)
    if update or not os.path.exists(dst_directory):
        try:
            os.removedirs(dst_directory)
        except:
            pass
        os.mkdir(dst_directory)
        os.chdir(CURRENT_DIRECTORY)
        call(f'ffmpeg -i {movie_path} -vf scale=360:-1 -r {fps} -f image2 {dst_directory}/%06d.jpg')
    return dst_directory


if __name__ == '__main__':
    parser = ArgumentParser(description='名称が連番になっている画像ファイルを次々と表示する')
    parser.add_argument('target', help='画像ファイルが入っているディレクトリ又は動画ファイル', type=str)
    parser.add_argument('--fps', help='1秒あたりに表示する画像数', default=5, type=int)
    parser.add_argument('--s', help='画像の長辺のピクセル数', default=50, type=int)
    args = parser.parse_args()

    img_directory = args.target
    # args.targetに動画ファイルを指定された場合
    if is_movie(args.target):
        img_directory = movie2images(movie_path=args.target, fps=args.fps)

    # レンダラーのインスタンスを起動
    img_files: list = sorted(glob(os.path.join(img_directory, '*')))
    img_basenames: list = list(map(os.path.basename, img_files))
    renderers: List[ImageRenderer] = [
        ImageRenderer(longer_size=args.s)
        for _ in img_files
    ]

    # 画像を読み込む
    echo(style('全ての画像の読み込み中', fg='bright_green'))
    with ThreadPoolExecutor() as executor:
        for img_file, renderer in zip(img_files, renderers):
            executor.submit(renderer.prepare, fp=img_file, verbose=True)

    # アニメーションを表示する
    delta_t = 1. / args.fps
    processing_delay = False
    while confirm(style('再生しますか?', fg='bright_red')):
        for renderer, img_basename in zip(renderers, img_basenames):
            # 画面への描画
            start = time()
            clear()
            echo(style(img_basename, fg='green'))
            renderer.render()
            if processing_delay: echo(style('処理落ち発生中', fg='bright_red'))

            # フレーム切り替えまでの残り時間を計算
            time_for_rendering = time() - start
            remaining_time = delta_t - time_for_rendering
            if remaining_time < 0:
                processing_delay = True
            else:
                sleep(remaining_time)

    echo(style('終了', fg='bright_green'))
