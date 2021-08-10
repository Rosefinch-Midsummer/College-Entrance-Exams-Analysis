# -*- coding: utf-8 -*-
import streamlit as st
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode
import pandas as pd
import plotly.express as px



num_exams = st.sidebar.slider('老高考全国卷总考试次数', 1, 20)



uploaded_file = st.file_uploader("请选择要上传的csv格式表格！")
if uploaded_file is not None:
	df = pd.read_csv(uploaded_file)
	df = df.set_index('考试时间', drop=False)
	AgGrid(df,editable=True, fit_columns_on_grid_load=False)
        

else:
    df_template = pd.DataFrame('',index=range(num_exams), columns=['考试时间','语文', '数学', '英语', '物理', '化学', '生物'])
    with st.form('example form') as f:
        st.header('成绩单')
        st.write('考试时间格式为XXXX-XX-XX，例如2021-08-10')
        response = AgGrid(df_template, editable=True, fit_columns_on_grid_load=False)
        st.form_submit_button()
        df = pd.DataFrame(response['data'])
        df = df.set_index('考试时间', drop=False)
        st.dataframe(df) 
        df.to_csv('df.csv', index=False)


num = st.sidebar.slider('要分析的特定考试序号', 1, 20)

st.subheader(f"第{num}次考试得分率雷达图")
placeholder = st.empty()

def radar_chart(num):  
    specific_df = pd.DataFrame(dict(r=[int(df['语文'][num-1])/150,int(df['数学'][num-1])/150,int(df['英语'][num-1])/150,int(df['物理'][num-1])/110,int(df['化学'][num-1])/100,int(df['生物'][num-1])/90],theta=['语文', '数学', '英语', '物理', '化学', '生物']))
    fig = px.line_polar(specific_df, r='r', theta='theta', line_close=True)
    placeholder.write(fig)

radar_chart(num)


#add a selectbox to the sidebar
subject= st.sidebar.selectbox('选择要分析的科目', ['语文', '数学', '英语', '物理', '化学', '生物'])

st.write(f"""## {subject}科目考试成绩分析 """)

st.write(df[subject])

st.line_chart(df[subject])





