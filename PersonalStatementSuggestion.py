from pdfReader import readPDF
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
import os
import re

os.environ["OPENAI_API_KEY"] = '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'


def get_numerator_from_fraction(string):
    """
    This helper function is used to get the score from the answer created by LLM

    return: int
    """
    pattern = r'(\d+)'  # Regular expression pattern to match the numerator
    match = re.search(pattern, string)
    if match:
        numerator = int(match.group(1))  # Extract the numerator from the matched group
        return numerator
    return -1  # Return None if no fraction is found

def CreateSuggestion(file):
    """
    This function is used to generate the answer list with the data type Document

    In this function, we will combine 6 questions with the essay to ask OpenAI's LLM to get the feedback
    After generating answers, we will collect them into a list to prepare for the summarization.

    return: List[Document]
    """
    content = readPDF(file)

    Question_List = [content]
    prompt_List = []
    answer_List_Doc = []
    prompt_List.append("Does the essay effectively demonstrate that the author has experienced significant and relevant "
                         "personal growth?  Provide suggestions being detailed. ")
    prompt_List.append("Does the essay provide succinct, detailed, and compelling information about the author such that "
                         "the reader is able to get a clear picture of the author as a well-rounded individual? Provide "
                         "suggestions being detailed")
    prompt_List.append("Does the essay is written in such a way that it consistently engages the reader and memorably "
                         "stands out from other essays responding to the same prompt? Provide suggestions being detailed. ")
    prompt_List.append("Are sentences forceful, clear, and logical, a variety of sentence structures are present, "
                         "and diction is precise and expressive using college-level vocab? Provide suggestions being "
                         "detailed. ")
    prompt_List.append("Is tone and/or voice mature, consistent, and suitable to the prompt (less academic, more "
                         "conversational, storytelling)? Provide suggestions being detailed. ")
    prompt_List.append("How many points out of 100 will you give this personal essay? You should just give me the score")

    for i in prompt_List:
        Question_List.append(i)
        llm = OpenAI(model_name="text-davinci-003", max_tokens=3100)
        answer = llm(Question_List)
        answer_List_Doc.append(Document(page_content=answer))
        Question_List = [content]

    return answer_List_Doc


def summary_answer(answer_List):
    """
    This function is used to summarize the answer to get a final suggestion

    return: str
    """
    llm = OpenAI(model_name="text-davinci-003", max_tokens=1500)
    chain = load_summarize_chain(llm, chain_type="refine", verbose=True)
    result = chain.run(answer_List[:-1])
    return result


def suggestions(file):
    """
    This function is used to generate the final suggestions that needs to be displayed in the html

    return: str
    """
    answer_doc = CreateSuggestion(file)
    score = int(get_numerator_from_fraction(answer_doc[-1].page_content))
    suggestion = summary_answer(answer_doc)
    final = "The score of this personal statement is {}".format(score) + suggestion
    return final


