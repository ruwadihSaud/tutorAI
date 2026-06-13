import streamlit as st


NAV_ITEMS = [
    {
        "label": "Dashboard",
        "icon": "🎯",
        "page": "pages/Dashboard.py",
    },
    {
        "label": "My Learning",
        "icon": "📖",
        "page": "pages/My_Learning.py",
    },
    {
        "label": "Contact Us",
        "icon": "📧",
        "page": "pages/contact.py",
    },
    {
        "label": "Help",
        "icon": "🛟",
        "page": "pages/Help.py",
    },
]


def render_nav():
    with st.container(border=True):
        st.markdown("### Navigation")

        for item in NAV_ITEMS:
            button_label = f"{item['icon']}  {item['label']}"

            if st.button(
                button_label,
                use_container_width=True,
                key=f"nav_{item['label']}"
            ):
                st.switch_page(item["page"])