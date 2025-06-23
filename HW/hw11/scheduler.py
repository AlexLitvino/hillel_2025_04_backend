from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import queue
import random
import threading
import time

OrderRequestBody = tuple[str, datetime]


storage = {
    "users": [],
    "dishes": [
        {
            "id": 1,
            "name": "Salad",
            "value": 1099,
            "restaurant": "Silpo",
        },
        {
            "id": 2,
            "name": "Soda",
            "value": 199,
            "restaurant": "Silpo",
        },
        {
            "id": 3,
            "name": "Pizza",
            "value": 599,
            "restaurant": "Kvadrat",
        },
    ],
    # ...
}


class Scheduler:
    def __init__(self):
        self.orders: queue.Queue[OrderRequestBody] = queue.Queue()
        self.shipping_orders: queue.Queue[OrderRequestBody] = queue.Queue()

    def process_orders(self) -> None:
        print("SCHEDULER PROCESSING...")

        while True:
            order = self.orders.get(True)

            time_to_wait = order[1] - datetime.now()

            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)
                time.sleep(0.5)
            else:
                self.shipping_orders.put(order)
                print(f"\n\t{order[0]} SENT TO SHIPPING DEPARTMENT")

    def delivery_orders(self):
        print("SCHEDULER SHIPPING...")

        while True:
            order = self.shipping_orders.get(True)

            def _get_delivery_provider():
                """Returns less loaded delivery provider"""
                uklon_active_shipping = Uklon.NUMBER_OF_ACTIVE_SHIPPING
                uber_active_shipping = Uber.NUMBER_OF_ACTIVE_SHIPPING
                #print(f"Uklon = {uklon_active_shipping}, Uber = {uber_active_shipping}")

                if uklon_active_shipping < uber_active_shipping:
                    return Uklon()
                elif uber_active_shipping < uklon_active_shipping:
                    return Uber()
                else:
                    return random.choice([Uklon, Uber])()

            delivery_provider: DeliveryProvider = _get_delivery_provider()
            delivery_thread = threading.Thread(target=delivery_provider.ship, args=(order,))
            delivery_thread.start()


    def add_order(self, order: OrderRequestBody) -> None:
        self.orders.put(order)
        print(f"\n\t{order[0]} ADDED FOR PROCESSING")


class DeliveryProvider(ABC):
    NUMBER_OF_ACTIVE_SHIPPING = 0

    @abstractmethod
    def ship(self, order: OrderRequestBody):
        pass


class Uklon(DeliveryProvider):

    def ship(self, order: OrderRequestBody):
        Uklon.NUMBER_OF_ACTIVE_SHIPPING += 1
        time.sleep(5)
        print(f"\tOrder {order[0]} is delivered by {self.__class__.__name__}")
        Uklon.NUMBER_OF_ACTIVE_SHIPPING -= 1


class Uber(DeliveryProvider):

    def ship(self, order: OrderRequestBody):
        Uber.NUMBER_OF_ACTIVE_SHIPPING += 1
        time.sleep(3)
        print(f"\tOrder {order[0]} is delivered by {self.__class__.__name__}")
        Uber.NUMBER_OF_ACTIVE_SHIPPING -= 1


def main():
    scheduler = Scheduler()
    thread = threading.Thread(target=scheduler.process_orders, daemon=True)
    delivery_thread = threading.Thread(target=scheduler.delivery_orders, daemon=True)
    thread.start()
    delivery_thread.start()

    # user input:
    # A 5 (in 5 days)
    # B 3 (in 3 days)
    while True:
        order_details = input("Enter order details: ")
        data = order_details.split(" ")
        order_name = data[0]
        delay = datetime.now() + timedelta(seconds=int(data[1]))
        scheduler.add_order(order=(order_name, delay))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        raise SystemExit(0)
