from document_loader import load_all_documents
from extraction_chain import extract_all_facts
from reasoning_chain import identify_killer
import json
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    """
    Stage 2: Document Forensics Pipeline
    NO embeddings - Pure reasoning chain
    """
    
    print("=" * 80)
    print("🔍 STAGE 2: DOCUMENT FORENSICS")
    print("=" * 80)
    
    # PHASE 1: Load all 12 documents
    print("\n📂 PHASE 1: Loading Documents...")
    print("-" * 80)
    
    docs_folder = "docs"  # Put your 12 files here
    documents = load_all_documents(docs_folder)
    
    print(f"\n✅ Loaded {len(documents)} documents")
    for doc_name in documents.keys():
        print(f"   📄 {doc_name}")
    
    # PHASE 2: Extract key facts from each document
    print("\n" + "=" * 80)
    print("🧠 PHASE 2: Extracting Facts...")
    print("-" * 80)
    
    extracted_facts = extract_all_facts(documents)
    
    # Save extraction results
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/extracted_facts.json", "w", encoding="utf-8") as f:
        json.dump(extracted_facts, f, indent=2)
    
    print("\n✅ Fact extraction complete!")
    print("💾 Saved to: outputs/extracted_facts.json")
    
    # PHASE 3: Final reasoning to identify killer
    print("\n" + "=" * 80)
    print("🎯 PHASE 3: Identifying Killer...")
    print("-" * 80)
    
    killer_analysis = identify_killer(extracted_facts)
    
    # Save final result
    with open("outputs/final_result.json", "w", encoding="utf-8") as f:
        json.dump(killer_analysis, f, indent=2)
    
    print("\n" + "=" * 80)
    print("🏆 FINAL RESULT")
    print("=" * 80)
    print(f"\n🔴 KILLER IDENTIFIED: {killer_analysis['killer']}")
    print(f"\n📋 REASONING:\n{killer_analysis['reasoning']}")
    print("\n💾 Saved to: outputs/final_result.json")
    print("\n" + "=" * 80)
    
    return killer_analysis

if __name__ == "__main__":
    main()
