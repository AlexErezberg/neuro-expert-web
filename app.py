import streamlit as st
import json
import random
from docx import Document
import io
from fpdf import FPDF

# 1. ТВОЙ СВЯЩЕННЫЙ КЛАСС (Вставь сюда СВОЙ код полностью)
# Я ставлю заглушку, замени её своим NeuroExpertMaster со всеми методами!

class NeuroExpertMaster:
    def __init__(self, matrix):
        self.lib = matrix
        # ... тут все твои инициализации (rv, nv и т.д.) ...
    
    def apply_gender(self, text, gen, is_endo):
        # ... твой метод утюга ...
        return text

    def run(self, code_str, pr_in, t_in):
        # ... твой метод RUN ...
        return "Здесь будет результат работы твоего движка"

    def save_to_word(self, text):
        # ... твой метод сохранения ...
        doc = Document()
        doc.add_paragraph(text)
        bio = io.BytesIO()
        doc.save(bio)
        return bio.getvalue()

# 2. ЗАГРУЗКА ДАННЫХ
@st.cache_data
def load_matrix():
    # 'utf-8-sig' автоматически отрезает невидимую метку BOM
    with open('expert_matrix.json', 'r', encoding='utf-8-sig') as f:
        return json.load(f)

matrix = load_matrix()

# 3. ИНТЕРФЕЙС STREAMLIT
st.set_page_config(page_title="NeuroExpert Web", page_icon="🧠")
st.title("🧠 Система экспертной оценки коннектома")

# Боковая панель
with st.sidebar:
    st.header("Паспорт")
    gender = st.radio("Пол", ["Мужской", "Женский"])
    profile = st.selectbox("Тип профиля", ["0*", "1", "2", "3", "4", "5", "7", "8", "9", "9гэ"])

# Слайдеры баллов
st.subheader("Оценка функций (0-5)")
cols = st.columns(2)
funcs = ["Нейродинамика", "Гнозис", "Праксис кин.", "Праксис дин.", "Праксис констр.", "Речь (аф)", "Речь (диз)", "Память", "Мышление", "Внимание"]
scores = []
for i, f in enumerate(funcs):
    with cols[i % 2]:
        scores.append(st.slider(f, 0, 5, 0))

# Надстройки и теги
adj_keys = list(matrix.get("phenomenology_adjustments", {}).keys())
presets = st.multiselect("Надстройки", adj_keys)
tags_in = st.text_input("Теги через запятую")

# ЗАПУСК
if st.button("СГЕНЕРИРОВАТЬ"):
    expert = NeuroExpertMaster(matrix)
    # Формируем код: Тип+Пол / 10 цифр
    gen_mark = 'ж' if gender == "Женский" else 'м'
    code = f"{profile}{gen_mark}/{''.join(map(str, scores))}"
    
    # Вызов твоего RUN
    res = expert.run(code, ",".join(presets), tags_in)
    
    st.markdown("### Итоговый протокол:")
    st.write(res)
    
    # Скачивание Word
    word_data = expert.save_to_word(res)
    st.download_button("📥 Скачать .docx", word_data, "Expert_Report.docx")

# НОВЫЙ БЕЗОПАСНЫЙ PDF (fpdf2 style)
    pdf = FPDF()
    pdf.add_page()
    # Используем стандартный шрифт, который поддерживает Unicode
    pdf.set_font("Arial", size=12) 
    
    # Заголовок (пишем через метод multi_cell для надежности)
    pdf.multi_cell(0, 10, txt="РЕЗУЛЬТАТЫ ОБСЛЕДОВАНИЯ", align='C')
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=f"Пациент: {patient_fio}, {patient_age} лет")
    pdf.ln(5)
    
    # Основной текст
    pdf.multi_cell(0, 10, txt=res)
    
    # Выхлоп в память
    pdf_output = pdf.output() 
    
    st.download_button(
        label="📄 Скачать Протокол .pdf",
        data=bytes(pdf_output),
        file_name=f"Expert_{patient_fio}.pdf",
        mime="application/pdf"
    )
