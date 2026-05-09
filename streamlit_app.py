import streamlit as st
import requests
import time
import json

st.set_page_config(
    page_title="AI Animation Generator",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 AI Animation Generator")
st.caption("LTX 2.3 Powered • Ultra Fast • Free")

st.divider()

# Style select
style = st.selectbox(
    "🎨 Animation Style",
    [
        "Cartoon 2D",
        "Anime",
        "Ghibli Style", 
        "3D Cartoon",
        "Realistic Cinematic",
        "Fantasy Art"
    ]
)

# Duration
duration = st.slider(
    "⏱️ Video Duration (seconds)",
    min_value=1,
    max_value=6,
    value=3
)

# Quality
quality = st.radio(
    "⚡ Quality",
    ["Fast", "Balanced", "Quality"],
    horizontal=True,
    index=1
)

# Resolution
resolution = st.selectbox(
    "📐 Resolution",
    ["512x768", "768x512", "512x512", "1024x576"]
)

# Character
character = st.selectbox(
    "👤 Main Character",
    [
        "Young Boy",
        "Young Girl",
        "Fantasy Hero",
        "Anime Character",
        "Animal Character",
        "No Character - Landscape Only"
    ]
)

# Scene
scene = st.text_area(
    "✍️ Scene Describe කරන්න",
    placeholder="Example: A young boy walking through magical forest, golden sunlight, cinematic...",
    height=120
)

# Camera
camera = st.selectbox(
    "🎥 Camera Motion",
    [
        "Static",
        "Slow Pan Left",
        "Slow Pan Right",
        "Zoom In",
        "Zoom Out",
        "Cinematic Drone"
    ]
)

st.divider()

# Resolution split
width = int(resolution.split("x")[0])
height = int(resolution.split("x")[1])

# Quality map
quality_map = {
    "Fast": "Fast: distilled 8 steps",
    "Balanced": "Balanced: two-stage 30+4",
    "Quality": "Quality: HQ res_2s sampler"
}

if st.button("🎬 Animation හදන්න!", use_container_width=True):
    if not scene:
        st.error("❌ Scene describe කරන්න!")
    else:
        # Full prompt
        full_prompt = f"{scene}, {character}, {style} style, {camera} camera motion, cinematic lighting, high quality, smooth animation"

        st.info(f"📝 Prompt: {full_prompt}")

        with st.spinner("🎨 Rendering... ටිකක් ඉන්න!"):
            try:
                # Gradio API call
                payload = {
                    "data": [
                        full_prompt,        # prompt
                        quality_map[quality], # preset
                        width,              # width
                        height,             # height
                        duration,           # length seconds
                        24,                 # fps
                        42,                 # seed
                        True                # randomize seed
                    ]
                }

                response = requests.post(
                    "https://techfreakworm-ltx2-3-studio.hf.space/api/predict",
                    json=payload,
                    timeout=300,
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 200:
                    result = response.json()
                    
                    # Video URL ගන්නවා
                    video_data = result.get("data", [])
                    
                    if video_data:
                        video_url = video_data[0]
                        
                        if isinstance(video_url, dict):
                            video_url = video_url.get("url", "")
                        
                        if video_url:
                            st.success("✅ Animation Ready!")
                            
                            # Full URL හදනවා
                            if not video_url.startswith("http"):
                                video_url = f"https://techfreakworm-ltx2-3-studio.hf.space/file={video_url}"
                            
                            # Video download
                            video_response = requests.get(video_url, timeout=60)
                            
                            st.video(video_response.content)
                            
                            st.download_button(
                                label="⬇️ Download Video",
                                data=video_response.content,
                                file_name="animation.mp4",
                                mime="video/mp4",
                                use_container_width=True
                            )
                        else:
                            st.error("Video URL හම්බ වුනේ නෑ!")
                            st.json(result)
                    else:
                        st.error("Response empty!")
                        st.json(result)

                else:
                    st.error(f"API Error: {response.status_code}")
                    st.code(response.text)

            except requests.exceptions.Timeout:
                st.error("⏰ Timeout! Space busy නම් ටිකක් ඉඳලා try කරන්න")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
