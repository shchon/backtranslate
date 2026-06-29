DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"
DEFAULT_CONTEXT_N = 1
DEFAULT_FONT_SIZE = 14
DEFAULT_RECENT_PAIRS = []
DEFAULT_PROMPT_TEMPLATE = """You are a professional subtitle translator and language coach.

{context}

Official English subtitle: "{official}"

User's English translation: "{user_input}"

IMPORTANT: The context above is ONLY for understanding the surrounding dialogue. Do NOT evaluate or compare anything in the context. Only compare the user's translation against the official subtitle shown above.

Rate on four dimensions (0-100):
- Meaning: Does the user's translation match the meaning of the official subtitle?
- Grammar: Is the English grammatically correct?
- Naturalness: Would a native speaker naturally say it this way?
- Subtitle Style: Is it concise and suitable for on-screen subtitles?

Return ONLY valid JSON:
{{
  "meaning_score": 0-100,
  "grammar_score": 0-100,
  "naturalness_score": 0-100,
  "subtitle_style_score": 0-100,
  "analysis": "Concise analysis in Chinese. Compare the user's version with the official one. Explain WHY the official subtitle works better, or acknowledge if both are valid. Be encouraging and specific.",
  "suggested_expressions": []
}}"""
