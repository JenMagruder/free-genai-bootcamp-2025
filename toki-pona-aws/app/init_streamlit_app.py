import streamlit as st

pg = st.navigation([st.Page(page="000_learn_tokipona.py", url_path='Learn_Toki_Pona'),
                    st.Page(page="00_tokipona_eng.py", url_path='Toki_Pona_to_English'),
                    st.Page(page="01_eng_tokipona.py", url_path='Englisj_to_Toki_Pona')])
pg.run()