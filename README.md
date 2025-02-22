# pychat
Voglio creare una web application per gestire una chat tra due individui.
I tipi di utenti possono essere gli utilizzatori (chiunque) oppure i counselor (soggetti abilitati). Infine ci saranno gli amministratori.
L'applicazione deve quindi consentire la registrazione di nuovi utenti e la creazione di utenti amministratori che gestiscano l'ambiente.
Ogni utente può avviare più chat e ogni counselor può partecipare a più chat.
Le chat devono mantenere la storia della conversazione che può essere ripresa in qualunque momento.


Vorrei creare due docker:
1) application server in python che lavori tramite pagina web in react e API rest
2) db server in postgresql per gestire utenti e chat





------------work in progress

# Comandi per risolvere:
## Elimina eventuali container residui
docker-compose down --remove-orphans
## Ricostruisci le immagini
docker-compose build --no-cache
## Avvia i container
docker-compose up -d


Se usi Windows, assicurati che:
I file non siano in una cartella OneDrive/Dropbox
I Dockerfile abbiano estensione corretta (senza .txt nascosto)
I permessi delle cartelle consentano l'accesso a Docker


## Controlla che i Dockerfile siano riconosciuti
docker-compose config




Importante: Se incontri errori di connessione al database:

Verifica che MariaDB sia effettivamente in ascolto sulla porta 3306:
docker-compose exec db mysql -u user -ppassword mydatabase

Controlla i log del database:
docker-compose logs db


# Problema di connessione a MariaDB:
Il client MySQL non è installato nel container. Per accedere al database usa:
docker-compose exec db mariadb -u user -ppassword mydatabase


# Verifica privilegi utente database:
docker-compose exec db mariadb -u root -prootpassword -e "SHOW GRANTS FOR 'user'@'%';"


# API
Per creare utenti
$ curl -X POST -H "Content-Type: application/json" -d '{
    "username": "testuser",
    "email": "user@example.com",
    "password": "password123"
}' http://localhost:5000/api/auth/register
{"msg":"User created"}
