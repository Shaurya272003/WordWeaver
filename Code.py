!pip install transformers nltk fpdf
!pip install nltk
!python -m nltk.downloader averaged_perceptron_tagger
!pip install pyttsx3
!pip install comtypes
# !pip install espeak
# !espeak --version
# !ls -l /usr/local/lib/ | grep libespeak.so.1
# !sudo apt-get install espeak
!apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg
!pip install pyaudio
!pip install gtts
!apt-get update
!apt-get install libespeak1
!pip install pydub
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re
from gtts import gTTS
from pydub import AudioSegment

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Function to initialize WordNet Lemmatizer
lemmatizer = WordNetLemmatizer()

# Define a function to extract idioms from the text
def extract_idioms(text):
    # Define a regular expression pattern to match idioms
    idiom_pattern = r'\b(?:at the end of the day|back to square one|ball is in your court)\b'  # Add more idioms as needed

    # Extract idioms from the text
    idioms = re.findall(idiom_pattern, text)
    return idioms

# Function to get word meanings from WordNet
def get_word_meanings(word):
    synsets = wordnet.synsets(word)
    meanings = []
    for synset in synsets[:1]:  # Limit to the first two meanings
        meanings.append(synset.definition())
    return meanings

# Function to categorize tokens into parts of speech and their meanings
def categorize_tokens(tokens,text):
    parts_of_speech = {
        'noun': set(),
        'pronoun': set(),
        'adjective': set(),
        'verb': set(),
        'idiom': set(),  # Include idioms as a category
    }
    for word, pos in nltk.pos_tag(tokens):
        lemmatized_word = lemmatizer.lemmatize(word, pos='n')
        if pos.startswith('N'):
            parts_of_speech['noun'].add((word, lemmatized_word, tuple(get_word_meanings(lemmatized_word))))
        elif pos.startswith('PRP'):
            parts_of_speech['pronoun'].add((word, lemmatized_word, tuple(get_word_meanings(lemmatized_word))))
        elif pos.startswith('JJ'):
            parts_of_speech['adjective'].add((word, lemmatized_word, tuple(get_word_meanings(lemmatized_word))))
        elif pos.startswith('V'):
            parts_of_speech['verb'].add((word, lemmatized_word, tuple(get_word_meanings(lemmatized_word))))
    idioms = extract_idioms(text)
    for idiom in idioms:
        parts_of_speech['idiom'].add((idiom, idiom, tuple([idiom])))  # Assuming idiom meanings are the same as the idiom itself

    return parts_of_speech

# Function to convert text to speech using gTTS
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    return tts

# Function to combine audio files into one
def combine_audio(files, output_file):
    combined = None
    for file in files:
        sound = AudioSegment.from_mp3(file)
        if combined is None:
            combined = sound
        else:
            combined += sound
    # combined.export(output_file, format="mp3")
    # Check if there are any audio files
    if combined is not None:
        combined.export(output_file, format="mp3")
    else:
        print("No audio files to combine.")

# Prompt the user to enter the story
input_story = input("Enter the story: ")

# Tokenize the input story
tokens = word_tokenize(input_story)

# Perform part-of-speech tagging and categorize tokens
parts_of_speech = categorize_tokens(tokens,input_story)

# List to store generated audio texts
audio_texts = []

# Print parts of speech and meanings if tokens are present
if parts_of_speech:
    print("Custom Vocabulary Sheet:")
    print("-" * 30)
    for category, words in parts_of_speech.items():
        print(f"{category.capitalize()}:")
        for word, lemma, meanings in sorted(words):
            print(f"  {word} ({lemma}):")
            for meaning in meanings:
                print(f"    - {meaning}")
            # Convert each word's lemma to speech and add it to the audio texts
            audio_texts.append(lemma)
    print()
    # Combine all audio texts into one
    combined_audio = ""
    for text in audio_texts:
        combined_audio += text + " "
    # Convert combined text to speech
    tts = text_to_speech(combined_audio)
    # Save the combined speech as an audio file
    combined_file = "combined_output.mp3"
    tts.save(combined_file)
    print(f"Combined audio saved as: {combined_file}")

else:
    print("No tokens found in the input story. Please enter a valid story.")
