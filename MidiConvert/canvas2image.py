import sys
import midiAngeloConversions

n = len(sys.argv)
if n != 4 :
    print("INVALID INPUT: Three inputs required,", n-1,"provided.\n REQUIRED PARAMITERS: outputFileName PixelArray scale")
    exit(1)

midiAngeloConversions.canvas2image(sys.argv[1],sys.argv[2],sys.argv[3])