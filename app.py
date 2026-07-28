import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3

st.title("Statystyki piłkarskie")
st.set_page_config(layout="wide")

conn = sqlite3.connect("staty.db")
mecze = """
    SELECT 
    Mecze.kolejka,
    gospodarze.Nazwa AS Gospodarz,
    goscie.Nazwa AS Gosc,
    Mecze.stat_gospo AS 'Faule gospodarz',
    Mecze.stat_gosc AS 'Faule gosc',
    (Mecze.stat_gospo + Mecze.stat_gosc) AS 'Meczowe',
    Sędziowie.Nazwa AS Sędzia
    FROM Mecze
    LEFT JOIN Kluby AS gospodarze ON Mecze.id_gospo = gospodarze.id
    LEFT JOIN kluby AS goscie ON Mecze.id_gosc = goscie.id
    LEFT JOIN Sędziowie ON Mecze.id_sedzia = Sędziowie.id;
        """
dfekstra = pd.read_sql_query(mecze, conn)

polacz = sqlite3.connect("Worldcup.db")
ogólna = """
    SELECT 
    kraj1.Nazwa as 'Drużyna 1', 
    kraj2.Nazwa as 'Drużyna 2',
    Mecze.gole_kraj1 AS 'Gole drużyny 1',
    Mecze.gole_kraj2 As 'Gole drużyny 2',
    Mecze.strzaly_kraj1 AS 'Strzały drużyny 1',
    Mecze.strzaly_kraj2 AS 'Strzały drużyny 2',
    Mecze.celne_kraj1 AS 'Celne strzały drużyny 1',
    Mecze.celne_kraj2 AS 'Celne strzały drużyny 2',
    Mecze.faule_kraj1 AS 'Faule drużyny 1', 
    Mecze.faule_kraj2 AS 'Faule drużyny 2',
    Mecze.rozne_kraj1 AS 'Rożne drużyny 1',
    Mecze.rozne_kraj2 AS 'Rożne drużyny 2',
    Mecze.kartki_kraj1 AS 'Kartki drużyny 1',
    Mecze.kartki_kraj2 AS 'Kartki drużyny 2',
    Mecze.auty_kraj1 AS 'Auty drużyny 1',
    Mecze.auty_kraj2 AS 'Auty drużyny 2',
    Mecze.odbiory_kraj1 AS 'Odbiory drużyny 1',
    Mecze.odbiory_kraj2 AS 'Odbiory drużyny 2',
    Mecze.spalone_kraj1 AS 'Spalone drużyny 1',
    Mecze.spalone_kraj2 AS 'Spalone drużyny 2',
    Mecze.podania_kraj1 AS 'Podania drużyny 1',
    Mecze.podania_kraj2 AS 'Podania drużyny 2',
    Sędziowie.Nazwa AS Sędzia
    FROM Mecze 	
    LEFT Join Kraje as kraj1 on Mecze.id_kraj1 = kraj1.id_kraj
    LEFT Join Kraje as kraj2 on Mecze.id_kraj2 = kraj2.id_kraj
    LEFT Join Sędziowie on Mecze.id_sędzia = Sędziowie.id_sędzia;
    """
dfwc = pd.read_sql_query(ogólna, polacz)

sędziowa = """
        SELECT Sędziowie.Nazwa, count(*) as mecze, avg(faule_kraj1 + faule_kraj2) as Faule, avg(kartki_kraj1 + kartki_kraj2) as Kartki
        from Mecze, Sędziowie
        where Mecze.id_sędzia = Sędziowie.id_sędzia
        group by Nazwa
        order by faule desc
        """
dfsedzia = pd.read_sql_query(sędziowa, polacz).round(2)


df1 = dfwc[['Drużyna 1', 'Gole drużyny 1', 'Gole drużyny 2', 'Strzały drużyny 1', 'Strzały drużyny 2', 'Celne strzały drużyny 1', 'Celne strzały drużyny 2',  'Faule drużyny 1', 'Faule drużyny 2', 'Rożne drużyny 1', 'Rożne drużyny 2', 'Kartki drużyny 1', 'Kartki drużyny 2', 'Auty drużyny 1', 'Auty drużyny 2', 'Odbiory drużyny 1', 'Odbiory drużyny 2', 'Podania drużyny 1', 'Podania drużyny 2', 'Spalone drużyny 1', 'Spalone drużyny 2']].copy()
df2 = dfwc[['Drużyna 2', 'Gole drużyny 2', 'Gole drużyny 1', 'Strzały drużyny 2', 'Strzały drużyny 1', 'Celne strzały drużyny 2', 'Celne strzały drużyny 1', 'Faule drużyny 2', 'Faule drużyny 1', 'Rożne drużyny 2', 'Rożne drużyny 1', 'Kartki drużyny 2', 'Kartki drużyny 1', 'Auty drużyny 2', 'Auty drużyny 1', 'Odbiory drużyny 2', 'Odbiory drużyny 1', 'Podania drużyny 2', 'Podania drużyny 1', 'Spalone drużyny 2', 'Spalone drużyny 1']].copy()
df1.columns = df2.columns = ['Drużyna', 'Gole strzelone', 'Gole stracone', 'Strzały wykonane', 'Strzały przeciwko', 'Celne wykonane', 'Celne przeciwko', 'Faule popełnione', 'Faule wywalczone', 'Rożne zdobyte', 'Rożne stracone', 'Kartki otrzymane', 'Kartki przeciwko', 'Auty zdobyte', 'Auty przeciwko', 'Odbiory wykonane', 'Odbiory przeciwko', 'Podania wykonane', 'Podania przeciwnika', 'Spalone zrobione', 'Spalone przeciwnika']
dfciek = pd.concat([df1, df2], ignore_index=True)
dfsrednie = dfciek.groupby('Drużyna').mean().round(2).reset_index()

Czeska, ILiga, Ekstraklasa2, Norweska, Szwedzka,  Mundial, Ekstraklasa1 = st.tabs(["Chance Liga", "Betclic 1 Liga","Ekstraklasa 2026/2027", "Elitenserien 2026", "Allsvenskan 2026",  "Mistrzostwa Świata 2026", "Ekstraklasa 25/26"])


with Mundial:
    st.subheader("Tabela drużyn z ich statystykami średnio co mecz", text_alignment='center')
    st.dataframe(dfsrednie, hide_index=True)
    st.info("Statystyki obejmują wyłącznie regulaminowy czas gry, bez dogrywki", icon="❕", width=515 )

    st.subheader("Tabela statystyk sędziów", text_alignment='center')
    p1, p2 = st.columns([1,1])
    ls = np.sort(pd.unique(dfwc['Sędzia']))

    with p1:
        st.write("Tabela sędziów z ich faulami i kartkami średnio co mecz")
        st.dataframe(dfsedzia, hide_index=True, width='stretch')

    with p2:
        sw = st.selectbox("Mecze sędziego ", ls)
        st.dataframe(dfwc[(dfwc['Sędzia'] == sw)], hide_index=True, column_order=['Drużyna 1','Drużyna 2', 'Faule drużyny 1', 'Faule drużyny 2', 'Kartki drużyny 1', 'Kartki drużyny 2'])
        dfs = dfsedzia[dfsedzia["Nazwa"] == sw]
        st.write("Średnia odwgizdanych fauli: ", dfs["Faule"].mean())
        st.write("Średnia pokazanych kartek: ", dfs["Kartki"].mean())



    st.subheader("Porównywarka drużyn", text_alignment='center')
    Mapping = {
        "Gole": ["Gole drużyny 1", "Gole drużyny 2"],
        "Strzały": ["Strzały drużyny 1", "Strzały drużyny 2"],
        "Celne strzały": ["Celne strzały drużyny 1", "Celne strzały drużyny 2"],
        "Faule": ["Faule drużyny 1", "Faule drużyny 2"],
        "Rzuty rożne": ["Rożne drużyny 1", "Rożne drużyny 2"],
        "Kartki": ["Kartki drużyny 1", "Kartki drużyny 2"],
        "Auty": ["Auty drużyny 1", "Auty drużyny 2"],
        "Odbiory": ["Odbiory drużyny 1", "Odbiory drużyny 2"],
        "Spalone": ["Spalone drużyny 1", "Spalone drużyny 2"],
        "Podania": ["Podania drużyny 1", "Podania drużyny 2"]
    }

    lk = np.sort(pd.unique(dfciek['Drużyna']))
    p1, p2, p3 = st.columns([1, 1, 1])
    kategorie = dfwc.columns.tolist()
    with p2:
        wybrane = st.multiselect("Statystyki do porównywarki", placeholder="Wybierz statystyki",options=list(Mapping.keys()))
        kolumnywybrane = ["Drużyna 1", "Drużyna 2"]
        for kategorie in wybrane:
            kolumnywybrane.extend(Mapping[kategorie])

    kl = [
        'Drużyna 1', 'Gole drużyny 1', 'Strzały drużyny 1', 'Celne strzały drużyny 1', 'Faule drużyny 1', 'Rożne drużyny 1', 'Kartki drużyny 1', 'Auty drużyny 1', 'Odbiory drużyny 1', 'Spalone drużyny 1', 'Podania drużyny 1',
    ]

    kp = [
        'Drużyna 2', 'Gole drużyny 2', 'Strzały drużyny 2', 'Celne strzały drużyny 2', 'Faule drużyny 2', 'Rożne drużyny 2', 'Kartki drużyny 2', 'Auty drużyny 2', 'Odbiory drużyny 2', 'Spalone drużyny 2', 'Podania drużyny 2',
    ]

    dfm1 = dfwc.copy()
    dfm2 = dfwc.copy()
    pl, kol1, kol2, pp = st.columns([1,2,2,1])
    with kol1:
        d1 = st.selectbox("Wybierz drużynę 1 do wyświetlenia:", lk)

        m1 = (dfm1['Drużyna 2'] == d1)
        dfm1.loc[m1, kl + kp] = dfm1.loc[m1, kp + kl].values
        st.dataframe(dfm1[dfm1['Drużyna 1'] == d1], column_order=kolumnywybrane, hide_index=True)
        dfd1 = dfciek[dfciek['Drużyna'] == d1]

        st.write("Statystyki: ", d1)
        st.write("Gole strzelone", dfd1["Gole strzelone"].mean().round(2),"Gole stracone", dfd1["Gole stracone"].mean().round(2))
        st.write("Strzały wykonane", dfd1["Strzały wykonane"].mean().round(2), "Strzały przeciwko", dfd1["Strzały przeciwko"].mean().round(2))
        st.write("Celne strzały wykonane", dfd1["Celne wykonane"].mean().round(2), "Celne strzały przeciwko", dfd1["Celne przeciwko"].mean().round(2))
        st.write("Faule popełnione", dfd1["Faule popełnione"].mean().round(2), "Faule wywalczone", dfd1["Faule wywalczone"].mean().round(2))
        st.write("Rożne zdobyte", dfd1["Rożne zdobyte"].mean().round(2), "Rożne stracone", dfd1["Rożne stracone"].mean().round(2))
        st.write("Kartki otrzymane", dfd1["Kartki otrzymane"].mean().round(2), "Kartki przeciwko", dfd1["Kartki przeciwko"].mean().round(2))
        st.write("Auty zdobyte", dfd1["Auty zdobyte"].mean().round(2), "Auty przeciwko", dfd1["Auty przeciwko"].mean().round(2))
        st.write("Odbiory wykonane", dfd1["Odbiory wykonane"].mean().round(2), "Odbiory przeciwko", dfd1["Odbiory przeciwko"].mean().round(2))
        st.write("Podania wykonane", dfd1["Podania wykonane"].mean().round(2), "Podania przeciwnika", dfd1["Podania przeciwnika"].mean().round(2))
        st.write("Spalone zrobione", dfd1["Spalone zrobione"].mean().round(2), "Spalone przeciwnika", dfd1["Spalone przeciwnika"].mean().round(2))

    with kol2:
        d2 = st.selectbox("Wybierz drużynę 2 do wyświetlenia:", lk)
        m2 = (dfm2['Drużyna 2'] == d2)
        dfm2.loc[m2, kl + kp] = dfm2.loc[m2, kp + kl].values
        st.dataframe(dfm2[dfm2['Drużyna 1'] == d2], column_order=kolumnywybrane, hide_index=True)
        dfd2 = dfciek[dfciek['Drużyna'] == d2]

        st.write("Statystyki: ", d2)
        st.write("Gole strzelone", dfd2["Gole strzelone"].mean().round(2), "Gole stracone", dfd2["Gole stracone"].mean().round(2))
        st.write("Strzały wykonane", dfd2["Strzały wykonane"].mean().round(2), "Strzały przeciwko", dfd2["Strzały przeciwko"].mean().round(2))
        st.write("Celne strzały wykonane", dfd2["Celne wykonane"].mean().round(2), "Celne strzały przeciwko", dfd2["Celne przeciwko"].mean().round(2))
        st.write("Faule popełnione", dfd2["Faule popełnione"].mean().round(2), "Faule wywalczone", dfd2["Faule wywalczone"].mean().round(2))
        st.write("Rożne zdobyte", dfd2["Rożne zdobyte"].mean().round(2), "Rożne stracone", dfd2["Rożne stracone"].mean().round(2))
        st.write("Kartki otrzymane", dfd2["Kartki otrzymane"].mean().round(2), "Kartki przeciwko", dfd2["Kartki przeciwko"].mean().round(2))
        st.write("Auty zdobyte", dfd2["Auty zdobyte"].mean().round(2), "Auty przeciwko", dfd2["Auty przeciwko"].mean().round(2))
        st.write("Odbiory wykonane", dfd2["Odbiory wykonane"].mean().round(2), "Odbiory przeciwko", dfd2["Odbiory przeciwko"].mean().round(2))
        st.write("Podania wykonane", dfd2["Podania wykonane"].mean().round(2), "Podania przeciwnika", dfd2["Podania przeciwnika"].mean().round(2))
        st.write("Spalone zrobione", dfd2["Spalone zrobione"].mean().round(2), "Spalone przeciwnika", dfd2["Spalone przeciwnika"].mean().round(2))



with Ekstraklasa1:
    st.subheader("Statystyki drużyn ekstraklasy")
    dfekstrah = dfekstra[['Gospodarz', 'Faule gospodarz', 'Faule gosc', 'Meczowe']].copy()
    dfekstrah = dfekstrah.rename(columns={
        'Gospodarz': 'Drużyna',
        'Faule gospodarz': 'Faule zrobione',
        'Faule gosc': 'Faule wywalczone'
    })

    dfekstraa = dfekstra[['Gosc', 'Faule gosc', 'Faule gospodarz', 'Meczowe']].copy()
    dfekstraa = dfekstrah.rename(columns={
        'Gosc': 'Drużyna',
        'Faule gosc': 'Faule zrobione',
        'Faule gospodarz': 'Faule wywalczone'
    })
    dfekstraw = pd.concat([dfekstrah, dfekstraa], ignore_index=True)
    dfekstrap = dfekstraw.groupby('Drużyna').agg({
    'Faule zrobione': 'mean',
    'Faule wywalczone': 'mean',
    'Meczowe': 'mean'
    }).reset_index().round(1)

    dfekstras = dfekstra.groupby('Sędzia').agg(
    Meczów =('Sędzia', 'count'),
    średnia=('Meczowe', 'mean')
    ).reset_index().round(1)


    a1, a2 = st.columns(2)
    with a1:
        st.dataframe(dfekstrap, hide_index=True, width=500)
    with a2:
        st.dataframe(dfekstras, hide_index=True, width=500)


    st.subheader("Wszystkie mecze ekstraklasy wybranej drużyny")
    lista_kluby = dfekstra["Gospodarz"].unique()
    Klub = st.selectbox("Wybierz drużynę", lista_kluby, width = 300)
    dfekstra_gospo = dfekstra[dfekstra['Gospodarz'] == Klub]
    dfekstra_gosc = dfekstra[dfekstra['Gosc'] == Klub]
    f1 = dfekstra_gospo["Faule gospodarz"].mean()
    f2 = dfekstra_gosc["Faule gosc"].mean()
    f3 = dfekstra_gospo["Faule gosc"].mean()
    f4 = dfekstra_gosc["Faule gospodarz"].mean()

    g1, g2, g3 = st.columns(3)
    with g1:
        st.subheader("Popełnianie fauli")
        st.write(f"{Klub} jako gospodarz", f1.round(2))
        st.write(f"{Klub} jako gość", f2.round(2))
        st.write("Średnio popełniane", ((f1 + f2) / 2).round(2))

    with g2:
        st.subheader("Wywalczanie fauli")
        st.write(f"{Klub} jako gospodarz", f3.round(2))
        st.write(f"{Klub} jako gość", f4.round(2))
        st.write("Średnio wywalczane", ((f3+f4)/2).round(2))
    with g3:
        st.subheader("Meczowe faule")
        st.write("Faule meczowe jako gospodarz", (f1 + f3).round(2))
        st.write("Faule meczowe jako gość", (f2 + f4).round(2))
        st.write("Średnie meczowe", ((f1+f3+f2+f4)/2).round(2))




    st.subheader("Wykres fauli popełnionych jako gospodarz")
    warp = st.number_input("Wpisz linijkę fauli", value=0, width=300)
    dfp = dfekstra_gospo.copy()
    dfp['Spełniona linia?'] = np.where(
        dfp['Faule gospodarz'] >= warp,
        'Tak',
        'Nie'
    )

    wykresp = px.bar(
        dfp,
        x='Gosc',
        y='Faule gospodarz',
        text='Faule gospodarz',
        color='Spełniona linia?',
        color_discrete_map ={
            'Tak': '#2ca02c',
            'Nie': '#d62728'
        },
        hover_data = ['Sędzia']
    )


    wykresp.add_hline(y=warp, line_dash="dash", line_color='green', line_width=2, annotation_text="Linia wpisana", annotation_position="top right")
    wykresp.update_xaxes(categoryorder='array', categoryarray=dfp['Gosc'])
    st.plotly_chart(wykresp)
    dfpw = dfp['Spełniona linia?'].value_counts()
    st.write("Spełnienie warunku: ", dfpw.get("Tak"), '/',  17)

    st.subheader("Wykres fauli wywalczonych jako gospodarz")
    warw = st.number_input("Wpisz min liczbę fauli", value=0, width=300)
    dfw = dfekstra_gospo.copy()
    dfw['Spełniona linia?'] = np.where(
        dfp['Faule gosc'] >= warw,
        'Tak',
        'Nie'
    )

    wykresw = px.bar(
        dfw,
        x='Gosc',
        y='Faule gosc',
        text='Faule gosc',
        color='Spełniona linia?',
        color_discrete_map={
            'Tak': '#2ca02c',
            'Nie': '#d62728'
        },
        hover_data=['Sędzia']
    )

    wykresw.add_hline(y=warw, line_dash="dash", line_color='green', line_width=2, annotation_text="Linia wpisana",annotation_position="top right")
    wykresw.update_xaxes(categoryorder='array', categoryarray=dfw['Gosc'])
    st.plotly_chart(wykresw)
    dfww = dfw['Spełniona linia?'].value_counts()
    st.write("Spełnienie warunku: ", dfww.get("Tak"), '/', 17)

    st.subheader(f"{Klub} jako gospodarz")
    st.dataframe(dfekstra_gospo, hide_index=True)
    st.subheader(f"{Klub} jako gość")
    st.dataframe(dfekstra_gosc, hide_index=True)

Dane = sqlite3.connect("Dane.db")
Danemecze = """SELECT m.kolejka, 
r.Nazwa           AS Rozgrywki, 
gosp.Nazwa        AS Gospodarz, 
gosc.Nazwa        AS Gosc, 

stat_gosp.Strzaly AS "Strzaly Gospo", 
stat_gosp.Rozne   AS "Rożne Gospo", 
stat_gosp.Faule   AS "Faule Gospo", 

stat_gosc.Strzaly AS "Strzaly Gosc", 
stat_gosc.Rozne   AS "Rożne Gosc", 
stat_gosc.Faule   AS "Faule Gosc", 
s.nazwa           as Sedzia

FROM Mecze m
JOIN Rozgrywki r ON m.id_rozgrywek = r.id_rozgrywek
JOIN Druzyny gosp ON m.id_gospodarz = gosp.id_druzyna
JOIN Druzyny gosc ON m.id_gosc = gosc.id_druzyna
JOIN Statystyki stat_gosp ON m.id_mecz = stat_gosp.id_mecz AND stat_gosp.rola = 'Gospodarz'
JOIN Statystyki stat_gosc ON m.id_mecz = stat_gosc.id_mecz AND stat_gosc.rola = 'Gość'
JOIN Sedziowie s on m.id_sedzia = s.id_sedzia
ORDER BY m.kolejka DESC; 
            """
dane = pd.read_sql_query(Danemecze, Dane)

def pokaz_srednie_sedziego(df_ligi):
    df_ligi["Faule Meczowe"] = df_ligi['Faule Gospo'] + df_ligi['Faule Gosc']
    df_sedziowie = df_ligi.groupby('Sedzia').agg(
        Meczów=('Sedzia', 'count'),
        Średnia_fauli=('Faule Meczowe', 'mean')
    ).reset_index().round(1)

    st.dataframe(df_sedziowie, hide_index=True, width= 530)

def pokaz_srednie_fauli(df_ligi):
    df_ligi_faule_gospo = df_ligi.groupby('Gospodarz').agg(
        Średnia_popełnione=('Faule Gospo', 'mean'),
        Średnia_wywalczone=('Faule Gosc', 'mean')
    ).reset_index().round(1)

    df_ligi_faule_gosc = df_ligi.groupby('Gosc').agg(
        Średnia_popełnione=('Faule Gosc', 'mean'),
        Średnia_wywalczone=('Faule Gospo', 'mean')
    ).reset_index().round(1)

    a1, a2 = st.columns(2)
    with a1:
        st.dataframe(df_ligi_faule_gospo, hide_index=True, width=500, height=600)
    with a2:
        st.dataframe(df_ligi_faule_gosc, hide_index=True, width=500, height=600)

def pokaz_srednie_strzalow(df_ligi):
    df_ligi_strzały_gospo = df_ligi.groupby('Gospodarz').agg(
        Średnia_strzały_wykonane=('Strzaly Gospo', 'mean'),
        Średnia_strzały_przeciwnika=('Strzaly Gosc', 'mean')
    ).reset_index().round(1)

    df_ligi_strzały_gosc = df_ligi.groupby('Gosc').agg(
        Średnia_strzały_wykonane=('Strzaly Gosc', 'mean'),
        Średnia_strzały_przeciwnika=('Strzaly Gospo', 'mean')
    ).reset_index().round(1)

    b1, b2 = st.columns(2)
    with b1:
        st.dataframe(df_ligi_strzały_gospo, hide_index=True, width=500, height=600)
    with b2:
        st.dataframe(df_ligi_strzały_gosc, hide_index=True, width=500, height=600)

def pokaz_srednie_roznych(df_ligi):
    df_ligi_rożne_gospo = df_ligi.groupby('Gospodarz').agg(
        Średnia_rożne_wykonane=('Rożne Gospo', 'mean'),
        Średnia_rożne_przeciwnika=('Rożne Gosc', 'mean')
    ).reset_index().round(1)

    df_ligi_rożne_gosc = df_ligi.groupby('Gosc').agg(
        Średnia_rożne_wykonane=('Rożne Gosc', 'mean'),
        Średnia_rożne_przeciwnika=('Rożne Gospo', 'mean')
    ).reset_index().round(1)

    sr1, sr2 = st.columns(2)
    with sr1:
        st.dataframe(df_ligi_rożne_gospo, hide_index=True, width=500, height=600)
    with sr2:
        st.dataframe(df_ligi_rożne_gosc, hide_index=True, width=500, height=600)

with Szwedzka:
    liga_szwedzka = dane[dane["Rozgrywki"] == 'Allsvenskan']
    st.subheader("Wszystkie mecze ligi szwedzkiej")
    st.dataframe(liga_szwedzka, hide_index=True)

    st.subheader("Sędziowie ligi")
    pokaz_srednie_sedziego(liga_szwedzka)
    st.subheader("Średnie fauli")
    pokaz_srednie_fauli(liga_szwedzka)
    st.subheader("Średnie strzałów")
    pokaz_srednie_strzalow(liga_szwedzka)
    st.subheader("Średnie rożnych")
    pokaz_srednie_roznych(liga_szwedzka)

with Norweska:
    liga_norweska = dane[dane["Rozgrywki"] == 'Eliteserien']
    st.subheader("Wszystkie mecze ligi norweskiej")
    st.dataframe(liga_norweska, hide_index=True)

    st.subheader("Sędziowie ligi")
    pokaz_srednie_sedziego(liga_norweska)
    st.subheader("Średnie fauli")
    pokaz_srednie_fauli(liga_norweska)
    st.subheader("Średnie strzałów")
    pokaz_srednie_strzalow(liga_norweska)
    st.subheader("Średnie rożnych")
    pokaz_srednie_roznych(liga_norweska)

with Ekstraklasa2:
    Ekstraklasa = dane[dane["Rozgrywki"] == 'Ekstraklasa']
    st.subheader("Wszystkie mecze ligi polskiej")
    st.dataframe(Ekstraklasa, hide_index=True)

    st.subheader("Sędziowie ligi")
    pokaz_srednie_sedziego(Ekstraklasa)
    st.subheader("Średnie fauli")
    pokaz_srednie_fauli(Ekstraklasa)
    st.subheader("Średnie strzałów")
    pokaz_srednie_strzalow(Ekstraklasa)
    st.subheader("Średnie rożnych")
    pokaz_srednie_roznych(Ekstraklasa)

with ILiga:
    pierwsza_liga = dane[dane["Rozgrywki"] == '1 Liga']
    st.subheader("Wszystkie mecze 1 ligi polskiej")
    st.dataframe(pierwsza_liga, hide_index=True)

    st.subheader("Sędziowie ligi")
    pokaz_srednie_sedziego(pierwsza_liga)
    st.subheader("Średnie fauli")
    pokaz_srednie_fauli(pierwsza_liga)
    st.subheader("Średnie strzałów")
    pokaz_srednie_strzalow(pierwsza_liga)
    st.subheader("Średnie rożnych")
    pokaz_srednie_roznych(pierwsza_liga)

with Czeska:
    liga_czeska = dane[dane["Rozgrywki"] == 'Chance Liga']
    st.subheader("Wszystkie mecze ligi czeskiej")
    st.dataframe(liga_czeska, hide_index=True)

    st.subheader("Sędziowie ligi")
    pokaz_srednie_sedziego(liga_czeska)
    st.subheader("Średnie fauli")
    pokaz_srednie_fauli(liga_czeska)
    st.subheader("Średnie strzałów")
    pokaz_srednie_strzalow(liga_czeska)
    st.subheader("Średnie rożnych")
    pokaz_srednie_roznych(liga_czeska)
