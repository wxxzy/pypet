import sounddevice as sd
from pathlib import Path
import numpy as np
import librosa
import os

# This script serves as example to parsing the txt alignments. It will iterate over all 
# utterances of the dataset, split utterances on silences that are longer 0.4s and play them.
# (this does not change your files)

librispeech_root = "D:/dataset/ST-CMDS-20170001_1-OS"   # Replace with yours

def split_on_silences(audio_fpath, words, end_times):
    if not audio_fpath.exists():
        return
    # Load the audio waveform
    sample_rate = 16000     # Sampling rate of LibriSpeech 
    wav, _ = librosa.load(str(audio_fpath.absolute()), sample_rate)
    
    words = np.array(words)
    start_times = np.array([0.0] + end_times[:-1])
    end_times = np.array(end_times)
    assert len(words) == len(end_times) == len(start_times)
    assert words[0] == '' and words[-1] == ''
    
    # Break the sentence on pauses that are longer than 0.4s
    mask = (words == '') & (end_times - start_times >= 0.4)
    mask[0] = mask[-1] = True
    breaks = np.where(mask)[0]
    segment_times = [[end_times[s], start_times[e]] for s, e in zip(breaks[:-1], breaks[1:])]
    segment_times = (np.array(segment_times) * sample_rate).astype(np.int)
    wavs = [wav[segment_time[0]:segment_time[1]] for segment_time in segment_times]
    texts = [' '.join(words[s + 1:e]).replace("  ", " ") for s, e in zip(breaks[:-1], breaks[1:])]
    
    # Play the audio segments
    print("From %s" % audio_fpath)
    if len(wavs) > 1:
        print("This sentence was split in %d segments:" % len(wavs))
    else:
        print("There are no silences long enough for this sentence to be split:")
    for wav, text in zip(wavs, texts):
        # Pad the waveform with 1 second of silence because sounddevice tends to cut them early
        # when playing them. You shouldn't need to do that in your parsers.
        wav = np.concatenate((wav, [0] * sample_rate))
        print("\t%s" % text)
        sd.play(wav, sample_rate, blocking=True)
    print("")
    
    return wavs, texts

if __name__ == '__main__':
    data_root = Path(librispeech_root)
    speaker_dirs = data_root.glob("*.metadata")
    alignment_fpath = data_root.joinpath("ST-CMDS.alignment.txt")
    if not os.path.exists(alignment_fpath):
        raise Exception("Alignment file not found. Did you download and merge the txt "
                        "alignments with your LibriSpeech dataset?")
    alignment_file = open(alignment_fpath, "r")
    for line in alignment_file:
        utterance_id, words, end_times = line.strip().split(' ')
        words = words.replace('\"', '').split(',')
        end_times = [float(e) for e in end_times.replace('\"', '').split(',')]
        audio_fpath = data_root.joinpath(utterance_id + '.wav')
        # Split utterances on silences
        wavs, texts = split_on_silences(audio_fpath, words, end_times)
    alignment_file.close()
