from pdfReader import readPDF, get_pdf_content
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import os
import re

os.environ["OPENAI_API_KEY"] = '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'

def get_first_number(s):
    match = re.search(r'\d+', s)
    if match:
        return int(match.group(0))
    else:
        return s


def create_suggestions(file):
    """
    Read the provided personal statement, and answer questions we provide

    return: list with answers
    """

    result = []
    llm = OpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo"
    )

    content = readPDF(file)
    Queries = ["Here is the personal statement that you need to read, and I need you to ask you some questions "
               "when you finish reading. " + content,
               "Does the essay effectively demonstrate that the author has experienced significant and relevant "
               "personal growth?  Provide suggestions being detailed. ",
               "Does the essay provide succinct, detailed, and compelling information about the author such that "
               "the reader is able to get a clear picture of the author as a well-rounded individual? Provide "
               "suggestions being detailed",
               "Does the essay is written in such a way that it consistently engages the reader and memorably "
               "stands out from other essays responding to the same prompt? Provide suggestions being detailed. ",
               "Are sentences forceful, clear, and logical, a variety of sentence structures are present, "
               "and diction is precise and expressive using college-level vocab? Provide suggestions being "
               "detailed. ",
               "Is tone and/or voice mature, consistent, and suitable to the prompt (less academic, more "
               "conversational, storytelling)? Provide suggestions being detailed. "]
    conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory())
    conversation.run(Queries[0])
    result.append(conversation.run(Queries[1]))
    result.append(conversation.run(Queries[2]))
    result.append(conversation.run(Queries[3]))
    result.append(conversation.run(Queries[4]))
    result.append(conversation.run(Queries[5]))

    llm_grade = OpenAI(model_name="text-davinci-003", max_tokens=1024)
    Grade_question = """Here is the personal statement that you need to read, and  I need you to grade it from 0 to 100.
    You should just answer the number of score without anything else""" + content
    answer = llm_grade(Grade_question)
    grade_num = get_first_number(answer)
    return result, grade_num


def get_the_final_evaluations(result):
    """
    Change the list of answer become a whole string answer

    return: str
    """

    answer = ""
    for i in result:
        answer += i
        answer += '\n'
    return answer


def evaluations_and_suggestions(file):
    """
    Extract the evaluations and suggestions from the answer provided by the AI

    return: str(evaluation) , str(suggestion)
    """
    chat = ChatOpenAI(temperature=0)
    result, grade = create_suggestions(file)
    answer = get_the_final_evaluations(result)
    batch_message = [
        [
            SystemMessage(content="You are a helpful assistant that can extract informations from paragraph. "
                                  "I need you to extract suggestions with their examples in the following paragraph."),
            HumanMessage(content=answer)
        ],

        [
            SystemMessage(content="You are a helpful assistant that can extract informations from paragraph. "
                                  "I need you to extract the feedbacks in the following paragraph."),
            HumanMessage(content=answer)
        ]
    ]
    need = chat.generate(batch_message)
    return need.generations[1][0].text, need.generations[0][0].text, grade
