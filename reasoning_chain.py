from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)

# Final reasoning prompt
reasoning_prompt = PromptTemplate(
    input_variables=["consolidated_facts"],
    template="""You are solving a murder investigation for Dr. Ayan's death.

IMPORTANT CONTEXT FROM PREVIOUS INVESTIGATION:
- Dr. Ayan said: "If I'm dead before midnight, don't look for a killer. Look for a beneficiary."
- Tea service was mentioned as suspicious
- Ethics layer was disabled
- Administrator override IS-01 occurred
- Time manipulation detected
- Ministry involvement suspected
- Brother's record was recalculated

EXTRACTED FACTS FROM ALL DOCUMENTS:
{consolidated_facts}

TASK:
Based ONLY on the evidence above, identify the individual responsible for Dr. Ayan's death.

Consider:
1. Financial motives (beneficiaries)
2. System overrides and access
3. Timeline of events
4. Medical tampering
5. Who had the means, motive, and opportunity

Return your analysis in this JSON format:
{{
  "killer": "FULL NAME of the primary person responsible",
  "reasoning": "Clear explanation of why this person is responsible, citing specific evidence",
  "accomplices": ["list any accomplices if applicable"],
  "key_evidence": ["list the most damning pieces of evidence"]
}}

Return ONLY valid JSON.
"""
)

# Create chain
reasoning_chain = reasoning_prompt | llm


def identify_killer(extracted_facts):
    """
    Final reasoning to identify the killer
    """
    print("\n🧠 Running final analysis...")
    
    # Consolidate all facts into readable format
    consolidated = json.dumps(extracted_facts, indent=2)
    
    try:
        # Run reasoning
        response = reasoning_chain.invoke({
            "consolidated_facts": consolidated
        })
        
        # Extract content
        if hasattr(response, 'content'):
            result = response.content
        else:
            result = str(response)
        
        # Clean JSON
        result = result.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        result = result.strip()
        
        # Parse JSON
        analysis = json.loads(result)
        
        print("   ✅ Analysis complete")
        
        return analysis
        
    except json.JSONDecodeError as e:
        print(f"   ⚠️  JSON parsing error: {e}")
        print(f"   Raw response: {result[:500]}")
        return {
            "killer": "PARSING_ERROR",
            "reasoning": result,
            "error": str(e)
        }
        
    except Exception as e:
        print(f"   ❌ Reasoning failed: {e}")
        return {
            "killer": "ERROR",
            "error": str(e)
        }
