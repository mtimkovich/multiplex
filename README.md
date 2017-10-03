# Multiplex

Watch multiple videos at the same time!

![preview](https://i.imgur.com/xbjH9a0h.png)

## Installation

Multiplex requires ffmpeg installed to work.

```bash
virtualenv env
source env/bin/activate
pip install requirements.txt
```

## Usage

```
usage: combine videos [-h] [--output OUTPUT] [--frame-rate FRAME_RATE]
                      videos [videos ...]

positional arguments:
  videos                video files to combine

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        filename to output to (default: output.mp4)
  --frame-rate FRAME_RATE, -f FRAME_RATE
                        video frame rate (default: 30)
```

## Issues

- Videos must have the same frame rate
- Output videos are much larger than input videos

## Author

Max Timkovich

## License

Multiplex is licensed under the MIT license.
