from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from src.mobj_types.mobj_type import MobjType
from src.mobjs.mobj import Mobj
from src.scopes.scope import Scope


class InferenceRule(ABC):
    """
    Abstract class for inference rules, that is, rules that allow us to
    create new valid statements from existing ones.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def types_are_valid(self, *mobj_types: MobjType) -> bool:
        """
        Returns True if the types of the mobjs are valid for this rule.
        """

    @abstractmethod
    def is_applicable(self, scope: Scope, *args: Mobj) -> bool:
        """
        Returns True if the rule can be applied.
        """

    @abstractmethod
    def infer(self, scope: Scope, *args: Mobj):
        """
        Applies the rule.
        """
