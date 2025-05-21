import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns 

st.set_page_config(page_title="CSV Visualizer", page_icon="📊")
st.title("📊 CSV Visualization App")

st.write("### 1. Upload your CSV file")
uploaded_file = st.file_uploader("Drag and drop your file here", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File loaded successfully!")
else:
    df = pd.DataFrame({
        'Age': [25, 30, 35],
        'Salary': [40000, 55000, 75000],
        
    })
    st.info("ℹ️ Using sample data. Upload a file to use yours ^^ .")


numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

if len(numeric_cols) < 2:
    st.warning("⚠️ We need at least 2 number columns to analyze")
else:
    st.write(f"### 2. 🔢 Available numeric columns: {', '.join(numeric_cols)}")
    
    
    st.write("### 3. 📊 Select visualization type")
    graph_type = st.selectbox(
        "Choose a graph type:",
        options=[
            "Correlation Heatmap",
            "Custom Scatter Plot (choose columns)",
            "Histogram",
            "Scatter Plot (auto strongest correlation)",
            
        ]
    )
    
    st.markdown("---")
    
    if graph_type == "Correlation Heatmap":
        st.write("#### 🔥 Correlation Heatmap: ")
        fig, ax = plt.subplots(figsize=(10,8))
        sns.heatmap(df[numeric_cols].corr(), cmap="coolwarm", annot=True, ax=ax)
        st.pyplot(fig)
        
        
        corr_matrix = df[numeric_cols].corr()
        corr_pairs = corr_matrix.stack()
        corr_pairs = corr_pairs[corr_pairs != 1]
        
        if not corr_pairs.empty:
            strongest_pair = corr_pairs.abs().idxmax()
            strongest_value = corr_pairs.loc[strongest_pair]
            
            st.write("### � Strongest Correlation")
            st.write(f"Strongest pair: {strongest_pair[0]} vs {strongest_pair[1]}")
            st.write(f"Correlation: {strongest_value:.2f}")
    
    elif graph_type == "Scatter Plot (auto strongest correlation)":
        corr_matrix = df[numeric_cols].corr()
        corr_pairs = corr_matrix.stack()
        corr_pairs = corr_pairs[corr_pairs != 1]
        
        if not corr_pairs.empty:
            strongest_pair = corr_pairs.abs().idxmax()
            strongest_value = corr_pairs.loc[strongest_pair]
            
            st.write("#### 📈 Scatter Plot (strongest correlation)")
            st.write(f"Automatically selected: {strongest_pair[0]} vs {strongest_pair[1]}")
            st.write(f"Correlation: {strongest_value:.2f}")
            
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x=strongest_pair[0], y=strongest_pair[1], color='blue')
            st.pyplot(fig)
            st.balloons()
    
    elif graph_type == "Custom Scatter Plot (choose columns)":
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X-axis", numeric_cols)
        with col2:
            y_axis = st.selectbox("Y-axis", numeric_cols)
        
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=x_axis, y=y_axis, color='green')
        st.pyplot(fig)
    
    
    elif graph_type == "Histogram":
        selected_column = st.selectbox("Select column for histogram", numeric_cols)
        
        
        fig, ax = plt.subplots()
        sns.histplot(data=df, x=selected_column, kde=True)
        st.pyplot(fig)

st.markdown("---")
