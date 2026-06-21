# TutorAI

## Project Structure

1. `backend/tutor.py`: مسؤول عن توزيع طلب الطالب على المهمة المناسبة.
2. `backend/generators/`: شروط المهام والـ prompts الخاصة بكل نوع من الردود.
3. `backend/data/`: بيانات الدروس، اختبارات تحديد المستوى، وفهرس الدروس.
4. `frontend/learning_journey/`: واجهات ردود الوكيل داخل رحلة التعلم مثل الاختبار، الدرس، والتحقق من الفهم.
5. `frontend/components/`: مكونات الواجهة العامة والمشتركة مثل التشات والهيدر والفوتر.
6. `frontend/pages/`: صفحات واجهة Streamlit.
7. `backend/test_tutor.py`: اختبار الوكيل وتوجيه المهام واسترجاع الدروس.
8. `backend/services/LLM.py`: اختيار المودل الأساسي وربط جميع خدمات الـ LLM، و`ollama_service.py` مسؤول عن الاتصال بـ Ollama.
9. `backend/main.py`: نقاط FastAPI التي تربط الواجهة مع `tutor.py`.

## Request Flow

`pages` -> `components/chat.py` -> `backend/main.py` -> `backend/tutor.py` -> `generators` -> `services/LLM.py` -> model service

تعرض الردود التعليمية التفاعلية من خلال `frontend/learning_journey/`، وتقرأ بياناتها من `backend/data/`.
