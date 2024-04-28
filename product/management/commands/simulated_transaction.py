import logging
from django.core.management.base import BaseCommand
import threading
from product.models import Product
from django.db import transaction

logger = logging.getLogger(__name__)

PRODUCT_NAME = "Test_transaction"
INITIAL_STOCK = 10
NUM_THREADS = 2
QUANTITY_PER_THREAD = 1


class Command(BaseCommand):
    help = "제품 재고와의 경쟁 상태를 시뮬레이션하고 트랜잭션을 사용하여 해결합니다."

    def handle(self, *args, **options):
        product = Product.objects.create(name=PRODUCT_NAME, stock=INITIAL_STOCK)
        initial_stock = product.stock

        threads = []
        for i in range(NUM_THREADS):
            t = threading.Thread(
                target=self.purchase, args=(product.id, QUANTITY_PER_THREAD)
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        product.refresh_from_db()
        final_stock = product.stock
        self.stdout.write(self.style.SUCCESS(f"초기 수량: {initial_stock}"))
        self.stdout.write(self.style.SUCCESS(f"최종 수량: {final_stock}"))

    @classmethod
    def purchase(cls, product_id, quantity):
        try:
            with transaction.atomic():
                product = Product.objects.select_for_update().get(pk=product_id)

                if product.stock < quantity:
                    raise ValueError("재고가 충분하지 않습니다.")

                logger.info(f"제품: {product.name} 수량: {quantity} 개 구매중")
                product.stock -= quantity
                product.save()
        except Exception as e:
            logger.error(f"구매 중 오류가 발생했습니다.: {e}")
