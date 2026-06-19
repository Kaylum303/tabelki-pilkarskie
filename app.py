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
    Sędziowie.Nazwa AS Sędzia
    FROM Mecze 	
    LEFT Join Kraje as kraj1 on Mecze.id_kraj1 = kraj1.id_kraj
    LEFT Join Kraje as kraj2 on Mecze.id_kraj2 = kraj2.id_kraj
    LEFT Join Sędziowie on Mecze.id_sędzia = Sędziowie.id_sędzia;
    """
dfwc = pd.read_sql_query(ogólna, polacz)
sędziowa = """
        SELECT Sędziowie.Nazwa, sum(faule_kraj1 + faule_kraj2) as faule
        from Mecze, Sędziowie
        where Mecze.id_sędzia = Sędziowie.id_sędzia
        group by Nazwa
        order by faule desc
        """
dfsedzia = pd.read_sql_query(sędziowa, polacz)


df1 = dfwc[['Drużyna 1', 'Gole drużyny 1', 'Gole drużyny 2', 'Strzały drużyny 1', 'Strzały drużyny 2', 'Faule drużyny 1', 'Faule drużyny 2', 'Rożne drużyny 1', 'Rożne drużyny 2', 'Kartki drużyny 1', 'Kartki drużyny 2']].copy()
df2 = dfwc[['Drużyna 2', 'Gole drużyny 2', 'Gole drużyny 1', 'Strzały drużyny 2', 'Strzały drużyny 1', 'Faule drużyny 2', 'Faule drużyny 1', 'Rożne drużyny 2', 'Rożne drużyny 1', 'Kartki drużyny 2', 'Kartki drużyny 1']].copy()
df1.columns = ['Drużyna', 'Gole strzelone', 'Gole stracone', 'Strzały wykonane', 'Strzały przeciwko', 'Faule popełnione', 'Faule wywalczone', 'Rożne zdobyte', 'Rożne stracone', 'Kartki otrzymane', 'Kartki przeciwko']
df2.columns = ['Drużyna', 'Gole strzelone', 'Gole stracone', 'Strzały wykonane', 'Strzały przeciwko', 'Faule popełnione', 'Faule wywalczone', 'Rożne zdobyte', 'Rożne stracone', 'Kartki otrzymane', 'Kartki przeciwko']
dfciek = pd.concat([df1, df2], ignore_index=True)
dfsrednie = dfciek.groupby('Drużyna').mean().reset_index()

Mundial, Ekstraklasa = st.tabs(["Mistrzostwa Świata 2026", "Ekstraklasa 25/26"])

with Ekstraklasa:
    st.subheader("Wszystkie mecze")
    lista_kluby = dfekstra["Gospodarz"].unique()
    Klub = st.selectbox("Wybierz drużynę gopsodarzy",  lista_kluby)
    dfmecz_wk = dfekstra[dfekstra['Gospodarz'] == Klub]
    st.dataframe(dfmecz_wk, hide_index=True)

with Mundial:
    st.subheader("Tabela ogólna statystyk drużyn", text_alignment='center')
    st.dataframe(dfsrednie, hide_index=True)

    p1, p2, p3 = st.columns([1,1,1])


    with p2:
        st.subheader("Tabela ogólna sędziów", text_alignment='center')
        st.dataframe(dfsedzia, hide_index=True, use_container_width=True)

    st.subheader("Porównywarka drużyn", text_alignment='center')
    lk = pd.unique(dfciek['Drużyna'])
    lks = np.sort(lk)



    pl, kol1 , kol2, pp = st.columns([1,2,2,1])
    with kol1:
        d1 = st.selectbox("Wybierz drużynę 1 do wyświetlenia:", lks)
        st.dataframe(dfwc[(dfwc['Drużyna 1'] == d1) | (dfwc['Drużyna 2'] == d1)], hide_index=True)
        dfd1 = dfciek[dfciek['Drużyna'] == d1]
        st.write("Statystyki ", d1)
        st.write("Gole strzelone", dfd1["Gole strzelone"].mean())
        st.write("Gole stracone", dfd1["Gole stracone"].mean())
        st.write("Strzały wykonane", dfd1["Strzały wykonane"].mean())
        st.write("Strzały przeciwko", dfd1["Strzały przeciwko"].mean())
        st.write("Faule popełnione", dfd1["Faule popełnione"].mean())
        st.write("Faule wywalczone", dfd1["Faule wywalczone"].mean())
        st.write("Kartki otrzymane", dfd1["Kartki otrzymane"].mean())
        st.write("Kartki przeciwko", dfd1["Kartki przeciwko"].mean())





    with kol2:
        d2 = st.selectbox("Wybierz drużynę 2 do wyświetlenia:", lks)
        st.dataframe(dfwc[(dfwc['Drużyna 1'] == d2) | (dfwc['Drużyna 2'] == d2)], hide_index=True)
        dfd2 = dfciek[dfciek['Drużyna'] == d2]
        st.write("Statystyki ", d2)
        st.write("Gole strzelone", dfd2["Gole strzelone"].mean())
        st.write("Gole stracone", dfd2["Gole stracone"].mean())
        st.write("Strzały wykonane", dfd2["Strzały wykonane"].mean())
        st.write("Strzały przeciwko", dfd2["Strzały przeciwko"].mean())
        st.write("Faule popełnione", dfd2["Faule popełnione"].mean())
        st.write("Faule wywalczone", dfd2["Faule wywalczone"].mean())
        st.write("Kartki otrzymane", dfd2["Kartki otrzymane"].mean())
        st.write("Kartki przeciwko", dfd2["Kartki przeciwko"].mean())



#st.subheader("Stastyki z całego sezonu")
#st.write("Średnie faule popełnione", round(df["FC"].mean(),2))
#st.write("Średnie faule wywalczone", round(df["FW"].mean(),2))
#st.write("Średnie faule meczowe", round(df["FM"].mean(),2))

#st.subheader("Ostatnie mecze")
#datar=df.iloc[::-1]
#liczba = st.slider("Liczba ostatnich meczy", min_value=1, max_value=17)
#ost=datar.head(liczba)
#st.dataframe(ost, hide_index=True)
#st.write("Średnie faule popełnione dla wybranych ostatnich meczy:", round(ost["FC"].mean(),2))
#st.write("Średnie faule popełnione dla wybranych ostatnich meczy:", round(ost["FW"].mean(),2))
#st.write("Średnie faule popełnione dla wybranych ostatnich meczy:", round(ost["FM"].mean(),2))

#st.subheader("Podana minimalna liczba fauli")
#war = st.text_input("Wpisz min liczbę fauli", value=0)
#minw = df[df["FC"] > int(war)]
#st.dataframe(minw, hide_index=True)
#st.write("Liczba meczy z wybranym warunkiem:", len(minw.index) ,'/', len(df.index))



#with st.sidebar:
#    st.header("Faule")
#    st.header("Strzały")
#    st.header("Rzuty rożne")