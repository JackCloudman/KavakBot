from typing import List

from openai.types.beta.threads import FileCitationAnnotation


def remove_file_annotations(text: str, annotations: List[FileCitationAnnotation]) -> str:
    for annotation in annotations:
        text = text.replace(annotation.text, "")
    return text
