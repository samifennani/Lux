import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Future Luxe AI Recommender", layout="wide")

# تحميل مكتبة model-viewer من CDN
components.html("""
<script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
""", height=0)

# Load CSV
csv_path = os.path.join(os.path.dirname(__file__), "products.csv")
df = pd.read_csv(csv_path)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

st.title("Future Luxe AI Product Explorer")

# Sidebar - Customer Preferences
st.sidebar.header("Customer Preferences")
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
product_type = st.sidebar.selectbox("Product Type", df['type'].unique())
color = st.sidebar.selectbox("Preferred Color", df['color'].unique())
budget = st.sidebar.slider("Budget (USD)", 500, 15000, 500)

# Filter products
filtered = df[
    (df['type'] == product_type) &
    (df['color'] == color) &
    (df['price'] <= budget)
]

st.header("Recommended Products")
if not filtered.empty:
    for idx, row in filtered.iterrows():
        st.subheader(row['name'])
        st.image(row['image_url'], width=150)
        st.write(f"Price: ${row['price']}")
        st.write(row['description'])

        # Embed 3D model
        model_html = f"""
        <model-viewer src="{row['model_3d']}" alt="{row['name']}" 
        auto-rotate camera-controls background-color="#FFFFFF" style="width: 100%; height: 400px;">
        </model-viewer>
        """
        components.html(model_html, height=450)
else:
    st.write("No products match your preferences. Try adjusting your filters.")
