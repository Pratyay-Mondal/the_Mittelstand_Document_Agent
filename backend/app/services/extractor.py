import re
import logging
from typing import Optional, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from app.config import settings
from app.models.extraction import DocumentExtraction, ExtractionField

logger = logging.getLogger(__name__)

# A robust prompt for extracting Mittelstand specifics
EXTRACTION_PROMPT = """\
You are an expert at analyzing German business documents like invoices (Rechnungen), NDAs (Geheimhaltungsvereinbarungen), and supply contracts (Lieferverträge).

Carefully extract the following structured information from the document text below.
Rules:
- Only extract information that is EXPLICITLY stated in the document text.
- If a field is not present in the document, set its value to null.
- For confidence: set 1.0 if the value is clearly and unambiguously present, 0.8 if reasonably clear, 0.5 if uncertain.
- For source_page: set null if you cannot determine the page.

DOCUMENT TEXT:
{text}
"""


async def extract_structured_data(text: str) -> DocumentExtraction:
    """
    Given the full document text (or a reasonable prefix), extracts structured data
    using Ollama's structured output mode. Confidence scores are assigned via
    heuristics since local LLMs don't reliably self-report confidence.
    """
    llm = ChatOllama(
        base_url=settings.ollama_base_url,
        model=settings.ollama_chat_model,
        temperature=0.0,
    )

    prompt = ChatPromptTemplate.from_template(EXTRACTION_PROMPT)
    chain = prompt | llm.with_structured_output(DocumentExtraction)

    try:
        # Limit text to avoid blowing the context window
        result = await chain.ainvoke({"text": text[:4000]})
        return _assign_heuristics(result)

    except Exception as e:
        logger.error(f"Extraction failed: {e}", exc_info=True)
        # Return an empty DocumentExtraction as fallback
        return DocumentExtraction()


def _assign_heuristics(result: Any) -> DocumentExtraction:
    """
    Normalize the LLM output into a proper DocumentExtraction with
    ExtractionField objects and heuristic confidence scores.
    """
    # Convert to dict if needed
    if result is None:
        return DocumentExtraction()

    if isinstance(result, DocumentExtraction):
        raw = result.model_dump()
    elif isinstance(result, dict):
        raw = result
    elif hasattr(result, "dict"):
        raw = result.dict()
    else:
        logger.warning(f"Unexpected extraction result type: {type(result)}")
        return DocumentExtraction()

    final = DocumentExtraction()

    for key in [
        "invoice_number", "date", "total_amount", "vendor_name",
        "vendor_address", "customer_name", "tax_rate", "currency"
    ]:
        value = raw.get(key)
        
        # Helper to set an empty field that needs human review
        def set_empty():
            setattr(final, key, ExtractionField(value="", confidence=0.0, source_page=None))

        if value is None:
            set_empty()
            continue

        if isinstance(value, dict) and "value" in value:
            # Already in ExtractionField shape
            val = value.get("value")
            conf = value.get("confidence", 0.5)
            page = value.get("source_page")

            if val is None or (isinstance(val, str) and not val.strip()):
                set_empty()
                continue

            # Clamp confidence
            conf = max(0.0, min(1.0, float(conf)))
            setattr(final, key, ExtractionField(value=str(val), confidence=conf, source_page=page))

        elif isinstance(value, ExtractionField):
            if value.value is None or not str(value.value).strip():
                set_empty()
            else:
                setattr(final, key, value)

        elif isinstance(value, str) and value.strip():
            # Raw string value — assign heuristic confidence
            conf = _heuristic_confidence(key, value)
            setattr(final, key, ExtractionField(value=value, confidence=conf, source_page=1))

        elif value:
            val_str = str(value).strip()
            if val_str:
                conf = _heuristic_confidence(key, val_str)
                setattr(final, key, ExtractionField(value=val_str, confidence=conf, source_page=1))
            else:
                set_empty()
        else:
            set_empty()

    return final


def _heuristic_confidence(key: str, value: str) -> float:
    """Assign a heuristic confidence score based on field type and value patterns."""
    if len(value) <= 1:
        return 0.3

    # Date patterns (DD.MM.YYYY or similar)
    if key == "date":
        if re.match(r"\d{1,2}\.\d{1,2}\.\d{2,4}", value):
            return 0.95
        if re.match(r"\d{4}-\d{2}-\d{2}", value):
            return 0.95
        return 0.5

    # Amount patterns (numbers with comma/dot)
    if key in ("total_amount", "tax_rate"):
        if re.search(r"\d+[.,]\d+", value):
            return 0.9
        return 0.5

    # Currency (EUR, USD, etc.)
    if key == "currency":
        if value.upper() in ("EUR", "USD", "CHF", "GBP", "€", "$"):
            return 0.95
        return 0.6

    # Invoice number (alphanumeric pattern)
    if key == "invoice_number":
        if re.match(r"[A-Za-z0-9\-/]+", value) and len(value) >= 3:
            return 0.9
        return 0.6

    # Names and addresses — reasonable confidence if non-trivial
    if len(value) > 5:
        return 0.85
    return 0.6
