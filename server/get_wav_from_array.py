import numpy as np
import scipy.io.wavfile as wav
import sys

SAMPLE_RATE = 16000

def to_wav(load_path, load_name):
    print(f"load path: {load_path}")
    target_path = f"./feedback_raw_audio/{load_name}.wav"
    print(f"target path: {target_path}")

    raw_arr = np.load(load_path, allow_pickle=True)
    scaled_arr = np.int16(raw_arr / np.max(np.abs(raw_arr)) * 32767)

    wav.write(target_path, SAMPLE_RATE, scaled_arr)

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("USAGE: python get_wav_from_array.py load_name")
        print("\t no need to end with .npy")
        print("\t this will directly use directory_path: ./feedback_collection/")
        print("\t or USE: python get_wav_from_array.py directory_path load_name")
    else:
        if len(args) == 3:
            path = args[1] + "/" + args[2] + ".npy"
            name = args[2]
        else:
            path = "./feedback_collection/" + args[1] + ".npy"
            name = args[1]
        to_wav(path, name)