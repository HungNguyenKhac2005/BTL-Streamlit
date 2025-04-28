# import thư viện 
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
from random import randint

# set tiêu đề cho wed
st.title("Wedside phân tích dữ liệu rạp phim")
col1,col2,col3 = st.columns([2,2,2])
with col1:
    st.header("DashBoard")
with col2:
    st.header("Hà Nội Ngày:")
with col3:
    st.header("25/04/2025")

# chuyển màu nền thành màu xanh
st.markdown(
    """
    <style>
    .stApp {
        background: #e0f7fa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# tạo hiệu ứng load data 
st.write("Tiến trình tải dữ liệu...")
progress = st.progress(0)
for i in range(101):
    time.sleep(0.001)
    progress.progress(i)
st.success('Hoàn Tất!')

# Thu thập dữ liệu và tải dữ liệu lên
@st.cache_data
def load_data():
    return pd.read_csv('https://raw.githubusercontent.com/nv-thang/DataVisualizationCourse/refs/heads/main/Dataset%20for%20Practice/movies.csv')
with st.expander("Xem data tại đây"):
    data = load_data()
    
    # thêm các dữ liệu mới cần thiết cho dữ liệu
    cinema = ['beta xuân đỉnh','beta mỹ đình','cinema thăng long','rạp chiếu phim quốc gia','beta đan phượng','beta xuân thủy','rạp phim lotte','rạp phim đôi','beta ứng hòa','beta hòai đức']
    data['cinema'] = [cinema[randint(0,len(cinema)-1)] for i in range(len(data))]
    data['gia phim'] = [randint(50000,180000) for i in range(len(data))]
    months = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"]
    months_of_df = []
    for i in range(len(data)):
        months_of_df.append(months[randint(0,len(months)-1)])
    data['months'] = months_of_df
    st.write("Dữ Liêu: ",data)

# Chia bố cục cho giao diện 
col1,col2,col3,col4,col5,col6,col7 = st.columns([1,3,1,2,1,3,1])
with col2:
    st.metric(label="Total Sales",value=str(round(data['gia phim'].sum()/1000000,2)) + " M",delta='+50')
with col4:
    st.metric(label="YTD Growth %",value=4.8,delta='+5')
with col6:
    st.metric(label="LY Sales",value=str(round((data['gia phim'].sum()-100000000)/1000000,2)) + " M",delta='-5')

st.write('-----------------------------------------------------------')

# tạo các tab thay đổi 
tab1,tab2,tab3 = st.tabs(['Tổng quan','Top 5 Brands in sales','Top 5 slowest selling brand'])
cinema_total_sales = data.groupby("cinema")['gia phim'].sum().sort_values(ascending=False)
name_cinema = cinema_total_sales.index.to_list()
total_sales = cinema_total_sales.values.tolist()

# tạo các slicer đặt ở thanh tab bên trái
select_option = st.sidebar.selectbox('Chọn cinema ở đây..',options=name_cinema)
months.append("No Months")
select_months = st.sidebar.select_slider("Chọn tháng ở đây..",options=months)

# tạo các def để vẽ biểu đồ và thay đổi khi cần
def top_5(select_months):
    if(select_months == 'No Months'):
        cinema_total_sales = data.groupby("cinema")['gia phim'].sum().sort_values(ascending=False)
        name_cinema = cinema_total_sales.index.to_list()
        total_sales = cinema_total_sales.values.tolist()
        plt.figure(figsize=(5,3))
        sns.barplot(x=total_sales[:5],y=name_cinema[:5],palette='Blues')
        plt.title("Top 5 Brands in sales",fontsize=24,pad=15)
        plt.xlabel("Tổng doanh thu")
        plt.ylabel("Tên rạp chiếu")
        st.pyplot(plt)
    else:
        df = data[data['months'] == select_months]
        cinema_total_sales = df.groupby("cinema")['gia phim'].sum().sort_values(ascending=False)
        name_cinema = cinema_total_sales.index.to_list()
        total_sales = cinema_total_sales.values.tolist()
        plt.figure(figsize=(5,3))
        sns.barplot(x=total_sales[:5],y=name_cinema[:5],palette='Blues')
        plt.title("Top 5 Brands in sales " + select_months,fontsize=24,pad=15)
        plt.xlabel("Tổng doanh thu")
        plt.ylabel("Tên rạp chiếu")
        st.pyplot(plt)

def top_5_down(select_months):
    if(select_months == 'No Months'):
        cinema_total_sales = data.groupby("cinema")['gia phim'].sum().sort_values(ascending=False)
        name_cinema = cinema_total_sales.index.to_list()
        total_sales = cinema_total_sales.values.tolist()
        plt.figure(figsize=(5,3))
        sns.barplot(x=total_sales[5:],y=name_cinema[5:],palette='Reds')
        plt.title("Top 5 slowest selling brand",fontsize=24,pad=15)
        plt.xlabel("Tổng doanh thu")
        plt.ylabel("Tên rạp chiếu")
        st.pyplot(plt)
    else:
        df = data[data['months'] == select_months]
        cinema_total_sales = df.groupby("cinema")['gia phim'].sum().sort_values(ascending=False)
        name_cinema = cinema_total_sales.index.to_list()
        total_sales = cinema_total_sales.values.tolist()
        plt.figure(figsize=(5,3))
        sns.barplot(x=total_sales[5:],y=name_cinema[5:],palette='Reds')
        plt.title("Top 5 slowest selling brand " + select_months,fontsize=24,pad=15)
        plt.xlabel("Tổng doanh thu")
        plt.ylabel("Tên rạp chiếu")
        st.pyplot(plt)

# tạo các exoander để them thông tin và xem phân tích dữ liệu
with st.expander('Xem thông tin của ' + select_option + ' tại đây'):
        st.write("Tên rạp chiếu: ",select_option)
        
# Tạo chức năng cho từng tab
with tab1:
    col1,col2 = st.columns([1,1])
    with col1:
        plt.figure(figsize=(7,5))
        sns.barplot(x=name_cinema[:5],y=total_sales[:5],palette='Blues')
        plt.title("Top 5 Brands in sales",fontsize=24,pad=15)
        plt.xticks(rotation=45,ha='right')
        st.pyplot(plt)
    with col2:
        plt.figure(figsize=(7,5))
        sns.barplot(x=name_cinema[5:],y=total_sales[5:],palette='Reds')
        plt.title("Top 5 slowest selling brand",fontsize=24,pad=15)
        plt.xticks(rotation=45,ha='right')
        st.pyplot(plt)
with tab2:
    select_radio = st.radio("Chọn biểu đồ ở đây..",['Bar plot','Line plot','pie plot'],horizontal=True)
    if(select_radio == 'Bar plot'):
        top_5(select_months)
    if(select_radio == 'pie plot'):
        percents = []
        for i in range(5):
            percent = (total_sales[i]/data['gia phim'].sum())*100
            percents.append(percent)
        plt.figure(figsize=(5,3))
        plt.pie(percents,labels=name_cinema[:5],autopct='%1.1f%%',colors=['#FFB3BA',  # hồng pastel
                '#BAE1FF',  # xanh da trời nhạt
                '#BFFCC6',  # xanh lá mint
                '#FFFFBA',  # vàng nhạt
                '#D5AAFF'],wedgeprops={'edgecolor':'black','linewidth':1.5})
        plt.title("Phần trăm tổng doanh thu của rạp chiếu")
        st.pyplot(plt)
    if(select_radio == 'Line plot'):
        plt.figure(figsize=(5,3))
        plt.plot(name_cinema,total_sales,marker='o')
        plt.xticks(rotation=45,ha='right')
        plt.title('Biểu đồ đường thể hiện tổng doanh thu của từng rạp chiều')
        plt.xlabel("tên rạp chiếu")
        plt.ylabel('tổng doanh thu')
        st.pyplot(plt)
with tab3:
    select_radio = st.radio("Chọn biểu đồ ở đây....",['Bar plot','Line plot','pie plot'],horizontal=True)
    if(select_radio == 'Bar plot'):
        top_5_down(select_months)
    if(select_radio == 'pie plot'):
        percents = []
        index=-5
        for i in range(5):
            percent = (total_sales[index]/data['gia phim'].sum())*100
            index+=1
            percents.append(percent)
        plt.figure(figsize=(5,3))
        plt.pie(percents,labels=name_cinema[5:],autopct='%1.1f%%',colors=['#FFB3BA',  # hồng pastel
                '#BAE1FF',  # xanh da trời nhạt
                '#BFFCC6',  # xanh lá mint
                '#FFFFBA',  # vàng nhạt
                '#D5AAFF'],wedgeprops={'edgecolor':'black','linewidth':1.5})
        plt.title("Phần trăm tổng doanh thu của rạp chiếu")
        st.pyplot(plt)
    if(select_radio == 'Line plot'):
        plt.figure(figsize=(5,3))
        plt.plot(name_cinema,total_sales,marker='o')
        plt.xticks(rotation=45,ha='right')
        plt.title('Biểu đồ đường thể hiện tổng doanh thu của từng rạp chiều')
        plt.xlabel("tên rạp chiếu")
        plt.ylabel('tổng doanh thu')
        st.pyplot(plt)

st.write('-----------------------------------------------------------')

# tạo tab cho phần tổng doanh thu
tab1,tab2 = st.tabs(['Tổng quan','Chi tiết'])
with st.expander('Xem Phân tích dữ liệu tại đây..'):
        st.write("Đã phân tích dữ liêu")
with tab1:
    plt.figure(figsize=(15,5))
    total_sales_months = data.groupby("months")['gia phim'].sum().sort_values(ascending=True)
    month = total_sales_months.index.to_list()
    total_sales = total_sales_months.values.tolist()
    sns.barplot(x=month,y=total_sales,palette='GnBu')
    plt.title("Biểu đồ tổng doanh thu theo tháng",fontsize=24,pad=15)
    plt.xticks(rotation=45,ha='right')
    plt.xlabel('tên rạp chiểu',fontsize=15)
    plt.ylabel("Tổng doanh thu",fontsize=15)
    st.pyplot(plt)
def tong_doanh_thu_rap_theo_thang(select_option):
    df = data[data['cinema'] == select_option]
    df_select_option = df.groupby('months')['gia phim'].sum().sort_values().reset_index()
    plt.figure(figsize=(15,5))
    sns.barplot(x='months',y='gia phim',data=df_select_option,palette='YlGnBu')
    plt.title('Doanh thu của rạp ' + select_option.upper() +" theo các tháng",fontsize=24,pad=15)
    st.pyplot(plt)
with tab2:
    tong_doanh_thu_rap_theo_thang(select_option)

st.write('-----------------------------------------------------------')

# tạo tab cho phần tổng sản lượng bán
tab1,tab2 = st.tabs(['Tổng quan','Chi tiết'])
with st.expander('Xem Phân tích dữ liệu tại đây..'):
        st.write("Đã phân tích dữ liêu")
with tab1:
    if(select_months == 'No Months'):
        count_cinema = data['cinema'].value_counts().reset_index()
        plt.figure(figsize=(15,5))
        sns.barplot(x='cinema',y='count',data=count_cinema,palette='PuBu')
        plt.title("Tổng sản lượng vé bán theo rạp",fontsize=24,pad=15)
        plt.xticks(rotation=45,ha='right')
        plt.xlabel('tên rạp chiểu',fontsize=15)
        plt.ylabel("Tổng sản lượng bán",fontsize=15)
        st.pyplot(plt)
    else:
        df = data[data['months'] == select_months]
        count_cinema = df['cinema'].value_counts().reset_index()
        plt.figure(figsize=(15,5))
        sns.barplot(x='cinema',y='count',data=count_cinema,palette='PuBu')
        plt.title("Tổng sản lượng vé bán theo " + select_months,fontsize=24,pad=15)
        plt.xticks(rotation=45,ha='right')
        plt.xlabel('tên rạp chiểu',fontsize=15)
        plt.ylabel("Tổng sản lượng bán",fontsize=15)
        st.pyplot(plt)
with tab2:
    df = data[data['cinema'] == select_option]
    count_cinema = df['months'].value_counts().reset_index()
    plt.figure(figsize=(15,5))
    sns.barplot(x='months',y='count',data=count_cinema,palette='PuBu')
    plt.title("Tổng sản lượng vé bán theo " + select_option.upper(),fontsize=24,pad=15)
    plt.xticks(rotation=45,ha='right')
    plt.xlabel('tên rạp chiểu',fontsize=15)
    plt.ylabel("Tổng sản lượng bán",fontsize=15)
    st.pyplot(plt)









