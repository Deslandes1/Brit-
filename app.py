import streamlit as st
import asyncio
import edge_tts

# ================== Page Config ==================
st.set_page_config(
    page_title="Britney Gengel – Haiti's Saint",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================== Styling ==================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&display=swap');
    .stApp {
        background: radial-gradient(circle at center, #1a0f0a, #2a1e12);
        color: #fdf0d8;
    }
    h1, h2, h3 {
        font-family: 'Cinzel', serif;
        color: #ffcc88;
        text-shadow: 0 0 8px #cc8844;
    }
    .prayer-card {
        background: rgba(0,0,0,0.7);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255,200,100,0.5);
        box-shadow: 0 0 25px rgba(255,200,100,0.2);
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        font-size: 0.8rem;
        opacity: 0.8;
    }
    .saint-title {
        font-size: 2.2rem;
        text-align: center;
        margin-bottom: 0;
    }
    .energy-orb {
        width: 120px;
        height: 120px;
        background: radial-gradient(circle, rgba(255,200,100,0.3), transparent);
        border-radius: 50%;
        margin: 20px auto;
        animation: pulse 3s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(1); opacity: 0.5; }
    }
    .avatar-img {
        border-radius: 50%;
        width: 90px;
        height: 90px;
        object-fit: cover;
        border: 2px solid #ffaa66;
        box-shadow: 0 0 20px rgba(255,170,102,0.6);
    }
</style>
""", unsafe_allow_html=True)

# ================== Multilingual Prayer Texts ==================
prayer_britney_en = """
Brit, God had a mission for you so he sent you to Haiti because he wanted you to become a Saint,  
a Saint to save our children from hunger.  

We know that when you traveled to the eternal orient you knew that would happen but chose to not tell Mommy Cherylann, Papi, Tonton and Ritchy.  
However, your coming to Haiti among those who came was special because as Jesus was crucified on a cross, you also were crucified to become something greater – greater than human could ever imagine – to build a home for our innocent kids who were struggling with Haiti's life adversities.  

Because of you, roads were built.  
Because of you, Haitian fathers and mothers worked in the Brit's home construction to feed their own children.  
Because of you, this place called Grand‑Goâve, on a mountaintop with wild trees and no water, has become an oasis of love, peace and hope for the next generations of leaders in Haiti.  

We thank you from the bottom of our heart for your sacrifice and God's plan through you.  
Amen. Amen. Amen.
"""

prayer_britney_fr = """
Brit, Dieu avait une mission pour toi, alors il t'a envoyée en Haïti parce qu'il voulait que tu deviennes une Sainte,  
une Sainte pour sauver nos enfants de la faim.  

Nous savons que lorsque tu as voyagé vers l'orient éternel, tu savais ce qui allait arriver, mais tu as choisi de ne pas le dire à Maman Cherylann, Papi, Tonton et Ritchy.  
Pourtant, ta venue en Haïti parmi ceux qui sont venus était spéciale, car comme Jésus a été crucifié sur une croix, toi aussi tu as été crucifiée pour devenir quelque chose de plus grand – plus grand que ce que l'humain pourrait jamais imaginer – pour construire une maison pour nos enfants innocents qui luttaient contre les adversités de la vie en Haïti.  

Grâce à toi, des routes ont été construites.  
Grâce à toi, des pères et mères haïtiens ont travaillé à la construction de la maison de Brit pour nourrir leurs propres enfants.  
Grâce à toi, cet endroit appelé Grand‑Goâve, sur une montagne avec des arbres sauvages et sans eau, est devenu une oasis d'amour, de paix et d'espoir pour les prochaines générations de dirigeants en Haïti.  

Nous te remercions du fond du cœur pour ton sacrifice et pour le plan de Dieu à travers toi.  
Amen. Amen. Amen.
"""

prayer_britney_es = """
Brit, Dios tenía una misión para ti, por eso te envió a Haití porque quería que te convirtieras en Santa,  
una Santa para salvar a nuestros niños del hambre.  

Sabemos que cuando viajaste al oriente eterno sabías lo que iba a pasar, pero elegiste no decírselo a Mamá Cherylann, Papi, Tonton y Ritchy.  
Sin embargo, tu venida a Haití entre los que vinieron fue especial, porque así como Jesús fue crucificado en una cruz, tú también fuiste crucificada para convertirte en algo más grande – más grande de lo que el humano podría imaginar – para construir un hogar para nuestros niños inocentes que luchaban contra las adversidades de la vida en Haití.  

Gracias a ti, se construyeron caminos.  
Gracias a ti, padres y madres haitianos trabajaron en la construcción de la casa de Brit para alimentar a sus propios hijos.  
Gracias a ti, este lugar llamado Grand‑Goâve, en la cima de una montaña con árboles salvajes y sin agua, se ha convertido en un oasis de amor, paz y esperanza para las próximas generaciones de líderes en Haití.  

Te agradecemos desde el fondo de nuestro corazón por tu sacrificio y por el plan de Dios a través de ti.  
Amén. Amén. Amén.
"""

prayer_britney_zh = """
布里特，上帝对你有一个使命，所以他派你去了海地，因为他想让你成为一位圣人，  
一位拯救我们孩子免于饥饿的圣人。  

我们知道，当你前往永恒的东方时，你知道会发生什么，但你选择不告诉妈妈谢丽尔安、爸爸、通顿和里奇。  
然而，你来到海地是特别的，因为正如耶稣被钉在十字架上一样，你也被钉在十字架上，成为更伟大的存在——超越人类想象——为那些与海地生活逆境作斗争的无辜孩子们建立一个家园。  

因为有你，道路被修建。  
因为有你，海地的父亲和母亲们在布里特家园的工地上工作，养活自己的孩子。  
因为有你，这个叫做大戈阿沃的地方，一个原本只有野树和没有水的山顶，变成了爱、和平与希望的绿洲，造福海地下一代的领袖们。  

我们从心底感谢你的牺牲，以及上帝通过你所行的计划。  
阿门。阿门。阿门。
"""

# Map languages
prayers = {
    "English": {
        "text": prayer_britney_en,
        "voice": "en-US-ChristopherNeural"
    },
    "French": {
        "text": prayer_britney_fr,
        "voice": "fr-FR-HenriNeural"
    },
    "Spanish": {
        "text": prayer_britney_es,
        "voice": "es-ES-AlvaroNeural"
    },
    "Chinese": {
        "text": prayer_britney_zh,
        "voice": "zh-CN-YunxiNeural"
    }
}

# ================== Cached TTS Audio ==================
@st.cache_data(show_spinner=False)
def get_audio_bytes(text, voice):
    async def _generate():
        communicate = edge_tts.Communicate(text, voice)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return audio_data
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(_generate())
    loop.close()
    return result

# ================== Sidebar ==================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/circled.png", width=80)
    st.markdown("## GlobalInternet.py")
    st.markdown("**Gesner Deslandes**, Engineer-in-Chief")
    st.markdown("---")
    st.markdown("### 🌐 Language")
    language = st.selectbox("Choose language", list(prayers.keys()))
    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("📱 (509)-47385663")
    st.markdown("✉️ deslandes78@gmail.com")
    st.markdown("🌐 [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown("### 💰 Offer a Donation")
    st.markdown("Support this eternal work: **$9.99 USD** (one‑time)")
    st.markdown("*All proceeds keep the energy alive*")
    st.markdown("---")
    st.caption("© 2025 GlobalInternet.py")

# ================== Main Layout with Avatar ==================
st.markdown('<div class="energy-orb"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.title("🕊️ Britney Gengel – Haiti's Saint 🕊️")
    st.markdown("### *A Canonization Rosary Book*")
with col2:
    avatar_url = "https://raw.githubusercontent.com/Deslandes1/Rosary-of-Kettely-Elucia-/refs/heads/main/Gesner%20Deslandes.png"
    st.markdown(f'<img src="{avatar_url}" class="avatar-img" style="float:right;">', unsafe_allow_html=True)

st.markdown("#### *Canonized by Gesner Deslandes – Eternal Light of Haiti*")
st.caption("Built by Gesner Deslandes at GlobalInternet.py")

# ================== Rosary Counter ==================
def rosary_counter(person_name):
    st.markdown("---")
    st.subheader("📿 Interactive Rosary – Click each bead as you pray")
    beads = 10
    if f"beads_{person_name}" not in st.session_state:
        st.session_state[f"beads_{person_name}"] = [False] * beads
    
    cols = st.columns(beads)
    for i, col in enumerate(cols):
        with col:
            if st.button("●", key=f"{person_name}_bead_{i}", use_container_width=True):
                st.session_state[f"beads_{person_name}"][i] = not st.session_state[f"beads_{person_name}"][i]
                st.rerun()
            if st.session_state[f"beads_{person_name}"][i]:
                st.markdown('<div style="color:#ffaa44; text-align:center;">✨</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="color:#666; text-align:center;">○</div>', unsafe_allow_html=True)
    
    if all(st.session_state[f"beads_{person_name}"]):
        st.success(f"✨ You have completed the rosary for Britney Gengel! May her light shine forever. ✨")
        if st.button("Reset Rosary", key=f"reset_{person_name}"):
            st.session_state[f"beads_{person_name}"] = [False] * beads
            st.rerun()
    else:
        st.caption(f"{sum(st.session_state[f'beads_{person_name}'])} / {beads} beads prayed")

# ================== Prayer Card with AI Voice ==================
st.markdown('<div class="prayer-card">', unsafe_allow_html=True)
st.markdown('<div class="saint-title">🌸 Saint Britney Gengel – Brit, Haiti\'s Saint 🌸</div>', unsafe_allow_html=True)
st.markdown("*Her sacrifice built an oasis of love*")
st.markdown(prayers[language]["text"])

if st.button("🔊 Recite Prayer (Energy Activation)", key="britney_pray"):
    with st.spinner("Generating sacred audio..."):
        audio_bytes = get_audio_bytes(prayers[language]["text"], prayers[language]["voice"])
        st.audio(audio_bytes, format="audio/mp3")
    st.balloons()
    st.markdown('<div style="background: radial-gradient(circle, gold, transparent); padding: 1rem; border-radius: 20px; text-align:center;">✨ The spirit of Britney Gengel embraces Haiti. Amen. Amen. Amen. ✨</div>', unsafe_allow_html=True)

rosary_counter("Britney")
st.markdown('</div>', unsafe_allow_html=True)

# ================== Footer ==================
st.markdown("""
<div class="footer">
    <p>🌌 *In the name of the 1 – the Architect of this Universe* 🌌</p>
    <p>May the eternal soul of Britney Gengel watch over Haiti's children and bring hope to Grand‑Goâve.</p>
    <p>Built by Gesner Deslandes – GlobalInternet.py | For canonization inquiries, contact above.</p>
</div>
""", unsafe_allow_html=True)
