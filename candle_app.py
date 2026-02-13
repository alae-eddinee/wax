import streamlit as st
import pandas as pd
import io

# --- 1. SETUP & THEME CONFIGURATION ---
st.set_page_config(page_title="Candle Cost Calculator", page_icon="", layout="wide")

# FORCE LIGHT MODE CSS
# This injects CSS to force white backgrounds and black text even if your computer is in Dark Mode.
st.markdown("""
    <style>
        /* Force main background to white */
        .stApp {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        /* Force sidebar to light gray */
        [data-testid="stSidebar"] {
            background-color: #F0F2F6 !important;
        }
        /* Force text colors to black for readability */
        .stApp, .stApp * {
            color: #31333F !important;
        }
        /* Fix headers specifically */
        h1, h2, h3, h4, h5, h6 {
            color: #1f2937 !important;
        }
        /* Fix paragraph and span text */
        p, span, div, label {
            color: #31333F !important;
        }
        /* Fix metrics color */
        [data-testid="stMetricValue"] {
            color: #000000 !important;
        }
        /* Fix metric labels */
        [data-testid="stMetricLabel"] {
            color: #6b7280 !important;
        }
        /* Fix table text */
        .dataframe {
            color: #000000 !important;
        }
        /* Fix expander headers */
        .streamlit-expanderHeader {
            color: #1f2937 !important;
        }
        /* Fix selectbox and other input elements */
        .stSelectbox > div > div {
            color: #31333F !important;
        }
        /* Fix dropdown options */
        .stSelectbox option {
            background-color: #FFFFFF !important;
            color: #31333F !important;
        }
        /* Fix dropdown container */
        .stSelectbox[data-testid="stSelectbox"] {
            background-color: #FFFFFF !important;
        }
        /* Fix selectbox input field */
        .stSelectbox input {
            color: #31333F !important;
            background-color: #FFFFFF !important;
        }
        /* Fix selectbox dropdown options */
        div[data-testid="stSelectbox"] div[role="listbox"] {
            background-color: #FFFFFF !important;
            color: #31333F !important;
        }
        /* Fix individual selectbox options */
        div[data-testid="stSelectbox"] div[role="option"] {
            background-color: #FFFFFF !important;
            color: #31333F !important;
        }
        /* Fix selectbox text when an option is selected */
        .stSelectbox > div > div > div > div > div {
            color: #31333F !important;
        }
        /* Fix slider labels */
        .stSlider > div > div > div {
            color: #31333F !important;
        }
        /* Fix number input */
        .stNumberInput > div > div {
            color: #31333F !important;
        }
        /* Fix checkbox */
        .stCheckbox > label {
            color: #31333F !important;
        }
    </style>
""", unsafe_allow_html=True)

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
11,Candle Wick Sticker,"Double-sided, Dia 20mm, Color: White",1500,PIECE,0.071,106.5
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
wicks_df = df[df['Product Name'].str.contains("Wick") & ~df['Product Name'].str.contains("Holder|Sticker")]
sticker_row = df[df['Item No'] == 11].iloc[0]

# --- 3. UI LAYOUT ---
st.title("🕯️ Candle Cost Calculator")

# --- SELECTION AREA ---
col_sel1, col_sel2, col_sel3 = st.columns(3)

with col_sel1:
    st.subheader("1. Choose Wax")
    wax_choice = st.selectbox("Wax Type", waxes_df['Product Name'].unique(), index=0)
    wax_row = waxes_df[waxes_df['Product Name'] == wax_choice].iloc[0]

with col_sel2:
    st.subheader("2. Choose Fragrance")
    # This selector lets you see the price and name
    scent_choice_label = st.selectbox("Fragrance Oil", fragrances_df['Display Label'].unique(), index=0)
    scent_row = fragrances_df[fragrances_df['Display Label'] == scent_choice_label].iloc[0]

with col_sel3:
    st.subheader("3. Choose Wick")
    wick_choice = st.selectbox("Wick Size", wicks_df['Description'].unique())
    wick_row = wicks_df[wicks_df['Description'] == wick_choice].iloc[0]

st.divider()

# --- FRAGRANCE LOAD SECTION ---
st.subheader("⚙️ Settings: Fragrance Load")
st.caption("How much oil to add to the wax?")

col_load_slider, col_load_info = st.columns([1, 1])

with col_load_slider:
    fragrance_load = st.slider(
        "Fragrance Percentage (%)", 
        min_value=1, 
        max_value=12, 
        value=6
    )

with col_load_info:
    # Logic to explain the percentage to the user
    if fragrance_load < 6:
        st.warning(f"⚠️ **{fragrance_load}% is Low.** The scent might be too weak.")
    elif 6 <= fragrance_load <= 8:
        st.success(f"✅ **{fragrance_load}% is Perfect.** (Recommended 6-8%). Good scent, burns well.")
    elif 9 <= fragrance_load <= 10:
        st.success(f"🔥 **{fragrance_load}% is Strong.** (Max recommended). Very strong scent.")
    else:
        st.error(f"🛑 **{fragrance_load}% is Risky.** Over 10% can cause the oil to seep out of the candle.")

# Jar Settings
col_jar1, col_jar2, col_jar3 = st.columns(3)
with col_jar1:
    jar_size = st.number_input("Candle Jar Size (grams of wax)", value=200, step=10)
with col_jar2:
    wax_amount_kg = st.number_input("Wax Amount (kg)", value=1.0, min_value=0.1, max_value=10.0, step=0.1)
with col_jar3:
    include_sticker = st.checkbox("Include Wick Sticker cost?", value=True)

# --- CALCULATIONS ---
WAX_AMOUNT_KG = wax_amount_kg
cost_wax = WAX_AMOUNT_KG * wax_row['Unit Price']
fragrance_weight_kg = (fragrance_load / 100.0) * WAX_AMOUNT_KG
cost_fragrance = fragrance_weight_kg * scent_row['Unit Price']

total_mixture_g = (WAX_AMOUNT_KG + fragrance_weight_kg) * 1000
num_candles = int(total_mixture_g / jar_size)

cost_wicks = num_candles * wick_row['Unit Price']
cost_stickers = (num_candles * sticker_row['Unit Price']) if include_sticker else 0.0

total_batch_cost = cost_wax + cost_fragrance + cost_wicks + cost_stickers
cost_per_candle = total_batch_cost / num_candles if num_candles > 0 else 0.0

# --- RESULTS ---
st.divider()
st.markdown(f"### 📊 Results: {scent_row['Scent Name']}")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Batch Cost", f"${total_batch_cost:.2f}")
m2.metric("Cost Per Candle", f"${cost_per_candle:.2f}")
m3.metric("Candles Produced", f"{num_candles}")
m4.metric("Fragrance Used", f"{fragrance_weight_kg*1000:.0f} g")

# Breakdown Table
breakdown_df = pd.DataFrame({
    "Item": [wax_row['Product Name'], f"Oil: {scent_row['Scent Name']}", "Wicks", "Stickers"],
    "Unit Price": [f"${wax_row['Unit Price']}/kg", f"${scent_row['Unit Price']}/kg", f"${wick_row['Unit Price']:.4f}/pc", f"${sticker_row['Unit Price']:.3f}/pc"],
    "Quantity": [f"{WAX_AMOUNT_KG:.1f} kg", f"{fragrance_weight_kg*1000:.1f} g", f"{num_candles} pcs", f"{num_candles} pcs" if include_sticker else "0"],
    "Cost": [f"${cost_wax:.2f}", f"${cost_fragrance:.2f}", f"${cost_wicks:.2f}", f"${cost_stickers:.2f}"]
})
st.table(breakdown_df)

# --- THE STEPS (RECIPE) ---
st.markdown("## 📝 Making Guide (Steps)")
st.caption("Based on the PDF Guide using Soy Wax")

# Using Expanders to organize the steps cleanly
with st.expander("Step 1: Preparation (Before you start)", expanded=True):
    st.markdown(f"""
    1.  **Clean & Dry:** Ensure your **{num_candles}** containers are clean and dry.
    2.  **Wick:** Attach the wick ({wick_row['Description']}) to the center of the container using a wick sticker or glue.
    3.  **Secure:** Use a wick holder to keep the wick standing straight up.
    """)

with st.expander("Step 2: Melting the Wax", expanded=True):
    st.markdown(f"""
    1.  **Weigh:** Measure out **{WAX_AMOUNT_KG*1000:.0f}g** of {wax_row['Product Name']}.
    2.  **Melt:** Place wax in a double boiler or wax melter.
    3.  **Heat:** Melt slowly. **Do NOT** heat directly over an open flame.
    4.  **Stir:** Stir occasionally to ensure even melting.
    """)

with st.expander("Step 3: Adding Fragrance (Crucial Step)", expanded=True):
    st.markdown(f"""
    1.  **Cool Down:** Once melted, let the wax cool down to **60°C - 65°C**.
    2.  **Measure:** Weigh out **{fragrance_weight_kg*1000:.1f}g** of **{scent_row['Scent Name']}**.
    3.  **Mix:** Pour the oil into the wax.
    4.  **Stir:** Stir gently but thoroughly for **2 minutes** to ensure the oil binds to the wax.
    """)

with st.expander("Step 4: Pouring", expanded=True):
    st.markdown("""
    1.  **Cool Further:** Let the mixture cool down to **50°C - 55°C**. This helps get a smooth top.
    2.  **Pour:** Slowly pour the wax into your containers.
    3.  **Tap:** Gently tap the container to release any air bubbles.
    """)

with st.expander("Step 5: Cooling & Curing", expanded=True):
    st.markdown("""
    1.  **Rest:** Let the candles sit at room temperature (20°C - 25°C). Avoid drafts or AC.
    2.  **Wait:** Allow to cool for at least **4-6 hours** (24 hours is best).
    3.  **Trim:** Before lighting, trim the wick to about **0.6cm - 1.0cm**.
    """)