# Stage 2: Document Forensics

## 🎯 Competition-Safe Architecture
- ✅ NO embeddings
- ✅ NO vector databases
- ✅ Pure LLM reasoning chains
- ✅ Modular pipeline
- ✅ Clean evidence generation

## 📁 Folder Structure

```
Stage-2/
├── main.py                  # Main pipeline orchestrator
├── document_loader.py       # Universal file loader (txt/pdf/csv/json)
├── extraction_chain.py      # Fact extraction using LangChain
├── reasoning_chain.py       # Final killer identification
├── qa.py                    # Interactive Q&A system
├── requirements.txt         # Dependencies
├── .env                     # API keys (create this)
├── docs/                    # Place 12 documents here
│   ├── ATLAS_Admin_Logs.txt
│   ├── Financial_Ledger.csv
│   ├── Security_Access.json
│   ├── Medical_Log_Ayaan.pdf
│   └── ... (8 more files)
└── outputs/                 # Auto-generated results
    ├── extracted_facts.json
    └── final_result.json
```

## ⚙️ Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create .env File
```bash
# Create .env file in Stage-2/ folder
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Add Documents
- Create `docs/` folder
- Place all 12 documents inside

## 🚀 Usage

### Run Full Pipeline
```bash
python main.py
```

This will:
1. Load all 12 documents
2. Extract facts from each
3. Identify the killer
4. Save outputs to `outputs/` folder

### Interactive Q&A (For Stage Questions)
```bash
python qa.py
```

Then ask specific questions like:
- "Who had access to the ATLAS system on January 14?"
- "What financial transactions occurred on January 12?"
- "Who is listed as the beneficiary?"

## 📸 Evidence Generation

For competition submission:
1. Run `python main.py` for full pipeline
2. Take screenshot of console output (shows all phases)
3. For specific questions, use `qa.py` and screenshot each answer
4. All outputs saved to `outputs/` folder

## 🧠 How It Works

### Phase 1: Document Loading
- Handles TXT, PDF, CSV, JSON
- Converts everything to readable text
- No embeddings used

### Phase 2: Fact Extraction
- LangChain prompt template
- Groq LLM (llama-3.3-70b-versatile)
- Extracts structured facts from each doc
- Saves to `extracted_facts.json`

### Phase 3: Final Reasoning
- Consolidates all facts
- Applies investigation logic
- Identifies killer with evidence
- Saves to `final_result.json`

## ⚠️ Competition Rules Compliance

✅ **ALLOWED:**
- LangChain prompt templates
- Groq LLM
- Document loaders
- Text processing
- Pandas for CSV
- pypdf for PDF

❌ **NOT ALLOWED:**
- FAISS, Chroma, Pinecone
- Embeddings
- Vector databases
- RetrievalQA chains
- Hardcoded answers

## 📦 Submission Checklist

Before zipping:
- [ ] Remove `venv/` folder
- [ ] Remove `.env` file
- [ ] Keep only source code
- [ ] Keep `outputs/` folder with results
- [ ] Add screenshots
- [ ] Ensure ZIP < 8MB

## 🎯 Strategy Notes

From Stage 1 clues:
- "Look for a beneficiary, not a killer"
- Tea poisoning suspected
- Ethics layer disabled
- Override IS-01 detected
- Time manipulation
- Brother's record recalculated

Stage 2 likely reveals:
- Financial beneficiary
- Override authorization trail
- Medical tampering evidence
- Payment records
