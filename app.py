import streamlit as st
import json
import io
from docx import Document

# --- 1. ЗАГЛУШКА ДВИЖКА (ПОКА НЕ ТРОГАЕМ, ЖДЕМ КОМАНДЫ) ---
class NeuroExpertMaster:
    def __init__(self, matrix): self.lib = matrix
    def run(self, code, adj, tags): return f"ДВИЖОК ГОТОВ. ШИФР: {code}\nНАДСТРОЙКИ: {adj}\nТЕГИ: {tags}"
    def save_to_word(self, text, fio):
        doc = Document(); doc.add_paragraph(text); bio = io.BytesIO()
        doc.save(bio); return bio.getvalue()

# --- 2. НАСТРОЙКИ ИНТЕРФЕЙСА (АНИМАЦИЯ И ФОН) ---
st.set_page_config(page_title="NeuroExpert Web", page_icon="🧠", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stSlider { margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #2e6bef; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ДАННЫЕ (СПИСКИ) ---
PROFILES = ["0*", "0+", "00", "0т", "0-", "0сон", "7", "8", "9", "9гэ", "0000", "0", "1", "2", "3", "4", "5"]
ADJUSTMENTS = ["н", "праврег", "леврег", "Асенс", "Аэф", "Ааф", "Аак", "Асем", "неглект", "Апрдин", "Апркин", "Апркон", "АгнП", "АгнЛ", "Апат", "ДЭП", "МСА", "МКАС", "ТАЛАМ", "РЕТИК", "СТРИАР", "МПС", "Дгор", "Дсом", "Дког", "Дтр", "Дгорсом"]
TAGS = ["параноид", "манерный", "аутист", "алко", "люся", "психопат", "диализ", "афазия_сенс", "номина", "па", "пид"]
FUNCTIONS = ["1. Внимание", "2. Зрит.пред.гнозис", "3. Простран.гнозис", "4. Динам. праксис", "5. Кинестет. праксис", "6. Конструктив. праксис", "7. Счет", "8. Речь", "9. Память", "10. Мышление"]

# --- 4. ОБОЛОЧКА ---
st.title("🧠 NeuroExpert: Коннектом-Интерфейс")

with st.sidebar:
    st.header("📋 Паспорт")
    fio = st.text_input("ФИО", "Иванов И.И.")
    age = st.number_input("Возраст", 1, 110, 65)
    gender = st.radio("Пол", ["м", "ж"], horizontal=True)
    st.markdown("---")
    st.subheader("💎 Профиль")
    p_type = st.selectbox("Шифр типа", PROFILES)
    st.markdown("---")
    st.info("v66.8 | Mobile Ready")

# ПОЛЗУНКИ (В 2 колонки для смартфона)
st.subheader("📊 Функциональный статус (0-5)")
scores = []
cols = st.columns(2)
for i, name in enumerate(FUNCTIONS):
    with cols[i % 2]:
        scores.append(st.select_slider(name, options=[0, 1, 2, 3, 4, 5], value=0))

# НАДСТРОЙКИ И ТЕГИ
st.markdown("---")
sel_adj = st.multiselect("🛠 Надстройки (Сбои и Афазии)", ADJUSTMENTS)
sel_tags = st.multiselect("🏷 Теги (Маркеры)", TAGS)

# ФИНАЛЬНЫЙ КОД
full_code = f"{p_type}{gender}/{''.join(map(str, scores))}"
st.code(f"Актуальный шифр: {full_code}", language="text")

if st.button("🚀 СГЕНЕРИРОВАТЬ ПРОТОКОЛ"):
    # Тут будет вызов твоего Умного Движка
    expert = NeuroExpertMaster({})
    res = expert.run(full_code, ",".join(sel_adj), ",".join(sel_tags))
    
    st.markdown("### Итоговое заключение:")
    st.text_area("", res, height=300)
    
    word_data = expert.save_to_word(res, fio)
    st.download_button("📥 Скачать .docx", word_data, f"{fio}.docx")
