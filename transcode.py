from argparse import ArgumentParser
import math
import re
import json
import os
from ffmpeg import *

'''
supported video codecs: h264, h265
supported audio codecs: aac, ac3, mp3, vorbis, opus
'''
def convert_size(raw_size):
   sizes = {
   'KB': math.pow(2, 0),
   'MB': math.pow(2, 10),
   'GB': math.pow(2, 20)
   }
   matches = re.match(r'([0-9]+)([a-zA-Z]{2})', raw_size)
   return int(matches.group(1)) * sizes[matches.group(2)]

encoders = {
    'h264': 'libx264',
    'h265': 'libx265',
    'aac': 'aac',
    'mp3': 'libmp3lame',
    'vorbis': 'libvorbis',
    'opus': 'libopus'
}

parser = ArgumentParser()
parser.add_argument('-i', '--input', type=str, required=True)
parser.add_argument('-o', '--output', type=str, required=True)
constraints =  parser.add_mutually_exclusive_group(required=True)
constraints.add_argument('-s', '--size', type=str)
constraints.add_argument('-q', '--quality', type=int)
constraints.add_argument('--copy', action='store_true')
parser.add_argument('--vcodec', type=str)
parser.add_argument('--acodec', type=str)
args = parser.parse_args()
codec = []

probe = json.loads(probe(args.input))
is_video = False
for stream in probe['streams']:
    if stream['codec_type'] == 'video':
        is_video = True
        break

if args.vcodec:
    codec.append(encoders[args.vcodec])
if args.acodec:
    codec.append(encoders[args.acodec])

if args.size:
    # bitrate calculation
    duration = float(probe['format']['duration'])
    target_size = convert_size(args.size)
    total_rate = target_size * 8 / duration
    if is_video:
        video_rate, audio_rate = int(), int()
        if total_rate < 500:
            print("Target size too low!")
            exit(1)
        elif 500 < total_rate < 2000:
            audio_rate = 64
        elif 2000 < total_rate < 4000:
            audio_rate = 128
        elif 4000 < total_rate < 8000:
            audio_rate = 224
        elif 8000 < total_rate < 15000:
            audio_rate = 448
        video_rate = total_rate - audio_rate
        transcode_size(args.input, args.output, 'video', codec, [str(video_rate)+'K', str(audio_rate)+'K'])
    else:
        transcode_size(args.input, args.output, 'audio', codec, [str(total_rate)+'K'])
elif args.quality:
    quality = args.quality
    qualities = {
    1: (25, 64),
    2: (23, 128),
    3: (20, 224),
    4: (18, 256),
    5: (16, 448)
    }
    if is_video:
        transcode_qual(args.input, args.output, 'video', codec, [str(qualities[quality][0]), str(qualities[quality][1])+'K'])
    else:
        transcode_qual(args.input, args.output, 'audio', codec, [str(qualities[quality][1])+'K'])