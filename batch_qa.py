"""
Batch Question Processor
Answer multiple questions at once and save all evidence
"""

from document_loader import load_all_documents
from qa import answer_question
import os
import json
from datetime import datetime

def process_batch_questions(questions_file="questions.txt"):
    """
    Process multiple questions from a file
    Generates evidence for all questions
    """
    
    print("=" * 80)
    print("📋 BATCH QUESTION PROCESSOR")
    print("=" * 80)
    
    # Load documents
    print("\n📂 Loading documents...")
    documents = load_all_documents("docs")
    print(f"✅ Loaded {len(documents)} documents\n")
    
    # Load questions
    if not os.path.exists(questions_file):
        print(f"❌ Error: {questions_file} not found!")
        print("\nCreate a file called 'questions.txt' with one question per line:")
        print("Example:")
        print("  Who accessed the system on January 14?")
        print("  What financial transactions occurred?")
        print("  Who is the beneficiary?")
        return
    
    with open(questions_file, "r", encoding="utf-8") as f:
        questions = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    if not questions:
        print(f"❌ No questions found in {questions_file}")
        return
    
    print(f"📝 Found {len(questions)} questions\n")
    print("=" * 80)
    
    # Process each question
    results = []
    
    for i, question in enumerate(questions, 1):
        print(f"\n❓ Question {i}/{len(questions)}: {question}")
        print("🔄 Processing...")
        
        answer = answer_question(documents, question)
        
        print("\n" + "-" * 80)
        print(f"🎯 Answer:")
        print("-" * 80)
        print(answer)
        print("-" * 80)
        
        # Save individual answer
        os.makedirs("outputs", exist_ok=True)
        with open(f"outputs/answer_{i}.txt", "w", encoding="utf-8") as f:
            f.write(f"QUESTION {i}:\n{question}\n\n")
            f.write(f"ANSWER:\n{answer}\n")
        
        print(f"💾 Saved: outputs/answer_{i}.txt")
        
        results.append({
            "question_number": i,
            "question": question,
            "answer": answer
        })
    
    # Save all results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = f"outputs/all_answers_{timestamp}.json"
    
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": timestamp,
            "total_questions": len(questions),
            "results": results
        }, f, indent=2)
    
    print("\n" + "=" * 80)
    print("✅ BATCH PROCESSING COMPLETE")
    print("=" * 80)
    print(f"\n📊 Processed {len(questions)} questions")
    print(f"💾 Summary saved: {summary_file}")
    print(f"📁 Individual answers: outputs/answer_1.txt through outputs/answer_{len(questions)}.txt")
    print("\n🎯 Next steps:")
    print("   1. Review all answers in outputs/ folder")
    print("   2. Take screenshots of console output")
    print("   3. Include relevant screenshots in your ZIP submission")
    print("=" * 80)


def create_sample_questions():
    """
    Create a sample questions.txt file
    """
    sample = """# Sample questions for Stage 2
What condition did Dr. Ayaan suffer from?
Who returned the tea tray at 10:14?
When was the study accessed?
What caused the blackout?
Which entity funded supplement purchases?
What intermediary was used?
Who was removed from the will?
What crime did ATLAS detect?
What system state followed the override?
Who can authorize override?
"""
    
    with open("questions.txt", "w", encoding="utf-8") as f:
        f.write(sample)
    
    print("✅ Created sample questions.txt file")
    print("   Edit this file with your actual competition questions")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--create-sample":
        create_sample_questions()
    else:
        process_batch_questions()
