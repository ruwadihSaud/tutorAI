# frontend/styles/theme.py

COLORS = {
    "primary": "#2563EB",
    "primary_dark": "#1E40AF",
    "secondary": "#14B8A6",
    "background": "#F8FAFC",
    "surface": "#FFFFFF",
    "sidebar": "#F1F5F9",
    "text": "#000000",
    "muted_text": "#64748B",
    "border": "#E2E8F0",
    "success": "#16A34A",
    "warning": "#F59E0B",
    "danger": "#DC2626",
    "info": "#0284C7",
    "button": "#2563EB",
}


def get_global_styles() -> str:
    return f"""
    <style>

        /* --------------- main --------------- */

        /* App background */
        [data-testid="stAppViewContainer"] {{
            background-color: {COLORS["background"]};
            color: {COLORS["text"]};
        }}

        /* Global font */
        html, body, [class*="css"] {{
            font-family: "Segoe UI", Arial, sans-serif !important;
        }}

        /* Hide only decoration, not the sidebar toggle */
        div[data-testid="stDecoration"] {{
            display: none !important;
        }}

        #MainMenu {{
            visibility: hidden !important;
        }}

        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 4rem !important;
        }}

        /* --------------- streamlit header --------------- */

        header[data-testid="stHeader"] {{
            background-color: transparent !important;
            border-bottom: none !important;
        }}

        [data-testid="collapsedControl"] {{
            background-color: {COLORS["surface"]} !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 10px !important;
            color: {COLORS["primary"]} !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.12) !important;
            padding: 6px !important;
        }}

        /* --------------- sidebar navigation --------------- */

        [data-testid="stSidebar"] * {{
            color: {COLORS["text"]} !important; 
        }}
        section[data-testid="stSidebar"] {{
            background-color: {COLORS["surface"]};
            color: {COLORS["text"]} !important;
            border-right: 1px solid {COLORS["border"]};
        }}

        section[data-testid="stSidebar"] a {{
            border-radius: 12px !important;
            padding: 10px 12px !important;
            margin-bottom: 6px !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            font-family: "Segoe UI", Arial, sans-serif !important;
            text-decoration: none !important;
        }}
        
        section[data-testid="stSidebar"] a:hover {{
            background-color: #2564EB34 !important;
            color: {COLORS["text"]} !important;
        }}

        /* --------------- components --------------- */

        /* Header component */
        .tutorai-header {{
            padding: 20px 0 10px 0;
            margin-bottom: 10px;
        }}

        .tutorai-header h1 {{
            margin: 0;
            color: {COLORS["primary"]};
            font-size: 42px;
            font-weight: 800;
        }}

        .tutorai-header p {{
            margin: 6px 0 0 0;
            color: {COLORS["muted_text"]};
            font-size: 16px;
        }}


        /* Cards */
        .tutorai-card {{
            background-color: {COLORS["surface"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        }}

        .tutorai-section-title {{
            color: {COLORS["text"]};
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 12px;
        }}

        .tutorai-muted {{
            color: #334155 !important;
            font-size: 14px !important;
            line-height: 1.6 !important;
        }}

        .tutorai-muted strong {{
            color: {COLORS["text"]} !important;
            font-weight: 700 !important;
        }}

        .tutorai-lesson-meta {{
            background-color: #F8FAFC;
            border: 1px solid {COLORS["border"]};
            border-radius: 12px;
            padding: 12px 14px;
            margin: 12px 0 16px 0;
        }}

        .lesson-content {{
            color: {COLORS["text"]} !important;
            font-size: 15px !important;
            line-height: 1.8 !important;
            margin: 0 !important;
        }}


        /* Page Title */
        .page-title {{
            margin-bottom: 18px;
        }}

        .page-title h2 {{
            color: {COLORS["text"]};
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 4px;
        }}

        .page-title p {{
            color: {COLORS["muted_text"]};
            font-size: 14px;
            margin: 0;
        }}

        .tutorai-title-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 8px 0;
        }}

        .tutorai-title-meta span {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background-color: #EFF6FF;
            color: #1E3A8A;
            border: 1px solid #BFDBFE;
            border-radius: 10px;
            padding: 6px 10px;
            font-size: 13px;
            font-weight: 600;
        }}

        .tutorai-title-meta strong {{
            color: {COLORS["primary_dark"]};
            font-weight: 800;
        }}

        /* Buttons */
        div[data-testid="stButton"] button {{
            background-color: {COLORS["surface"]} !important;
            color: {COLORS["primary"]} !important;
            border: 1px solid {COLORS["primary"]} !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
        }}

        div[data-testid="stButton"] button:hover {{
            background-color: {COLORS["primary"]} !important;
            color: #FFFFFF !important;
            border-color: {COLORS["primary_dark"]} !important;
        }}

        div[data-testid="stButton"] button:active {{
            background-color: {COLORS["primary_dark"]} !important;
            color: #FFFFFF !important;
            border-color: {COLORS["primary_dark"]} !important;
        }}

        div[data-testid="stButton"] button:disabled,
        div[data-testid="stButton"] button:disabled:hover {{
            background-color: #F1F5F9 !important;
            color: #94A3B8 !important;
            border-color: {COLORS["border"]} !important;
            cursor: not-allowed !important;
        }}


        /* Chat */
        .chat-message {{
            padding: 12px 14px;
            border-radius: 12px;
            margin-bottom: 10px;
            font-size: 14px;
            line-height: 1.5;
        }}

        .assistant-message {{
            background-color: #F1F5F9;
            color: {COLORS["text"]};
            border: 1px solid {COLORS["border"]};
        }}

        .user-message {{
            background-color: {COLORS["primary"]};
            color: white;
            margin-left: 24px;
        }}

        div[data-testid="stChatMessage"] {{
            background-color: {COLORS["surface"]} !important;
            color: {COLORS["text"]} !important;
            box-sizing: border-box !important;
            max-width: 100% !important;
            border-radius: 14px !important;
            padding: 10px 12px !important;
            margin-bottom: 10px !important;
            border: 1px solid {COLORS["border"]} !important;
        }}

        div[data-testid="stChatMessage"] * {{
            color: {COLORS["text"]} !important;
        }}

        div[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) {{
            background-color: {COLORS["surface"]} !important;
            color: {COLORS["text"]} !important;
            border-left: 4px solid {COLORS["secondary"]} !important;
            margin-right: 14px !important;
        }}

        div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {{
            background-color: {COLORS["surface"]} !important;
            color: {COLORS["text"]} !important;
            border-color: {COLORS["border"]} !important;
            border-left: 4px solid {COLORS["primary"]} !important;
            margin-left: 8px !important;
            margin-right: 0 !important;
        }}

        div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) * {{
            color: {COLORS["text"]} !important;
        }}

        div[data-testid="stChatMessage"] [data-testid="stChatMessageAvatar"] {{
            background-color: #DBEAFE !important;
            border: 1px solid #BFDBFE !important;
        }}

        div[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"])
        [data-testid="stChatMessageAvatar"] {{
            background-color: #CCFBF1 !important;
            border: 1px solid #99F6E4 !important;
            color: #0F766E !important;
        }}

        div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"])
        [data-testid="stChatMessageAvatar"] {{
            background-color: #DBEAFE !important;
            border: 1px solid #BFDBFE !important;
            color: {COLORS["primary_dark"]} !important;
        }}

        div[data-testid="stChatMessage"] [data-testid="stChatMessageAvatar"] svg,
        div[data-testid="stChatMessage"] [data-testid="stChatMessageAvatar"] * {{
            color: inherit !important;
            fill: currentColor !important;
        }}

        div[data-testid="stChatInput"] {{
            background-color: transparent !important;
            padding-top: 8px !important;
        }}

        div[data-testid="stChatInput"] > div {{
            background-color: {COLORS["surface"]} !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 14px !important;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06) !important;
            padding: 2px 8px !important;
        }}

        div[data-testid="stChatInput"] [data-baseweb="textarea"],
        div[data-testid="stChatInput"] [data-baseweb="base-input"],
        div[data-testid="stChatInput"] [data-baseweb="textarea"] > div {{
            background-color: {COLORS["surface"]} !important;
            color: {COLORS["text"]} !important;
        }}

        div[data-testid="stChatInput"] textarea {{
            background-color: {COLORS["surface"]} !important;
            color: {COLORS["text"]} !important;
            border: none !important;
            box-shadow: none !important;
            font-size: 14px !important;
            line-height: 1.5 !important;
            caret-color: {COLORS["text"]} !important;
            -webkit-text-fill-color: {COLORS["text"]} !important;
        }}

        div[data-testid="stChatInput"] textarea::placeholder {{
            color: {COLORS["muted_text"]} !important;
        }}

        div[data-testid="stChatInput"] > div:focus-within {{
            border-color: {COLORS["primary"]} !important;
            box-shadow: 0 0 0 3px #DBEAFE !important;
        }}

        div[data-testid="stChatInput"] button {{
            color: {COLORS["primary"]} !important;
            border-radius: 10px !important;
        }}

        div[data-testid="stChatInput"] button:hover {{
            background-color: #EFF6FF !important;
            color: {COLORS["primary_dark"]} !important;
        }}

        .start-button-wrap {{
            width: fit-content;
            margin-top: 6px;
        }}

        div[data-testid="stVerticalBlock"]:has(.start-button-wrap) div[data-testid="stButton"] button {{
            min-width: 96px !important;
            padding: 8px 18px !important;
        }}

        div[data-testid="stVerticalBlock"]:has(.chat-sticky-marker) {{
            position: sticky !important;
            top: 24px !important;
            align-self: flex-start !important;
            z-index: 50 !important;
        }}

        .chat-sticky-marker {{
            display: none;
        }}

        /* Form submit buttons */
        div[data-testid="stFormSubmitButton"] button {{
            background-color: {COLORS["button"]} !important;
            color: #FFFFFF !important;
            border: 1px solid {COLORS["primary_dark"]} !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
        }}

        div[data-testid="stFormSubmitButton"] button:hover {{
            background-color: {COLORS["primary_dark"]} !important;
            color: #FFFFFF !important;
            border-color: {COLORS["primary_dark"]} !important;
        }}

        /* Placement test */
        div[data-testid="stForm"]:has(.placement-test-marker) {{
            background-color: {COLORS["surface"]} !important;
            color: {COLORS["text"]} !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 12px !important;
            padding: 16px !important;
            box-shadow: none !important;
        }}

        div[data-testid="stForm"]:has(.placement-test-marker) * {{
            color: {COLORS["text"]} !important;
        }}

        div[data-testid="stForm"]:has(.placement-test-marker)
        div[data-testid="stRadio"] {{
            background-color: {COLORS["surface"]} !important;
            border-bottom: 1px solid {COLORS["border"]} !important;
            padding: 12px 0 16px 0 !important;
            margin-bottom: 4px !important;
        }}

        div[data-testid="stForm"]:has(.placement-test-marker)
        div[data-testid="stWidgetLabel"] p {{
            color: {COLORS["text"]} !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            line-height: 1.5 !important;
        }}

        div[data-testid="stForm"]:has(.placement-test-marker)
        div[role="radiogroup"] {{
            gap: 8px !important;
        }}

        div[data-testid="stForm"]:has(.placement-test-marker)
        label[data-baseweb="radio"] {{
            width: 100% !important;
            background-color: #F8FAFC !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 10px !important;
            padding: 9px 11px !important;
            margin: 0 !important;
        }}

        div[data-testid="stForm"]:has(.placement-test-marker)
        label[data-baseweb="radio"]:hover {{
            background-color: #EFF6FF !important;
            border-color: #93C5FD !important;
        }}

        div[data-testid="stForm"]:has(.placement-test-marker)
        label[data-baseweb="radio"]:has(input:checked) {{
            background-color: #EFF6FF !important;
            border-color: {COLORS["primary"]} !important;
            box-shadow: 0 0 0 1px {COLORS["primary"]} !important;
        }}

        div[data-testid="stForm"]:has(.placement-test-marker)
        input[type="radio"] {{
            accent-color: {COLORS["primary"]} !important;
        }}

        div[data-testid="stForm"]:has(.placement-test-marker)
        div[data-testid="stFormSubmitButton"] button {{
            width: 100% !important;
            background-color: {COLORS["primary"]} !important;
            color: #FFFFFF !important;
            border-color: {COLORS["primary_dark"]} !important;
            margin-top: 12px !important;
        }}

        div[data-testid="stForm"]:has(.placement-test-marker)
        div[data-testid="stFormSubmitButton"] button * {{
            color: #FFFFFF !important;
        }}


        /* Footer */
        footer {{
            visibility: hidden !important;
        }}

        .tutorai-footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: {COLORS["surface"]};
            color: {COLORS["muted_text"]};
            text-align: center;
            padding: 10px 0;
            font-size: 13px;
            border-top: 1px solid {COLORS["border"]};
            z-index: 999;
        }}

        .tutorai-footer span {{
            font-weight: 600;
            color: {COLORS["primary"]};
        }}
        /* Chat card container */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.chat-card-marker) {{
            position: sticky !important;
            top: 24px !important;
            align-self: flex-start !important;
            z-index: 50 !important;
            background-color: {COLORS["surface"]} !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 16px !important;
            padding: 18px !important;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05) !important;
            margin-bottom: 16px !important;
        }}
    </style>
    """
