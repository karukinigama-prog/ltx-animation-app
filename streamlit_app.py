import streamlit as st
import requests
import json

st.set_page_config(
    page_title="AI Animation Generator",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 AI Animation Generator")
st.caption("LTX 2.3 Powered • Free")

st.divider()

style = st.selectbox(
    "🎨 Animation Style",
    ["Cartoon 2D","Anime","Ghibli Style",
     "3D Cartoon","Realistic Cinematic","Fantasy Art"]
)

duration = st.slider("⏱️ Duration (seconds)", 1, 6, 3)

quality = st.radio(
    "⚡ Quality",
    ["Fast", "Balanced", "Quality"],
    horizontal=True,
    index=1
)

resolution = st.selectbox(
    "📐 Resolution",
    ["512x768","768x512","512x512","1024x576"]
)

character = st.selectbox(
    "👤 Character",
    ["Young Boy","Young Girl","Fantasy Hero",
     "Anime Character","Animal Character","Landscape Only"]
)

scene = st.text_area(
    "✍️ Scene Describe කරන්න",
    placeholder="A young boy walking through magical forest, golden sunlight...",
    height=120
)

camera = st.selectbox(
    "🎥 Camera Motion",
    ["Static","Slow Pan Left","Slow Pan Right",
     "Zoom In","Zoom Out","Cinematic Drone"]
)

st.divider()

width = int(resolution.split("x")[0])
height = int(resolution.split("x")[1])

quality_map = {
    "Fast": "Fast: distilled 8 steps",
    "Balanced": "Balanced: two-stage 30+4",
    "Quality": "Quality: HQ res_2s sampler"
}

SPACE_URL = "https://techfreakworm-ltx2-3-studio.hf.space"

if st.button("🎬 Animation හදන්න!", use_container_width=True):
    if not scene:
        st.error("❌ Scene describe කරන්න!")
    else:
        full_prompt = f"{scene}, {character}, {style} style, {camera} camera, cinematic lighting, high quality"
        st.info(f"📝 Prompt: {full_prompt}")

        with st.spinner("🎨 Rendering... ටිකක් ඉන්න!"):
            try:
                # Step 1 - Job submit කරනවා
                submit_payload = {
                    "data": [
                        full_prompt,
                        quality_map[quality],
                        width,
                        height,
                        duration,
                        24,
                        42,
                        True
                    ],
                    "fn_index": 0,
                    "session_hash": "streamlit123"
                }

                submit_response = requests.post(
                    f"{SPACE_URL}/queue/join",
                    json=submit_payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )

                st.write(f"Submit status: {submit_response.status_code}")

                if submit_response.status_code == 200:
                    event_id = submit_response.json().get("event_id")
                    st.write(f"Event ID: {event_id}")

                    # Step 2 - Result poll කරනවා
                    import time
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    for i in range(60):
                        time.sleep(3)
                        progress_bar.progress((i+1)/60)
                        status_text.text(f"Generating... {(i+1)*5}s")

                        data_response = requests.get(
                            f"{SPACE_URL}/queue/data?session_hash=streamlit123",
                            timeout=30,
                            stream=True
                        )

                        for line in data_response.iter_lines():
                            if line:
                                line_str = line.decode('utf-8')
                                if line_str.startswith("data:"):
                                    try:
                                        data = json.loads(line_str[5:])
                                        msg = data.get("msg", "")

                                        if msg == "process_completed":
                                            output = data.get("output", {})
                                            video_data = output.get("data", [])

                                            if video_data:
                                                video_info = video_data[0]
                                                if isinstance(video_info, dict):
                                                    video_url = video_info.get("url", "")
                                                    if not video_url.startswith("http"):
                                                        video_url = f"{SPACE_URL}/file={video_url}"
                                                else:
                                                    video_url = f"{SPACE_URL}/file={video_info}"

                                                progress_bar.progress(1.0)
                                                status_text.text("✅ Done!")

                                                video_bytes = requests.get(video_url).content
                                                st.success("✅ Animation Ready!")
                                                st.video(video_bytes)
                                                st.download_button(
                                                    "⬇️ Download Video",
                                                    data=video_bytes,
                                                    file_name="animation.mp4",
                                                    mime="video/mp4",
                                                    use_container_width=True
                                                )
                                                st.stop()
                                    except:
                                        pass
                        break

                else:
                    st.error(f"Submit failed: {submit_response.status_code}")
                    st.code(submit_response.text)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
