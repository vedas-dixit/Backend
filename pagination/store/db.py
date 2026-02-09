from typing import List
from datetime import datetime, timedelta
from models.models import DataModel, Status

store_data: List[DataModel] = [
    DataModel(id=1, amount=250.0, status=Status.pending, created_at=datetime.now() - timedelta(days=3)),
    DataModel(id=2, amount=1200.0, status=Status.completed, created_at=datetime.now() - timedelta(days=2)),
    DataModel(id=3, amount=500.0, status=Status.failed, created_at=datetime.now() - timedelta(days=1)),
    DataModel(id=4, amount=800.0, status=Status.completed, created_at=datetime.now()),

    DataModel(id=5, amount=150.0, status=Status.pending, created_at=datetime.now() - timedelta(days=7)),
    DataModel(id=6, amount=2200.0, status=Status.completed, created_at=datetime.now() - timedelta(days=5)),
    DataModel(id=7, amount=75.5, status=Status.failed, created_at=datetime.now() - timedelta(days=10)),
    DataModel(id=8, amount=999.99, status=Status.pending, created_at=datetime.now() - timedelta(hours=12)),
    DataModel(id=9, amount=430.0, status=Status.completed, created_at=datetime.now() - timedelta(days=4)),
    DataModel(id=10, amount=60.0, status=Status.failed, created_at=datetime.now() - timedelta(days=8)),

    DataModel(id=11, amount=3100.0, status=Status.completed, created_at=datetime.now() - timedelta(days=15)),
    DataModel(id=12, amount=275.75, status=Status.pending, created_at=datetime.now() - timedelta(hours=3)),
    DataModel(id=13, amount=890.0, status=Status.failed, created_at=datetime.now() - timedelta(days=6)),
    DataModel(id=14, amount=1450.0, status=Status.completed, created_at=datetime.now() - timedelta(days=1)),
    DataModel(id=15, amount=20.0, status=Status.pending, created_at=datetime.now() - timedelta(days=20)),
]
