class ExportProgress:
    def __init__(self, file_path : str, total_steps=100, current_step=0, time_elapsed=0, time_remaining=0):
        self.file_path = file_path
        self.total_steps = total_steps
        self.current_step = current_step
        self.time_elapsed = time_elapsed
        self.time_remaining = time_remaining