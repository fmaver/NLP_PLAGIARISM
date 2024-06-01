from pydantic import Field

from plagiarism.domain.schemas import CamelCaseModel


class SimilarSentences(CamelCaseModel):
    """
    Similar Sentences.
    """

    submitted_sentence: str = Field(
        description="The submitted sentence",
    )
    plagiarised_sentence: str = Field(
        description="The saved sentence that is similar to the submitted sentence.",
    )
    plagiarised_author: str = Field(
        description="The author of the plagiarised sentence.",
    )
    plagiarised_filename: str = Field(
        description="The filename of the plagiarised sentence.",
    )
    score: float = Field(
        description="The sentence's score for plagiarism.",
    )


class AssignmentStored(CamelCaseModel):
    """
    Assignment Stored Event.
    """

    author: str = Field(
        description="The author of the assignment.",
        examples=["Francisco Maver"],
    )
    name: str = Field(
        description="The assignment's name.",
        examples=["La larga cola"],
    )
    score: float = Field(
        description="The assignment's score for plagiarism.",
    )
    topic: str = Field(
        description="The assignment's topic.",
        examples=["Sistemas Emergentes"],
    )
    similar_sentences: list[SimilarSentences]
