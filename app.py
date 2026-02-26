import streamlit as st
import json
import random
import io
from docx import Document
from fpdf import FPDF

# --- 1. ТВОЙ СВЯЩЕННЫЙ КЛАСС (ВСТАВЬ СЮДА СВОЙ NeuroExpertMaster ЦЕЛИКОМ) ---
class NeuroExpertMaster:
    def __init__(self, matrix):
        self.lib = matrix
        self.rv = self.lib.get("risk_verification", {})
        self.nv = self.lib.get("neuro_vectors", {})
    def apply_gender(self, text, gen, is_endo):
        return text # Твой метод утюга
    def run(self, code_str, pr_in, t_in):
        return "Здесь должен быть результат твоего метода RUN"
    def save_to_word(self, text):
        doc = Document()
        doc.add_paragraph(text)
        bio = io.BytesIO()
        doc.save(bio)
        return bio.getvalue()
    def save_to_pdf(self, text):
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        # Тянем шрифт из сети, чтобы не было ошибок кодировки
        pdf.add_font("DejaVu", "", "https://github.com")
        pdf.set_font("DejaVu", size=12)
        
        # Обработка текста, чтобы не вылетало на переносах
        for line in text.split('\n'):
            pdf.multi_cell(0, 10, txt=line)
            
        return pdf.output() 

# --- 2. ЗАГРУЗКА ---
@st.cache_data
def load_matrix():
    with open('expert_matrix.json', 'r', encoding='utf-8-sig') as f:
        return json.load(f)

matrix = load_matrix()

# --- 3. ИНТЕРФЕЙС ---
st.set_page_config(page_title="NeuroExpert Web", layout="wide")

with st.sidebar:
    st.header("📋 Паспорт")
    fio = st.text_input("ФИО", "Иванов И.И.")
    p_type = st.selectbox("Тип", ["0*", "1", "2", "3", "4", "5", "7", "8", "9", "9гэ"])
    p_gen = st.radio("Пол", ["м", "ж"], horizontal=True)

st.subheader("📊 Функции (0-5)")
f_names = ["Внимание", "Зрит.Гнозис", "Простр.Гнозис", "Дин.Праксис", "Кин.Праксис", "Констр.Праксис", "Счет", "Речь", "Память", "Мышление"]
scores = []
cols = st.columns(5)
for i, name in enumerate(f_names):
    with cols[i % 5]:
        scores.append(st.slider(name, 0, 5, 0))

adj_list = list(matrix.get("phenomenology_adjustments", {}).keys())
presets = st.multiselect("🛠 Надстройки", adj_list)
tags_list = list(matrix.get("tags", {}).keys())
selected_tags = st.multiselect("🏷 Теги", tags_list)

if st.button("🚀 СГЕНЕРИРОВАТЬ"):
    full_code = f"{p_type}{p_gen}/{''.join(map(str, scores))}"
    expert = NeuroExpertMaster(matrix)
    res = expert.run(full_code, ",".join(presets), ",".join(selected_tags))
    
    st.markdown("### Протокол:")
    st.text_area("", res, height=400)
    
    # Кнопка Ворд
    word_data = expert.save_to_word(res)
    st.download_button("📥 Скачать .docx", word_data, f"{fio}.docx")
