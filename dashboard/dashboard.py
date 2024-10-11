import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Buka dan baca dataset yang digunakan
orders_df = pd.read_csv('dashboard/olist_orders_dataset.csv')
order_items_df = pd.read_csv('dashboard/olist_order_items_dataset.csv')
customers_df = pd.read_csv('dashboard/olist_customers_dataset.csv')

# Merge data
merged_df = order_items_df.merge(orders_df, on='order_id').merge(customers_df, on='customer_id')
items_orders = pd.merge(order_items_df, orders_df, on='order_id', how='inner')
orders_customers = pd.merge(orders_df, customers_df, on='customer_id', how='inner')

# Menghitung returned_orders
returned_orders = items_orders[items_orders['order_status'].isin(['canceled', 'unavailable'])]

# Menghitung returned_count
returned_count = returned_orders['product_id'].value_counts().reset_index()
returned_count.columns = ['product_id', 'returned_count']

# Menghitung total_sales
total_sales = items_orders['product_id'].value_counts().reset_index()
total_sales.columns = ['product_id', 'total_sales']

# Apa saja produk terlaris yang dijual ?
def plot_top_selling_products():
    top_categories = merged_df['product_id'].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_categories.values, y=top_categories.index, palette='viridis')
    plt.title('Penjualan Teratas Berdasarkan product_id')
    plt.xlabel('Jumlah Penjualan')
    plt.ylabel('Product ID')
    st.pyplot(plt)

# Bagaimana tren pengembalian produk dalam dataset ini?
def plot_return_trends():
    # Merge returns
    returns = pd.merge(returned_count, total_sales, on='product_id', how='left')
    returns['return_percentage'] = (returns['returned_count'] / returns['total_sales']) * 100

    # Membuat bins dan labels 
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']
    returns['return_range'] = pd.cut(returns['return_percentage'], bins=bins, labels=labels, right=False)

    # Menghitung return_range untuk tiap produk
    return_counts = returns['return_range'].value_counts().reset_index()
    return_counts.columns = ['return_range', 'product_count']

    plt.figure(figsize=(14, 8))
    sns.barplot(x='return_range', y='product_count', data=return_counts, palette='viridis')
    plt.title("Jumlah Produk Berdasarkan Rentang Persentase Pengembalian")
    plt.xlabel("Rentang Persentase Pengembalian")
    plt.ylabel("Jumlah Produk")
    plt.tight_layout()
    st.pyplot(plt)

# Bagaimana distribusi order status untuk setiap states pelanggan ?
def plot_order_status_distribution():
    order_status_distribution = orders_customers.groupby(['customer_state', 'order_status']).size().unstack().fillna(0)

    plt.figure(figsize=(14, 8))
    order_status_distribution.plot(kind='bar', stacked=True, colormap='viridis', ax=plt.gca())
    plt.title("Distribusi Status Pesanan untuk Setiap Negara Bagian")
    plt.xlabel("Negara Bagian")
    plt.ylabel("Jumlah Pesanan")
    plt.xticks(rotation=45)
    plt.legend(title="Status Pesanan", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

    plt.figure(figsize=(14, 8))
    sns.heatmap(order_status_distribution, annot=True, fmt=".0f", cmap='viridis')
    plt.title("Heatmap Distribusi Status Pesanan untuk Setiap Negara Bagian")
    plt.xlabel("Status Pesanan")
    plt.ylabel("Negara Bagian")
    plt.tight_layout()
    st.pyplot(plt)

# Tampilan dashboard
st.title('Dashboard Analisis Data')
st.sidebar.header('Pilih Grafik untuk Ditampilkan')
option = st.sidebar.selectbox('Pilih Analisis', ['Produk Terlaris', 'Tren Pengembalian Produk', 'Distribusi Order Status'])

if option == 'Produk Terlaris':
    plot_top_selling_products()
elif option == 'Tren Pengembalian Produk':
    plot_return_trends()
elif option == 'Distribusi Order Status':
    plot_order_status_distribution()
