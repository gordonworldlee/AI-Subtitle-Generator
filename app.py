import os
import pytube
import time
import math 
import ffmpeg 
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator



def extract_audio(input_file):
    extracted_audio = f"audio-{input_file}.wav"
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True, cmd=r'C:\ffmpeg-7.0.1-full_build\bin\ffmpeg.exe')
    return extracted_audio



def format(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours :02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    printed = f"{hours :02d}:{minutes:02d}:{seconds:02d}:{milliseconds:02d}"

    return formatted_time, printed

def transcribe(audio, fast):
    model = WhisperModel(fast)
    segments, info = model.transcribe(audio)
    language = info[0]
    #print(f" Transcription Language: {language}")
    segments = list(segments) # this is where the transcribe happens

    for segment in segments: 
        p1, formatted1 = format(segment.start)
        p2, formatted2 = format(segment.end)
        #print("[%s - %s] %s" % (formatted1, formatted2, segment.text))
    return language, segments




def generate_subs(input, language, segments):
    file = f"sub-{input}.{language}.srt"
    text = ""
    for index, segment in enumerate(segments):
        segment_start, x1 = format(segment.start)
        segment_end, x2 = format(segment.end)

        text += f"{str(index + 1)}\n"
        text += f"{segment_start} --> {segment_end}\n"
        if language != 'en':
            translated = GoogleTranslator(source='auto', target='en').translate(text=segment.text)
            text += f"{translated}\n\n"
        else:
            text += f"{segment.text}\n\n"
    f = open(file, "w")
    f.write(text)
    f.close()
    return file



def embed_subs(title, file, language):
    video_input_stream = ffmpeg.input(title)
    subtitle_input_stream = ffmpeg.input(file)
    output_video = f"output-{title}-{language}.mp4"
    subtitle_track_tile = file.replace(".srt","")
    stream = ffmpeg.output(video_input_stream, output_video,
                           vf = f"subtitles={file}")
    ffmpeg.run(stream, overwrite_output=True, cmd=r'C:\ffmpeg-7.0.1-full_build\bin\ffmpeg.exe')
    return output_video


