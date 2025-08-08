# app.py

import streamlit as st

page1 = st.Page("pages/page1.py", title="首页")
page2 = st.Page("pages/page2.py", title="企业数据录入")
page3 = st.Page("pages/page3.py", title="AI智能助手")

pg = st.navigation([page1, page2, page3])
pg.run()
