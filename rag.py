import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI

from rag_faiss import FAISSRetriever


load_dotenv()


@dataclass(frozen=True)
class Evidence:
    title: str
    url: str


class ScientificRetriever:
    MODEL = "gpt-5.6-luna"

    TRUSTED_DOMAINS = [
        "fao.org",
        "ipcc.ch",
        "cbd.int",
        "nature.com",
        "sciencedirect.com",
    ]

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing from .env")

        self.client = OpenAI(api_key=api_key)
        self.vector_db = FAISSRetriever()

    def retrieve(self, query: str):
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        vector_results = self.vector_db.search(query, top_k=3)

        response = self.client.responses.create(
            model=self.MODEL,
            tools=[
                {
                    "type": "web_search",
                    "filters": {
                        "allowed_domains": self.TRUSTED_DOMAINS
                    },
                }
            ],
            input=(
                "Research this environmental question using "
                "authoritative scientific sources.\n\n"
                f"Question: {query}\n\n"
                "Relevant knowledge retrieved from the local "
                "scientific vector database:\n"
                f"{vector_results}"
            ),
        )

        sources = []

        for item in response.output:
            if getattr(item, "type", None) != "message":
                continue

            for content in item.content:
                annotations = getattr(content, "annotations", [])

                for annotation in annotations:
                    if getattr(annotation, "type", None) == "url_citation":
                        sources.append(
                            Evidence(
                                title=annotation.title,
                                url=annotation.url,
                            )
                        )

        return {
            "research": response.output_text,
            "vector_results": vector_results,
            "sources": sources,
        }

    def retrieve_for_risk(self, risk: dict):
        query = (
            f"Scientific evidence for {risk['reason']} "
            f"Focus on the relationship between "
            f"{', '.join(risk['metrics'])}. "
            "Include measurable environmental effects and "
            "evidence relevant to practical interventions."
        )

        return self.retrieve(query)