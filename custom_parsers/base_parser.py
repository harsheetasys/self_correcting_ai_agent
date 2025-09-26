"""Base classes and types for parser implementations.

Each custom bank parser must inherit from :class:`BaseParser` and
implement the :meth:`parse` method.  Parsers take a path to a PDF
statement and return a :class:`pandas.DataFrame` matching the
expected CSV schema.

The goal of this contract is to provide a simple and uniform
interface for the agent and test harness to consume, irrespective
of bank‑specific quirks.
"""

from abc import ABC, abstractmethod
import pandas as pd

class BaseParser(ABC):
    @abstractmethod
    def parse(self, pdf_path: str) -> pd.DataFrame:
        """Return a DataFrame that exactly matches the expected CSV schema."""
        ...
