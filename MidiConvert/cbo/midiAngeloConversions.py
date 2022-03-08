from itertools import groupby
from unittest import skip

import pygame
from PIL import Image
from midiutil import MIDIFile

A0_NOTE = 21
C8_NOTE = 108

# helper functions for conversions

def lerp(min, max, note):
  return int(min + note * (max - min))


def convert_rgb_to_note(r, g, b):
  return lerp(A0_NOTE, C8_NOTE, int((r+g+b)/6.0)/255.0)


def add_note(song, track, pitch, time, duration):
  song.addNote(track, 0, pitch, time, duration, 100)


def create_midi(tempo, data):
  #print('Converting to MIDI.')
  song = MIDIFile(1)
  song.addTempo(0, 0, tempo)

  grouped = [(note, sum(1 for i in g)) for note, g in groupby(data)]
  time = 0
  for note, duration in grouped:
    add_note(song, 0, note, time, duration)
    time += duration
  return song


def play_midi(music_file):
  clock = pygame.time.Clock()
  try:
    pygame.mixer.music.load(music_file)
    # print("Music file %s loaded. Press Ctrl + C to stop playback." % music_file)
  except Exception as e:
    # print("Error loading file: %s - %s" % (music_file, e))
    return
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
    clock.tick(30)


def get_song_data(filename):
  try:
    im = Image.open(filename).convert('RGB')
  except Exception as e:
    # print("Error loading image: %s" % e)
    raise SystemExit
  # print("Img %s loaded." % filename)
  w, h = im.size
  return [convert_rgb_to_note(*im.getpixel((x, y))) for y in range(h) for x in range(w)]


def convert(img_file, midi_file, play):
  pygame.init()
  data = get_song_data(img_file)
  song = create_midi(240, data)

  return song
  with open(midi_file, 'wb') as f:
    song.writeFile(f)

  if play:
    try:
      play_midi(midi_file)
    except KeyboardInterrupt:
      pygame.mixer.music.fadeout(1000)
      pygame.mixer.music.stop()
      raise SystemExit

"""
unpacks data string into an array/grid of pixel values, returns a NxM nested list
"""
def unpackDataString(str):
    str = str.replace("\n","\\n")
    str = str.split("\\n")
    del str[-1]
    result = []
    for row in str:
        row = row.replace("(","")
        row = row.replace(")","")
        row = row.split(" ")
        del row[-1]
        newrow = []
        for pixel in row:
            pixel = pixel.split(",")
            for i in range(0, len(pixel)):
              pixel[i] = int(pixel[i])
            newrow.append(pixel)
        result.append(newrow)
    return result


# End of Helper Functions, The last three are funtions you would wnat to call upon

"""
Converts a nested list of pixel RGB values into an image
@:param outputFileName -> name of the image file that will be exported. it will be saved in the woring directoru 
@:param P -> A NxM nested list of pixel values 
    example: [[[r,g,b],[r,g,b]],[r,g,b],[r,g,b]] would represent a 2x2 image
@param scale -> the magnification factor of the generated image. its main purpose
    is for exporting images for the user to look at
@param show -> false by default. displays the image after generation, not recomended outside of testing
"""
def canvas2image(outputFileName, dataString, scale, show=False):

    P = unpackDataString(dataString)
    N = len(P)
    M = len(P[0])

    img = Image.new('RGB', (N, M), color=0)
    # img.show()
    pixels = img.load()

    for i in range(img.size[0]):  # for every pixel:
        for j in range(img.size[1]):
            newPix = P[i][j]
            pixels[i, j] = (newPix[0], newPix[1], newPix[2])

    intscale = (int)(scale)

    img = img.resize((img.size[0]*intscale,img.size[1]*intscale),Image.NEAREST)

    if show == True:
        img.show()

    img.save(outputFileName + "x"+(str)(scale)+".PNG")
    img.close()


"""
Converts a image into a midi file
@:param inputFileName -> name/path of the image file to be converted
@:param outputFileName -> the name of the midi file being generated. it will be saved in the working directory
@:param playback -> false by default. Played the midi file after conversion. not recomended outside of testing
"""
def image2midi(inputFileName,outputFileName,playback=False):
    convert(inputFileName,outputFileName,playback)


""" 
Converts a nested list of pixel RGB values into a midi file
@:param outputFileName -> the name of the midi file being generated. it will be saved in the working directory
@:param P -> A NxM nested list of pixel values 
    example: [[[r,g,b],[r,g,b]],[r,g,b],[r,g,b]] would represent a 2x2 image
@param show -> false by default. displays the image after generation, not recomended outside of testing
@:param playback -> false by default. Played the midi file after conversion. not recomended outside of testing
"""
def canvas2midi(outputFileName, P, show=False, playback=False):
    canvas2image(outputFileName+"-canvas2midiTEMP",P,1,show)
    return convert(outputFileName+"-canvas2midiTEMPx1.PNG",outputFileName+".midi",playback)