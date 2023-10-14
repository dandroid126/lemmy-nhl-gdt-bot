from dataclasses import dataclass


@dataclass
class DailyThreadsRecord:
    post_id: int
    date: str
    is_featured: bool
