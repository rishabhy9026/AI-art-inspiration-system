import os
import re
import json
import base64
import random
import requests
from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
print("DEBUG:", os.environ.get("GROQ_API_KEY"))

app = Flask(__name__, static_folder="Static", static_url_path="/static")
app.secret_key = os.environ.get("SECRET_KEY", "aria-secret-2024")
CORS(app, supports_credentials=True)

# ── Groq API ──────────────────────────────────────────────────────────────────
# FIX: Use the correct environment variable name "GROQ_API_KEY"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "mixtral-8x7b-32768"   # fast & free on Groq
GROQ_VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"  # vision model for image analysis

# ── Aria chatbot system prompt ────────────────────────────────────────────────
CHAT_SYSTEM = """You are Aria, a creative AI assistant inside an AI Art Studio app.
Your personality: warm, encouraging, imaginative, and concise.
Your job: help users craft amazing image ideas and prompts.

Rules:
- Keep replies short (3-5 sentences max unless listing ideas)
- Use simple, vivid language
- Always end with an actionable suggestion to try generating
- If user shares an idea, help refine it into a more vivid description
- Suggest lighting, mood, color palette, and composition when relevant
- Be enthusiastic but not over the top
- Use bullet points only when listing multiple ideas
"""

# ── Image analysis system prompt ─────────────────────────────────────────────
IMAGE_ANALYSIS_SYSTEM = """You are Aria, a creative AI art director and photo enhancement expert.
When given an image, analyze it and provide specific, actionable suggestions to make it better.

Your analysis should cover:
1. **Composition** – framing, rule of thirds, balance
2. **Lighting** – current lighting and how to improve it
3. **Color & Mood** – palette, contrast, atmosphere
4. **Style Enhancement** – which art styles would elevate this image
5. **AI Generation Prompt** – suggest a ready-to-use prompt to recreate/enhance this image

Keep your tone warm, encouraging, and specific. Format with clear sections.
End with a suggested prompt the user can paste directly into the generator."""

# ── Style presets ─────────────────────────────────────────────────────────────
STYLE_KEYWORDS = {
    "realistic":  "photorealistic, 8k ultra HD, cinematic lighting, hyperdetailed, shot on Sony A7R, depth of field",
    "anime":      "anime style, vibrant colors, Studio Ghibli inspired, detailed linework, soft shading, beautiful scenery",
    "cartoon":    "cartoon style, bold outlines, bright flat colors, Pixar-inspired, expressive characters",
    "oil_paint":  "oil painting, impressionist brushstrokes, rich textures, museum quality, painterly, canvas texture",
    "watercolor": "watercolor painting, soft washes, delicate details, translucent layers, artistic, dreamy",
    "cyberpunk":  "cyberpunk, neon lights, rain-soaked streets, dystopian future, dark atmosphere, high contrast",
    "fantasy":    "epic fantasy, magical atmosphere, detailed worldbuilding, dramatic lighting, mystical, ethereal",
    "minimalist": "minimalist, clean composition, negative space, simple geometric forms, elegant, modern",
}


# ── Groq Helpers ──────────────────────────────────────────────────────────────

def groq_chat(messages: list, system: str = "") -> str:
    """Send chat to Groq and return text response."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set in .env file")

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "system", "content": system}] + messages if system else messages,
        "max_tokens": 512,
        "temperature": 0.8,
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    r = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


def groq_vision_chat(messages: list, system: str = "") -> str:
    """Send vision chat (with image) to Groq and return text response."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set in .env file")

    payload = {
        "model": GROQ_VISION_MODEL,
        "messages": [{"role": "system", "content": system}] + messages if system else messages,
        "max_tokens": 1024,
        "temperature": 0.8,
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    r = requests.post(GROQ_URL, json=payload, headers=headers, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


def story_to_prompt(story: str, style: str) -> str:
    """Convert a story/idea into an optimized image generation prompt using Groq."""
    style_suffix = STYLE_KEYWORDS.get(style.lower(), STYLE_KEYWORDS["realistic"])

    try:
        messages = [{
            "role": "user",
            "content": f"""Convert this creative idea into a vivid, detailed image generation prompt (max 90 words).
Focus on: subject, environment, lighting, mood, color palette, composition.
Idea: "{story}"
Style to append: {style_suffix}

Return ONLY the final prompt text. No explanations, no quotes, no labels."""
        }]
        enhanced = groq_chat(messages)
        if style_suffix.split(",")[0] not in enhanced:
            enhanced = f"{enhanced}, {style_suffix}"
        return enhanced
    except Exception as e:
        print(f"Prompt enhancement error: {e}")
        return f"{story.strip()}, {style_suffix}, masterpiece, highly detailed"


def generate_image_pollinations(prompt: str, seed: int = None, width: int = 768, height: int = 512) -> str:
    """Generate image via Pollinations.ai and return base64."""
    if seed is None:
        seed = random.randint(1, 999999)

    quality_boost = "masterpiece, best quality, highly detailed, sharp focus"
    full_prompt = f"{prompt}, {quality_boost}"

    encoded = requests.utils.quote(full_prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width={width}&height={height}&seed={seed}"
        f"&nologo=true&enhance=true&model=flux"
    )
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    return base64.b64encode(r.content).decode("utf-8")


# ── Auth Routes ───────────────────────────────────────────────────────────────

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    # Accept ANY non-empty username and password
    if username and password:
        session["user"] = username
        return jsonify({"ok": True, "username": username})
    return jsonify({"ok": False, "error": "Please enter a username and password."}), 401


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/me", methods=["GET"])
def me():
    if "user" in session:
        return jsonify({"ok": True, "username": session["user"]})
    return jsonify({"ok": False}), 401


# ── Page Routes ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("Static", "login.html")


@app.route("/app")
def main_app():
    return send_from_directory("Static", "index.html")


# ── Chat Route ────────────────────────────────────────────────────────────────

@app.route("/api/chat", methods=["POST"])
def chat():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json(force=True)
    history = data.get("history", [])
    user_msg = (data.get("message") or "").strip()

    if not user_msg:
        return jsonify({"error": "Message is required."}), 400

    messages = history[-20:] + [{"role": "user", "content": user_msg}]

    try:
        reply = groq_chat(messages=messages, system=CHAT_SYSTEM)
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"error": f"Chat failed: {str(e)}"}), 500


# ── Image Analysis Route (NEW) ────────────────────────────────────────────────

@app.route("/api/analyze-image", methods=["POST"])
def analyze_image():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json(force=True)
    image_data = data.get("image")       # base64 string
    image_type = data.get("type", "image/jpeg")  # mime type
    user_note  = (data.get("note") or "").strip()

    if not image_data:
        return jsonify({"error": "No image provided."}), 400

    # Build user message with image
    user_content = [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:{image_type};base64,{image_data}"
            }
        }
    ]

    if user_note:
        user_content.append({
            "type": "text",
            "text": f"Please analyze this image and suggest how to make it better. User note: {user_note}"
        })
    else:
        user_content.append({
            "type": "text",
            "text": "Please analyze this image and provide detailed suggestions to make it more stunning and visually appealing. Also give me an AI generation prompt to recreate or enhance it."
        })

    messages = [{"role": "user", "content": user_content}]

    try:
        reply = groq_vision_chat(messages=messages, system=IMAGE_ANALYSIS_SYSTEM)
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Image analysis error: {e}")
        return jsonify({"error": f"Image analysis failed: {str(e)}"}), 500


# ── Image Generation Route ────────────────────────────────────────────────────

@app.route("/api/generate", methods=["POST"])
def generate():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json(force=True)
    story = (data.get("story") or "").strip()
    style = (data.get("style") or "realistic").strip()
    variations = int(data.get("variations", 1))
    variations = max(1, min(variations, 4))
    width = int(data.get("width", 768))
    height = int(data.get("height", 512))

    if not story:
        return jsonify({"error": "Story/prompt is required."}), 400

    try:
        prompt = story_to_prompt(story, style)
    except Exception as e:
        prompt = f"{story}, {STYLE_KEYWORDS.get(style, '')}, masterpiece"

    images = []
    base_seed = random.randint(1, 100000)
    for i in range(variations):
        seed = base_seed + i * 137
        try:
            img_b64 = generate_image_pollinations(prompt, seed=seed, width=width, height=height)
            images.append({"seed": seed, "data": img_b64})
        except Exception as e:
            images.append({"seed": seed, "error": str(e)})

    return jsonify({"prompt": prompt, "images": images, "style": style})


# ── Styles Info Route ─────────────────────────────────────────────────────────

@app.route("/api/styles", methods=["GET"])
def get_styles():
    styles = [
        {"id": "realistic",  "name": "Realistic",   "icon": "📷"},
        {"id": "anime",      "name": "Anime",        "icon": "✨"},
        {"id": "cartoon",    "name": "Cartoon",      "icon": "🎨"},
        {"id": "oil_paint",  "name": "Oil Paint",    "icon": "🖌️"},
        {"id": "watercolor", "name": "Watercolor",   "icon": "💧"},
        {"id": "cyberpunk",  "name": "Cyberpunk",    "icon": "🌃"},
        {"id": "fantasy",    "name": "Fantasy",      "icon": "🔮"},
        {"id": "minimalist", "name": "Minimalist",   "icon": "⬜"},
    ]
    return jsonify({"styles": styles})


if __name__ == "__main__":
    app.run(debug=True, port=5000)