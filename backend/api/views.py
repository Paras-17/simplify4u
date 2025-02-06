import json
import os
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit

from bs4 import BeautifulSoup
import re
# In views.py
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def summarize_view(request):
    return process_text(request, "summarize")

@csrf_exempt
def translate_view(request):
    return process_text(request, "translate")

@csrf_exempt
def analyze_view(request):
    return process_text(request, "analyze")

# Load Hugging Face API key from environment
HF_API_KEY = os.environ.get("HF_API_KEY")
if not HF_API_KEY:
    raise Exception("Hugging Face API key not set in environment variables.")

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# Define model endpoints for each task.
MODEL_ENDPOINTS = {
    "summarize": "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
    "translate": "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-mul-en",
    "analyze": "https://api-inference.huggingface.co/models/t5-base"  # Using T5 as a generic text-to-text model
}
@csrf_exempt
def preprocess_text(text):
    text = BeautifulSoup(text, "html.parser").get_text()  # Remove HTML
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)  # Remove markdown images
    text = re.sub(r"https?://\S+\.(jpg|jpeg|png|gif|webp|svg)", "", text)  # Remove image URLs
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize spaces
    return text

@csrf_exempt
def process_text(request, task):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "")

            if not text:
                return JsonResponse({"error": "Text input is required."}, status=400)

            clean_text = preprocess_text(text)  # Preprocess before sending to the model

            if task not in MODEL_ENDPOINTS:
                return JsonResponse({"error": "Invalid task. Use 'summarize', 'translate', or 'analyze'."}, status=400)

            payload = {"inputs": clean_text}
            response = requests.post(MODEL_ENDPOINTS[task], headers=HEADERS, json=payload)

            if response.status_code != 200:
                return JsonResponse({"error": response.json()}, status=response.status_code)

            result = response.json()
            output = result[0].get("summary_text") or result[0].get("translation_text") or result[0].get("generated_text")

            return JsonResponse({"response": output})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

@csrf_exempt
def call_inference_api(model_url, payload):
    response = requests.post(model_url, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return None, response.json()
    result = response.json()
    # Depending on the model, the output key might differ
    # For summarization, it's often "summary_text"; for translation, "translation_text"; for T5 it might be "generated_text"
    # We'll check for common keys:
    output = result[0].get("summary_text") or result[0].get("translation_text") or result[0].get("generated_text")
    return output, None

@csrf_exempt
@ratelimit(key='ip', rate=os.environ.get("RATE_LIMIT", "10/m"), block=True)
def summarize_text(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "")
            if not text:
                return JsonResponse({"error": "Text input is required."}, status=400)
            payload = {"inputs": text}
            output, error = call_inference_api(MODEL_ENDPOINTS["summarize"], payload)
            if error:
                return JsonResponse({"error": error}, status=500)
            return JsonResponse({"response": output})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

@csrf_exempt
@ratelimit(key='ip', rate=os.environ.get("RATE_LIMIT", "10/m"), block=True)
def translate_text(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "")
            if not text:
                return JsonResponse({"error": "Text input is required."}, status=400)
            payload = {"inputs": text}
            output, error = call_inference_api(MODEL_ENDPOINTS["translate"], payload)
            if error:
                return JsonResponse({"error": error}, status=500)
            return JsonResponse({"response": output})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

@csrf_exempt
@ratelimit(key='ip', rate=os.environ.get("RATE_LIMIT", "10/m"), block=True)
def analyze_text(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "")
            if not text:
                return JsonResponse({"error": "Text input is required."}, status=400)
            # Here we use T5 with a custom prompt for analysis.
            prompt = f"Analyze the following text and provide key insights:\n\n{text}"
            payload = {"inputs": prompt}
            output, error = call_inference_api(MODEL_ENDPOINTS["analyze"], payload)
            if error:
                return JsonResponse({"error": error}, status=500)
            return JsonResponse({"response": output})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)
