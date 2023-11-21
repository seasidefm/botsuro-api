BOT_PERSONALITY_QUERY = """
*[_type == "botPersonality" && platform == "{PLATFORM}" && isActive == true] {{
  persona,
  aiPrompt
}}
"""