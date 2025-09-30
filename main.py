import os
from datetime import datetime
from dotenv import load_dotenv
from pdf_tools import process_pdfs
from memory_manager import MemoryManager
from agent import ResearchAssistantAgent
from simple_visualizer import SimpleMemoryVisualizer  # Changed import

load_dotenv()


def get_pdf_files_from_folder(folder_path="data"):
    """
    Automatically get all PDF files from a folder.
    """
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist!")
        return []
    
    pdf_files = [
        os.path.join(folder_path, f) 
        for f in os.listdir(folder_path) 
        if f.endswith('.pdf')
    ]
    
    if not pdf_files:
        print(f"Warning: No PDF files found in '{folder_path}' folder!")
    
    return pdf_files


def main():
    visualizer = SimpleMemoryVisualizer()  # Changed class name
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    pdf_files = get_pdf_files_from_folder("data")
    
    if not pdf_files:
        print("No PDF files to process. Exiting...")
        return
    
    print(f"\n{'='*60}")
    print(f"Starting Research Assistant with {len(pdf_files)} PDF(s)")
    print(f"{'='*60}")
    
    # Log session start
    visualizer.log_session(session_id=session_id, pdfs=pdf_files)  # Simplified params
    
    # Process all PDFs
    retriever, summary = process_pdfs(pdf_files)
    
    # Log long-term memory initialization
    visualizer.log_memory_op(  # Changed method name
        operation="add",
        memory_type="long_term",
        session_id=session_id
    )
    
    # Initialize memory manager and assistant
    memory_manager = MemoryManager()
    assistant = ResearchAssistantAgent(retriever, summary, memory_manager)

    print("\n" + "="*60)
    print("Research Assistant Ready! Type 'exit' to quit.")
    print("Type 'visualize' to generate memory visualizations.")
    print("="*60 + "\n")
    
    # Interactive loop
    while True:
        query = input("You: ")
        
        if query.lower() in ["exit", "quit"]:
            assistant.end_session()
            
            # Log session end
            visualizer.log_memory_op(  # Changed method name
                operation="clear",
                memory_type="short_term",
                session_id=session_id
            )
            
            print("\n" + "="*60)
            print("Session ended. Insights saved to long-term memory.")
            print("="*60)
            
            # Ask if user wants visualizations
            generate_viz = input("\nGenerate memory visualizations? (y/n): ")
            if generate_viz.lower() == 'y':
                visualizer.create_visualizations()  # Changed method name
            
            break
        
        if query.lower() == "visualize":
            print("\nGenerating visualizations...")
            visualizer.create_visualizations()  # Changed method name
            print()
            continue
        
        if not query.strip():
            continue
        
        # Get answer from assistant
        answer = assistant.ask(query)
        
        # Log the query (simplified params)
        short_term_context = memory_manager.get_short_term_context()
        visualizer.log_query(
            session_id=session_id,
            query=query,
            answer=answer,
            short_term_used=len(short_term_context) > 0,
            long_term_used=True
        )
        
        # Log memory operations
        visualizer.log_memory_op(  # Changed method name
            operation="add",
            memory_type="short_term",
            session_id=session_id
        )
        
        if len(short_term_context) > 0:
            visualizer.log_memory_op(  # Changed method name
                operation="retrieve",
                memory_type="short_term",
                session_id=session_id
            )
        
        visualizer.log_memory_op(  # Changed method name
            operation="retrieve",
            memory_type="long_term",
            session_id=session_id
        )
        
        # Display answer
        print(f"\nAssistant: {answer}\n")
        print("-" * 60 + "\n")


if __name__ == "__main__":
    main()