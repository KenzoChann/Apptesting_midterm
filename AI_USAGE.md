# AI Usage Declaration and Audit

**Group:** Trial run  **Members:** Kaung Myat Tun

---

## Part 1 -- AI usage declaration

| Tool | What we used it for | Where in the project | How we checked it before relying on it |
|---|---|---|---|
| Claude | Explained the assignment, suggested the smoke, slow and regression tests, suggested the bug fixes, drafted FINDINGS.md and this audit | `tests/test_bookstore.py`, `bookstore_app/users.py`, `bookstore_app/cart.py`, `bookstore_app/catalog.py`, `FINDINGS.md`, `AI_USAGE.md` | Ran every regression test on the shipped code and saw it fail, committed the failing test before the fix, then ran the full suite after the fix. Compared the shipped and fixed pytest output for all 8 audited tests. |
| Codex | Generated a folder tree of the zip, to check the files were received correctly | Not in the repository | Compared the tree with the tree made by Claude. They matched. |

---

## Part 2 -- Audit of the supplied test set

`ai_review/test_ai_generated.py` contains eight tests. Command used for both runs:

```text
python -m pytest ai_review/ -v
```

Shipped run: `4 failed, 4 passed in 0.08s`. Fixed run (all six bugs fixed): `1 failed, 7 passed in 0.08s`.

### Summary table

| # | Test | What it claims to catch | Shipped | Fixed | Verdict | Auditor |
|---|---|---|---|---|---|---|
| 1 | `test_cart_total_sums_items` | cart total is wrong | FAIL | PASS | Genuine detection | Kaung |
| 2 | `test_login_rejects_wrong_password` | login accepts a wrong password | PASS | PASS | Detects nothing | Kaung |
| 3 | `test_search_finds_exact_title` | search does not find a product | PASS | PASS | Detects nothing | Kaung |
| 4 | `test_import_returns_count` | bulk-import count is wrong | FAIL | PASS | Genuine detection | Kaung |
| 5 | `test_register_duplicate_returns_false` | duplicate registration succeeds | PASS | PASS | Detects nothing | Kaung |
| 6 | `test_checkout_empty_returns_none` | empty checkout does not return None | FAIL | PASS | Genuine detection | Kaung |
| 7 | `test_add_to_cart_returns_true_for_known_product` | known product cannot be added | PASS | PASS | Detects nothing | Kaung |
| 8 | `test_search_is_limited_to_ten_results` | search returns more than ten results | FAIL | FAIL | Invented requirement | Kaung |

### Detail entries

#### Test: `test_cart_total_sums_items`  (`ai_review/test_ai_generated.py:12`)

**Audited by:** Kaung

**1. What it claims to catch.** That `Cart.total()` returns the wrong sum for two items.

**2. Evidence -- against the shipped code**

```text
ai_review/test_ai_generated.py::test_cart_total_sums_items FAILED        [ 12%]
>       assert c.total() == 30
E       assert 10 == 30
```

**3. Evidence -- against your fixed code**

```text
ai_review/test_ai_generated.py::test_cart_total_sums_items PASSED        [ 12%]
```

**4. What that pair proves.** Row FAIL then PASS: genuine detection. The shipped `total()` skipped the last item and returned 10 instead of 30. After the loop was fixed, the test passed.

**5. Verdict:** Genuine detection

---

#### Test: `test_login_rejects_wrong_password`  (`ai_review/test_ai_generated.py:19`)

**Audited by:** Kaung

**1. What it claims to catch.** That `login()` accepts a wrong password.

**2. Evidence -- against the shipped code**

```text
ai_review/test_ai_generated.py::test_login_rejects_wrong_password PASSED [ 25%]
```

**3. Evidence -- against your fixed code**

```text
ai_review/test_ai_generated.py::test_login_rejects_wrong_password PASSED [ 25%]
```

**4. What that pair proves.** Row PASS then PASS: detects nothing. The real login bug is the opposite: the shipped `login()` refused a correct password that contains a symbol (`"pass@123"`). This test only checks that a wrong password is refused, and that already worked. To catch the bug it would have to register a password with a symbol and assert that logging in with it returns True.

**5. Verdict:** Detects nothing

---

#### Test: `test_search_finds_exact_title`  (`ai_review/test_ai_generated.py:25`)

**Audited by:** Kaung

**1. What it claims to catch.** That search cannot find a product by its title.

**2. Evidence -- against the shipped code**

```text
ai_review/test_ai_generated.py::test_search_finds_exact_title PASSED     [ 37%]
```

**3. Evidence -- against your fixed code**

```text
ai_review/test_ai_generated.py::test_search_finds_exact_title PASSED     [ 37%]
```

**4. What that pair proves.** Row PASS then PASS: detects nothing. The test searches with the same capital letters as the title (`"Python Testing"`). The real search bug is that upper and lower case are treated as different. To catch it, the test would have to search with `"python testing"` and expect `[1]`.

**5. Verdict:** Detects nothing

---

#### Test: `test_import_returns_count`  (`ai_review/test_ai_generated.py:31`)

**Audited by:** Kaung

**1. What it claims to catch.** That `import_products()` returns the wrong number.

**2. Evidence -- against the shipped code**

```text
ai_review/test_ai_generated.py::test_import_returns_count FAILED         [ 50%]
E       AssertionError: assert 3 == 2
```

**3. Evidence -- against your fixed code**

```text
ai_review/test_ai_generated.py::test_import_returns_count PASSED         [ 50%]
```

**4. What that pair proves.** Row FAIL then PASS: genuine detection. Importing 2 products returned 3 (`count + 1`). After the change to `return count`, the test passed.

**5. Verdict:** Genuine detection

---

#### Test: `test_register_duplicate_returns_false`  (`ai_review/test_ai_generated.py:37`)

**Audited by:** Kaung

**1. What it claims to catch.** That registering the same username twice succeeds.

**2. Evidence -- against the shipped code**

```text
ai_review/test_ai_generated.py::test_register_duplicate_returns_false PASSED [ 62%]
```

**3. Evidence -- against your fixed code**

```text
ai_review/test_ai_generated.py::test_register_duplicate_returns_false PASSED [ 62%]
```

**4. What that pair proves.** Row PASS then PASS: detects nothing. `register()` already returns False for a taken username, so there is no bug here. The test checks behaviour that was never broken, and it gives false confidence that the users module was checked.

**5. Verdict:** Detects nothing

---

#### Test: `test_checkout_empty_returns_none`  (`ai_review/test_ai_generated.py:43`)

**Audited by:** Kaung

**1. What it claims to catch.** That checking out an empty cart does not return None.

**2. Evidence -- against the shipped code**

```text
ai_review/test_ai_generated.py::test_checkout_empty_returns_none FAILED  [ 75%]
>       assert Cart(Catalog()).checkout() is None
E       assert [] is None
```

**3. Evidence -- against your fixed code**

```text
ai_review/test_ai_generated.py::test_checkout_empty_returns_none PASSED  [ 75%]
```

**4. What that pair proves.** Row FAIL then PASS: genuine detection. The shipped `checkout()` returned `[]`, but its docstring says it returns None for an empty cart. After the fix, the test passed.

**5. Verdict:** Genuine detection

---

#### Test: `test_add_to_cart_returns_true_for_known_product`  (`ai_review/test_ai_generated.py:48`)

**Audited by:** Kaung

**1. What it claims to catch.** That a known product cannot be added to the cart.

**2. Evidence -- against the shipped code**

```text
ai_review/test_ai_generated.py::test_add_to_cart_returns_true_for_known_product PASSED [ 87%]
```

**3. Evidence -- against your fixed code**

```text
ai_review/test_ai_generated.py::test_add_to_cart_returns_true_for_known_product PASSED [ 87%]
```

**4. What that pair proves.** Row PASS then PASS: detects nothing. `Cart.add()` already works for a known product. The test only checks the return value, so it is not linked to any bug I found.

**5. Verdict:** Detects nothing

---

#### Test: `test_search_is_limited_to_ten_results`  (`ai_review/test_ai_generated.py:55`)

**Audited by:** Kaung

**1. What it claims to catch.** That `search()` returns more than ten results.

**2. Evidence -- against the shipped code**

```text
ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results FAILED [100%]
>       assert len(cat.search("match")) <= 10
E       AssertionError: assert 20 <= 10
```

**3. Evidence -- against your fixed code**

```text
ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results FAILED [100%]
E       AssertionError: assert 20 <= 10
```

**4. What that pair proves.** Row FAIL then FAIL: invented requirement. The docstring of `search()` says it returns a list of product ids whose title contains the keyword. It never mentions a limit of ten. The test demands a feature that was never part of the application.

**5. Verdict:** Invented requirement

---

## Part 3 -- Coverage against our own bug hunt

| Bug (our description) | We found it | The supplied set catches it | Which test, and how we established that |
|---|---|---|---|
| `login()` refuses a correct password with a symbol | Yes | No | `test_login_rejects_wrong_password` passed on the shipped code (Part 2, test 2) |
| `total()` skips the last item | Yes | Yes | `test_cart_total_sums_items`, FAIL then PASS |
| `checkout()` on an empty cart returns `[]` | Yes | Yes | `test_checkout_empty_returns_none`, FAIL then PASS |
| `import_products()` returns count + 1 | Yes | Yes | `test_import_returns_count`, FAIL then PASS |
| `search()` is case-sensitive | Yes | No | `test_search_finds_exact_title` passed on the shipped code |

---

## Part 4 -- Verdict

1. **Most common failure mode:** "detects nothing" (PASS then PASS), 4 of 8 tests (#2, #3, #5, #7). Genuine detection: 3 (#1, #4, #6). Invented requirement: 1 (#8). Locks in the bug: 0.

2. **Why a passing test on buggy code is more dangerous than a crash:** A failing test is red, so someone investigates it. A green test is trusted and nobody looks at it again. `test_login_rejects_wrong_password` stayed green while `login()` refused correct passwords with symbols. A team could believe login was tested when the real bug was never checked.

3. **Did the supplied set catch anything we missed?** No. It caught 3 of our 5 recorded bugs (total, empty checkout, import count) and missed 2 (login with symbols, case-sensitive search). Its search test used the same capital letters as the title, so it could not see the case bug.

4. **Checks we will do before trusting a generated test:** (a) run it on the shipped code and on the fixed code and compare the pair, not just one run; (b) compare each assert with the docstring in the application, as we did for the "ten results" limit, which `search()` never promised; (c) ask which input would make the test fail on the bug, for example a password with a symbol for login; (d) check that the test passes after the fix.