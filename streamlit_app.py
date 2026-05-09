import streamlit as st
import requests
import time

# Page config
st.set_page_config(
    page_title="🎬 AI Animation Generator",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 AI Animation Generator")
st.caption("LTX-2 powered • Ultra Fast • Free")

# Colab URL input
colab_url = st.text_input(
    "🔗 Colab Server URL",
    placeholder="https://xxxx-xx-xx.ngrok-free.app"
)

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
duration = st.selectbox(
    "⏱️ Video Duration",
    [
        "3 seconds",
        "5 seconds",
        "8 seconds",
        "10 seconds"
    ]
)

# Characters
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

# Scene description
scene = st.text_area(
    "✍️ Scene Describe කරන්න",
    placeholder="Example: A young boy walking through a magical forest, golden sunlight, Ghibli style, cinematic...",
    height=120
)

# Camera motion
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

# Quality
quality = st.select_slider(
    "⚡ Speed vs Quality",
    options=["Ultra Fast", "Fast", "Balanced", "High Quality", "Ultra Quality"]
)

st.divider()

# Generate
if st.button("🎬 Animation හදන්න!", use_container_width=True):
    
    if not colab_url:
        st.error("❌ Colab URL දාන්න!")
    elif not scene:
        st.error("❌ Scene describe කරන්න!")
    else:
        
        # Full prompt build
        full_prompt = f"{scene}, {character}, {style} style, {camera} camera, cinematic lighting, high quality animation"
        
        st.info(f"📝 Prompt: {full_prompt}")
        
        with st.spinner("🎨 Rendering... ටිකක් ඉන්න!"):
            try:
                response = requests.post(
                    f"{colab_url}/generate",
                    json={
                        "prompt": full_prompt,
                        "duration": duration,
                        "quality": quality
                    },
                    timeout=300
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result["status"] == "success":
                        st.success("✅ Animation Ready!")
                        
                        # Video show
                        video_response = requests.get(
                            f"{colab_url}/video",
                            timeout=60
                        )
                        
                        st.video(video_response.content)
                        
                        st.download_button(
                            label="⬇️ Download Video",
                            data=video_response.content,
                            file_name="animation.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
                        
            except requests.exceptions.Timeout:
                st.error("⏰ Timeout! Colab check කරන්න")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
