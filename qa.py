from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from document_loader import load_all_documents
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

# Q&A prompt template
qa_prompt = PromptTemplate(
    input_variables=["all_documents", "question"],
    template="""You are a forensic document analyst answering questions about a murder investigation.

ALL DOCUMENTS:
{all_documents}

QUESTION: {question}

INSTRUCTIONS:
- Answer based ONLY on information in the documents above
- Be specific and cite which document contains the information
- If the answer is not in the documents, say "Information not found in documents"
- Keep answers concise and factual
- Include relevant dates, times, names, and numbers

ANSWER:
"""
)

# Create chain
qa_chain = qa_prompt | llm


def answer_question(documents, question):
    """
    Answer a specific question about the documents
    """
    # Consolidate all documents
    all_docs = []
    for doc_name, content in documents.items():
        all_docs.append(f"=== {doc_name} ===\n{content[:4000]}\n")  # Limit each doc
    
    consolidated = "\n\n".join(all_docs)
    
    try:
        # Run Q&A
        response = qa_chain.invoke({
            "all_documents": consolidated,
            "question": question
        })
        
        # Extract content
        if hasattr(response, 'content'):
            answer = response.content
        else:
            answer = str(response)
        
        return answer.strip()
        
    except Exception as e:
        return f"ERROR: {str(e)}"


def main():
    """
    Interactive Q&A system
    """
    print("=" * 80)
    print("🔍 STAGE 2: DOCUMENT Q&A SYSTEM")
    print("=" * 80)
    
    # Load documents
    print("\n📂 Loading documents...")
    docs_folder = "docs"
    
    if not os.path.exists(docs_folder):
        print(f"❌ Error: '{docs_folder}/' folder not found!")
        print("   Create 'docs/' folder and add your 12 documents")
        return
    
    documents = load_all_documents(docs_folder)
    print(f"✅ Loaded {len(documents)} documents\n")
    
    # Interactive loop
    print("=" * 80)
    print("Ask questions about the documents. Type 'quit' to exit.")
    print("=" * 80)
    print()
    
    question_number = 1
    
    while True:
        # Get question
        question = input(f"❓ Question {question_number}: ").strip()
        
        # Exit condition
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Exiting Q&A system. Goodbye!")
            break
        
        # Skip empty
        if not question:
            print("⚠️  Please enter a question.\n")
            continue
        
        # Answer
        print("\n🔄 Processing...\n")
        answer = answer_question(documents, question)
        
        print("=" * 80)
        print(f"🎯 ANSWER #{question_number}:")
        print("=" * 80)
        print(answer)
        print("=" * 80)
        print()
        
        # Save to file for evidence
        os.makedirs("outputs", exist_ok=True)
        with open(f"outputs/question_{question_number}.txt", "w", encoding="utf-8") as f:
            f.write(f"QUESTION: {question}\n\n")
            f.write(f"ANSWER:\n{answer}\n")
        
        print(f"💾 Saved to: outputs/question_{question_number}.txt\n")
        
        question_number += 1


# CLI mode for single questions
def cli_mode():
    """
    Command-line mode for single questions
    Usage: python qa.py "Who accessed the system?"
    """
    import sys
    
    if len(sys.argv) < 2:
        main()  # Interactive mode
        return
    
    question = " ".join(sys.argv[1:])
    
    print("=" * 80)
    print("🔍 STAGE 2: DOCUMENT Q&A")
    print("=" * 80)
    
    # Load documents
    print("\n📂 Loading documents...")
    documents = load_all_documents("docs")
    print(f"✅ Loaded {len(documents)} documents\n")
    
    # Answer
    print(f"❓ Question: {question}\n")
    print("🔄 Processing...\n")
    answer = answer_question(documents, question)
    
    print("=" * 80)
    print("🎯 ANSWER:")
    print("=" * 80)
    print(answer)
    print("=" * 80)


if __name__ == "__main__":
    cli_mode()
