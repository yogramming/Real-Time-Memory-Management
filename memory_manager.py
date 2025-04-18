class MemoryManager:
    def __init__(self, total_pages=256):
        self.total_pages = total_pages
        self.pages = [None] * total_pages  # None = free, otherwise process ID
        self.processes = {}

    def allocate_memory(self, process_id, num_pages):
        """Allocates memory and returns a success message."""
        free_blocks = [i for i, p in enumerate(self.pages) if p is None]
        if len(free_blocks) < num_pages:
            return f"❌ Not enough memory for {num_pages} pages!"

        allocated_pages = free_blocks[:num_pages]
        for page in allocated_pages:
            self.pages[page] = process_id
        self.processes[process_id] = allocated_pages

        return f"✅ Process {process_id} allocated {num_pages} pages!"

    def deallocate_memory(self, process_id):
        """Frees memory and returns a success message."""
        if process_id in self.processes:
            for page in self.processes.pop(process_id):
                self.pages[page] = None
            return f"🔄 Process {process_id} memory deallocated!"
        return f"⚠ Error: Process {process_id} not found!"

    def get_memory_state(self):
        """Returns a user-friendly view of memory state."""
        return [p if p is not None else "Free" for p in self.pages]
