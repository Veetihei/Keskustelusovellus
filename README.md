Keskustelusovellus on käytössä osoitteessa https://hajoitustyo-keskustelusovellus.fly.dev/
Jos sivu ei aukea heti, koita päivittää sivu.

Jos linkki ei toimi, niin sovelluksen saa käynnistettyä paikallisesti lataamalla tämä repositorio ja tekemällä seuraavat asiat:

lisää juuri kansioon tiedosto nimeltä ".env" Ja määritä sen sisältö seuraavanlaiseksi:

DATABASE_URL=tietokannan-paikallinen-osoite

SECRET_KEY=salainen-avain

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```

Määritellään tietokannan skeema komennolla
```
$ psql < schema.sql
```

schema.sql tiedosto luo samalla 2 aihealuetta valmiiksi aloittamisen helpottamiseksi.

nyt sovelluksen pitäisi käynnistyä komennolla
```
flask run
```
osoitteeseen http://127.0.0.1:5000/

Sovelluksen saa suljettua painamalla ctrl+c terminaalissa, ja virtuaaliympäristön saa keskeytettyä komennolla
```
deactivate
```

Keskustelusovelluksessa on eri aihealueita, joita admin käyttäjät voivat lisätä ja poistaa. Aihelueet ovat joko avoimia kaikille, tai näkyvissä vain sisäänkirjautuneille admineille. Etusivulla näkyy, kuinka monta ketjua kussakin aihealueessa on.

Sovellukseen voi rekisteröityä joko tavallisena käyttäjänä tai admin-käyttäjänä. Rekisteröityneet käyttäjät voivat aloittaa uusia ketjuja eri aihealueisiin, sekä vastata omiin tai muiden ketjuihin viesteillä. 

Sisäänkirjautuneet käyttäjät voivat myös upvotettaa tai downvotettaa kaikkia ketjun vastauksia.

Käyttäjät voivat poistaa omia viestejä ja aloittamiaan ketjuja. Adminit puolestaan voivat poistaa kenen tahansa aloittamia ketjuja ja viestejä. 

Sovelluksessa on myös hakutoiminto, joka etsii hakusanaa ketjujen otsikoista, sekä ohjeet-sivu.

Sovellus on tehty Helsingin-yliopiston tietokantasovellus-kurssia varten.
