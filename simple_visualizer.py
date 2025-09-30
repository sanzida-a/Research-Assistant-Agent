import json
import os
from datetime import datetime
import matplotlib.pyplot as plt


class SimpleMemoryVisualizer:
    """
    Simplified visualizer for memory usage in Research Assistant Agent.
    Focuses on core metrics: memory operations and retrieval stats.
    """
    
    def __init__(self, log_file="memory_logs.json"):
        self.log_file = log_file
        self.logs = self._load_logs()
    
    def _load_logs(self):
        """Load existing logs or create new log file."""
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return {
            "sessions": [],
            "queries": [],
            "memory_ops": []
        }
    
    def _save_logs(self):
        """Save logs to file."""
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=2)
    
    def log_session(self, session_id: str, pdfs: list):
        """Log a new session."""
        self.logs["sessions"].append({
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "pdfs": pdfs,
            "query_count": 0
        })
        self._save_logs()
    
    def log_query(self, session_id: str, query: str, answer: str, 
                  short_term_used: bool, long_term_used: bool):
        """Log a query."""
        self.logs["queries"].append({
            "session_id": session_id,
            "query": query,
            "short_term_used": short_term_used,
            "long_term_used": long_term_used,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update session query count
        for session in self.logs["sessions"]:
            if session["session_id"] == session_id:
                session["query_count"] += 1
        
        self._save_logs()
    
    def log_memory_op(self, operation: str, memory_type: str, session_id: str):
        """Log memory operation (add/retrieve/clear)."""
        self.logs["memory_ops"].append({
            "operation": operation,  # "add", "retrieve", "clear"
            "memory_type": memory_type,  # "short_term", "long_term"
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        })
        self._save_logs()
    
    def visualize_memory_usage(self):
        """Create simple visualization of memory usage."""
        if not self.logs["memory_ops"]:
            print("No memory operations logged yet.")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('Memory Usage Analysis', fontsize=14, fontweight='bold')
        
        # 1. Memory Operations Count
        operations = {}
        for op in self.logs["memory_ops"]:
            key = f"{op['memory_type']}_{op['operation']}"
            operations[key] = operations.get(key, 0) + 1
        
        labels = list(operations.keys())
        values = list(operations.values())
        colors = ['#3498db' if 'short' in l else '#e74c3c' for l in labels]
        
        ax1.bar(range(len(labels)), values, color=colors, alpha=0.7)
        ax1.set_xticks(range(len(labels)))
        ax1.set_xticklabels(labels, rotation=45, ha='right')
        ax1.set_ylabel('Count')
        ax1.set_title('Memory Operations')
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. Memory Type Usage in Queries
        if self.logs["queries"]:
            st_only = sum(1 for q in self.logs["queries"] 
                         if q["short_term_used"] and not q["long_term_used"])
            lt_only = sum(1 for q in self.logs["queries"] 
                         if q["long_term_used"] and not q["short_term_used"])
            both = sum(1 for q in self.logs["queries"] 
                      if q["short_term_used"] and q["long_term_used"])
            
            sizes = [st_only, lt_only, both]
            labels = ['Short-Term\nOnly', 'Long-Term\nOnly', 'Both']
            colors = ['#3498db', '#e74c3c', '#9b59b6']
            
            ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                   startangle=90)
            ax2.set_title('Memory Usage in Queries')
        
        plt.tight_layout()
        plt.savefig('memory_usage.png', dpi=150, bbox_inches='tight')
        print("Visualization saved: memory_usage.png")
        plt.close()
    
    def generate_report(self):
        """Generate simple text report."""
        report = []
        report.append("="*60)
        report.append("MEMORY USAGE REPORT")
        report.append("="*60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Session Stats
        report.append("SESSION STATISTICS")
        report.append("-"*60)
        report.append(f"Total Sessions: {len(self.logs['sessions'])}")
        if self.logs["sessions"]:
            total_queries = sum(s["query_count"] for s in self.logs["sessions"])
            report.append(f"Total Queries: {total_queries}")
            report.append(f"Average Queries per Session: {total_queries/len(self.logs['sessions']):.1f}\n")
        
        # Memory Operations
        report.append("MEMORY OPERATIONS")
        report.append("-"*60)
        st_ops = [op for op in self.logs["memory_ops"] if op["memory_type"] == "short_term"]
        lt_ops = [op for op in self.logs["memory_ops"] if op["memory_type"] == "long_term"]
        
        report.append(f"Short-Term Operations: {len(st_ops)}")
        report.append(f"Long-Term Operations: {len(lt_ops)}\n")
        
        # Query Stats
        if self.logs["queries"]:
            report.append("QUERY STATISTICS")
            report.append("-"*60)
            st_used = sum(1 for q in self.logs["queries"] if q["short_term_used"])
            lt_used = sum(1 for q in self.logs["queries"] if q["long_term_used"])
            
            report.append(f"Queries using Short-Term Memory: {st_used} "
                         f"({st_used/len(self.logs['queries'])*100:.1f}%)")
            report.append(f"Queries using Long-Term Memory: {lt_used} "
                         f"({lt_used/len(self.logs['queries'])*100:.1f}%)\n")
        
        # Session Details
        if self.logs["sessions"]:
            report.append("SESSION DETAILS")
            report.append("-"*60)
            for i, session in enumerate(self.logs["sessions"], 1):
                report.append(f"\nSession {i}: {session['session_id']}")
                report.append(f"  Started: {session['start_time']}")
                report.append(f"  PDFs: {len(session['pdfs'])}")
                report.append(f"  Queries: {session['query_count']}")
        
        report.append("\n" + "="*60)
        
        # Save and print
        report_text = '\n'.join(report)
        with open('memory_report.txt', 'w') as f:
            f.write(report_text)
        
        print("Report saved: memory_report.txt\n")
        print(report_text)
    
    def create_visualizations(self):
        """Generate all visualizations and report."""
        print("\n" + "="*60)
        print("GENERATING VISUALIZATIONS")
        print("="*60 + "\n")
        
        self.visualize_memory_usage()
        self.generate_report()
        
        print("\n" + "="*60)
        print("ALL VISUALIZATIONS COMPLETED!")
        print("="*60)
        print("\nGenerated files:")
        print("  📊 memory_usage.png - Memory operations visualization")
        print("  📄 memory_report.txt - Statistics report")
        print("="*60 + "\n")