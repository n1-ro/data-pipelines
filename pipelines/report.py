"""Run summaries for each pipeline stage."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RunSummary:
    stage: str
    rows_read: int
    rows_kept: int
    rows_dropped: int = 0
    outputs: list[str] | None = None

    @property
    def drop_rate(self) -> float:
        if self.rows_read == 0:
            return 0.0
        return (self.rows_dropped / self.rows_read) * 100

    def render(self) -> str:
        lines = [
            f"[{self.stage}] read={self.rows_read} kept={self.rows_kept} "
            f"dropped={self.rows_dropped} ({self.drop_rate:.1f}%)"
        ]
        if self.outputs:
            lines.append("outputs:")
            lines.extend(f"  - {o}" for o in self.outputs)
        return "\n".join(lines)
