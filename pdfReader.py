from langchain.document_loaders import PyPDFLoader
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
import os

os.environ["OPENAI_API_KEY"] = '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'
loader = PyPDFLoader("2_personalStatementSample_PersonalStatements.pdf")
pages = loader.load_and_split()
content = "Here is a personal statement used for applying for a college. " + pages[0].page_content

Question_List = [content]
Question_List_copy = [content]
prompt_List = []
answer_List = []
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
prompt_List.append("How many points out of 100 will you give this personal essay?")

for i in prompt_List:
    Question_List.append(i)
    llm = OpenAI(model_name="text-davinci-003", max_tokens=3100)
    answer = llm(Question_List)
    answer_List.append(Document(page_content=answer))
    Question_List = Question_List_copy

llm = OpenAI(model_name="text-davinci-003", max_tokens=1500)
chain = load_summarize_chain(llm, chain_type="refine", verbose=True)
result = chain.run(answer_List)
print(result)

