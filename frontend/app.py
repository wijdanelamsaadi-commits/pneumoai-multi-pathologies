"""
Interface Streamlit pour le systeme de detection de pneumonie
Avec evaluation de la qualite de l'image
"""

import streamlit as st
import sys
import os

# Ajouter le dossier src au path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from quality_assessment import QualityAssessment


# ===== CONFIGURATION DE LA PAGE =====
st.set_page_config(
    page_title="Detection Pneumonie + Qualite",
    page_icon="🫁",
    layout="wide"
)


# ===== CHARGEMENT DU MODELE (avec cache) =====
@st.cache_resource
def load_resources():
    """Charger le modele et le module qualite (une seule fois)"""
    model_path = "models/pneumonia_binary.keras"
    if not os.path.exists(model_path):
        model_path = "models/pneumonia_model.keras"
    model = load_model(model_path)
    quality = QualityAssessment()
    return model, quality


# ===== FONCTIONS UTILES =====
def predict_pneumonia(image, model):
    """Faire la prediction de pneumonie"""
    img_resized = image.resize((224, 224))
    img_array = np.array(img_resized) / 255.0
    img_batch = np.expand_dims(img_array, axis=0)
    
    prediction = model.predict(img_batch, verbose=0)
    probability = float(prediction[0][0])
    
    if probability >= 0.5:
        diagnosis = "PNEUMONIA"
        confidence = probability * 100
    else:
        diagnosis = "NORMAL"
        confidence = (1 - probability) * 100
    
    return diagnosis, confidence, probability


def get_color_for_decision(decision):
    """Couleur selon la decision"""
    colors = {
        'ACCEPTABLE': '#00C851',     # Vert
        'MOYENNE': '#FF8800',        # Orange
        'REJET': '#FF4444',          # Rouge
    }
    return colors.get(decision, '#666666')


# ===== INTERFACE =====

# Titre principal
st.title("🫁 Detection de Pneumonie par Intelligence Artificielle")
st.markdown("### Avec evaluation de la qualite de la radiographie")
st.markdown("---")


# Charger les ressources
with st.spinner("Chargement du systeme..."):
    model, quality_module = load_resources()

st.success("✅ Systeme charge et pret!")


# Sidebar avec informations
with st.sidebar:
    st.header("ℹ️ A propos")
    st.markdown("""
    Ce systeme analyse une radiographie thoracique en 2 etapes:
    
    **1. Evaluation de la qualite**
    - Nettete (detection flou)
    - Luminosite (exposition)
    - Contraste
    
    **2. Diagnostic de pneumonie**
    - Modele: MobileNetV2
    - Precision: 88.62%
    
    **Decisions possibles:**
    - 🟢 Diagnostic fiable
    - 🟠 Diagnostic avec prudence
    - 🔴 Reacquisition requise
    """)
    
    st.markdown("---")
    st.markdown("**PFE 2026**")
    st.markdown("Detection automatique de pneumonie")


# Zone principale
st.header("📤 Uploader une radiographie")

uploaded_file = st.file_uploader(
    "Choisir une image (JPEG, PNG)",
    type=['jpg', 'jpeg', 'png']
)


if uploaded_file is not None:
    
    # Charger l'image
    image = Image.open(uploaded_file).convert('RGB')
    
    # Layout en 2 colonnes
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🖼️ Image uploadee")
        st.image(image, caption=uploaded_file.name, use_container_width=True)
    
    with col2:
        st.subheader("📊 Resultats de l'analyse")
        
        # ===== ANALYSE DE QUALITE =====
        with st.spinner("Analyse de la qualite..."):
            quality_result = quality_module.evaluate(image)
        
        # Score global de qualite
        st.markdown("#### 🔍 Qualite de l'image")
        
        # Barre de progression colorée pour le score global
        global_score = quality_result['global_score']
        decision = quality_result['decision']
        color = get_color_for_decision(decision)
        
        st.markdown(f"""
        <div style='background-color:{color}; padding:10px; border-radius:5px; text-align:center; color:white; font-weight:bold; font-size:18px;'>
            {decision} - Score: {global_score:.1f}/100
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Details des 3 criteres
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric(
                "Nettete", 
                f"{quality_result['sharpness']['score']:.0f}/100",
                delta=None
            )
            st.progress(quality_result['sharpness']['score'] / 100)
        
        with col_b:
            st.metric(
                "Luminosite", 
                f"{quality_result['brightness']['score']:.0f}/100"
            )
            st.progress(quality_result['brightness']['score'] / 100)
        
        with col_c:
            st.metric(
                "Contraste", 
                f"{quality_result['contrast']['score']:.0f}/100"
            )
            st.progress(quality_result['contrast']['score'] / 100)
        
        st.markdown("---")
        
        # ===== DIAGNOSTIC =====
        st.markdown("#### 🩺 Diagnostic")
        
        if decision == 'REJET':
            st.error("❌ **DIAGNOSTIC NON EFFECTUE**")
            st.warning(f"⚠️ {quality_result['recommendation']}")
        else:
            with st.spinner("Analyse par l'IA..."):
                diagnosis, confidence, probability = predict_pneumonia(image, model)
            
            # Afficher diagnostic
            if diagnosis == "PNEUMONIA":
                st.error(f"🔴 **{diagnosis}** detecte")
            else:
                st.success(f"🟢 **{diagnosis}** (poumons sains)")
            
            # Confiance
            st.metric("Confiance du diagnostic", f"{confidence:.1f}%")
            st.progress(confidence / 100)
            
            st.markdown("---")
            
            # ===== DECISION FINALE =====
            st.markdown("#### 🎯 Decision finale")
            
            if decision == 'ACCEPTABLE':
                st.success(f"""
                ✅ **DIAGNOSTIC FIABLE**
                
                Diagnostic: **{diagnosis}** ({confidence:.1f}%)
                
                La qualite de l'image est suffisante pour un diagnostic fiable.
                """)
            elif decision == 'MOYENNE':
                st.warning(f"""
                ⚠️ **DIAGNOSTIC AVEC PRUDENCE**
                
                Diagnostic: **{diagnosis}** ({confidence:.1f}%)
                
                La qualite de l'image est moyenne. Une validation par un radiologue est recommandee.
                """)


else:
    # Message d'accueil quand pas d'image
    st.info("👆 Uploader une radiographie pour commencer l'analyse")
    
    st.markdown("---")
    st.markdown("### 📚 Comment ca marche?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 1️⃣ Upload
        Uploadez une radiographie thoracique (JPEG ou PNG)
        """)
    
    with col2:
        st.markdown("""
        ### 2️⃣ Analyse
        Le systeme evalue la qualite ET detecte la pneumonie
        """)
    
    with col3:
        st.markdown("""
        ### 3️⃣ Decision
        Diagnostic fiable, avec prudence ou rejet selon la qualite
        """)
