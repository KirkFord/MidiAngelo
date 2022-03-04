from PIL import Image

from itertools import groupby

import pygame, argparse
from PIL import Image
from midiutil import MIDIFile

A0_NOTE = 21
C8_NOTE = 108


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
  with open(midi_file, 'wb') as f:
    song.writeFile(f)

  if play:
    try:
      play_midi(midi_file)
    except KeyboardInterrupt:
      pygame.mixer.music.fadeout(1000)
      pygame.mixer.music.stop()
      raise SystemExit







def canvas2image(outputFileName, P, scale, show=False):
    N = len(P)
    M = len(P[0])

    img = Image.new('RGB', (N, M), color=0)
    # img.show()
    pixels = img.load()

    for i in range(img.size[0]):  # for every pixel:
        for j in range(img.size[1]):
            newPix = P[j][i]
            print(newPix)
            pixels[i, j] = (newPix[0], newPix[1], newPix[2])

    img = img.resize((img.size[0]*scale,img.size[1]*scale),Image.NEAREST)

    if show == True:
        img.show()

    img.save(outputFileName + "x"+(str)(scale)+".PNG")
    img.close()

def image2midi(inputFileName,outputFileName,playback=False):
    convert(inputFileName,outputFileName,playback)

def canvas2midi(outputFileName, P, show=False, playback=False):
    canvas2image(outputFileName+"-canvas2midiTEMP",P,1,show)
    # print(outputFileName)
    # print("yeet")

    convert(outputFileName+"-canvas2midiTEMPx1.PNG",outputFileName+".midi",playback)