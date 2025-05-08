from services.mercadoPago_service import PaymentStrategy


class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def process_payment(self, data):
        return self._strategy.create_payment(data)