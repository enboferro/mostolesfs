import streamlit as st
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh

# 1. CONFIGURACIÓN
st.set_page_config(page_title="MÓSTOLES FS - Control v1.6", layout="wide")
st_autorefresh(interval=1000, key="f5_refresh")
s = st.session_state

# ESTILOS PARA BOTONES GRANDES Y COLORES MÓSTOLES (AZUL/ROJO)
st.markdown("""
    <style>
    div.stButton > button { height: 3em; font-weight: bold !important; }
    .main-timer button { height: 5em !important; font-size: 2rem !important; background-color: #0047AB !important; color: white !important; }
    .stop-timer button { height: 5em !important; font-size: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>Control de Tiempos y Faltas - MÓSTOLES</h1>", unsafe_allow_html=True)

# 2. INICIALIZACIÓN DE SEGURIDAD
if 'js' not in s:
    n = ["Serra","Julian","Omar","Tony","Rochina","Benages","Pedrito","Parre Jr","Baeza","Manu","Pedro Toro","Paco Silla","Jose","Coque","Nacho Gomez"]
    s.js = [{"n":x,"t":0.0,"i":None,"p":False,"g":0,"s":0,"e":0,"r":0} for x in n]

# Asegurar que todas las variables existen
vars_check = {'ml':0, 'mr':0, 'fl':0, 'fr':0, 'ta':0.0, 'ic':None, 'on':False}
for k, v in vars_check.items():
    if k not in s: s[k] = v

ah = time.time()
td = s.ta + (ah - s.ic if s.on and s.ic else 0)

# 3. CABECERA
c1, c2 = st.columns([4,1])
with c1:
    col_img, col_txt = st.columns([0.5, 3.5])
    # Escudo del Móstoles
    col_img.image("https://upload.wikimedia.org/wikipedia/en/thumb/0/03/CD_M%C3%B3stoles_URJC_logo.png/200px-CD_M%C3%B3stoles_URJC_logo.png", width=60)
    rv = col_txt.text_input("RIVAL", "RIVAL", label_visibility="collapsed").upper()
if c2.button("🔄 RESET"):
    s.clear()
    st.rerun()

# 4. MARCADOR Y FALTAS
m1, m2, m3 = st.columns([2,3,2])

with m1:
    st.metric("MÓSTOLES GOLES", s.ml)
    if st.button("⚽ GOL MÓSTOLES", key="btn_g_lud", use_container_width=True):
        s.ml += 1
        st.rerun()
    st.write("---")
    st.metric("FALTAS MÓSTOLES", s.fl)
    cf1, cf2 = st.columns(2)
    if cf1.button("➕", key="f_lud_p"): s.fl += 1; st.rerun()
    if cf2.button("➖", key="f_lud_m"): s.fl = max(0, s.fl-1); st.rerun()

with m2:
    mm, sv = divmod(int(td), 60)
    st.markdown(f"<h1 style='text-align:center; font-size:4.5rem; margin-bottom:0;'>{mm:02d}:{sv:02d}</h1>", unsafe_allow_html=True)
    if not s.on:
        st.markdown('<div class="main-timer">', unsafe_allow_html=True)
        if st.button("▶ START", key="btn_start", use_container_width=True):
            s.ic, s.on = ah, True
            for j in s.js: 
                if j["p"]: j["i"] = ah
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="stop-timer">', unsafe_allow_html=True)
        if st.button("⏸ STOP", key="btn_stop", use_container_width=True):
            s.ta += ah - s.ic
            s.on, s.ic = False, None
            for j in s.js:
                if j["p"] and j["i"]: j["t"] += ah - j["i"]; j["i"] = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with m3:
    st.metric(f"{rv[:5]} GOLES", s.mr)
    if st.button(f"⚽ GOL {rv[:3]}", key="btn_g_riv", use_container_width=True):
        s.mr += 1
        st.rerun()
    st.write("---")
    st.metric(f"FALTAS {rv[:3]}", s.fr)
    rf1, rf2 = st.columns(2)
    if rf1.button("➕", key="f_riv_p"): s.fr += 1; st.rerun()
    if rf2.button("➖", key="f_riv_m"): s.fr = max(0, s.fr-1); st.rerun()

# 5. PISTA Y JUGADORES
st.divider()
en_pista = sum(1 for x in s.js if x["p"])
st.subheader(f"🏃 EN PISTA: {en_pista} / 5")

cols = st.columns(3)
for idx, j in enumerate(s.js):
    with cols[idx % 3]:
        with st.container(border=True):
            tt = j["t"] + (ah - j["i"] if s.on and j["p"] and j["i"] else 0)
            mj, sj = divmod(int(tt), 60)
            mins = tt / 60.0
            c_fat = "#2ecc71" if mins <= 3 else ("#f39c12" if mins <= 5 else "#e74c3c")
            
            cn, ct = st.columns([1.5, 1])
            cn.write(f"{'🟢' if j['p'] else '🔴'} **{j['n']}**")
            ct.write(f"⏱️ **{mj:02d}:{sj:02d}**")
            
            ancho = min((mins / 7.0) * 100, 100)
            st.markdown(f'<div style="border:1px solid #ddd;border-radius:5px;background:#eee;height:10px;width:100%;"><div style="background-color:{c_fat};width:{ancho}%;height:100%;border-radius:4px;"></div></div>', unsafe_allow_html=True)
            
            st.write("")
            s1,s2,s3,s4 = st.columns(4)
            if s1.button("🎯", key=f"t{idx}"): j["s"]+=1
            if s2.button("🛡️", key=f"r{idx}"): j["r"]+=1
            if s3.button("❌", key=f"e{idx}"): j["e"]+=1
            if s4.button("⚽", key=f"g{idx}"): 
                j["g"]+=1
                s.ml+=1
                st.rerun()
            
            if st.button("SALIR" if j["p"] else "ENTRAR", key=f"c{idx}", use_container_width=True):
                if not j["p"] and en_pista < 5:
                    j["p"], j["i"] = True, (ah if s.on else None)
                elif j["p"]:
                    if s.on and j["i"]: j["t"] += ah - j["i"]
                    j["p"], j["i"] = False, None
                st.rerun()

st.divider()
if st.button("💾 DESCARGAR RESULTADOS"):
    df = pd.DataFrame(s.js)
    st.download_button("BAJAR CSV", df.to_csv(index=False).encode('utf-8'), f"MOSTOLES_{rv}.csv")

st.markdown("<p style='text-align:center;color:gray;'>Desarrollado por Kike v1.6 - MÓSTOLES Edition</p>", unsafe_allow_html=True)
