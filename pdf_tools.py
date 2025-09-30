from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from llm_config import get_llm, get_embeddings


def summarise_text(text: str, source_name: str = "") -> str:
    """
    Summarize text into key insights using LLM.
    """
    llm = get_llm()
    source_prefix = f"From {source_name}:\n" if source_name else ""
    prompt = f"Summarize the following document text into key insights:\n\n{text[:5000]}"
    response = llm.invoke([("user", prompt)])
    return source_prefix + response.content


def process_pdfs(pdf_paths: list[str], persist_directory="chroma_db"):
    """
    Reads multiple PDFs, chunks them, stores in a Chroma vector DB,
    and returns a retriever + overall summary.
    """
    all_docs = []
    summaries = []
    
    # Load all PDFs and create summaries
    for pdf_path in pdf_paths:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        
        # Add metadata to track which document each chunk comes from
        for doc in docs:
            doc.metadata['source_file'] = pdf_path
        
        all_docs.extend(docs)
        
        # Create summary for this specific PDF
        combined_text = "\n\n".join([doc.page_content for doc in docs])
        summary = summarise_text(combined_text[:5000], source_name=pdf_path)
        summaries.append(f"\n{'='*50}\nDocument: {pdf_path}\n{'='*50}\n{summary}")

    # Split all documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=100
    )
    docs_split = text_splitter.split_documents(all_docs)

    # Create vector store with all documents
    embeddings = get_embeddings()
    vectordb = Chroma.from_documents(
        documents=docs_split,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    retriever = vectordb.as_retriever(search_kwargs={"k": 6})  # Retrieve more docs

    # Combine all summaries
    combined_summary = "\n\n".join(summaries)
    
    print(f"\nProcessed {len(pdf_paths)} PDFs:")
    for pdf_path in pdf_paths:
        print(f"  - {pdf_path}")
    print(f"Total chunks created: {len(docs_split)}\n")
    
    return retriever, combined_summary