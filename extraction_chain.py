from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq LLM - Using smaller model to save tokens
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # Faster, fewer tokens
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)

# Extraction prompt template
extraction_prompt = PromptTemplate(
    input_variables=["document_name", "document_content"],
    template="""You are a forensic AI investigator analyzing evidence for a murder case.

DOCUMENT NAME: {document_name}

DOCUMENT CONTENT:
{document_content}

Extract the following information in JSON format:
{{
  "key_people": ["list of people mentioned"],
  "suspicious_actions": ["list of suspicious activities"],
  "financial_anomalies": ["list of financial irregularities"],
  "timeline_events": ["list of events with times/dates"],
  "system_overrides": ["list of system/security overrides"],
  "medical_findings": ["list of medical observations"],
  "other_evidence": ["any other relevant evidence"]
}}

Return ONLY valid JSON. Be thorough but concise.
"""
)

# Create chain
extraction_chain = extraction_prompt | llm


def extract_all_facts(documents):
    """
    Extract key facts from all documents
    Returns: dict of {doc_name: extracted_facts}
    """
    all_facts = {}
    
    for doc_name, content in documents.items():
        print(f"\n🔍 Analyzing: {doc_name}")
        
        try:
            # Run extraction (reduced content to save tokens)
            response = extraction_chain.invoke({
                "document_name": doc_name,
                "document_content": content[:4000]  # Reduced from 8000 to 4000
            })
            
            # Extract content
            if hasattr(response, 'content'):
                result = response.content
            else:
                result = str(response)
            
            # Clean JSON (remove markdown code blocks if present)
            result = result.strip()
            if result.startswith("```json"):
                result = result[7:]
            if result.startswith("```"):
                result = result[3:]
            if result.endswith("```"):
                result = result[:-3]
            result = result.strip()
            
            # Parse JSON
            facts = json.loads(result)
            all_facts[doc_name] = facts
            
            print(f"   ✅ Extracted {len(facts)} fact categories")
            
        except json.JSONDecodeError as e:
            print(f"   ⚠️  JSON parsing error: {e}")
            print(f"   Raw response: {result[:200]}")
            all_facts[doc_name] = {"raw_response": result}
            
        except Exception as e:
            print(f"   ❌ Extraction failed: {e}")
            all_facts[doc_name] = {"error": str(e)}
    
    return all_facts
