"""Your test suite. Write smoke, regression, and slow tests here.

Every test MUST carry exactly one marker (@pytest.mark.smoke / regression /
slow) and name its author in the docstring, e.g.:

    @pytest.mark.smoke
    def test_login_works():
        '''Author: <name>. Smoke test for login.'''

Run:  pytest            (all)     pytest -m smoke     pytest -m regression
"""
import pytest
from bookstore_app import Users, Catalog, Cart


@pytest.mark.smoke
def test_example_register():
    """Author: <example>. Smoke: a new user can register."""
    assert Users().register("newuser", "password123") is True


# ---- YOUR SMOKE TESTS (at least 5) ----

@pytest.mark.smoke
def test_register_then_login_works():
    """Author: Kaung. Smoke: a new user can register and then log in."""
    users = Users()
    assert users.register("alice", "secret123") is True
    assert users.login("alice", "secret123") is True


@pytest.mark.smoke
def test_login_rejects_wrong_password():
    """Author: Kaung. Smoke: login must refuse a wrong password."""
    users = Users()
    users.register("bob", "secret123")
    assert users.login("bob", "notmypassword") is False


@pytest.mark.smoke
def test_add_product_is_saved():
    """Author: Kaung. Smoke: a product added to the catalog is stored."""
    catalog = Catalog()
    catalog.add_product(1, "Python", 30)
    assert 1 in catalog.products
    assert catalog.products[1]["title"] == "Python"
    assert catalog.search("Python") == [1]


@pytest.mark.smoke
def test_add_to_cart_puts_item_in_cart():
    """Author: Kaung. Smoke: a known product reaches the cart."""
    catalog = Catalog()
    catalog.add_product(1, "Python", 30)
    cart = Cart(catalog)
    assert cart.add(1) is True
    assert cart.items == [1]


@pytest.mark.smoke
def test_checkout_with_items_creates_order():
    """Author: Kaung. Smoke: checkout of a non-empty cart gives an order."""
    catalog = Catalog()
    catalog.add_product(1, "Python", 30)
    catalog.add_product(2, "Testing", 20)
    cart = Cart(catalog)
    cart.add(1)
    cart.add(2)
    order = cart.checkout()
    assert order == [1, 2]
    assert cart.items == []
    assert cart.history() == [[1, 2]]


@pytest.mark.regression
def test_login_accepts_password_with_symbols():
    """Author: Kaung. Regression for Users.login().

    Wrong behaviour: login() removes all non-letter/number characters from
    the typed password, so "pass@123" becomes "pass123" and never matches.
    Correct behaviour: login() compares the exact password that was stored.
    """
    users = Users()
    users.register("carol", "pass@123")
    assert users.login("carol", "pass@123") is True


@pytest.mark.regression
def test_cart_total_includes_last_item():
    """Author: Kaung. Regression for Cart.total().

    Wrong behaviour: the loop stops one item early, so the last item is not
    counted (10 + 20 + 5 returns 30).
    Correct behaviour: total() adds every item in the cart (35).
    """
    catalog = Catalog()
    catalog.add_product(1, "A", 10)
    catalog.add_product(2, "B", 20)
    catalog.add_product(3, "C", 5)
    cart = Cart(catalog)
    cart.add(1)
    cart.add(2)
    cart.add(3)
    assert cart.total() == 35


@pytest.mark.regression
def test_checkout_empty_cart_returns_none():
    """Author: Kaung. Regression for Cart.checkout().

    Wrong behaviour: checkout of an empty cart returns [] and saves an
    empty order in the history.
    Correct behaviour (from the docstring): return None and save no order.
    """
    cart = Cart(Catalog())
    assert cart.checkout() is None
    assert cart.history() == []


@pytest.mark.regression
def test_import_products_returns_exact_count():
    """Author: Kaung. Regression for Cart.import_products().

    Wrong behaviour: importing 2 products returns 3 (count + 1).
    Correct behaviour: return how many products were imported (2).
    """
    cart = Cart(Catalog())
    assert cart.import_products([(1, "A", 5), (2, "B", 6)]) == 2


@pytest.mark.slow
def test_bulk_import_of_200000_products_then_search():
    """Author: Kaung. Slow: bulk import of a very large product list.

    Slow because import_products() loops over 200,000 products one by one,
    and then 30 searches each check all 200,000 titles.
    """
    catalog = Catalog()
    cart = Cart(catalog)
    big_list = [(i, f"Book {i}", 10) for i in range(200000)]
    cart.import_products(big_list)
    # check the real data, not the return value
    assert len(catalog.products) == 200000
    assert catalog.products[199999]["title"] == "Book 199999"
    for k in range(30):
        assert k in catalog.search(f"Book {k}")

@pytest.mark.slow
def test_many_searches_on_a_large_catalog():
    """Author: Kaung. Slow: many searches over a large catalog.

    Slow because search() checks every product title each time, so
    200 searches over 100,000 products means about 20 million checks.
    """
    catalog = Catalog()
    for i in range(100000):
        catalog.add_product(i, f"Book {i}", 10)
    for k in range(200):
        results = catalog.search(f"Book {k}")
        assert k in results