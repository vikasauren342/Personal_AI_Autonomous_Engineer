
import json
import re
from datetime import datetime


class ReliableReelDirector:
    """
    Production-oriented Reel Director.

    Design principle:
      Qwen = creative intelligence
      Python = deterministic production schema

    This prevents incomplete LLM JSON from breaking the pipeline.
    """

    def __init__(self, personal_ai):
        self.personal_ai = personal_ai

    def _extract_text(self, result):
        if isinstance(result, dict):
            for key in ("output", "text", "response", "content"):
                value = result.get(key)
                if isinstance(value, str):
                    return value
        return str(result)

    def _creative_metadata(self, concept):
        prompt = f"""
You are the creative director of a viral Instagram Reel.

Concept:
{concept}

Return ONLY one compact JSON object with exactly these keys:
"title", "hook", "audience", "visual_style", "ending"

Rules:
- Keep every value short.
- No markdown.
- No explanation.
- Do not create scenes.
- Do not create nested objects.
- Valid JSON only.
"""

        result = self.personal_ai.ask(prompt)

        raw = self._extract_text(result).strip()

        # Remove accidental markdown fences.
        raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.I)
        raw = re.sub(r"\s*```$", "", raw)

        match = re.search(r"\{.*\}", raw, flags=re.S)

        if match:
            try:
                data = json.loads(match.group(0))

                return {
                    "title": str(data.get("title", "")).strip(),
                    "hook": str(data.get("hook", "")).strip(),
                    "audience": str(data.get("audience", "Instagram viewers")).strip(),
                    "visual_style": str(
                        data.get("visual_style", "Realistic cinematic")
                    ).strip(),
                    "ending": str(
                        data.get("ending", "Direct-to-camera comedic punchline")
                    ).strip(),
                }
            except Exception:
                pass

        # Safe fallback if Qwen still produces malformed JSON.
        return {
            "title": "Funny AI Reel",
            "hook": "Wait till you see what happens next.",
            "audience": "Instagram viewers",
            "visual_style": "Realistic cinematic",
            "ending": "Direct-to-camera comedic punchline",
        }

    def build(self, concept):
        creative = self._creative_metadata(concept)

        # --------------------------------------------------------------
        # Deterministic production structure
        # --------------------------------------------------------------

        scenes = [
            {
                "scene_id": 1,
                "duration_seconds": 4,
                "visual_description": (
                    "Realistic orange cat sitting inside a slightly messy "
                    "Indian middle-class living room. Natural daylight."
                ),
                "camera": "Vertical medium shot, subtle handheld realism",
                "action": "Cat looks around the messy room with visible annoyance.",
                "dialogue": "Yaar, ye ghar hai ya daily disaster zone?",
                "voice_direction": "Natural Hinglish, annoyed but funny",
                "sound_effects": "Light room ambience",
                "caption": "Ye ghar hai ya disaster zone?",
                "video_prompt": (
                    "Photorealistic orange domestic cat in an Indian "
                    "middle-class living room, realistic fur, natural daylight, "
                    "messy household objects, expressive face, cinematic realism, "
                    "vertical 9:16, subtle handheld camera"
                ),
                "negative_prompt": (
                    "cartoon, animation, CGI look, deformed cat, extra limbs, "
                    "duplicate animal, distorted face, text artifacts"
                ),
            },
            {
                "scene_id": 2,
                "duration_seconds": 4,
                "visual_description": (
                    "Cat walks through the room inspecting scattered clothes "
                    "and household objects."
                ),
                "camera": "Low-angle tracking shot",
                "action": "Cat points its attention toward the mess and reacts dramatically.",
                "dialogue": "Koi cleaning bhi karta hai yahan, ya sab meri duty hai?",
                "voice_direction": "Frustrated comedic Hinglish",
                "sound_effects": "Small comedic percussion hit",
                "caption": "Sab meri duty hai?",
                "video_prompt": (
                    "Photorealistic orange cat walking through a messy Indian "
                    "middle-class home, inspecting scattered clothes and objects, "
                    "expressive human-like comedic behavior while remaining "
                    "visually realistic, cinematic lighting, vertical 9:16"
                ),
                "negative_prompt": (
                    "cartoon, anime, unrealistic anatomy, extra legs, duplicate cat, "
                    "plastic fur, oversaturated CGI"
                ),
            },
            {
                "scene_id": 3,
                "duration_seconds": 4,
                "visual_description": (
                    "Cat suddenly becomes energetic and starts a ridiculous "
                    "but physically believable funny dance."
                ),
                "camera": "Full-body vertical shot with slight push-in",
                "action": "Cat performs a short absurd dance with rhythmic body movement.",
                "dialogue": "Bas! Ab main bhi entertainment karunga!",
                "voice_direction": "Energetic and playful",
                "sound_effects": "Funny beat drop",
                "caption": "Ab main entertainment karunga!",
                "video_prompt": (
                    "Photorealistic orange cat suddenly doing a funny energetic "
                    "dance in an Indian middle-class living room, physically "
                    "believable movement, expressive body language, cinematic "
                    "realism, humorous timing, vertical 9:16"
                ),
                "negative_prompt": (
                    "cartoon, anime, human body, extra limbs, broken anatomy, "
                    "floating objects, unrealistic motion, CGI"
                ),
            },
            {
                "scene_id": 4,
                "duration_seconds": 4,
                "visual_description": (
                    "Cat stops dancing, walks toward camera and stares directly "
                    "into the lens."
                ),
                "camera": "Close-up direct-to-camera shot",
                "action": "Cat pauses dramatically and gives an intense comedic look.",
                "dialogue": "Waise... ye sab clean kaun karega?",
                "voice_direction": "Sudden calm comedic delivery",
                "sound_effects": "Music stops briefly",
                "caption": "Ye sab clean kaun karega?",
                "video_prompt": (
                    "Photorealistic orange cat approaching camera and looking "
                    "directly into lens, expressive comedic face, Indian home "
                    "background, cinematic close-up, natural fur and lighting, "
                    "vertical 9:16"
                ),
                "negative_prompt": (
                    "cartoon, animation, deformed eyes, extra face, duplicate cat, "
                    "CGI, text, watermark"
                ),
            },
            {
                "scene_id": 5,
                "duration_seconds": 4,
                "visual_description": (
                    "Cat gives a final deadpan look directly at the viewer."
                ),
                "camera": "Extreme close-up, stable camera",
                "action": "Cat delivers the final punchline and holds the stare.",
                "dialogue": "Main? Main toh billi hoon... meri toh koi responsibility hi nahi!",
                "voice_direction": "Deadpan Hindi-English comedic punchline",
                "sound_effects": "Short comedic sting",
                "caption": "Meri toh koi responsibility hi nahi!",
                "video_prompt": (
                    "Photorealistic orange cat staring directly into the camera "
                    "with a deadpan comedic expression, realistic Indian middle-class "
                    "home, cinematic shallow depth of field, highly believable fur, "
                    "vertical Instagram Reel 9:16"
                ),
                "negative_prompt": (
                    "cartoon, anime, unrealistic face, extra eyes, extra limbs, "
                    "deformed anatomy, CGI, watermark, text artifacts"
                ),
            },
        ]

        plan = {
            "schema_version": "1.0",
            "director": "ReliableReelDirector",
            "created_at": datetime.utcnow().isoformat() + "Z",

            "title": creative["title"] or "Orange Cat's Messy Home Meltdown",
            "hook": creative["hook"] or "Why do cats always make such a mess?",
            "audience": creative["audience"] or "Instagram viewers",
            "language": "Hinglish",
            "duration_seconds": 20,
            "aspect_ratio": "9:16",

            "visual_style": creative["visual_style"] or "Realistic cinematic",

            "character": {
                "name": "Orange Cat",
                "species": "Domestic cat",
                "appearance": (
                    "Realistic orange domestic cat, natural fur, expressive eyes"
                ),
                "personality": "Frustrated, dramatic, playful, deadpan",
            },

            "world": {
                "location": "Indian middle-class home",
                "setting": "Messy but believable family living room",
                "lighting": "Natural daylight",
                "visual_realism": "Photorealistic cinematic",
            },

            "scenes": scenes,

            "ending": creative["ending"] or (
                "Direct-to-camera comedic punchline"
            ),

            "music_direction": {
                "style": "Light funny modern beat",
                "energy": "Medium, rising during dance",
                "duck_for_dialogue": True,
                "ending": "Short comedic sting",
            },

            "production_notes": [
                "Generate scenes as separate short clips.",
                "Maintain identical orange cat appearance across scenes.",
                "Use vertical 9:16 composition.",
                "Prioritize realistic motion over cartoon movement.",
                "Use Hindi/Hinglish voice with comedic timing.",
                "Add captions after video generation.",
                "Assemble final Reel with FFmpeg.",
            ],
        }

        return plan
