# REPORT.md

Group: Trial run   Members: Kaung Myat Tun

## Part A -- Test types

### Smoke tests
**Definition.** A smoke test is a quick check that the most important features work at a basic level. It does not look for small details. It only asks: is the application alive and usable?

**When it runs.** On every push and after every deployment, before any other test. It must finish in a few seconds.

**Bookstore examples.**
1. Register a new user and log in with the same password.
2. Add a product to the catalog, add it to the cart, and check out a non-empty cart.

### Regression tests
**Definition.** A regression test checks one specific bug that was found and fixed, to make sure it does not come back. It fails while the bug exists and passes after the fix.

**When it runs.** Whenever the code changes, for example before merging a change and in the full nightly run. The suite grows with every bug, so it is usually run in CI and not by hand before every commit.

**Bookstore examples.**
1. `cart.total()` must include the last item in the cart (10 + 20 + 5 must give 35, not 30).
2. `catalog.search("python")` must find the book "Python Testing", whatever the letter case.

### Slow tests
**Definition.** A slow test takes a long time because it uses a lot of data or repeats many operations. It tests the application under heavy work.

**When it runs.** Not on every push. It runs on a schedule (for example every night) and before a release.

**Bookstore examples.**
1. Import 200,000 products with `import_products()` and then search them.
2. Run 200 searches over a catalog of 100,000 products.

## Part B -- Scenario classification

**1. Password-reset email delivered within one minute: slow.**
The test has to wait for an email system outside the application, and it must wait up to a full minute. A test that waits this long is slow, and it can also fail for reasons that are not a bug (a slow mail server). It should run in the nightly run, not on every push.

**2. A fixed bug in the shipping-cost calculation has not returned: regression.**
The bug was found before and fixed. The test exists only to prove it does not come back. It is a plain calculation, so it is fast, and it is not slow and not smoke.

**3. A nightly job can generate a sales report from ten years of orders: slow.**
Ten years of orders is a very large amount of data, so the test takes a long time. It runs at night, so it should not block developers during the day. It is not smoke, because it is not a basic check of the main features.

**4. The payment page loads after every deployment: smoke.**
Payment is a core feature, and the check is quick and basic: does the page load at all? If it fails, the deployment is broken, so it should run first after every deployment.

**5. A refund issued twice does not credit the customer twice (a fault reported last quarter): regression.**
This is a real fault that was reported and fixed. The test makes sure the double credit does not come back. It checks one precise rule and is fast, so it is not smoke and not slow.

**6. The recommendation engine still responds when the catalog holds one million titles: slow.**
One million titles is a very large data set, so the test is heavy and takes a long time. It checks performance under load, and it fits the nightly run. If the engine had failed with big catalogs before, it could also be a regression test, but the scenario does not say that.

## Part B -- Scenario classification

### Scenario 1 : Verify that a password-reset email is delivered within one minute.
**Answered by: Preston Shah Aman**
Classification: slow.
 
The test has to wait for up to a minute and depends on an external email service, so it is too slow and too unreliable to run on every push. It belongs in a scheduled or pre-release run. A quick check that the "reset password" request is accepted could be a smoke test, but verifying delivery within one minute is slow.

### Scenario 2 : Verify that a previously fixed bug in shipping-cost calculation has not returned.
**Answered by: Kaung Myat Tun**
Classification: regression.

The shipping-cost calculation previously contained a bug that was
fixed. This test checks that later changes have not reintroduced it.

### Scenario 3 : Verify that a nightly job can generate a sales report from ten years of orders.
**Answered by: Paing Oo Thant**
Classification: slow.

Generating a sales report from ten years of orders processes a large
historical dataset. The test should verify the report's correctness,
not merely that processing finishes.

### Scenario 4 : Verify that the payment page loads after every deployment.
**Answered by: Thin Thiri Zaw*
Classification: smoke.

Checking whether the payment page loads after deployment quickly
verifies an essential customer feature. It provides basic deployment
feedback without exhaustively testing payment processing.

### Scenario 5 : Verify that a refund issued twice does not credit the customer twice — a fault reported by a customer last quarter.
**Answered by: Aung Kyaw Phyo**
Classification: regression.

A customer previously reported that the same refund could be processed twice, causing the customer to receive two refund credits for a single transaction. This test reproduces the previously reported situation by submitting the same refund request twice. The first refund should successfully credit the customer, while the second identical request should not provide any additional credit. The test passes if the customer receives only one refund in total. This is classified as a regression test because it verifies that a previously fixed defect has not returned after changes have been made to the system.

### Scenario 6 : Verify that the recommendation engine still responds when the catalogue holds one million titles.
**Answered by: L Peter San Awng**
Classification: slow.

Testing recommendations with one million titles exercises a large
dataset and substantial processing work. It would also be regression
if it reproduced a specific previously fixed defect, but the scenario
does not state such a history.

---

## Part F -- Team reflection

**1. Why is running only regression tests before every commit inefficient?**
The regression suite gets bigger with every bug that is fixed, so running all of it before every commit takes more and more time, and developers start to skip it. It also only checks old bugs. It does not quickly tell you if the main features work. A short smoke suite is the better check before a commit, and the full regression suite belongs in CI.

**2. Why do smoke tests usually run first in a CI/CD pipeline?**
They are fast and they check the most important features. If a smoke test fails, the build is broken, and running the slower tests would waste time and computer power. The team gets feedback in seconds ("fail fast") and the slower tests only run when the basics are working.

**3. What risks arise if slow tests are never run?**
Problems with large data stay hidden until real customers meet them. In this project, the slow tests import 200,000 products and run many searches. If they are never run, a crash or a big slowdown with a large catalog would only be found in production. The slow tests in this project passed on the shipped code, so they did not find a bug, but they protect against that kind of problem in the future.

**4. Can one test belong to two categories? Give an example.**
Yes. The markers describe different characteristics of a test, not separate boxes. For example, a test that imports 100,000 products and checks that `import_products()` returns the right count (the bug where it returned count + 1) is a regression test, because it checks a fixed bug, and also a slow test, because it uses a lot of data. In CI it belongs in the nightly run.

**5. Bug finders and bug fixers are often different people in a real QA team. What does that separation change about how a bug report must be written?**
The fixer cannot ask the finder what they meant, so the report must stand on its own. It must give the exact function, the exact input, the actual wrong result (pasted, not described), the expected result, and the reason why that expected result is correct. Best of all it includes a failing test that the fixer can run. This is why `FINDINGS.md` has the Observed and Expected pair: for example, "`cart_total` returned 30 for items of 10, 20 and 5; it should return 35".

## Bonus -- A test with two markers

`test_large_import_returns_exact_count` carries both `@pytest.mark.regression` and `@pytest.mark.slow`.

**Why it is a regression test.** It checks a bug that was found and fixed: `import_products()` returned `count + 1`. On the original code the test fails (`200001 == 200000`) and after the fix it passes.

**Why it is slow.** It imports 200,000 products one by one, and each product goes through `add_product()`. This takes much longer than a smoke test, which finishes in a fraction of a second.

**Where it belongs in CI/CD.** In the scheduled nightly run with the full suite, not in the smoke run on every push. It must still run before a release. The two markers describe two different characteristics of the same test: what it protects (a fixed bug) and how heavy it is (a lot of data).
