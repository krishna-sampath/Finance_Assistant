from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

class LanguageAgent:
    def __init__(self):
        model_name = "google/flan-t5-small"
        pipe = pipeline(
            "text2text-generation",
            model=model_name,
            max_new_tokens=200,
            do_sample=False
        )
        llm = HuggingFacePipeline(pipeline=pipe)

        template_str = (
            "You are a helpful financial assistant. "
            "Based on the following information, provide a concise market brief in 3 bullet points, "
            "including key stock moves, earnings surprises, and risk insights:\n\n"  
            "{input_text}"
        )
        template = PromptTemplate(input_variables=["input_text"], template=template_str)
        self.chain = LLMChain(llm=llm, prompt=template)

    def generate_summary(self, input_text: str) -> str:
        # Pass the input_text into the chain correctly
        return self.chain.run({"input_text": input_text})