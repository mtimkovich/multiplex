import argparse
import cv2
import os
import shutil
import subprocess
import sys


def check_for_ffmpeg():
    with open(os.devnull, 'w') as devnull:
        try:
            ret = subprocess.call(['ffmpeg', '-version'], stdout=devnull)
        except OSError:
            ret = 1

        if ret != 0:
            print 'ffmpeg not installed'
            sys.exit(1)

check_for_ffmpeg()

parser = argparse.ArgumentParser('combine videos')
parser.add_argument('videos', nargs='+',
                    help='video files to combine')
parser.add_argument('--output', '-o', default='output.mp4',
                    help='filename to output to (default: output.mp4)')
parser.add_argument('--frame-rate', '-f', type=int, default=30,
                    help='video frame rate (default: 30)')
args = parser.parse_args()

cwd = os.getcwd()

videos = [os.path.abspath(v) for v in args.videos]
captures = [cv2.VideoCapture(v) for v in videos]

width = int(captures[0].get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(captures[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width, height)

os.mkdir('tmp')
comb = 'combined.mp4'
out_file = os.path.join('tmp', comb)

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter(out_file, fourcc, args.frame_rate, size)

# Combine video frames

while True:
    comb_frame = None
    num_finished = 0

    for v in captures:
        ret, frame = v.read()

        if not ret:
            num_finished += 1
            continue

        frame = cv2.resize(frame, size)

        if comb_frame is None:
            comb_frame = frame.copy()
        else:
            alpha = 0.75
            comb_frame = cv2.addWeighted(comb_frame, alpha, frame, 1-alpha, 0)

    if num_finished == len(captures):
        break

    out.write(comb_frame)

for v in captures:
    v.release()

out.release()

# Combine the audio
os.chdir('tmp')

# Extract audio
fns = []
for v in videos:
    fn, ext = os.path.splitext(v)
    fn = os.path.basename(fn)
    fns.append(fn)
    ret = subprocess.call('ffmpeg -i "{}" -ab 160k -ac 2 -ar 44100 -vn "{}.wav"'
                          .format(v, fn), shell=True)

    if ret != 0:
        sys.exit(1)

# Combine audio
inputs = ''.join(' -i "{}.wav"'.format(fn) for fn in fns)
output_wav = 'output.wav'

ret = subprocess.call('ffmpeg {} -filter_complex amix=inputs={} {}'
                      .format(inputs, len(videos), output_wav), shell=True)

if ret != 0:
    sys.exit(1)

# Replace audio on video
ret = subprocess.call('ffmpeg -i {} -i {} -c:v copy -map 0:v:0 -map 1:a:0 {}'
                      .format(comb, output_wav, args.output), shell=True)

if ret != 0:
    sys.exit(1)

os.chdir(cwd)
os.rename(os.path.join('tmp', args.output), args.output)

# Clean up
shutil.rmtree('tmp')
