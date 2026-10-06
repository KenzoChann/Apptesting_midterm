# FINDINGS.md -- Bug-hunt log

Group: Trial run   Members: Kaung

---

## Bug 1
- **Suspected:** `Users.login()` in `users.py`. The line `cleaned = "".join(ch for ch in password if ch.isalnum())` removes every symbol from the typed password, but `register()` stores the password unchanged.
- **Tried:** `register("carol", "pass@123")`, then `login("carol", "pass@123")`. Test: `test_login_accepts_password_with_symbols`.
- **Observed:** `AssertionError: assert False is True`. The correct password was refused.
- **Expected:** `True`. The docstring says login succeeds when "the password matches", and the same password was typed.
- **Fixed:** Removed the `cleaned` line. Now `stored == password`.
- **Author:** Kaung

---

## Bug 2
- **Suspected:** `Cart.total()` in `cart.py`. The loop is `range(len(self.items) - 1)`, which looks one step too short.
- **Tried:** Three items with prices 10, 20 and 5, then `total()`. Test: `test_cart_total_includes_last_item`.
- **Observed:** `assert 30 == 35`. The last item (5) was not counted.
- **Expected:** `35`. The docstring says the total of "everything currently in the cart".
- **Fixed:** The loop now goes over every item: `for pid in self.items`.
- **Author:** Kaung

---

## Bug 3
- **Suspected:** `Cart.checkout()` in `cart.py`. The docstring says it returns None for an empty cart, but the code has no check for that.
- **Tried:** `Cart(Catalog()).checkout()` on an empty cart. Test: `test_checkout_empty_cart_returns_none`.
- **Observed:** `assert [] is None`. It returned an empty list, and an empty order was saved in the history.
- **Expected:** `None`, and no order saved, as the docstring says.
- **Fixed:** Added `if not self.items: return None` at the start.
- **Author:** Kaung

---

## Bug 4
- **Suspected:** `Cart.import_products()` in `cart.py`. The last line is `return count + 1`, but the docstring says it returns how many products were imported.
- **Tried:** Imported 2 products: `[(1, "A", 5), (2, "B", 6)]`. Test: `test_import_products_returns_exact_count`.
- **Observed:** `AssertionError: assert 3 == 2`.
- **Expected:** `2`, the number of products imported.
- **Fixed:** Changed `return count + 1` to `return count`.
- **Author:** Kaung

---

## Bug 5
- **Suspected:** `Catalog.search()` in `catalog.py`. The check is `keyword in info["title"]`, which compares letters exactly, so upper and lower case count as different.
- **Tried:** Added a product titled `"Python Testing"`, then searched for `"python"`. Test: `test_search_ignores_upper_and_lower_case`.
- **Observed:** `assert [] == [1]`. The search returned an empty list, so the book was not found.
- **Expected:** `[1]`. A customer who types a lowercase word should still find the book, because the docstring says the search finds titles that contain the keyword.
- **Fixed:** Changed the check to `keyword.lower() in info["title"].lower()`.
- **Author:** Kaung