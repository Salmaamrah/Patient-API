# Patient-API

Een RESTful API voor het beheren van patiëntgegevens, gebouwd met FastAPI en SQLAlchemy.  
De API ondersteunt het aanmaken, ophalen, updaten en verwijderen van patiënten, inclusief validatie van gegevens en masking van diagnoses.  

## Features
- Voeg nieuwe patiënten toe met naam, telefoonnummer, diagnose, bloedgroep, leeftijd en e-mail
- Ophalen van alle patiënten of zoeken op:
  - **ID**
  - **Telefoonnummer**
- Updaten en verwijderen van patiënten
- Validaties:
  - Telefoonnummer moet 10 cijfers bevatten
  - Leeftijd mag niet negatief zijn
  - Unieke validatie voor telefoonnummer en e-mail
- Diagnoses worden gedeeltelijk geanonimiseerd (alleen de eerste 3 karakters zichtbaar)

| Methode | Endpoint                             | Beschrijving              |
| ------- | ------------------------------------ | ------------------------- |
| GET     | `/`                                  | Welkomstbericht           |
| GET     | `/patients/`                         | Alle patiënten ophalen    |
| GET     | `/patients/search/?phone=1234567890` | Zoeken op telefoonnummer  |
| GET     | `/patients/{patient_id}`             | Ophalen via ID            |
| POST    | `/patients/`                         | Nieuwe patiënt toevoegen  |
| PUT     | `/patients/{patient_id}`             | Patiëntgegevens bijwerken |
| DELETE  | `/patients/{patient_id}`             | Patiënt verwijderen       |

## ⚡ Installatie & Gebruik
1. **Download main.py**
   

2. **Maak een virtuele omgeving en installeer dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate   
   pip install -r requirements.txt
   ```

3. **Start de API**
   ```bash
   fastapi dev main.py
   ```

4. **Open de docs en gebruik de API**
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
