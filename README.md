Keskustelusovellus on käytössä osoitteessa https://hajoitustyo-keskustelusovellus.fly.dev/
Jos sivu ei aukea heti, koita päivittää sivu.

Jos linkki ei toimi, niin sovelluksen saa käynnistettyä paikallisesti lataamalla tämä repositorio ja tekemällä seuraavat asiat:

lisää juuri kansioon tiedosto nimeltä ".env" Ja määritä sen sisältö seuraavanlaiseksi:
'''
DATABASE_URL=tietokannan-paikallinen-osoite
SECRET_KEY=salainen-avain
'''
Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:
'''
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
'''
Määritellään tietokannan skeema komennolla
'''
$ psql < schema.sql
'''
schema.sql tiedosto luo samalla 2 aihealuetta valmiiksi aloittamisen helpottamiseksi.

nyt sovelluksen pitäisi käynnistyä komennolla
'''
flask run
'''
osoitteeseen http://127.0.0.1:5000/

Sovelluksen saa suljettua painamalla ctrl+c terminaalissa, ja virtuaaliympäristön saa keskeytettyä komennolla
'''
deactivate
'''

soveeluksen db.py tiedostossa saatta joutua muokkaamaan 
'''
.getenv(DATABASE_URL).replace("://", "ql://", 1)
'''
muotoon:
'''
.getenv(DATABASE_URL)
'''


Keskustelusovelluksessa on eri aihealueita, joita admin käyttäjät voivat lisätä ja poistaa. Aihelueet ovat joko avoimia kaikille, tai näkyvissä vain sisäänkirjautuneille admineille. Sovellukseen voi rekisteröityä joko tavallisena käyttäjänä tai admin-käyttäjänä. Rekisteröityneet käyttäjät voivat aloittaa uusia ketjuja eri aihealueisiin, sekä vastata omiin tai muiden ketjuihin viesteillä. Käyttäjät voivat poistaa omia viestejä ja aloittamiaan ketjuja. Adminit puolestaan voivat poistaa kenen tahansa aloittamia ketjuja ja viestejä. Sovelluksessa on myös hakutoiminto, joka etsii hakusanaa ketjujen otsikoista, sekä ohjeet-sivu.

Sovellukseen on tarkoitus toteuttaa vielä ainakin seuraavia ominaisuuksia:
- Aihealueisiin tulee näkyviin, kuinka monta ketjua ja viestiä siellä on
- ketjuihin tulee näkyviin kuinka monta viestiä siellä on
- virheiden käsittelyn ja turvallisuuden parantaminen
- ulkoasun muokkaus käyttäjäystävällisemmäksi
- mahdollisesti upvote/downvote ominaisuus ketjuihin ja viesteihin
