from html import escape

import streamlit as st


def render_video_card(video: dict | None) -> None:
    if not video or not video.get("video_url"):
        return

    title = escape(video.get("video_title", "Video explanation"))
    url = escape(video["video_url"], quote=True)
    st.markdown(
        f"""<div class="tutorai-video-resource">
<div class="tutorai-video-copy">
<span class="tutorai-video-label">RECOMMENDED VIDEO</span>
<strong>{title}</strong>
<span>Watch a visual explanation of this topic.</span>
</div>
<a class="tutorai-video-link" href="{url}" target="_blank" rel="noopener noreferrer">Watch video</a>
</div>""",
        unsafe_allow_html=True,
    )
