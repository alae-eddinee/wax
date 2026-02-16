import streamlit as st
import pandas as pd
import io

# --- 1. SETUP & THEME CONFIGURATION ---
st.set_page_config(page_title="Calculateur de Coût de Bougies", page_icon="", layout="wide")

# --- 2. DATA LOADING ---
csv_data = """Item No,Product Name,Description,Quantity,Unit,Unit Price,Amount
1,Soy Wax in Flakes,"Ingredients: 100% hydrogenated vegetable oil, MP 48-52°C",500,KG,2.6,1300.0
2,58/60 Fully Refined Paraffin Wax,"White Granules, MP 58-60°C, Oil Content ≤0.5%",1500,KG,1.72,2580.0
3,Wax Melter 1,"Color: Black, Vol: 8L, 1100W, EURO Standard",4,PIECE,55.32,221.28
4,Wax Melter 2,"Color: Black, Vol: 6L, 1100W, EURO Standard",2,PIECE,48.23,96.46
5,Electronic thermometer,"Range: -50°C to 300°C, Probe Length: 15cm",3,PIECE,1.15,3.45
6,White Cotton Wicks,"Size: 18ply * 6cmL",5000,PIECE,0.0058,29.0
7,White Cotton Wicks,"Size: 18ply * 12cmL",10000,PIECE,0.0104,104.0
8,White Cotton Wicks,"Size: 24ply * 17cmL",10000,PIECE,0.0124,124.0
9,White Cotton Wicks,"Size: 24ply * 20cmL",5000,PIECE,0.0165,82.5
10,Metal Candle Wick Holder,"Material: Stainless steel, Size: 10cmL * 2.5cmW",1000,PIECE,0.112,112.0
11,Candle Wick Sticker Sheet,"Double-sided, Dia 20mm, Color: White, 20 dots per sheet",1500,SHEET,0.071,106.5
12,Wax Melting Cup,"Material: 304 Stainless steel, 550ml",5,PIECE,3.5,17.5
13,Heat Gun,"Color: Black/White, 230V, 300W",5,PIECE,6.0,30.0
14,Candle Dye Color Liquid,"32 different colors, 10ml/bottle",160,BOTTLE,0.84,134.4
15,Fragrance Oil,"Scents: Ocean Gardenia",10,KG,27.89,278.9
16,Fragrance Oil,"Scents: French Vanilla",10,KG,19.2,192.0
17,Fragrance Oil,"Scents: Lavender",10,KG,20.11,201.1
18,Fragrance Oil,"Scents: Rosemary",10,KG,28.11,281.1
19,Fragrance Oil,"Scents: Amber Sandalwood",10,KG,25.6,256.0
20,Fragrance Oil,"Scents: Citronella Oil",10,KG,22.86,228.6
21,Fragrance Oil,"Scents: Jasmine Tea",10,KG,25.6,256.0
22,Fragrance Oil,"Scents: Oud",5,KG,39.72,198.6"""

@st.cache_data
def load_data():
    df = pd.read_csv(io.StringIO(csv_data))
    return df

df = load_data()

# Data Filters
fragrances_df = df[df['Product Name'].str.contains("Fragrance")].copy()
fragrances_df['Scent Name'] = fragrances_df['Description'].str.replace("Scents: ", "")
# Display label with price
fragrances_df['Display Label'] = fragrances_df['Scent Name'] + " ($" + fragrances_df['Unit Price'].astype(str) + "/kg)"

waxes_df = df[df['Product Name'].str.contains("Wax") & ~df['Product Name'].str.contains("Melter|Cup")]
waxes_df['Display Label'] = waxes_df['Product Name'] + " ($" + waxes_df['Unit Price'].astype(str) + "/kg)"
wicks_df = df[df['Product Name'].str.contains("Wick") & ~df['Product Name'].str.contains("Holder|Sticker")]
wicks_df['Display Label'] = wicks_df['Description'] + " ($" + wicks_df['Unit Price'].astype(str) + "/pc)"
sticker_row = df[df['Item No'] == 11].iloc[0]
STICKERS_PER_SHEET = 20

# --- 3. UI LAYOUT ---
st.title("🕯️ Calculateur de Coût de Bougies")

# --- SELECTION AREA ---
col_sel1, col_sel2, col_sel3 = st.columns(3)

with col_sel1:
    st.subheader("1. Choisir la Cire")
    wax_choice_label = st.selectbox("Type de Cire", waxes_df['Display Label'].unique(), index=0)
    wax_row = waxes_df[waxes_df['Display Label'] == wax_choice_label].iloc[0]

with col_sel2:
    st.subheader("2. Choisir le Parfum")
    # Ce sélecteur vous permet de voir le prix et le nom
    scent_choice_label = st.selectbox("Huile Parfumée", fragrances_df['Display Label'].unique(), index=0)
    scent_row = fragrances_df[fragrances_df['Display Label'] == scent_choice_label].iloc[0]

with col_sel3:
    st.subheader("3. Choisir la Mèche")
    wick_choice_label = st.selectbox("Taille de Mèche", wicks_df['Display Label'].unique())
    wick_row = wicks_df[wicks_df['Display Label'] == wick_choice_label].iloc[0]

st.divider()

# --- FRAGRANCE LOAD SECTION ---
st.subheader("⚙️ Paramètres : Charge en Parfum")
st.caption("Quelle quantité d'huile ajouter à la cire ?")

col_load_slider, col_load_info = st.columns([1, 1])

with col_load_slider:
    fragrance_load = st.slider(
        "Pourcentage de Parfum (%)", 
        min_value=1, 
        max_value=12, 
        value=6
    )

with col_load_info:
    # Logique pour expliquer le pourcentage à l'utilisateur
    if fragrance_load < 6:
        st.warning(f"⚠️ **{fragrance_load}% est Faible.** Le parfum pourrait être trop discret.")
    elif 6 <= fragrance_load <= 8:
        st.success(f"✅ **{fragrance_load}% est Parfait.** (Recommandé 6-8%). Bon parfum, brûle bien.")
    elif 9 <= fragrance_load <= 10:
        st.success(f"🔥 **{fragrance_load}% est Fort.** (Maximum recommandé). Parfum très intense.")
    else:
        st.error(f"🛑 **{fragrance_load}% est Risqué.** Plus de 10% peut faire couler l'huile hors de la bougie.")

# Jar Settings
col_jar1, col_jar2 = st.columns(2)
with col_jar1:
    jar_size = st.number_input("Taille du Pot de Bougie (grammes de cire)", value=200, step=10)
with col_jar2:
    wax_amount_kg = st.number_input("Quantité de Cire (kg)", value=1.0, min_value=0.1, max_value=10.0, step=0.1)

# --- CALCULATIONS ---
WAX_AMOUNT_KG = wax_amount_kg
cost_wax = WAX_AMOUNT_KG * wax_row['Unit Price']
fragrance_weight_kg = (fragrance_load / 100.0) * WAX_AMOUNT_KG
cost_fragrance = fragrance_weight_kg * scent_row['Unit Price']

total_mixture_g = (WAX_AMOUNT_KG + fragrance_weight_kg) * 1000
num_candles = int(total_mixture_g / jar_size)

cost_wicks = num_candles * wick_row['Unit Price']
cost_stickers = (num_candles / STICKERS_PER_SHEET) * sticker_row['Unit Price']

total_batch_cost = cost_wax + cost_fragrance + cost_wicks + cost_stickers
cost_per_candle = total_batch_cost / num_candles if num_candles > 0 else 0.0

# --- RESULTS ---
st.divider()
st.markdown(f"### 📊 Résultats : {scent_row['Scent Name']}")

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Coût Total du Lot", f"${total_batch_cost:.2f}")
m2.metric("Coût par Bougie FOB", f"${cost_per_candle:.2f}")
m3.metric("Coût par Bougie PRV DH HT", f"{cost_per_candle*17:.2f} DH")
m4.metric("Bougies Produites", f"{num_candles}")
m5.metric("Parfum Utilisé", f"{fragrance_weight_kg*1000:.0f} g")

# Breakdown Table
breakdown_df = pd.DataFrame({
    "Article": [wax_row['Product Name'], f"Huile : {scent_row['Scent Name']}", "Mèches", "Feuilles d'Autocollants"],
    "Prix Unitaire": [f"${wax_row['Unit Price']}/kg", f"${scent_row['Unit Price']}/kg", f"${wick_row['Unit Price']:.4f}/pc", f"${sticker_row['Unit Price']:.3f}/feuille"],
    "Quantité": [f"{WAX_AMOUNT_KG:.1f} kg", f"{fragrance_weight_kg*1000:.1f} g", f"{num_candles} pcs", f"{(num_candles/STICKERS_PER_SHEET):.1f} feuilles"],
    "Coût": [f"${cost_wax:.2f}", f"${cost_fragrance:.2f}", f"${cost_wicks:.2f}", f"${cost_stickers:.2f}"]
})
st.table(breakdown_df)

# --- THE STEPS (RECIPE) ---
st.markdown("## 📝 Guide de Fabrication (Étapes)")
st.caption("Basé sur le Guide PDF utilisant la Cire de Soja")

# Using Expanders to organize the steps cleanly
with st.expander("Étape 1 : Préparation (Avant de commencer)", expanded=True):
    st.markdown(f"""
    1.  **Nettoyer & Sécher :** Assurez-vous que vos **{num_candles}** conteneurs sont propres et secs.
    2.  **Mèche :** Attachez la mèche ({wick_row['Description']}) au centre du conteneur en utilisant un point d'autocollant de mèche ou de la colle.
    3.  **Fixer :** Utilisez un support de mèche pour maintenir la mèche droite.
    """)

with st.expander("Étape 2 : Fonte de la Cire", expanded=True):
    st.markdown(f"""
    1.  **Peser :** Mesurez **{WAX_AMOUNT_KG*1000:.0f}g** de {wax_row['Product Name']}.
    2.  **Faire fondre :** Placez la cire dans un bain-marie ou un fontoir à cire.
    3.  **Chauffer :** Faites fondre lentement. **NE PAS** chauffer directement sur une flamme nue.
    4.  **Remuer :** Remuez de temps en temps pour assurer une fonte uniforme.
    """)

with st.expander("Étape 3 : Ajout du Parfum (Étape Cruciale)", expanded=True):
    st.markdown(f"""
    1.  **Refroidir :** Une fois fondue, laissez la cire refroidir à **60°C - 65°C**.
    2.  **Mesurer :** Pesez **{fragrance_weight_kg*1000:.1f}g** de **{scent_row['Scent Name']}**.
    3.  **Mélanger :** Versez l'huile dans la cire.
    4.  **Remuer :** Remuez doucement mais soigneusement pendant **2 minutes** pour assurer que l'huile se lie à la cire.
    """)

with st.expander("Étape 4 : Coulage", expanded=True):
    st.markdown("""
    1.  **Refroidir davantage :** Laissez le mélange refroidir à **50°C - 55°C**. Cela aide à obtenir une surface lisse.
    2.  **Couler :** Versez lentement la cire dans vos conteneurs.
    3.  **Tapoter :** Tapotez doucement le conteneur pour libérer les bulles d'air.
    """)

with st.expander("Étape 5 : Refroidissement & Séchage", expanded=True):
    st.markdown("""
    1.  **Reposer :** Laissez les bougies reposer à température ambiante (20°C - 25°C). Évitez les courants d'air ou la climatisation.
    2.  **Attendre :** Laissez refroidir au moins **4-6 heures** (24 heures c'est idéal).
    3.  **Couper :** Avant d'allumer, coupez la mèche à environ **0.6cm - 1.0cm**.
    """)