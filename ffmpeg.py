import os
import subprocess
import sys

def transcode_size(in_file, out_file, in_type, codec, params):
    cmd = ['ffmpeg', '-loglevel', 'quiet', '-i', in_file, '-map', '0']
    if in_type == 'video':
        cmd.extend(['-c:v', codec[0], '-b:v', params[0], '-c:a', codec[1], '-b:a', params[1]])
    elif in_type == 'audio':
        cmd.extend(['-c:a', codec[0], '-b:a', params[0]])
    cmd.append(out_file)
    subprocess.run(cmd)

def transcode_qual(in_file, out_file, in_type, codec, params):
    cmd = ['ffmpeg', '-loglevel', 'quiet', '-i', in_file, '-map', '0']
    if in_type == 'video':
        cmd.extend(['-c:v', codec[0], '-crf:v', params[0], '-c:a', codec[1], '-b:a', params[1]])
    elif in_type == 'audio':
        cmd.extend(['-c:a', codec[0], '-b:a', params[0]])
    cmd.append(out_file)
    subprocess.run(cmd)

def probe(in_file):
    command_array = [
        'ffprobe',
        '-loglevel', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        in_file
    ]
    result = subprocess.run(command_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return result.stdout
