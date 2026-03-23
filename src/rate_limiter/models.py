from dataclasses import dataclass

@dataclass
class RateLimitResult:
    allowed: bool
    remaining: int
    reset_after: int
