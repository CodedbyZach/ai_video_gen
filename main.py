import requests
import streamlit as st
import json

st.set_page_config(page_title="AI Video Script Generator", layout="wide")

def generate_script_stream(topic, style):
    prompt = f"""
    Write a detailed video script for a YouTube-style video.
    Topic: {topic}
    Style: {style}
    Include:
    - A catchy title
    - A 5-sentence intro
    - 3 scene descriptions with voiceover text
    - A call to action at the end
    """

    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": True
    }

    try:
        response = requests.post(
            "http://192.168.61.131:11434/api/generate",
            headers=headers,
            data=json.dumps(payload),
            stream=True,
            timeout=60
        )
        response.raise_for_status()
        
        partial_script = ""
        for line in response.iter_lines():
            if line:
                json_line = json.loads(line.decode("utf-8"))
                partial_script += json_line.get("response", "")
                yield partial_script

    except Exception as e:
        yield f"Error communicating with Ollama: {e}"

st.title("🎬 AI Video Script & Scene Generator")
st.markdown("Generate YouTube-style scripts with scenes and voiceover suggestions.")

with st.form("script_form"):
    topic = st.text_input("Video Topic", "How Hydrogen Can Power the Future")
    style = st.selectbox("Video Style", ["Educational", "Inspirational", "Funny", "Explainer", "Product Review"])
    submit = st.form_submit_button("Generate Script")

if submit and topic:
    output_box = st.empty()  # create one container
    for partial_script in generate_script_stream(topic, style):
        output_box.text_area("📝 Generated Script (Streaming)", partial_script, height=400)
    st.download_button("📥 Download Script as .txt", partial_script, file_name="video_script.txt")
