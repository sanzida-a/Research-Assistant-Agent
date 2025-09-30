# 📚 Research Assistant AI Agent with Memory

A LangGraph-based AI agent that processes PDFs, answers queries using **retrieval-augmented generation (RAG)**, and leverages **dual memory systems** (short-term + long-term).  

This project is designed as a research companion, enabling cross-document analysis, persistent knowledge storage, and interactive Q&A with memory.

---

## 🚀 Key Features

- **LangGraph Agent**  
  Stateful agent with retrieval and answer nodes.
- **PDF Processing Pipeline**  
  Extracts, chunks, embeds, and summarizes documents.
- **Dual Memory System**  
  - Short-term: Session-based conversational memory  
  - Long-term: Persistent knowledge in ChromaDB  
- **Cross-Session Persistence**  
  Recall knowledge across multiple runs.  
- **Multi-Document Support**  
  Handle unlimited PDFs with cross-referencing.  
- **Visualization Tools**  
  Generate memory usage charts, retrieval flow diagrams, and timelines.  

---

## 🧠 Agent Architecture

```
User Query → Retrieve Node → Answer Node → END → Store in Short-Term Memory
```

- **Retrieve Node**: Finds top-k document chunks via ChromaDB search.  
- **Answer Node**: Combines:
  - Retrieved chunks  
  - Long-term summaries  
  - Short-term Q&A context  
  Then sends context to LLM for response generation.  

---

## 📊 Memory Design

| Aspect            | Short-Term Memory             | Long-Term Memory          |
|-------------------|-------------------------------|---------------------------|
| Storage           | Python list in RAM            | ChromaDB vector database  |
| Persistence       | Cleared after session         | Saved permanently on disk |
| Content           | Session Q&A pairs             | Document chunks & summaries|
| Purpose           | Maintain conversation flow    | Persistent knowledge       |
| Access            | Direct list lookup            | Semantic vector search     |

**Integration Strategy**:  
The agent combines both memories to generate contextual and comprehensive answers.  

---

## 📦 Project Structure

```
Research_Assistant_Agent/
├── agent.py              # LangGraph agent
├── llm_config.py         # LLM + embeddings config
├── memory_manager.py     # Short-term & long-term memory
├── pdf_tools.py          # PDF loader, chunker, embedder
├── memory_visualizer.py  # Charts, flow diagrams, reports
├── main.py               # Entry point
├── requirements.txt
├── data/                 # Place your PDFs here
│   ├── document1.pdf
│   ├── document2.pdf
└── .env                  # GitHub API key
```

---

## ⚙️ Installation & Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/research-assistant-agent.git
   cd research-assistant-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**  
   Create `.env` in the project root:
   ```env
   GITHUB_API_KEY=your_github_api_key_here
   ```

4. **Add your PDFs**  
   Place files inside the `data/` folder.

5. **Run the app**
   ```bash
   python main.py
   ```

---

## 📈 Visualization System

Type `visualize` during a session to generate:  
- `memory_usage.png` – Memory operation statistics  
- `retrieval_flow.png` – Retrieval process flowchart  
- `session_timeline.png` – Timeline of queries vs memory usage  
- `memory_report.txt` – Detailed text report  

At session end, typing `exit` prompts auto-generation of visualizations.

---

## 🧪 Example Queries & Agent Responses

- **Overview**:  
  _“What are the main topics covered in these documents?”_  
  → Returns topics from machine learning & deep learning PDFs.  

- **Follow-up**:  
  _“Can you explain more about CNNs?”_  
  → Uses short-term memory to expand contextually.  

- **Cross-session**:  
  _“What were the key points about neural networks?”_  
  → Retrieves from long-term memory even after restart.  

---

## 🎯 Main Findings Across All Documents

1. **Machine Learning Basics**  
   - Supervised & unsupervised algorithms  
   - Decision trees, random forests  
   - Model evaluation (accuracy, precision, recall)  

2. **Deep Learning Insights**  
   - Neural networks (CNNs, RNNs)  
   - Training techniques (backpropagation, optimizers)  
   - Applications in computer vision & NLP  

3. **Best Practices**  
   - Dataset recommendations (MNIST → CIFAR → ImageNet)  
   - Transfer learning & augmentation  
   - Optimization methods (SGD, Adam, learning rate scheduling)  

4. **Memory Utility**  
   - Short-term memory supports conversational flow  
   - Long-term memory enables persistence across sessions  
   - Integration ensures rich, contextual answers  

