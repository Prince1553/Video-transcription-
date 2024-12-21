from django.shortcuts import render
from django.http import JsonResponse
import whisper
import os
from collections import Counter
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import string
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

# Ensure punkt is downloaded
nltk.download('punkt')

# Load the Whisper model
model = whisper.load_model("base")

def home(request):
    return render(request, 'home.html')

def upload_video(request):
    if request.method == 'POST' and request.FILES['video']:
        video = request.FILES['video']
        video_path = f"media/{video.name}"
        with open(video_path, 'wb+') as destination:
            for chunk in video.chunks():
                destination.write(chunk)

         
        result = model.transcribe(video_path)
        transcription = result["text"]

        os.remove(video_path)   
        return JsonResponse({'transcription': transcription})
    return render(request, 'upload.html')

def search_word(request):
    transcription = request.GET.get('transcription', '')
    word = request.GET.get('word', '').lower()
    transcription_lower = transcription.lower()

    if word in transcription_lower:
        return JsonResponse({'found': True, 'message': f"'{word}' found!"})
    else:
        return JsonResponse({'found': False, 'message': f"'{word}' not found!"})

def count_word(request):
    transcription = request.GET.get('transcription', '')
    word = request.GET.get('word', '').lower()

    transcription = transcription.lower().translate(str.maketrans("", "", string.punctuation))
    word_count = Counter(transcription.split())[word]
    return JsonResponse({'word': word, 'count': word_count})

def generate_summary(request):
    transcription = request.GET.get('transcription', '')

    if not transcription.strip():
        return JsonResponse({'error': 'Transcription text is empty.'}, status=400)

    try:
        # Parse the transcription text
        parser = PlaintextParser.from_string(transcription, Tokenizer("english"))

        # Initialize the TextRank summarizer
        summarizer = TextRankSummarizer()

        # Generate the summary (extractive)
        summary = summarizer(parser.document, sentences_count=8)  # Adjust the number of sentences

        # Return the summary as a JSON response
        return JsonResponse({'summary': [str(sentence) for sentence in summary]})
    except Exception as e:
        # Handle any exceptions
        return JsonResponse({'error': str(e)}, status=500)
