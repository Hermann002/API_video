from sqlalchemy import create_engine, text

db_Connection_string = 'mysql+pymysql://h3gw8trhy0vhtiitvxy9:pscale_pw_b6TLW2YxsVlKeXNMQ2zdWuO0fMxUWROgigkFI5krkba@aws.connect.psdb.cloud/testdatabase'

#connexion à la BD
engine = create_engine(db_Connection_string,
    connect_args={
        "ssl": {
        "ssl_ca": "/etc/ssl/cert.pem"
        }
    })


#recuperation des informations dans la base de données

def fetch_user():
    with engine.connect() as conn:
        result = conn.execute(text("select * from Boutique"))

        result_dicts = []

        for row in result.all():
            result_dicts.append(row._asdict())
        
        return result_dicts
    
def fetch_live():
    with engine.connect() as conn:
        result = conn.execute(text("select * from Boutique"))

        result_dicts = []

        for row in result.all():
            result_dicts.append(row._asdict())
        
        return result_dicts

#ajout des données des lives crées dans la base de données
def db_append_live(user_data):
    with engine.connect() as conn:
        nomLive = user_data['nomLive']
        urlRtmp = user_data['urlRtmp']
        proprietaire = user_data['proprietaire']

        query = text(f'INSERT INTO Live (urlRtmp, LiveEventName, proprietaire) VALUES ("{urlRtmp}", "{nomLive}", "{proprietaire}")')

        conn.execute(query)
        return

#ajout des données des utilisateurs dans la base de données
def db_append_boutique(user_data):
    with engine.connect() as conn:
        name = user_data['name']
        shop = user_data['shop']
        address = user_data['email']
        local = user_data['local']
        query = text(f'INSERT INTO Boutique (nomProprietaire, nomBoutique, emailProp, localisation) VALUES ( "{name}", "{shop}", "{address}", "{local}")')

        conn.execute(query)
        return
    

# verification des informations reçues dans l'URL
def verify(live_name):
    lives = fetch_live()
    for live in lives :
        if live_name == live['proprietaire']:
            live_event_name = live['liveEventName']
    
    return live_event_name