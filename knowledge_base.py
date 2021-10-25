import streamlit as st
import pandas as pd
import time
import json
# import SessionState

# Set page config
st.set_page_config(page_title="QnA Knowledge Base", layout='centered',
                   page_icon='https://qnamaker.azureedge.net/Images/multi-turn.svg')

# Set page title text
st.title("""
QnA Bot Knowledge base
""")
st.caption("You can view and edit the details of your QnA Bot knowledge base here.")
st.write("")


try:
    # Load the knowledge base
    with open('knowledge_base.json') as file:
        data = json.load(file)
except:
    # Throw error
    st.error("Knowledge base (`knowledge_base.json`) can't be read.")
    exit()

st.write("#### Knowledge base information")
kb_name = st.text_input("Name", value=data['info']['name'], max_chars=60)
kb_version = st.text_input("Version", value=data['info']['version'])
kb_author = st.text_input("Author", value=data['info']['author'], max_chars=100)

if st.button("Save", key="s-kb-ginfo"):
    # Update the knowledge base general info
    data['info']['name'] = kb_name
    data['info']['version'] = kb_version
    data['info']['author'] = kb_author

    try:
        # Save the knowledge base
        with open('knowledge_base.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        with st.empty():
            st.success("Successfully updated general info of the knowledge base.")
            time.sleep(2.5)
            st.write("")
    except:
        # Throw error
        with st.empty():
            st.error("Something went wrong!")
            time.sleep(2.5)
            st.write("")


def parse(input_):
    if type(input_) is list:
        return "\n".join(input_)
    elif type(input_) is str:
        return input_.split("\n")


st.write("\n")
st.write("#### Edit questions and answers")
with st.expander("'I don't know' answers", expanded=True):
    st.write("When the QnA Bot can't predict a proper answer, one of these answers will be returned:")
    no_answer_data = st.text_area("Answers", value=parse(data['no_answer']), height=70)

    if st.button("Save", key="s-idont-know"):
        # Update the 'I don't know' answers in the knowledge base
        data['no_answer'] = parse(no_answer_data)

        try:
            # Save the knowledge base
            with open('knowledge_base.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            with st.empty():
                st.success("Successfully updated 'I don't know' answers of the knowledge base.")
                time.sleep(2.5)
                st.write("")
        except:
            # Throw error
            with st.empty():
                st.error("Something went wrong!")
                time.sleep(2.5)
                st.write("")

st.write("\n")
with st.expander("Questions and answers"):
    st.write("Edit question and answer pairs. Split items with a new line.")

    # Initialize section columns
    col1, col2 = st.columns(2)

    # Display the entries
    for i, item in enumerate(data['qna']):
        col1.text_area("Question " + str(i+1), value=parse(item['q']), height=50, key="q"+str(i+1))
        col2.text_area("Answer " + str(i+1), value=parse(item['a']), height=50, key="a"+str(i+1))

# # Set session state
# state = SessionState.get(num_displayed=5)
#
# # Config "Display more" button
# st.write("")
# if st.button('Display more'):
#     # Display the next five entries
#     for i in range(state.num_displayed, state.num_displayed+5):
#         q_data = data.iloc[i,0]
#         col1.text_area("Question " + str(i+1), value=q_data, height=120,
#                        max_chars=None, key="Q"+str(i+1))
#         a_data = data.iloc[i,1]
#         col2.text_area("Answer " + str(i+1), value=a_data, height=120,
#                        max_chars=None, key="A"+str(i+1))
#
#     state.num_displayed += 5
#
# st.write("1–" + str(state.num_displayed))