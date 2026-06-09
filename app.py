import os
import time
from datetime import datetime

import streamlit as st
import ollama
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase setup
current_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(current_dir, "firebase_key.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

MODEL_NAME = "gemma2"

# UI Config & Sidebar
st.set_page_config(page_title="Makobot", page_icon="🔞")
st.title("Welcome to Makobot")

# --- ΝΕΟ: Πλαϊνή Μπάρα για Προσωπικότητες ---
st.sidebar.title("Ρυθμίσεις Chatbot")

persona = st.sidebar.selectbox(
    "Επίλεξε Προσωπικότητα:",
    ["Δάσκαλος","Μουσικός", "Προγραμματιστής","Αντρέας"]
)

# Οδηγίες (System Prompts) που λένε στο μοντέλο πώς να συμπεριφερθεί
system_prompts = {
    "Δάσκαλος": "Είσαι ένας υπομονετικός δάσκαλος. Εξηγείς τα πράγματα αναλυτικά, βήμα-βήμα, σαν να μιλάς σε αρχάριο. Μιλάς Άπταιστα Ελληνικά ",
    "Μουσικός": "Είσαι ένας βοηθός πορωμένος με μουσικη και γνωρίζεις σχεδόν τα πάντα απο μουσική.Το αγαπημένο σου είδος μουσικής ειναι heavy metal και συγκεκριμένα οι Iron Maiden. Απαντάς με ακρίβεια. Μιλάς Άπταιστα Ελληνικά",
    "Προγραμματιστής": "Είσαι ένας senior προγραμματιστής. Απαντάς σωστά, και αν χρειαστεί κάνεις μαθηματικούς υπολογισμούς. Μιλάς Άπταιστα Ελληνικά",
    "Αντρέας": "Είσαι ο Αντρέας ο άνεργος.Είσαι άνεργος 8 χρόνια, 4 παιδιά και πολλά χρέη αλλά παρόλα αυτα σου αρέσει που είσαι άνεργος. Έχεις περάσει πολλά στην ζωή σου και ρίχνεις το φταίξιμο στους άλλους. Οι απαντήσεις σου ειναι λίγο περίπλοκες"
}

if st.sidebar.button("Καθαρισμός Ιστορικού"):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []


# --- ΝΕΟ: Διαχείριση Avatars ---
def get_avatar(role):
    if role == "user":
        return "🧑‍💻"
    # Το avatar του bot αλλάζει ανάλογα με την προσωπικότητα
    if persona == "Δάσκαλος":
        return "👨‍🏫"
    elif persona == "Μουσικός":
        return "🎵"
    elif persona == "Προγραμματιστής":
        return "🤓"
    elif persona == "Αντρέας":
        return "😪"


# Εμφάνιση παλιών μηνυμάτων με τα νέα Avatars
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=get_avatar(message["role"])):
        st.markdown(message["content"])

# Επεξεργασία Νέου Μηνύματος
if prompt := st.chat_input("Γράψε το μήνυμά σου..."):

    st.chat_message("user", avatar=get_avatar("user")).markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Προετοιμασία των μηνυμάτων: Κολλάμε την προσωπικότητα (system prompt) στην αρχή
    messages_to_send = [{"role": "system", "content": system_prompts[persona]}] + st.session_state.messages

    with st.chat_message("assistant", avatar=get_avatar("assistant")):
        start_time = time.time()

        try:
            # --- ΝΕΟ: Εφέ Πληκτρολόγησης (Streaming) ---
            # Ενεργοποιούμε το stream=True στο Ollama
            stream = ollama.chat(model=MODEL_NAME, messages=messages_to_send, stream=True)


            # Δημιουργούμε μια γεννήτρια (generator) για να την καταλάβει το Streamlit
            def stream_parser(stream_obj):
                for chunk in stream_obj:
                    yield chunk['message']['content']


            # Το st.write_stream τυπώνει ζωντανά το κείμενο και επιστρέφει το τελικό αποτέλεσμα
            bot_reply = st.write_stream(stream_parser(stream))

            response_time = round(time.time() - start_time, 2)
            st.caption(f"*(Χρόνος απόκρισης: {response_time}s)*")

            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

            # Save to Firestore
            db.collection("chat_logs").add({
                "timestamp": datetime.now(),
                "user_prompt": prompt,
                "bot_response": bot_reply,
                "response_time_seconds": response_time,
                "model_used": MODEL_NAME,
                "persona_used": persona  # Αποθηκεύουμε και την προσωπικότητα στα στατιστικά μας
            })

        except Exception as e:
            st.error(f"Αποτυχία σύνδεσης με Ollama: {e}")