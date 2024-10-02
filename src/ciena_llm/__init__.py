import logging
from typing import Optional, List
from tqdm import tqdm

import dotenv

# pylint: disable=wrong-import-position
dotenv.load_dotenv()

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
import pydantic
from seqia.article import Article
from seqia.article.loader import ArticleLoader
from seqia.location import Location
from seqia.utils.output import write_to_csv

from ciena_llm.llm_response import LLMResponseLocationList
from ciena_llm.config.loader import ConfigLoader
from ciena_llm.prompt_template_manager import PromptTemplateManager
from ciena_llm.response import parse_response_bool
from ciena_llm.response_validator import ResponseValidatorLocations


class ClimateImpactExtractor:
    def __init__(self, override_config_path=None):
        self.config = ConfigLoader(override_config_path=override_config_path).config

        self.article_loader = ArticleLoader()

        # Initialize the Ollama model
        self.llm_name = self.config["llm"]["name"]
        self.llm_temperature = self.config["llm"]["temperature"]
        self.llm_context_length = self.config["llm"]["context_length"]
        self.llm = OllamaLLM(
            model=self.llm_name,
            temperature=self.llm_temperature,
            num_ctx=self.llm_context_length,  # TODO why was this commented out?
        )

        self.ptm = PromptTemplateManager()

        self.binary_prompt_template = self.ptm.get_prompt_template(
            self.config["prompt"]["binary"]
        )
        self.impact_prompt_template = self.ptm.get_prompt_template(
            self.config["prompt"]["impact"]
        )
        self.location_prompt_template = self.ptm.get_prompt_template(
            self.config["prompt"]["location"]
        )

        self.parser_location = JsonOutputParser(pydantic_object=LLMResponseLocationList)
        self.answer_extractor_location_template = self.ptm.get_prompt_template(
            self.config["prompt"]["answer_extractor"],
            format_instructions=self.parser_location.get_format_instructions(),
        )

        # Load impacts from configuration
        self.impacts = self.config["impacts"]

    def __call__(self, dataset_path: str) -> List[Article]:
        articles = self.article_loader(dataset_path)

        for article in tqdm(articles, desc="Extracting locations from articles"):
            article = self.extract_locations(article)

            # DEBUG
            # if article:
            #     logging.debug("Article %s:\n%s", article.filename, article)

        return articles

    def check_context_lenght(self, text: str, prompt_template: PromptTemplate):
        num_tokens_text = self.llm.get_num_tokens(text)
        full_prompt = prompt_template.invoke({"text": text})
        num_tokens_full_prompt = self.llm.get_num_tokens(full_prompt.to_string())

        logging.debug("Num. tokens (text): %s", num_tokens_text)
        logging.debug("Num. tokens (full prompt): %s", num_tokens_full_prompt)
        if num_tokens_full_prompt > self.llm_context_length:
            logging.warning("Full prompt exceeds context length.")

    def extract_impacts(self, article: Article) -> Optional[Article]:
        text = article.get_headline_and_body(separator=".")

        # DEBUG
        full_prompt = self.binary_prompt_template.invoke({"text": text})
        logging.debug("Full Prompt:\n %s", full_prompt)

        self.check_context_lenght(text, self.binary_prompt_template)

        binary_chain = self.binary_prompt_template | self.llm
        binary_response = binary_chain.invoke({"text": text})
        binary_response = parse_response_bool(binary_response)

        article.drought = binary_response

        if not binary_response:
            return

        for impact in self.impacts:
            impact_chain = self.impact_prompt_template | self.llm
            impact_response = impact_chain.invoke(
                {"text": text, "impact": impact["name"]}
            )
            impact_response = parse_response_bool(impact_response)

            if impact_response:
                article.impacts_aggregated.append(impact["tag"])

        return article

    def extract_locations(self, article: Article) -> Optional[Article]:
        text = article.get_headline_and_body(separator=". ")

        # self.check_context_lenght(text, self.location_prompt_template)

        def log_io(stage: str, data: str):
            logging.debug("%s: %s", stage, data)
            return data

        location_chain = (
            self.location_prompt_template
            | (lambda output: log_io("Input to LLM (Location)", output))
            | self.llm
            | (lambda output: log_io("Output from LLM (Location)", output))
            | self.answer_extractor_location_template
            | (lambda output: log_io("Input to LLM (Answer Extractor)", output))
            | self.llm
            | (lambda output: log_io("Output from LLM (Answer Extractor)", output))
            | self.parser_location
        )

        try:
            location_response = location_chain.invoke({"text": text})
        except pydantic.ValidationError as e:
            logging.error("Failed to parse response: %s", e)
            raise e

        logging.debug("Location Response: %s", location_response)

        location_response: LLMResponseLocationList = LLMResponseLocationList.parse_obj(
            location_response
        )

        # TODO Validate location responses are in article text

        locations = []
        for location in location_response.locations:
            locations.append(
                Location(
                    name=location.location_name,
                    type=location.location_type,
                    start=None,
                    end=None,
                )
            )
        article.locations_aggregated = locations

        return article

    def write_excluded_problematic_articles_to_csv(self, file: str):
        self.article_loader.write_excluded_problematic_articles_to_csv(file)

    def write_summary_to_csv(self, articles: List[Article], file: str):
        write_to_csv(articles, file, self.config["output"]["summary"], "article")

    def write_location_to_csv(self, articles: List[Article], file: str):
        write_to_csv(
            articles,
            file,
            self.config["output"]["location_article"],
            "location_article",
        )
