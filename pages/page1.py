import streamlit as st

# 设置网页标题
st.title('小微企业信贷评分系统')

if st.button("启动系统"):
    st.switch_page("pages/page2.py")
