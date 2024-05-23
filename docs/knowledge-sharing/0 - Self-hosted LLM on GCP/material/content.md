<!--- file: docs/knowledge-sharing/0 - Self-hosted LLM on GCP/material/content.md --->
{% with pdf_file = "./genai-engineer-thailand-0-self-hosted-llm.pdf" %}

{% set solid_filepdf = '<i class="fas fa-file-pdf"></i>' %}
{% set empty_filepdf = '<i class="far fa-file-pdf"></i>' %}

## Example: Embedding a PDF file

<object data='{{ pdf_file }}' type="application/pdf">
    <embed src='{{ pdf_file }}' type="application/pdf" />
</object>

[PDF]({{ pdf_file }})

<a href="{{ pdf_file }}" class="image fit">{{ solid_filepdf }}</a>

{% endwith %}
