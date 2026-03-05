"""
Payments PRO (dataclasses + ABC + functions + logging)

Uruchom:
  python payments_pro.py
  python payments_pro.py --loglevel DEBUG
  python payments_pro.py --logfile payments.log --loglevel INFO
  python payments_pro.py --strict

Co pokazuje:
- ABC: PaymentMethod (interfejs)
- dataclasses: CardPayment / PayPalPayment / BankTransfer / CryptoPayment
- funkcje "proceduralne": create_payment(), process_payment(), process_batch()
- logowanie: konsola + opcjonalnie plik
- wyjątki domenowe + tryb strict/non-strict
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Tuple
import argparse
import logging
from logging.handlers import RotatingFileHandler


# =========================
# 1) Logging (PRO)
# =========================

def configure_logging(
    level: str = "INFO",
    logfile: Optional[str] = None,
    rotate: bool = True,
) -> logging.Logger:
    """
    Konfiguruje logowanie dla całej aplikacji.
    - level: DEBUG/INFO/WARNING/ERROR
    - logfile: jeśli podasz ścieżkę, logi idą także do pliku
    - rotate: jeśli logfile i rotate=True -> RotatingFileHandler
    """
    logger = logging.getLogger("payments")
    logger.setLevel(logging.DEBUG)  # logger zbiera wszystko, filtr robią handlery

    # Czyść handlery przy ponownym uruchomieniu w środowiskach notebook/IDE
    if logger.handlers:
        logger.handlers.clear()

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Konsola
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, level.upper(), logging.INFO))
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # Plik (opcjonalnie)
    if logfile:
        if rotate:
            fh = RotatingFileHandler(logfile, maxBytes=256_000, backupCount=3, encoding="utf-8")
        else:
            fh = logging.FileHandler(logfile, encoding="utf-8")

        fh.setLevel(getattr(logging, level.upper(), logging.INFO))
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    logger.debug("Logger configured | level=%s | logfile=%s | rotate=%s", level, logfile, rotate)
    return logger


# =========================
# 2) Errors (domena)
# =========================

class PaymentError(Exception):
    """Bazowy wyjątek domenowy płatności."""


class ValidationError(PaymentError):
    """Błąd walidacji danych wejściowych."""


class AuthorizationError(PaymentError):
    """Błąd autoryzacji (symulacja)."""


class ProcessingError(PaymentError):
    """Błąd przetwarzania (np. awaria bramki)."""


# =========================
# 3) Model domenowy
# =========================

@dataclass(frozen=True)
class PaymentReceipt:
    """Wynik płatności: to, co chcemy zwrócić na koniec pipeline."""
    payment_id: str
    method: str
    amount: float
    currency: str
    status: str
    created_at: str
    details: Dict[str, Any] = field(default_factory=dict)


class PaymentMethod(ABC):
    """
    Interfejs płatności. Każda metoda:
    - waliduje dane (validate)
    - wykonuje płatność (pay) i zwraca PaymentReceipt
    """

    @property
    @abstractmethod
    def method_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def pay(self, *, logger: logging.Logger) -> PaymentReceipt:
        raise NotImplementedError


# =========================
# 4) Metody płatności (dataclasses)
# =========================

def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def _make_payment_id(prefix: str) -> str:
    # prosta, czytelna "unikalność" (w realu: UUID)
    return f"{prefix}-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"


@dataclass
class CardPayment(PaymentMethod):
    card_number: str
    holder: str
    amount: float
    currency: str = "PLN"
    cvv: str = "000"

    @property
    def method_name(self) -> str:
        return "card"

    def validate(self) -> None:
        if not self.holder.strip():
            raise ValidationError("Card holder cannot be empty")
        digits = "".join(ch for ch in self.card_number if ch.isdigit())
        if len(digits) < 12:
            raise ValidationError("Card number seems too short")
        if self.amount <= 0:
            raise ValidationError("Amount must be positive")
        if len(self.cvv) not in (3, 4) or not self.cvv.isdigit():
            raise ValidationError("CVV must be 3 or 4 digits")

    def pay(self, *, logger: logging.Logger) -> PaymentReceipt:
        self.validate()
        last4 = "".join(ch for ch in self.card_number if ch.isdigit())[-4:]
        logger.info("Authorizing CARD payment | holder=%s | last4=%s | amount=%.2f %s",
                    self.holder, last4, self.amount, self.currency)

        # Symulacja autoryzacji
        if last4 == "0000":
            raise AuthorizationError("Card authorization declined (simulated)")

        payment_id = _make_payment_id("CARD")
        logger.info("Captured CARD payment | payment_id=%s", payment_id)

        return PaymentReceipt(
            payment_id=payment_id,
            method=self.method_name,
            amount=self.amount,
            currency=self.currency,
            status="CAPTURED",
            created_at=_now_iso(),
            details={"holder": self.holder, "last4": last4},
        )


@dataclass
class PayPalPayment(PaymentMethod):
    email: str
    amount: float
    currency: str = "PLN"

    @property
    def method_name(self) -> str:
        return "paypal"

    def validate(self) -> None:
        if "@" not in self.email or not self.email.strip():
            raise ValidationError("PayPal email is invalid")
        if self.amount <= 0:
            raise ValidationError("Amount must be positive")

    def pay(self, *, logger: logging.Logger) -> PaymentReceipt:
        self.validate()
        logger.info("Processing PAYPAL payment | email=%s | amount=%.2f %s",
                    self.email, self.amount, self.currency)

        # Symulacja awarii bramki
        if self.email.lower().endswith("@down.example"):
            raise ProcessingError("PayPal gateway timeout (simulated)")

        payment_id = _make_payment_id("PAYPAL")
        logger.info("Completed PAYPAL payment | payment_id=%s", payment_id)

        return PaymentReceipt(
            payment_id=payment_id,
            method=self.method_name,
            amount=self.amount,
            currency=self.currency,
            status="COMPLETED",
            created_at=_now_iso(),
            details={"email": self.email},
        )


@dataclass
class BankTransfer(PaymentMethod):
    account_number: str
    amount: float
    currency: str = "PLN"
    title: str = "Invoice payment"

    @property
    def method_name(self) -> str:
        return "bank_transfer"

    def validate(self) -> None:
        cleaned = self.account_number.replace(" ", "")
        if len(cleaned) < 10:
            raise ValidationError("Account number seems too short")
        if self.amount <= 0:
            raise ValidationError("Amount must be positive")
        if not self.title.strip():
            raise ValidationError("Transfer title cannot be empty")

    def pay(self, *, logger: logging.Logger) -> PaymentReceipt:
        self.validate()
        logger.info("Scheduling BANK TRANSFER | account=%s | amount=%.2f %s | title=%s",
                    self.account_number, self.amount, self.currency, self.title)

        payment_id = _make_payment_id("BANK")
        # przelew często jest asynchroniczny, więc dajemy status PENDING
        logger.info("BANK TRANSFER scheduled | payment_id=%s | status=PENDING", payment_id)

        return PaymentReceipt(
            payment_id=payment_id,
            method=self.method_name,
            amount=self.amount,
            currency=self.currency,
            status="PENDING",
            created_at=_now_iso(),
            details={"account": self.account_number, "title": self.title},
        )


@dataclass
class CryptoPayment(PaymentMethod):
    wallet: str
    amount: float
    currency: str = "USDT"
    network: str = "TRC20"

    @property
    def method_name(self) -> str:
        return "crypto"

    def validate(self) -> None:
        if len(self.wallet.strip()) < 8:
            raise ValidationError("Wallet address seems too short")
        if self.amount <= 0:
            raise ValidationError("Amount must be positive")
        if not self.network.strip():
            raise ValidationError("Network cannot be empty")

    def pay(self, *, logger: logging.Logger) -> PaymentReceipt:
        self.validate()
        logger.info("Broadcasting CRYPTO payment | network=%s | wallet=%s | amount=%.2f %s",
                    self.network, self.wallet[:6] + "..." + self.wallet[-4:], self.amount, self.currency)

        payment_id = _make_payment_id("CRYPTO")
        # crypto: często status CONFIRMED po czasie, tu symulujemy natychmiast
        logger.info("CRYPTO payment confirmed | payment_id=%s", payment_id)

        return PaymentReceipt(
            payment_id=payment_id,
            method=self.method_name,
            amount=self.amount,
            currency=self.currency,
            status="CONFIRMED",
            created_at=_now_iso(),
            details={"wallet": self.wallet, "network": self.network},
        )


# =========================
# 5) Factory + funkcje "pipeline"
# =========================

PAYMENT_FACTORY = {
    "card": CardPayment,
    "paypal": PayPalPayment,
    "bank_transfer": BankTransfer,
    "crypto": CryptoPayment,
}


def create_payment(payload: Dict[str, Any]) -> PaymentMethod:
    """
    Funkcja-fabryka: bierze słownik i tworzy obiekt PaymentMethod.
    payload musi mieć klucz "type".
    """
    if "type" not in payload:
        raise ValidationError("Missing 'type' in payload")

    payment_type = str(payload["type"]).strip().lower()
    cls = PAYMENT_FACTORY.get(payment_type)
    if not cls:
        raise ValidationError(f"Unknown payment type: {payment_type!r}")

    data = {k: v for k, v in payload.items() if k != "type"}
    try:
        return cls(**data)  # dataclass constructor
    except TypeError as e:
        # np. brak wymaganego pola lub literówka w nazwie klucza
        raise ValidationError(f"Invalid payload for {payment_type}: {e}") from e


def process_payment(payment: PaymentMethod, *, logger: logging.Logger) -> PaymentReceipt:
    """
    Funkcja "proceduralna", która działa z dowolnym PaymentMethod (polimorfizm).
    """
    logger.debug("process_payment() | method=%s | object=%r", payment.method_name, payment)
    receipt = payment.pay(logger=logger)
    logger.info("Payment done | method=%s | payment_id=%s | status=%s",
                receipt.method, receipt.payment_id, receipt.status)
    return receipt


def process_batch(
    payloads: Iterable[Dict[str, Any]],
    *,
    logger: logging.Logger,
    strict: bool = False
) -> Tuple[List[PaymentReceipt], List[Dict[str, Any]]]:
    """
    Przetwarza wiele płatności:
    - strict=False: błędy są logowane i lecimy dalej
    - strict=True: pierwszy błąd przerywa cały batch

    Zwraca:
    - receipts: lista poprawnie przetworzonych płatności
    - errors: lista słowników z informacją o błędzie + payload
    """
    receipts: List[PaymentReceipt] = []
    errors: List[Dict[str, Any]] = []

    for idx, payload in enumerate(payloads, start=1):
        try:
            logger.debug("Batch item %d | payload=%s", idx, payload)
            pm = create_payment(payload)
            receipt = process_payment(pm, logger=logger)
            receipts.append(receipt)

        except PaymentError as e:
            msg = f"Skipping item {idx}: {e}"
            if strict:
                logger.error("%s | payload=%s", msg, payload)
                raise
            logger.warning("%s | payload=%s", msg, payload)
            errors.append({"index": idx, "error": str(e), "payload": payload})

    logger.info("Batch finished | ok=%d | errors=%d | strict=%s", len(receipts), len(errors), strict)
    return receipts, errors


# =========================
# 6) CLI + demo
# =========================

def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Payments PRO demo (dataclasses + ABC + logging)")
    p.add_argument("--loglevel", default="INFO", help="DEBUG/INFO/WARNING/ERROR")
    p.add_argument("--logfile", default=None, help="Optional: path to log file")
    p.add_argument("--no-rotate", action="store_true", help="Disable log rotation for logfile")
    p.add_argument("--strict", action="store_true", help="Stop on first error")
    return p


def demo_payloads() -> List[Dict[str, Any]]:
    # Celowo mieszamy dobre i błędne przypadki
    return [
        {"type": "card", "card_number": "1234 5678 1234 5678", "holder": "Anna", "amount": 250.0, "currency": "PLN", "cvv": "123"},
        {"type": "paypal", "email": "ewa@example.com", "amount": 120.0, "currency": "PLN"},
        {"type": "bank_transfer", "account_number": "PL 12 3456 7890 1234", "amount": 500.0, "title": "FV/03/2026"},
        {"type": "crypto", "wallet": "TQ9sXk1nM2pQw8Zz7aBCdEFG", "amount": 99.0, "currency": "USDT", "network": "TRC20"},

        # Błędy:
        {"type": "card", "card_number": "0000 0000 0000 0000", "holder": "Jan", "amount": 10.0, "currency": "PLN", "cvv": "123"},  # autoryzacja odrzucona
        {"type": "paypal", "email": "bad-email", "amount": 50.0},  # walidacja
        {"type": "bank_transfer", "account_number": "PL 1", "amount": 200.0, "title": "OK"},  # walidacja
        {"type": "crypto", "wallet": "short", "amount": 1.0, "currency": "USDT", "network": "TRC20"},  # walidacja
        {"type": "unknown", "x": 1},  # nieznany typ
    ]


def main() -> int:
    args = build_arg_parser().parse_args()
    logger = configure_logging(
        level=args.loglevel,
        logfile=args.logfile,
        rotate=(not args.no_rotate),
    )

    logger.info("Start Payments PRO | strict=%s", args.strict)

    payloads = demo_payloads()
    try:
        receipts, errors = process_batch(payloads, logger=logger, strict=args.strict)
    except PaymentError as e:
        logger.error("Batch aborted due to error: %s", e)
        return 1

    
    logger.info("=== SUMMARY ===")
    for r in receipts:
        logger.info("OK | %s | %s | %.2f %s | %s", r.payment_id, r.method, r.amount, r.currency, r.status)

    for err in errors:
        logger.info("ERR | idx=%s | %s", err["index"], err["error"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
