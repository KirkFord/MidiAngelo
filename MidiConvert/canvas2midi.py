import sys
import midiAngeloConversions

n = len(sys.argv)
if n != 3 :
    print("INVALID INPUT: Three inputs required,", n-1,"provided.\n REQUIRED PARAMITERS: inputFileName outputFileName")
    exit(1)

print("calling ")
midiAngeloConversions.canvas2midi(sys.argv[1],sys.argv[2])