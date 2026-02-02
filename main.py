```python
import os
import asyncio
import edge_tts
import requests
import google.generativeai as genai
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# GitHub Secrets se API Key uthayega
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def create_video():
    topic = "Interesting space facts in Hindi"
    print("🎬 Scripting started...")
    response = model.generate_content(f"Write 5 short facts about {topic}. Simple and viral.")
    lines = [l for l in response.text.split('\n') if len(l) > 5][:5]

    print("🎙️ Generating Voiceover...")
    await edge_tts.Communicate(" ".join(lines), "hi-IN-MadhurNeural").save("voice.mp3")
    audio = AudioFileClip("voice.mp3")
    
    print("🖼️ Getting Images...")
    clips = []
    dur = audio.duration / 5
    for i, text in enumerate(lines):
        img_url = f"https://pollinations.ai/p/{text.replace(' ','_')}?width=1080&height=1920&seed={i}"
        with open(f"{i}.jpg", "wb") as f: f.write(requests.get(img_url).content)
        clips.append(ImageClip(f"{i}.jpg").set_duration(dur))

    print("⚙️ Finalizing Video...")
    video = concatenate_videoclips(clips, method="compose").set_audio(audio)
    video.write_videofile("final_short.mp4", fps=24, codec="libx264")
    print("✅ Done!")

if __name__ == "__main__":
    asyncio.run(create_video())
