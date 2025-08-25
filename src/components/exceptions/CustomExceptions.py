class ResumeExtractionException(Exception):
    """A custom exception for resume extraction error condition."""
    def __init__(self, message="Could not extract the resume!"):
        self.message = message
        super().__init__(self.message)

class ResumeScoringException(Exception):
    """A custom exception for resume scoring error condition."""
    def __init__(self, message="Could not calculate score for the components in the resume!"):
        self.message = message
        super().__init__(self.message)

class JDExtractionException(Exception):
    """A custom exception for resume scoring error condition."""
    def __init__(self, message="Could not extract the job description!"):
        self.message = message
        super().__init__(self.message)