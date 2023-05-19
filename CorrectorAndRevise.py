from pdfReader import readPDF, get_pdf_content
from PersonalStatementSuggestion import evaluations_and_suggestions
from langchain.llms import OpenAI
from langchain.chains import LLMChain, SequentialChain
from langchain import PromptTemplate
import os

os.environ["OPENAI_API_KEY"] = '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'


def correct_and_revise(file):
    """
    Read the file, and return the paper after grammar checking, the paper after revising according to feedback and
    suggestions, feedback, and suggestions

    return: str, str, str, str
    """
    context = readPDF(file)
    evaluations, suggestions, grade = evaluations_and_suggestions(file)

    correct_template = """
    I want you to act as a mean grammar teach that check the grammar in the paragraph {context} and return the result.
    You should only give me the corrected paper without anything else.
    """
    correct_template_prompt = PromptTemplate(
        input_variables=["context"],
        template=correct_template
    )

    revise_template = """
    I want you to act as a experienced writer who can revise his {correct_context} perfect """ + """according to the 
    {} and {} provided by other experienced author. You should only give me the revised paper without anything else.
    """.format(evaluations, suggestions)
    revise_template_prompt = PromptTemplate(
        input_variables=["correct_context"],
        template=revise_template
    )

    llm = OpenAI(temperature=0.5, model_name="gpt-3.5-turbo")
    correct_chain = LLMChain(llm=llm, prompt=correct_template_prompt, verbose=True, output_key="correct_context")
    revise_chain = LLMChain(llm=llm, prompt=revise_template_prompt, verbose=True, output_key="final_context")

    sequential_chain = SequentialChain(
        chains = [correct_chain, revise_chain],
        input_variables=['context'],
        output_variables=["correct_context", "final_context"],
        verbose=True
    )

    reply = sequential_chain({'context': context})
    return grade, reply["correct_context"], reply["final_context"], evaluations, suggestions
