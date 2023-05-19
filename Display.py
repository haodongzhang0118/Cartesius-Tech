import streamlit as st
from CorrectorAndRevise import correct_and_revise

st.title("Personal Statement Improvement")
file = st.file_uploader("Pick your personal statement")
# path = st.text_input('Give me your file path')

if file:
    # file = r"{}".format(path)
    file = r"{}".format("/Users/zhanghaodong/Desktop/test1.pdf")
    grade, grammar, revised, evaluations, suggestions = correct_and_revise(file)

    with st.expander("Personal Statement Grade"):
        st.info(grade)

    with st.expander("Grammar Corrected Paper"):
        st.info(grammar)

    with st.expander("Evaluations"):
        st.info(evaluations)

    with st.expander("Suggestions"):
        st.info(suggestions)

    with st.expander("Sample after revised according to suggestions"):
        st.info(revised)
