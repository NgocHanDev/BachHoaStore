from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Đặt mặc định cho Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BachHoaStore.settings')

app = Celery('BachHoaStore')

# Load config từ Django settings, namespace là CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tự động tìm và nạp các task từ ứng dụng trong dự án
app.autodiscover_tasks()

# Cấu hình định kỳ task
app.conf.beat_schedule = {
    'check-expired-products-every-0.005-minutes': {
        'task': 'product.tasks.check_and_update_expired_products',
        'schedule': 0.3,  # cứ mỗi 0.3 giây sẽ chạy task
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
