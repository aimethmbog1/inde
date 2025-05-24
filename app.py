# 📚 IMPORTER LES BIBLIOTHÈQUES
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ⚙️ CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Population India", layout="wide")

# 📥 CHARGEMENT DES DONNÉES
df = pd.read_csv("india.csv")

# 📅 PRÉSENCE D'UNE COLONNE 'Year' ?
has_year = 'Year' in df.columns
years_available = sorted(df['Year'].unique()) if has_year else []

# 📍 PRÉPARATION DE LA LISTE D'ÉTATS
list_of_states = sorted(df['State'].unique())
list_of_states.insert(0, 'Overall India')

# 🧭 SIDEBAR - CONTRÔLES UTILISATEUR
st.sidebar.title("📊 Visualisation de la Population")
selected_state = st.sidebar.selectbox("🗺️ Sélectionnez un État", list_of_states)

# 🧩 PARAMÈTRES VISUELS
primary = st.sidebar.selectbox("📏 Paramètre principal (taille)", sorted(df.columns[5:]))
secondary = st.sidebar.selectbox("🎨 Paramètre secondaire (couleur)", sorted(df.columns[5:]))

# 📆 FILTRE PAR ANNÉE SI DISPONIBLE
if has_year:
    year_selected = st.sidebar.select_slider("📆 Filtrer par année", options=years_available, value=years_available[-1])
else:
    year_selected = None

# 📍 AFFICHAGE DE LA CARTE
if st.sidebar.button("Afficher le graphique"):
    st.markdown("**🔹 Taille :** basée sur le paramètre principal sélectionné")
    st.markdown("**🔸 Couleur :** basée sur le paramètre secondaire sélectionné")

    # 🎯 FILTRAGE
    df_filtered = df.copy()
    if selected_state != 'Overall India':
        df_filtered = df_filtered[df_filtered['State'] == selected_state]
    if has_year and year_selected:
        df_filtered = df_filtered[df_filtered['Year'] == year_selected]

    # 🗺️ AFFICHAGE CARTE MAPBOX
    fig = px.scatter_mapbox(
        df_filtered,
        lat="Latitude",
        lon="Longitude",
        size=primary,
        color=secondary,
        hover_name="District",
        hover_data=["State", "Population"] + (["Year"] if has_year else []),
        color_continuous_scale=px.colors.sequential.Plasma,
        size_max=50,
        zoom=4 if selected_state == 'Overall India' else 5,
        mapbox_style="carto-positron",
        width=1200,
        height=800
    )
    st.plotly_chart(fig, use_container_width=True)

    # ⬇️ TÉLÉCHARGEMENT CSV
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Télécharger les données affichées",
        data=csv,
        file_name=f"population_{selected_state.replace(' ', '_').lower()}_{year_selected if year_selected else 'all'}.csv",
        mime="text/csv"
    )

    # 🎞️ ANIMATION TEMPORELLE
    if has_year:
        st.markdown("### 🎞️ Animation temporelle")
        df_anim = df if selected_state == 'Overall India' else df[df['State'] == selected_state]
        fig_anim = px.scatter_mapbox(
            df_anim,
            lat="Latitude",
            lon="Longitude",
            size=primary,
            color=secondary,
            animation_frame="Year",
            hover_name="District",
            hover_data=["State", "Population", "Year"],
            color_continuous_scale=px.colors.sequential.Plasma,
            size_max=45,
            zoom=4 if selected_state == 'Overall India' else 5,
            mapbox_style="carto-positron",
            width=1200,
            height=700
        )
        st.plotly_chart(fig_anim, use_container_width=True)

# 📋 TABLEAU INTERACTIF
st.markdown("## 📋 Données tabulaires interactives")
with st.expander("Afficher / Masquer le tableau"):
    df_table = df.copy()
    if selected_state != 'Overall India':
        df_table = df_table[df_table['State'] == selected_state]
    if has_year and year_selected:
        df_table = df_table[df_table['Year'] == year_selected]
    st.dataframe(df_table, use_container_width=True)

# 📌 NOTE
st.markdown("### 📌 Note")
st.write("Ce tableau est basé sur les données de la [Census 2011](http://census2011.censusindia.gov.in/).")
