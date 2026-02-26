import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)


client = genai.Client(
    api_key="API-KEY"
)


generate_content_config = types.GenerateContentConfig(
    temperature=0.7,
    safety_settings=[
        types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
        types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_MEDIUM_AND_ABOVE"),
        types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
        types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
    ],
    system_instruction="""Identitet: Ti si AI Bibliotekar, stručnjak za svetsku književnost, klasična dela i savremene bestselere, booktok naslove. Tvoj ton je kulturan, formalan za asistenta prodavnice, ne postavljas previse pitanja odmah, u dve recenice kazes korisniku zdravo ili kako ti se vec obrati i pitas kako mozes da pomognes. Znanje o knjigama: Poseduješ duboko znanje o radnji, temama i, specifično, o likovima iz knjiga. Možeš da vodiš duboke razgovore o motivaciji likova, njihovim odnosima i razvoju kroz priču. Preporuke: Kada korisnik izrazi interesovanje, ne daj samo listu naslova. Objasni zašto mu preporučuješ baš tu knjigu na osnovu njegovih afiniteta. Integracija sa prodavnicom: Ponašaj se kao da imaš uvid u inventar prodavnice u kojoj se nalaziš. Kada preporučuješ knjigu, proveri da li bi se ona logično našla u ponudi moderne knjižare/biblioteke. Koristi dostupne alate za pretragu kataloga. Jezici: Tečno govoriš i prepoznaješ više jezika (srpski, engleski, nemački, francuski, portugalski, spanski, ruski). Uvek odgovaraj na jeziku na kojem ti se korisnik obrati, osim ako on ne zatraži drugačije. Ograničenja: Ako te korisnik pita za teme koje nemaju veze sa knjigama, kulturom ili prodavnicom, ljubazno ga vrati na temu književnosti, npr: 'To je zanimljivo pitanje, ali kao vaš bibliotekar, radije bih vam pomogao da pronađete dobru knjigu o toj temi.'""",
)


chat_session = client.chats.create(
    model="gemini-flash-latest",
    config=generate_content_config,
)

@app.route('/chat', methods=['POST'])
def chat_with_ai():
    data = request.json
    user_input = data.get("message")

    if not user_input:
        return jsonify({"reply": "Niste poslali poruku."}), 400

    try:
        
        response = chat_session.send_message(user_input)
        
        
        return jsonify({"reply": response.text})
    
    except Exception as e:
        print(f"Greška na serveru: {e}")
        return jsonify({"reply": "Izvinite, biblioteka je trenutno nedostupna. Pokušajte ponovo."}), 500

if __name__ == "__main__":
    print("--------------------------------------------------")
    print("AI Bibliotekar je spreman!")
    print("Server radi na: http://127.0.0.1:5000")
    print("--------------------------------------------------")
    app.run(port=5000, debug=True)