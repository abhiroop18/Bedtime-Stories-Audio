import streamlit as st
from modules.story_generator import generate_story
from modules.audio_generator import text_to_audio
import streamlit.components.v1 as components
import base64


# --- Streamlit UI Config ---
st.set_page_config(page_title="AI Bedtime Story Generator", page_icon="🌙")
st.title("🌙 AI-Powered Personalized Bedtime Story Generator")

st.markdown("Fill in the details to create a magical story for your child!")

# --- Input Form ---
with st.form("story_form"):
    child_name = st.text_input("👶 Child's Name")
    child_age = st.number_input("🎂 Child's Age", min_value=1, max_value=12, step=1)
    child_hobbies = st.text_input("🎨 Hobbies (e.g., painting, dinosaurs)")
    story_tone = st.selectbox("🎭 Story Tone", ["Adventurous", "Funny", "Moral", "Magical"])

    submitted = st.form_submit_button("✨ Generate Story")

# --- Generate and Display Story ---
if submitted:
    if not child_name or not child_hobbies:
        st.error("❗ Please fill in all fields.")
    else:
        with st.spinner("Generating story..."):
            story = generate_story(
                name=child_name,
                age=child_age,
                hobbies=child_hobbies,
                tone=story_tone
            )

        st.subheader("📖 Generated Story")
        st.write(story)

    
   

    if not story.startswith("❌"):
        st.subheader("🔊 Listen to the Story")

        audio_path, error = text_to_audio(story)

        if error:
            st.error(f"Audio generation failed: {error}")
        else:
            try:
                # Read the file
                with open(audio_path, "rb") as f:
                    audio_bytes = f.read()

                # Encode to base64 for HTML audio playback
                b64_audio = base64.b64encode(audio_bytes).decode()

                # Display player via custom HTML
                audio_html = f"""
                    <audio controls autoplay>
                        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                        Your browser does not support the audio element.
                    </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)

                # Still offer download
                st.download_button(
                    label="💾 Download Audio",
                    data=audio_bytes,
                    file_name="bedtime_story.mp3",
                    mime="audio/mp3"
                )

            except Exception as e:
                st.error(f"Error playing audio: {e}")



    
