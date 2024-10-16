"""
Протестируйте классы из модуля homework/models
"""

import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 100)


@pytest.fixture()
def product_toy():
    return Product("toy", 500.50, "This is a toy", 5000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity_positive(self, product: Product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(product.quantity - 1) is True

    def test_product_check_quantity_more_than_available(self, product: Product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(product.quantity + 1) is False

    def test_product_buy_positive(self, product: Product):
        # TODO напишите проверки на метод buy
        amount = product.quantity // 2
        assert product.buy(amount)

    def test_product_buy_more_than_available(self, product):
        amount = product.quantity + 1
        with pytest.raises(ValueError):
            product.buy(amount)


@pytest.fixture(scope="function")
def cart() -> Cart:
    return Cart()


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    amount_added_product = 2
    amount_added_product_toy = 5

    def test_add_product(self, cart, product: Product):
        cart.add_product(product, TestCart.amount_added_product)
        assert cart.products[product] == TestCart.amount_added_product

    def test_add_double_product(self, cart: Cart, product: Product):
        cart.add_product(product, TestCart.amount_added_product)
        cart.add_product(product, TestCart.amount_added_product)
        assert cart.products[product] == TestCart.amount_added_product * 2

    def test_add_product_more_than_available(self, cart: Cart, product: Product):
        with pytest.raises(ValueError):
            cart.add_product(product, 2000)

    def test_add_zero_product(self, cart: Cart, product: Product):
        with pytest.raises(ValueError):
            cart.add_product(product, 0)

    def test_add_two_product(self, cart: Cart, product: Product, product_toy: Product):
        cart.add_product(product)
        cart.add_product(product_toy)
        assert cart.products[product] == 1 and cart.products[product_toy] == 1

    def test_remove_all_product(self, cart: Cart, product: Product):
        cart.add_product(product)
        cart.remove_product(product)
        assert product not in cart.products

    def test_remove_product_more_than_available(self, cart: Cart, product: Product):
        cart.add_product(product)
        remove_count = cart.products[product] + 1
        cart.remove_product(product, remove_count)
        assert product not in cart.products

    def test_remove_product(self, cart: Cart, product: Product):
        cart.add_product(product, TestCart.amount_added_product)
        initial_quantity = cart.products[product]
        remove_count = initial_quantity // 2
        cart.remove_product(product, remove_count)
        assert cart.products[product] == initial_quantity - remove_count

    def test_remove_another_product(self, cart: Cart, product: Product, product_toy: Product):
        with pytest.raises(KeyError):
            cart.add_product(product, TestCart.amount_added_product)
            initial_quantity = cart.products[product]
            remove_count = initial_quantity // 2
            cart.remove_product(product_toy, remove_count)

    def test_cler_cart(self, cart: Cart, product: Product, product_toy: Product):
        cart.add_product(product)
        cart.add_product(product_toy)
        cart.clear()
        assert not cart.products

    def test_cler_empty_cart(self, cart: Cart):
        cart.clear()
        assert not cart.products

    def test_get_total_prise(self, product, cart: Cart, product_toy: Product):
        cart.add_product(product, TestCart.amount_added_product)
        cart.add_product(product_toy, TestCart.amount_added_product_toy)
        total_price = cart.get_total_price()
        assert (
                       product.price * TestCart.amount_added_product + product_toy.price * TestCart.amount_added_product_toy) == total_price

    def test_buy(self, product: Product, cart: Cart):
        total_available_product = product.quantity
        cart.add_product(product, TestCart.amount_added_product)
        cart.buy()
        assert product.quantity == total_available_product - TestCart.amount_added_product
        assert not cart.products

    def test_buy_more_than_available(self, cart: Cart, product: Product):
        cart.add_product(product, product.quantity)
        cart.products[product] += 1
        with pytest.raises(ValueError):
            cart.buy()
