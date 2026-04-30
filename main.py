import streamlit as st
import pandas as pd

# Load data
predictions = pd.read_csv('user_product_predictions.csv')
products = pd.read_csv('products_names.csv')

st.title('🛒 Instacart Reorder Recommender')
st.markdown('Enter a User ID to get personalized product recommendations.')

user_id = st.number_input('User ID:', min_value=1, step=1, value=1)
k = st.slider('Number of recommendations (K):', min_value=5, max_value=30, value=10)

if st.button('Get Recommendations'):
    user_preds = predictions[predictions['user_id'] == user_id]
    
    if user_preds.empty:
        st.warning('User not found in the dataset.')
    else:
        top_k = (user_preds
                 .nlargest(k, 'pred_prob')
                 .merge(products, on='product_id'))
        
        st.success(f'Top-{k} Recommendations for User {user_id}:')
        display_df = top_k[['product_name', 'pred_prob']].reset_index(drop=True)
        display_df.columns = ['Product', 'Confidence']
        display_df.index += 1
        st.table(display_df)
