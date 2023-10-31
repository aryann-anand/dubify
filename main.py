'''
View the Readme.md file to see all the required dependencies for installation.
'''

# Import dependencies
from translate import Translator as Dubify
from moviepy.editor import VideoFileClip, AudioFileClip, clips_array
from googletrans import Translator
from gtts import gTTS
import requests
import whisper
import os


# Load the video
vid_in = "input_video.mp4"

# video-to-audio
vid = VideoFileClip(vid_in)
aud = vid.audio

# save the converted audio file
# define the output audio path and filename
aud_out = "original_audio.mp3"

aud.write_audiofile(aud_out)

vid.close()
aud.close()

'''
======================================================================================================================
'''

# Load the model
# model = whisper.load_model("base")
model = whisper.load_model("medium")    # refer Readme for different models

'''
======================================================================================================================
'''

# SPEECH TO TEXT

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("original_audio.mp3")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
# options = whisper.DecodingOptions()                       # for GPU
options = whisper.DecodingOptions(fp16 = False)            # for CPU
result = whisper.decode(model, mel, options)

# extracting only the text
speech_in  = result.text

'''
==================================== Export the speech to a text file ==============================================
'''

file_path = "original_speech.txt"

# Open the file in write mode and write the text to it
with open(file_path, 'w') as file:
    file.write(speech_in)

'''
====================================== Dubbing text to new language text ============================================
'''

# English to Hindi
def translate_to_hindi(text):
    translator= Dubify(to_lang="hi")
    translation = translator.translate(text)
    return translation


# English to Tamil
def translate_to_tamil(text):
    translator = Dubify(to_lang="ta")
    translation = translator.translate(text)
    return translation

# Load the text file
with open('original_speech.txt', 'r', encoding='utf-8') as file:
    english_content = file.read()

# Method call for Hindi Translation
hindi_translation = translate_to_hindi(english_content)

# Method call for Tamil Translation
tamil_translation = translate_to_tamil(english_content)

'''
======================================= Export the Translated Text to file =========================================
'''

# Saving the new Hindi text file
with open('speech_hindi.txt', 'w', encoding='utf-8') as hindi_file:
    hindi_file.write(hindi_translation)

# Saving the new Tamil text file
with open('speech_tamil.txt', 'w', encoding='utf-8') as tamil_file:
    tamil_file.write(tamil_translation)


'''
==================================== Converting Translated text to Regional Audio ===================================
'''

# Method for conversion and exporting
def text_to_audio(text, output_file, lang):
    tts = gTTS(text, lang=lang)
    tts.save(output_file)

# Loading Hindi text
with open('speech_hindi.txt', 'r', encoding='utf-8') as hindi_file:
    hindi_text = hindi_file.read()

# Loading Tamil text
with open('speech_tamil.txt', 'r', encoding='utf-8') as tamil_file:
    tamil_text = tamil_file.read()


# Method call for Hindi Speech
text_to_audio(hindi_text, 'audio_hindi.mp3', 'hi')

# Method call for Tamil Speech
text_to_audio(tamil_text, 'audio_tamil.mp3', 'ta')