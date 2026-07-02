import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

st.title("Statystyki piłkarskie")
st.set_page_config(layout="wide")

conn = sqlite3.connect("staty.db")
mecze = """
    SELECT 
    Mecze.kolejka,
    gospodarze.Nazwa AS Gospodarz,
    goscie.Nazwa AS Gosc,
    Mecze.stat_gospo AS 'Faule Gospo',
    Mecze.stat_gosc AS 'Faule Gosc',
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
        SELECT Sędziowie.Nazwa, avg(faule_kraj1 + faule_kraj2) as Faule, avg(kartki_kraj1 + kartki_kraj2) as Kartki
        from Mecze, Sędziowie
        where Mecze.id_sędzia = Sędziowie.id_sędzia
        group by Nazwa
        order by faule desc
        """
dfsedzia = pd.read_sql_query(sędziowa, polacz)


df1 = dfwc[['Drużyna 1', 'Gole drużyny 1', 'Gole drużyny 2', 'Strzały drużyny 1', 'Strzały drużyny 2', 'Faule drużyny 1', 'Faule drużyny 2', 'Rożne drużyny 1', 'Rożne drużyny 2', 'Kartki drużyny 1', 'Kartki drużyny 2', 'Auty drużyny 1', 'Auty drużyny 2', 'Odbiory drużyny 1', 'Odbiory drużyny 2', 'Podania drużyny 1', 'Podania drużyny 2', 'Spalone drużyny 1', 'Spalone drużyny 2']].copy()
df2 = dfwc[['Drużyna 2', 'Gole drużyny 2', 'Gole drużyny 1', 'Strzały drużyny 2', 'Strzały drużyny 1', 'Faule drużyny 2', 'Faule drużyny 1', 'Rożne drużyny 2', 'Rożne drużyny 1', 'Kartki drużyny 2', 'Kartki drużyny 1', 'Auty drużyny 2', 'Auty drużyny 1', 'Odbiory drużyny 2', 'Odbiory drużyny 1', 'Podania drużyny 2', 'Podania drużyny 1', 'Spalone drużyny 2', 'Spalone drużyny 1']].copy()
df1.columns = ['Drużyna', 'Gole strzelone', 'Gole stracone', 'Strzały wykonane', 'Strzały przeciwko', 'Faule popełnione', 'Faule wywalczone', 'Rożne zdobyte', 'Rożne stracone', 'Kartki otrzymane', 'Kartki przeciwko', 'Auty zdobyte', 'Auty przeciwko', 'Odbiory wykonane', 'Odbiory przeciwko', 'Podania wykonane', 'Podania przeciwnika', 'Spalone zrobione', 'Spalone przeciwnika']
df2.columns = ['Drużyna', 'Gole strzelone', 'Gole stracone', 'Strzały wykonane', 'Strzały przeciwko', 'Faule popełnione', 'Faule wywalczone', 'Rożne zdobyte', 'Rożne stracone', 'Kartki otrzymane', 'Kartki przeciwko', 'Auty zdobyte', 'Auty przeciwko', 'Odbiory wykonane', 'Odbiory przeciwko', 'Podania wykonane', 'Podania przeciwnika', 'Spalone zrobione', 'Spalone przeciwnika']
dfciek = pd.concat([df1, df2], ignore_index=True)
dfsrednie = dfciek.groupby('Drużyna').mean().round(2).reset_index()

Mundial, Ekstraklasa = st.tabs(["Mistrzostwa Świata 2026", "Ekstraklasa 25/26"])

with Ekstraklasa:
    st.subheader("Wszystkie mecze")
    lista_kluby = dfekstra["Gospodarz"].unique()
    Klub = st.selectbox("Wybierz drużynę gopsodarzy",  lista_kluby)
    dfmecz_wk = dfekstra[dfekstra['Gospodarz'] == Klub]
    st.dataframe(dfmecz_wk, hide_index=True)

with Mundial:
    st.subheader("Tabela drużyn z ich statystykami średnio co mecz", text_alignment='center')
    st.dataframe(dfsrednie, hide_index=True)
    st.info("Statystyki obejmują wyłącznie regulaminowy czas gry, bez dogrywki", icon="❕", width=515 )

    st.subheader("Tabela statystyk sędziów", text_alignment='center')
    p1, p2 = st.columns([1,1])
    ls = pd.unique(dfwc['Sędzia'])
    lss = np.sort(ls)

    with p1:
        st.write("Tabela sędziów z ich faulami i kartkami średnio co mecz")
        st.dataframe(dfsedzia, hide_index=True, use_container_width=True)

    with p2:
        sw = st.selectbox("Mecze sędziego ", lss)
        st.dataframe(dfwc[(dfwc['Sędzia'] == sw)], hide_index=True, column_order=['Drużyna 1','Drużyna 2', 'Faule drużyny 1', 'Faule drużyny 2', 'Kartki drużyny 1', 'Kartki drużyny 2'])
        dfs = dfsedzia[dfsedzia["Nazwa"] == sw]
        st.write("Średnia odwgizdanych fauli: ", dfs["Faule"].mean())
        st.write("Średnia pokazanych kartek: ", dfs["Kartki"].mean())



    st.subheader("Porównywarka drużyn", text_alignment='center')
    Mapping = {
        "Gole": ["Gole drużyny 1", "Gole drużyny 2"],
        "Strzały": ["Strzały drużyny 1", "Strzały drużyny 2"],
        "Faule": ["Faule drużyny 1", "Faule drużyny 2"],
        "Rzuty rożne": ["Rożne drużyny 1", "Rożne drużyny 2"],
        "Kartki": ["Kartki drużyny 1", "Kartki drużyny 2"],
        "Auty": ["Auty drużyny 1", "Auty drużyny 2"],
        "Odbiory": ["Odbiory drużyny 1", "Odbiory drużyny 2"],
        "Spalone": ["Spalone drużyny 1", "Spalone drużyny 2"],
        "Podania": ["Podania drużyny 1", "Podania drużyny 2"]
    }

    lk = np.sort(pd.unique(dfciek['Drużyna']))
    p1,p2,p3 = st.columns([1,1,1])
    kategorie = dfwc.columns.tolist()
    with p2:
        kategoriewybrane = st.multiselect("Statystyki do porównywarki", placeholder="Wybierz statystyki", options=list(Mapping.keys()))
        kolumnywybrane = ["Drużyna 1", "Drużyna 2"]
        for kategorie in kategoriewybrane:
            kolumnywybrane.extend(Mapping[kategorie])

            
    pl, kol1, kol2, pp = st.columns([1,2,2,1])
    with kol1:
        d1 = st.selectbox("Wybierz drużynę 1 do wyświetlenia:", lk)
        st.dataframe(dfwc[(dfwc['Drużyna 1'] == d1) | (dfwc['Drużyna 2'] == d1)], column_order=kolumnywybrane, hide_index=True)
        dfd1 = dfciek[dfciek['Drużyna'] == d1]

        st.write("Statystyki ", d1)
        st.write("Gole strzelone", dfd1["Gole strzelone"].mean().round(2),"Gole stracone", dfd1["Gole stracone"].mean().round(2))
        st.write("Strzały wykonane", dfd1["Strzały wykonane"].mean().round(2), "Strzały przeciwko", dfd1["Strzały przeciwko"].mean().round(2))
        st.write("Faule popełnione", dfd1["Faule popełnione"].mean().round(2), "Faule wywalczone", dfd1["Faule wywalczone"].mean().round(2))
        st.write("Rożne zdobyte", dfd1["Rożne zdobyte"].mean().round(2), "Rożne stracone", dfd1["Rożne stracone"].mean().round(2))
        st.write("Kartki otrzymane", dfd1["Kartki otrzymane"].mean().round(2), "Kartki przeciwko", dfd1["Kartki przeciwko"].mean().round(2))
        st.write("Auty zdobyte", dfd1["Auty zdobyte"].mean().round(2), "Auty przeciwko", dfd1["Auty przeciwko"].mean().round(2))
        st.write("Odbiory wykonane", dfd1["Odbiory wykonane"].mean().round(2), "Odbiory przeciwko", dfd1["Odbiory przeciwko"].mean().round(2))
        st.write("Podania wykonane", dfd1["Podania wykonane"].mean().round(2), "Podania przeciwnika", dfd1["Podania przeciwnika"].mean().round(2))
        st.write("Spalone zrobione", dfd1["Spalone zrobione"].mean().round(2), "Spalone przeciwnika", dfd1["Spalone przeciwnika"].mean().round(2))




    with kol2:
        d2 = st.selectbox("Wybierz drużynę 2 do wyświetlenia:", lk)
        st.dataframe(dfwc[(dfwc['Drużyna 1'] == d2) | (dfwc['Drużyna 2'] == d2)], column_order=kolumnywybrane, hide_index=True)
        dfd2 = dfciek[dfciek['Drużyna'] == d2]
        st.write("Statystyki ", d2)
        st.write("Gole strzelone", dfd2["Gole strzelone"].mean().round(2), "Gole stracone", dfd2["Gole stracone"].mean().round(2))
        st.write("Strzały wykonane", dfd2["Strzały wykonane"].mean().round(2), "Strzały przeciwko", dfd2["Strzały przeciwko"].mean().round(2))
        st.write("Faule popełnione", dfd2["Faule popełnione"].mean().round(2), "Faule wywalczone", dfd2["Faule wywalczone"].mean().round(2))
        st.write("Rożne zdobyte", dfd2["Rożne zdobyte"].mean().round(2), "Rożne stracone", dfd2["Rożne stracone"].mean().round(2))
        st.write("Kartki otrzymane", dfd2["Kartki otrzymane"].mean().round(2), "Kartki przeciwko", dfd2["Kartki przeciwko"].mean().round(2))
        st.write("Auty zdobyte", dfd2["Auty zdobyte"].mean().round(2), "Auty przeciwko", dfd2["Auty przeciwko"].mean().round(2))
        st.write("Odbiory wykonane", dfd2["Odbiory wykonane"].mean().round(2), "Odbiory przeciwko", dfd2["Odbiory przeciwko"].mean().round(2))
        st.write("Podania wykonane", dfd2["Podania wykonane"].mean().round(2), "Podania przeciwnika", dfd2["Podania przeciwnika"].mean().round(2))
        st.write("Spalone zrobione", dfd2["Spalone zrobione"].mean().round(2), "Spalone przeciwnika", dfd2["Spalone przeciwnika"].mean().round(2))