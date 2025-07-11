import re
from typing import Tuple

from ..config import PAYMENT_TYPES


def parse_message(text: str) -> Tuple[str, float, str, int]:
    """Parse 'Product - price - payment_type [xN]' messages."""
    parts = [p.strip() for p in text.split("-", maxsplit=2)]
    if len(parts) != 3:
        raise ValueError("Неверный формат. Используйте: Товар - цена - тип оплаты [xN]")

    product, price_str, payment_part = parts

    # Detect optional multiplier like x2 / х2 at the end
    multiplier_match = re.search(r"[xх]\s*(\d+)$", payment_part, flags=re.IGNORECASE)
    if multiplier_match:
        qty = int(multiplier_match.group(1))
        payment_type = payment_part[: multiplier_match.start()].strip()
    else:
        qty = 1
        payment_type = payment_part.strip()

    price = float(price_str.replace(",", ".").replace("₽", "").strip())

    if qty <= 0:
        raise ValueError("Количество должно быть > 0")

    payment_type = payment_type.lower()
    if payment_type not in PAYMENT_TYPES:
        raise ValueError(
            "Тип оплаты должен быть: " + ", ".join(PAYMENT_TYPES)
        )

    return product, price, payment_type, qty
