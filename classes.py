from typing import Any, Self
from enums import PartHeader
class EplanPart:
    def __init__(self, **kwargs):
        for attr in PartHeader:
            setattr(self, attr.name, kwargs.get(attr.value, None))
    
    def to_json(self) -> dict[str, Any]:
        return {attr.value: getattr(self, attr.name) for attr in PartHeader if type(getattr(self, attr.name)) in (str, int)}

class SAPPart:
    ItemName: str
    ItemCode: int
    FrgnName: str
    CardCode: str

    def __init__(self, **kwargs):
        if not (ItemCode := kwargs.get("ItemCode", None)):
            raise AttributeError("Part requires an ItemCode")
        try:
            self.ItemCode = int(ItemCode)
        except Exception as er:
            raise ValueError(f"Cannot convert {ItemCode} to int") from er

        for attr in ("ItemName", "FrgnName", "CardCode"):
            setattr(self, attr, kwargs.get(attr, None))

    def __str__(self, trunc=40):
        return f"{self.ItemCode}: {self.ItemName[:trunc]}{"..." if len(self.ItemName) > trunc else "".join((" " for _ in range(43 - len(self.ItemName))))} - {self.FrgnName[:trunc]}{"..." if len(self.FrgnName) > 43 else "".join((" " for _ in range(trunc - len(self.ItemName))))}"

    def __eq__(self, other: Self):
        return self.ItemCode == other.ItemCode

    def __gt__(self, other: Self):
        return self.ItemCode > other.ItemCode

    def __lt__(self, other: Self):
        return self.ItemCode < other.ItemCode

    def __hash__(self) -> int:
        return hash((self.ItemCode, self.ItemName, self.FrgnName, self.CardCode))

    def to_eplan_record(self) -> dict[PartHeader, str]:
        return {
            PartHeader.ERP_number: str(self.ItemCode),
            PartHeader.Supplier: self.CardCode,
        }