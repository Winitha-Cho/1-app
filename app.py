import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family'] = 'Tahoma'

st.title("กราฟเปรียบเทียบจำนวนเด็กเกิดกับผู้สูงอายุ")

# อ่าน Excel
df_birth = pd.read_excel("data.xlsx", sheet_name="births", index_col=0)  # index_col=0 ให้จังหวัดเป็น index
df_old = pd.read_excel("data.xlsx", sheet_name="elderly", index_col=0)

# แปลงให้เป็น long format
df_birth_long = df_birth.reset_index().melt(id_vars='จังหวัด', var_name='ปี', value_name='จำนวน')
df_old_long = df_old.reset_index().melt(id_vars='จังหวัด', var_name='ปี', value_name='จำนวน')

# Sidebar เลือกปีและจังหวัด
selected_years = st.sidebar.multiselect(
    "เลือกปี",
    options=df_birth_long['ปี'].unique(),
    default=df_birth_long['ปี'].unique()
)
selected_provinces = st.sidebar.multiselect(
    "เลือกจังหวัด",
    options=df_birth_long['จังหวัด'].unique(),
    default=df_birth_long['จังหวัด'].unique()
)

# กรองข้อมูล
df_birth_filtered = df_birth_long[
    (df_birth_long['ปี'].isin(selected_years)) &
    (df_birth_long['จังหวัด'].isin(selected_provinces))
]
df_old_filtered = df_old_long[
    (df_old_long['ปี'].isin(selected_years)) &
    (df_old_long['จังหวัด'].isin(selected_provinces))
]

# สร้างกราฟ
fig, ax = plt.subplots(figsize=(10,5))

for province in selected_provinces:
    birth_data = df_birth_filtered[df_birth_filtered['จังหวัด'] == province]
    old_data = df_old_filtered[df_old_filtered['จังหวัด'] == province]
    ax.plot(birth_data['ปี'], birth_data['จำนวน'], marker='o', label=f'จำนวนเด็กแรกเกิด ({province})')
    ax.plot(old_data['ปี'], old_data['จำนวน'], marker='o', label=f'ผู้สูงอายุ ({province})')

ax.set_xlabel('ปี')
ax.set_ylabel('จำนวนคน')
ax.set_title('จำนวนเด็กแรกเกิดเทียบกับผู้สูงอายุ')
ax.legend()
ax.grid(True)

st.pyplot(fig)
