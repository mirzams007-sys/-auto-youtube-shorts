```python
import os
import asyncio
import edge_tts
import requests
import google.generativeai as genai
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# 1. AI Setup (Dimaag)
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def make_video():
    topic = "3 Amazing facts about Space in Hindi"
    print("🚀 Step 1: Writing Script...")
    
    # AI se script mangna
    prompt = f"Write 3 very short interesting facts about {topic}. Each fact should be only 1 line. No intro, no outro."
    response = model.generate_content(prompt)
    facts = [line.strip() for line in response.text.split('\n') if len(line) > 10][:3]

    print("🎙️ Step 2: Creating Voiceover...")
    full_text = " . ".join(facts)
    voice_file = "voice.mp3"
    communicate = edge_tts.Communicate(full_text, "hi-IN-MadhurNeural")
    await communicate.save(voice_file)
    audio = AudioFileClip(voice_file)

    print("🖼️ Step 3: Generating Images...")
    clips = []
    duration_per_clip = audio.duration / len(facts)
    
    for i, text in enumerate(facts):
        # Pollinations AI se image lena
        img_url = f"https://pollinations.ai/p/{text.replace(' ','_')}?width=1080&height=1920&seed={i}"
        img_data = requests.get(img_url).content
        with open(f"{i}.jpg", "wb") as f:
            f.write(img_data)
        
        # Image clip banana
        clip = ImageClip(f"{i}.jpg").set_duration(duration_per_clip).set_fps(24)
        clips.append(clip)

    print("🎬 Step 4: Final Video Assembly...")
    final_video = concatenate_videoclips(clips, method="compose").set_audio(audio)
    final_video.write_videofile("yt_short.mp4", fps=24, codec="libx264", audio_codec="aac")
    print("✅ Success! Video ready: yt_short.mp4")

if __name__ == "__main__":
    asyncio.run(make_video())
```
