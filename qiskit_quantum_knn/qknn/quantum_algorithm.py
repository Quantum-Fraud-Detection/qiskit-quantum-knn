"""
This module implements the abstract base class for algorithm modules.

To create add-on algorithm modules subclass the QuantumAlgorithm
class in this module.
Doing so requires that the required algorithm interface is implemented.
"""

from abc import ABC, abstractmethod
from typing import Union, Dict, Optional
from qiskit.providers import Backend
from qiskit.utils import QuantumInstance


class QuantumAlgorithm(ABC):
    """
    Base class for Quantum Algorithms.

    This method should initialize the module and
    use an exception if a component of the module is available.
    """

    @abstractmethod
    def __init__(self,
                 quantum_instance: Optional[Union[QuantumInstance, Backend]]) -> None:
        self._quantum_instance = None
        if quantum_instance:
            self.quantum_instance = quantum_instance

    def run(self,
            quantum_instance: Optional[Union[QuantumInstance, Backend]] = None,
            **kwargs) -> Dict:
        """Execute the algorithm with selected backend.

        Args:
            quantum_instance: the experimental setting.
            kwargs (dict): kwargs
        Returns:
            dict: results of an algorithm.
        Raises:
        ValueError: If a quantum instance or backend has not been provided
        """
        if quantum_instance is None and self.quantum_instance is None:
            raise ValueError("Quantum device or backend "
                             "is needed since you are running quantum algorithm.")
        if isinstance(quantum_instance, Backend):
            self.set_backend(quantum_instance, **kwargs)
        else:
            if quantum_instance is not None:
                self.quantum_instance = quantum_instance

        return self._run()

    @abstractmethod
    def _run(self) -> Dict:
        raise NotImplementedError()

    @property
    def quantum_instance(self) -> Union[None, QuantumInstance]:
        """ Returns quantum instance. """
        return self._quantum_instance

    @quantum_instance.setter
    def quantum_instance(self, quantum_instance: Union[QuantumInstance, Backend]) -> None:
        """ Sets quantum instance. """
        if isinstance(quantum_instance, Backend):
            quantum_instance = QuantumInstance(quantum_instance)
        self._quantum_instance = quantum_instance

    def set_backend(self, backend: Backend, **kwargs) -> None:
        """ Sets backend with configuration. """
        self.quantum_instance = QuantumInstance(backend)
        self.quantum_instance.set_config(**kwargs)

    @property
    def backend(self) -> Backend:
        """ Returns backend. """
        return self.quantum_instance.backend

    @backend.setter
    def backend(self, backend: Backend):
        """ Sets backend without additional configuration. """
        self.set_backend(backend)
