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

st.sidebar.title("⚙️ Pengaturan Sistem")

# Sistem Keamanan Ganda
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success("✅ API Key sistem terhubung aman.")
except (KeyError, FileNotFoundError):
    API_KEY = st.sidebar.text_input("Masukkan API Key Gemini Anda:", type="password", help="Wajib diisi agar AI bisa bekerja.")

st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 **Dev: VDMotionStudio**")
st.sidebar.caption("Sistem Otomasi Infografis Standar Profesional")

st.title("⚡ Power Tools Kreator (Pro Layout Edition)")
st.markdown("Engine prompt untuk menghasilkan infografis **Creative Vector** bergaya dinamis (berisi doodle panah, blok terstruktur, dan ikon detail) persis seperti standar agensi kreatif.")
st.markdown("---")

# ==========================================
# Database Pemetaan Visual 
# ==========================================
TEMA_PROMPT = {
    "Creative Vector / Doodle Accent (Sesuai Referensi)": "high-end creative flat vector illustration, playful but professional infographic layout, subtle off-white background, hand-drawn doodle arrows directing flow, wavy section dividers, ultra-detailed 2D vector graphics, masterpiece",
    "Professional News Agency / Gov PSA": "high-end professional public service announcement infographic poster, clean vector style mixed with highly realistic 3D elements, smooth gradient background, highly structured grid layout, corporate typography",
    "Claymation / 3D Diorama Miniatur": "hyper-detailed miniature claymation diorama, tilt-shift photography, cute stylized stop-motion aesthetic, tactile clay textures, highly detailed 3D typography"
}

UKURAN_PROMPT = {
    "9:16 (Story/Shorts/Tiktok)": "aspect ratio 9:16",
    "1:1 (Feed/Square)": "aspect ratio 1:1",
    "4:5 (Portrait IG)": "aspect ratio 4:5",
    "16:9 (Landscape/YouTube)": "aspect ratio 16:9"
}

# ==========================================
# Fungsi Pemanggil AI (Sudah Diperbaiki Bebas Error)
# ==========================================
def generate_json_from_gemini(prompt_instruksi):
    if not API_KEY:
        st.error("⚠️ API Key belum dimasukkan. Silakan cek pengaturan di sidebar.")
        return None
        
    genai.configure(api_key=API_KEY)
    
    # Menghapus generation_config agar kompatibel dengan versi library lama
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    try:
        response = model.generate_content(prompt_instruksi)
        teks_hasil = response.text.strip()
        
        # Membersihkan tanda kutip markdown (```json ... ```) 
        if teks_hasil.startswith("```json"):
            teks_hasil = teks_hasil[7:]
        elif teks_hasil.startswith("```"):
            teks_hasil = teks_hasil[3:]
            
        if teks_hasil.endswith("```"):
            teks_hasil = teks_hasil[:-3]
            
        return json.loads(teks_hasil.strip())
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memanggil AI: Cek format atau API Key Anda. Detail: {e}")
        return None

# ==========================================
# Template Instruksi Ekstrem (PRO LAYOUT)
# ==========================================
TEMPLATE_PROMPT_ENGINEER = """
Kamu adalah Master Prompt Engineer untuk AI Image Generator (Flux/Midjourney). Tugasmu meracik TEPAT 1 (SATU) prompt visual yang mendikte tata letak infografis vertikal bergaya agensi kreatif yang dinamis, terstruktur, dan penuh elemen.

TUGAS PENTING: 
Teks (exact text) HARUS SANGAT SINGKAT (maksimal 2-4 kata) agar ejaan AI tepat.

Format JSON WAJIB:
{{
    "judul_infografis": "Judul Utama (Maks 4 kata)",
    "poin_materi": ["Poin 1", "Poin 2", "Poin 3", "Poin 4"],
    "prompt_gambar_flux": "A fully finished, highly engaging professional infographic poster, [UKURAN]. Visual aesthetic: [TEMA]. TYPOGRAPHY: Ultra-crisp, bold modern typography. LAYOUT STRUCTURE (DYNAMIC VERTICAL FLOW): The canvas is divided into distinct sections separated by subtle wavy lines. TOP HEADER: Catchy, massive bold 3D text reading 'JUDUL_UTAMA' with a tiny subtext box below it. BODY SECTIONS: 4 distinct horizontal blocks. Section 1: exact text 'POIN_1' accompanied by a large, highly detailed central vector illustration of [DESKRIPSI OBJEK 1], surrounded by small hand-drawn arrows pointing to tiny detailed sub-icons. Section 2: exact text 'POIN_2' with a main illustration of [DESKRIPSI OBJEK 2] and doodle arrows pointing to sub-icons. Section 3: exact text 'POIN_3' with [DESKRIPSI OBJEK 3] and doodle elements. Section 4: exact text 'POIN_4' with [DESKRIPSI OBJEK 4]. BOTTOM FOOTER: A distinct rectangular banner containing exact text 'CALL_TO_ACTION_SINGKAT' with a professional vector icon. BACKGROUND: Soft off-white/pastel background, populated with floating abstract shapes, tiny plus signs, and infographic dots. 8k resolution, award-winning Behance layout design."
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
        gaya_bahasa = st.selectbox("2. Gaya Bahasa Konten", ["Santai & Kreatif (Sesuai Referensi)", "Berita Nasional/Formal", "Singkat & Padat"])
    with col2:
        tema_desain = st.selectbox("3. Tema Visual", list(TEMA_PROMPT.keys()), key="tema1", index=0)
        ukuran_gambar = st.selectbox("4. Ukuran", list(UKURAN_PROMPT.keys()), key="ukur1", index=0)

    if st.button("Generate 1 Prompt Pro (Standar)", type="primary", use_container_width=True):
        if topik_standar:
            with st.spinner('Merumuskan struktur layout kreatif...'):
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
        tema_inst = st.selectbox("2. Tema Visual", list(TEMA_PROMPT.keys()), key="tema2", index=0)
    with col4:
        ukur_inst = st.selectbox("3. Ukuran", list(UKURAN_PROMPT.keys()), key="ukur2", index=0)

    if st.button("Ekstrak & Generate 1 Prompt Pro (Instant)", type="primary", use_container_width=True):
        if artikel:
            with st.spinner('Mengekstrak intisari dan menyusun tata letak...'):
                instruksi = f"""
                Ringkas teks berikut menjadi maksimal 4 poin SANGAT PENDEK: "{artikel}"
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
        tema_ide = st.selectbox("Tema Visual", list(TEMA_PROMPT.keys()), key="tema3", index=0)
    with col6:
        ukur_ide = st.selectbox("Ukuran", list(UKURAN_PROMPT.keys()), key="ukur3", index=0)
    
    if st.button("Generate 1 Konsep Final Pro (Idea Corner)", type="primary", use_container_width=True):
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
