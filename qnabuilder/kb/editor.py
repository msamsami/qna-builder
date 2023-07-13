import json
import sys
import time
from typing import Union

import streamlit as st


def parse(input: Union[list, str]) -> Union[str, list]:
    if type(input) is list:
        return "\n".join(input)
    elif type(input) is str:
        return input.split("\n")


# Set page config
st.set_page_config(
    page_title="QnA Knowledge Base Editor",
    layout="centered",
    page_icon="https://qnamaker.azureedge.net/Images/multi-turn.svg",
)

# Set page title text
st.title(
    """
QnA Knowledge Base Editor
"""
)
st.caption("You can view and edit the details of your QnA Bot knowledge base here.")
st.write("")

kb_dir = sys.argv[1]  # Get knowledge base directory from the command line argument
try:
    # Load the knowledge base
    with open(kb_dir) as file:
        data = json.load(file)
except:
    st.error(f"Knowledge base (`{kb_dir}`) can't be read.")
    exit()

st.write("#### Knowledge base information")
st.text_input("File path", value=kb_dir, max_chars=60, disabled=True)
kb_name = st.text_input("Name", value=data["info"]["name"], max_chars=60)
kb_version = st.text_input("Version", value=data["info"]["version"])
kb_author = st.text_input("Author", value=data["info"]["author"], max_chars=100)

if st.button("Save", key="s-kb-ginfo"):
    data["info"]["name"] = kb_name
    data["info"]["version"] = kb_version
    data["info"]["author"] = kb_author

    try:
        # Save the knowledge base
        with open(kb_dir, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        with st.empty():
            st.success("Successfully updated general info of the knowledge base.")
            time.sleep(2.5)
            st.write("")
    except:
        with st.empty():
            st.error("Something went wrong!")
            time.sleep(2.5)
            st.write("")


st.write("\n")
st.write("#### Edit questions and answers")
with st.expander("'I don't know' answers", expanded=True):
    st.write(
        "When the QnA Bot can't predict a proper answer, one of the following answers will be returned. "
        "Split the items with a new line."
    )
    no_answer_data = st.text_area(
        "Answers", value=parse(data["idk_answers"]), height=70
    )

    if st.button("Save", key="s-idont-know"):
        # Update the 'I don't know' answers in the knowledge base
        data["idk_answers"] = parse(no_answer_data)

        try:
            # Save the knowledge base
            with open(kb_dir, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            with st.empty():
                st.success(
                    "Successfully updated 'I don't know' answers of the knowledge base."
                )
                time.sleep(2.5)
                st.write("")
        except:
            with st.empty():
                st.error("Something went wrong!")
                time.sleep(2.5)
                st.write("")


questions = [None] * len(data["qna"])
answers = [None] * len(data["qna"])
st.write("\n")

with st.expander("Questions and answers"):
    st.write("Edit question and answer pairs. Split the items with a new line.")

    # Display the entries
    for i, item in enumerate(data["qna"]):
        col1, col2 = st.columns(2)
        questions[i] = col1.text_area(
            "Question " + str(i + 1),
            value=parse(item["q"]),
            height=50,
            key="q" + str(i + 1),
        )
        answers[i] = col2.text_area(
            "Answer " + str(i + 1),
            value=parse(item["a"]),
            height=50,
            key="a" + str(i + 1),
        )

        if st.button("Save", key=f"save{i}"):
            # Update the i-th question-answer pair in the knowledge base
            data["qna"][i]["q"] = parse(questions[i])
            data["qna"][i]["a"] = parse(answers[i])

            # Save the knowledge base
            with open(kb_dir, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
