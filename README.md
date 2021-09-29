# ffconsole
An extremely barebones command line wrapper for ffmpeg.
## Installation
1. Clone this repository
  ```sh
  git clone https://github.com/alfa-carinae/ffconsole.git
  ```
2. Open your terminal and change to the cloned directory.
3. Run `transcode.py`.
## Requirements
`ffmpeg` and `ffprobe` should be installed and added to the path. You can download them from their [website](https://ffmpeg.org/).
## Usage
```sh
python transcode.py <arguments>
```
### Supported arguments
- `-i, --input <file>` to point to an input file.
- `-o, --output <file>` to set the output file. Output container is selected automatically from the file name.
- `-s, --size <size>` to target an output size, should be of the format `<size><KB/MB/GB>`.
- `-q, --quality <quality>` to target a quality.
  - Five quality presets have been defined, namely 1-5, 1 being the lowest and 5 being the highest.
  - Note that quality and size are mutually exclusive, only one of the arguments should be provided.
  - Currently, the quality parameter ensures only the video is of a target quality, and hence of a variable bitrate. The audio is still of constant bitrate, predetermined according to the set quality.
- `--vcodec` to set the output video codec. Currently, `h264` and `h265` are supported.
- `--acodec` to set the output audio codec. Currently, `aac`, `mp3`, `vorbis` and `opus` are supported.
- `--retain` to retain the input video and audio codec.
### Examples
- ```sh
  python .\transcode.py --input .\tmp.mp4 --retain -q 1 --output tmp.mkv
  ```
- ```sh
  python .\transcode.py --input .\tmp.mp4 -s 10MB --vcodec h265 --acodec opus --output tmp.mkv
  ```
- ```sh
  python .\transcode.py --input .\tmp.mp4 -q 3 --vcodec h264 --acodec aac --output out.mp4
  ```
 
