import streamlit as st
import google.generativeai as genai
import json

# ==========================================
# Konfigurasi Halaman & API
# ==========================================
st.set_page_config(page_title="Power Tools Kreator", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stCodeBlock { margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# Sidebar & Pengaturan
# ==========================================
st.sidebar.title("⚙️ Pengaturan Sistem")
api_key = st.sidebar.text_input("Masukkan API Key Gemini Anda:", type="password", help="Wajib diisi agar AI bisa bekerja.")

st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 **Dev: VDMotionStudio**")
st.sidebar.caption("Sistem Otomasi Infografis Padat & High-Detail")

# ==========================================
# Header Utama
# ==========================================
st.title("⚡ Power Tools Kreator (Dense & Maximalist Edition)")
st.markdown("Menghasilkan 1 prompt gambar infografis yang **padat merayap, kaya detail, tanpa ruang kosong**, dan sangat menarik secara visual.")
st.markdown("---")

# ==========================================
# Database Pemetaan Visual 
# ==========================================
TEMA_PROMPT = {
    "Professional News Agency / Gov PSA": "high-end professional public service announcement infographic poster, clean vector style mixed with highly realistic 3D elements, smooth light blue to white gradient background, highly structured grid layout, corporate typography, bold red and dark grey text, masterpiece",
    "Claymation / 3D Diorama Miniatur": "hyper-detailed miniature claymation diorama, macro lens, tilt-shift photography, cute stylized stop-motion aesthetic, tactile clay textures, warm studio lighting, highly detailed 3D typography",
    "Modern Corporate & Clean Flat Vector": "high-end corporate flat vector illustration, dribbble style, crisp modern sans-serif typography, subtle drop shadows, clean geometric shapes, ultra-detailed 2D graphics"
}

UKURAN_PROMPT = {
    "9:16 (Story/Shorts/Tiktok)": "aspect ratio 9:16",
    "1:1 (Feed/Square)": "aspect ratio 1:1",
    "4:5 (Portrait IG)": "aspect ratio 4:5",
    "16:9 (Landscape/YouTube)": "aspect ratio 16:9"
}

# ==========================================
# Fungsi Pemanggil AI
# ==========================================
def generate_json_from_gemini(prompt_instruksi):
    if not api_key:
        st.error("⚠️ Silakan masukkan API Key Gemini di sidebar terlebih dahulu.")
        return None
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        'gemini-2.5-flash', 
        generation_config={"response_mime_type": "application/json"}
    )
    
    try:
        response = model.generate_content(prompt_instruksi)
        return json.loads(response.text)
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memanggil AI: {e}")
        return None

# ==========================================
# Template Instruksi Ekstrem (MAXIMALIST)
# ==========================================
TEMPLATE_PROMPT_ENGINEER = """
Kamu adalah Master Prompt Engineer untuk AI Image Generator (Flux/Midjourney). Tugasmu meracik TEPAT 1 (SATU) prompt visual yang mendikte tata letak infografis vertikal yang SANGAT PADAT, KAYA ELEMEN, SIBUK, dan MENARIK TANPA RUANG KOSONG (Zero empty space).

TUGAS PENTING: 
1. Buat 5 poin materi agar kanvas vertikal terisi penuh. 
2. Teks (exact text) HARUS SANGAT SINGKAT (maksimal 3-4 kata per poin) agar ejaan AI tepat.

Format JSON WAJIB:
{{
    "judul_infografis": "Judul Utama (Maks 4 kata)",
    "poin_materi": ["Poin 1", "Poin 2", "Poin 3", "Poin 4", "Poin 5"],
    "prompt_gambar_flux": "A fully finished, visually overwhelming, hyper-detailed professional infographic poster, [UKURAN]. Visual aesthetic: [TEMA]. TYPOGRAPHY: Ultra-crisp, modern sans-serif. LAYOUT STRUCTURE (DENSELY PACKED, EDGE-TO-EDGE): The entire canvas is filled with intricate elements, leaving NO empty space. TOP HEADER: Massive, eye-catching 3D text reading 'JUDUL_UTAMA' taking up the top section. HERO GRAPHIC: A large, highly complex central 3D illustration of [DESKRIPSI OBJEK UTAMA]. MIDDLE TO BOTTOM SECTION (ZIG-ZAG FLOW): A dense layout flowing downwards. Section 1: exact text 'POIN_1' next to a detailed 3D [IKON 1]. Section 2: exact text 'POIN_2' next to [IKON 2]. Section 3: exact text 'POIN_3' next to [IKON 3]. Section 4: exact text 'POIN_4' next to [IKON 4]. Section 5: exact text 'POIN_5' next to [IKON 5]. BACKGROUND FILLERS: The background is heavily populated with subtle connecting dotted lines, floating UI data panels, glowing abstract nodes, bar charts, and infographic arrows to eliminate any blank areas. 8k resolution, highly engaging dynamic composition, masterpiece."
}}
"""

# ==========================================
# Layout Tabs
# ==========================================
tab1, tab2, tab3 = st.tabs(["🎛️ Mode Standar", "🚀 Mode Instant", "💡 Idea Corner"])

# ------------------------------------------
# TAB 1: MODE STANDAR
# ------------------------------------------
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        topik_standar = st.text_input("1. Topik Infografis", placeholder="Contoh: Bahaya Merokok pada Remaja")
        gaya_bahasa = st.selectbox("2. Gaya Bahasa Konten", ["Berita Nasional/Formal", "Singkat & Padat", "Edukasi Ramah"])
    with col2:
        tema_desain = st.selectbox("3. Tema Visual", list(TEMA_PROMPT.keys()), key="tema1")
        ukuran_gambar = st.selectbox("4. Ukuran", list(UKURAN_PROMPT.keys()), key="ukur1", index=0)

    if st.button("Generate 1 Prompt Padat (Standar)", type="primary", use_container_width=True):
        if topik_standar:
            with st.spinner('Merumuskan layout infografis padat merayap...'):
                instruksi = f"""
                Topik: "{topik_standar}". Gaya bahasa: {gaya_bahasa}.
                [TEMA] = {TEMA_PROMPT[tema_desain]}
                [UKURAN] = {UKURAN_PROMPT[ukuran_gambar]}
                {TEMPLATE_PROMPT_ENGINEER}
                """
                hasil_json = generate_json_from_gemini(instruksi)
                if hasil_json:
                    st.success("✅ Berhasil! 1 Prompt JSON Anda sudah siap.")
                    st.subheader("🎨 Prompt Gambar Flux (Copy dan Paste ke Banana)")
                    st.code(hasil_json.get('prompt_gambar_flux', ''), language="text")
                    with st.expander("⚙️ Lihat Struktur JSON Lengkap"):
                        st.code(json.dumps(hasil_json, indent=4), language="json")
        else:
            st.warning("Isi topik terlebih dahulu.")

# ------------------------------------------
# TAB 2: MODE INSTANT
# ------------------------------------------
with tab2:
    artikel = st.text_area("1. Paste Materi/Regulasi Panjang", height=150)
    col3, col4 = st.columns(2)
    with col3:
        tema_inst = st.selectbox("2. Tema Visual", list(TEMA_PROMPT.keys()), key="tema2")
    with col4:
        ukur_inst = st.selectbox("3. Ukuran", list(UKURAN_PROMPT.keys()), key="ukur2", index=0)

    if st.button("Ekstrak & Generate 1 Prompt Padat (Instant)", type="primary", use_container_width=True):
        if artikel:
            with st.spinner('Mengekstrak intisari dan menyusun tata letak padat...'):
                instruksi = f"""
                Ringkas teks berikut menjadi maksimal 5 poin SANGAT PENDEK: "{artikel}"
                [TEMA] = {TEMA_PROMPT[tema_inst]}
                [UKURAN] = {UKURAN_PROMPT[ukur_inst]}
                {TEMPLATE_PROMPT_ENGINEER}
                """
                hasil_json = generate_json_from_gemini(instruksi)
                if hasil_json:
                    st.success("✅ Artikel berhasil diekstrak menjadi 1 infografis siap render!")
                    st.subheader("🎨 Prompt Gambar Flux (Copy dan Paste ke Banana)")
                    st.code(hasil_json.get('prompt_gambar_flux', ''), language="text")
                    with st.expander("⚙️ Lihat Struktur JSON Lengkap"):
                        st.code(json.dumps(hasil_json, indent=4), language="json")
        else:
            st.warning("Paste artikel terlebih dahulu.")

# ------------------------------------------
# TAB 3: IDEA CORNER
# ------------------------------------------
with tab3:
    st.markdown("Masukkan kata kunci. AI akan meracik **1 konsep infografis final** yang sangat tajam dan siap dieksekusi.")
    kata_kunci = st.text_input("Masukkan Kata Kunci Pokok", placeholder="Contoh: Pencegahan Stunting, Validasi PKH, dll.")
    col5, col6 = st.columns(2)
    with col5:
        tema_ide = st.selectbox("Tema Visual", list(TEMA_PROMPT.keys()), key="tema3")
    with col6:
        ukur_ide = st.selectbox("Ukuran", list(UKURAN_PROMPT.keys()), key="ukur3", index=0)
    
    if st.button("Generate 1 Konsep Final Padat (Idea Corner)", type="primary", use_container_width=True):
        if kata_kunci:
            with st.spinner('Meracik 1 konsep infografis tingkat tinggi...'):
                instruksi = f"""
                Berikan TEPAT 1 (SATU) konsep infografis terbaik berdasarkan kata kunci "{kata_kunci}".
                [TEMA] = {TEMA_PROMPT[tema_ide]}
                [UKURAN] = {UKURAN_PROMPT[ukur_ide]}
                {TEMPLATE_PROMPT_ENGINEER}
                """
                hasil_json = generate_json_from_gemini(instruksi)
                if hasil_json:
                    st.success("✅ 1 Konsep final berhasil dibuat! Tinggal copy-paste.")
                    st.subheader("🎨 Prompt Gambar Flux (Copy dan Paste ke Banana)")
                    st.code(hasil_json.get('prompt_gambar_flux', ''), language="text")
                    with st.expander("⚙️ Lihat Struktur JSON Lengkap"):
                        st.code(json.dumps(hasil_json, indent=4), language="json")
        else:
            st.warning("Isi kata kunci terlebih dahulu.")
