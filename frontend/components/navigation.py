import streamlit as st


NAV_ITEMS = [
    {
        "label": "My Learning",
        "icon": ":material/menu_book:",
        "page": "pages/My_Learning.py",
    },
    {
        "label": "Dashboard",
        "icon": ":material/dashboard:",
        "page": "pages/Dashboard.py",
    },
    {
        "label": "Contact Us",
        "icon": ":material/mail:",
        "page": "pages/contact.py",
    },
    {
        "label": "Help",
        "icon": ":material/help:",
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
                key=f"nav_{item['label']}",
            ):
                st.switch_page(item["page"])
