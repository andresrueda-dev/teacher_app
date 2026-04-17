import streamlit as st

from modules.live_class import live_class_ui
from modules.class_manager import class_manager_ui
from modules.students import students_ui
from modules.dojo import dojo_ui
from modules.backup import backup_ui
from modules.attendance import attendance_ui
from modules.incidents import incidents_ui
from modules.agenda import agenda_ui
from modules.formats import formats_ui

st.set_page_config(page_title="Teacher System", layout="wide")

st.title("🎓 TEACHER SYSTEM PRO")

# 🔧 Estado inicial
if "grupo_activo" not in st.session_state:
    st.session_state.grupo_activo = None

# 🚨 IMPORTANTE: SIN ESPACIOS ANTES
menu = st.sidebar.radio("Navegación", [
    "📚 Class Manager",
    "👨‍🎓 Students",
    "🔥 Dojo",
    "🎯 Clase en Vivo",
    "📝 Asistencia",
    "📋 Incidencias",
    "📅 Agenda",
    "📄 Formatos",
    "💾 Backup"
])

# 🔗 Navegación
if menu == "📚 Class Manager":
    class_manager_ui()

elif menu == "👨‍🎓 Students":
    students_ui()

elif menu == "🔥 Dojo":
    dojo_ui()

elif menu == "🎯 Clase en Vivo":
    live_class_ui()

elif menu == "📝 Asistencia":
    attendance_ui()

elif menu == "📋 Incidencias":
    incidents_ui()

elif menu == "📅 Agenda":
    agenda_ui()

elif menu == "📄 Formatos":
    formats_ui()

elif menu == "💾 Backup":
    backup_ui()
