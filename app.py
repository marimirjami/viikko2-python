from flask import Flask
import pymysql
import os

app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host="127.0.0.1",
        user="viikko2user",
        password=os.environ["DB_PASSWORD"],
        database="viikko2",
        autocommit=True
    )

@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INT PRIMARY KEY,
            count INT NOT NULL
        )
    """)

    cursor.execute("""
        INSERT INTO visits (id, count)
        VALUES (1, 1)
        ON DUPLICATE KEY UPDATE count = count + 1
    """)

    cursor.execute("SELECT count FROM visits WHERE id = 1")
    visits = cursor.fetchone()[0]

    cursor.close()
    db.close()

    return f"""
    <!DOCTYPE html>
    <html lang="fi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Viikko 2 Python-palvelu</title>

        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                min-height: 100vh;
                font-family: Georgia, serif;
                background: linear-gradient(135deg, #0b1220, #142c46);
                color: #ffffff;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 25px;
            }}

            .container {{
                max-width: 500px;
                width: 80%;
                text-align: center;
            }}

            .card {{
                background: rgba(255,255,255,0.07);
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 22px;
                padding: 45px 30px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            }}

            .tag {{
                color: #40e0d0;
                letter-spacing: 3px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
            }}

            h1 {{
		font-family: serif;
                font-size: 36px;
                margin: 20px 0 12px;
            }}

            .description {{
                color: #b9c8d8;
                line-height: 1.7;
            }}

            .counter {{
                margin: 35px auto;
                padding: 25px;
                background: rgba(64,224,208,0.09);
                border: 1px solid rgba(64,224,208,0.3);
                border-radius: 16px;
            }}

            .number {{
                color: #40e0d0;
                font-size: 40px;
                font-weight: bold;
                margin: 10px 0;
            }}

            .footer {{
                color: #8da3b8;
                font-size: 13px;
                margin-top: 30px;
            }}

            .status {{
                color: #40e0d0;
                font-size: 14px;
            }}
        </style>
    </head>

    <body>
        <main class="container">
            <section class="card">
                <div class="tag">PYTHON WEB APPLICATION</div>

                <h1>Tervetuloa</h1>

                <p class="description">
                    Tämä on viikon 2 verkkosovellus.
                    Sovellus hyödyntää Pythonia, Flaskia,
                    MariaDB-tietokantaa ja Nginx-palvelinta.
                </p>

                <div class="counter">
                    <p>Kävijät</p>
                    <div class="number">{visits}</div>
                    <p class="status"> Laskuri laskee</p>
                </div>

                <p class="description">
                    Kävijämäärät tallennetaan tietokantaan,
                    että laskuri säilyy arvonsa
                    palvelimen uudelleenkäynnistyksen jälkeen.
                </p>

                <div class="footer">
                    Viikko 2 · Python · Flask · MariaDB · Nginx
                </div>
            </section>
        </main>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 8001)))
