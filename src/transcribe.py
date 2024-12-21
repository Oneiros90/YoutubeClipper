import whisper
import re

import warnings
warnings.filterwarnings('ignore', module='whisper')

model = whisper.load_model("small")

def transcribe_audio(file_path):
    result = model.transcribe(file_path, word_timestamps=True)
    transcription = {
        "words": [],
        "text": ""
    }
    for segment in result["segments"]:
        for word in segment["words"]:
            transcription["words"].append(word)
    transcription["text"] = "".join(word["word"] for word in transcription["words"])
    return transcription

def find_phrase(transcription, phrase_regex):
    matches = re.finditer(phrase_regex, transcription["text"], re.IGNORECASE)
    results = []
    
    for match in matches:
        match_start_idx = match.start()
        match_end_idx = match.end()

        # Find the words that overlap with the match
        start_time = None
        end_time = None
        current_pos = 0

        for word in transcription["words"]:
            word_start = current_pos
            word_end = current_pos + len(word["word"])
            current_pos += len(word["word"])

            if word_start <= match_start_idx < word_end and start_time is None:
                start_time = word["start"]
            if word_start < match_end_idx <= word_end:
                end_time = word["end"]

        if start_time is not None and end_time is not None:
            results.append({"text": match.group(), "start": start_time, "end": end_time})
    
    return results

if __name__ == "__main__":
    print("Testing whisper.py")
    audio_path = input("Enter an audio file path: ")
    transcription = transcribe_audio(audio_path)
    print(transcription)
