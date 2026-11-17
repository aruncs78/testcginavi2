# SauceDemo Core Functional Scenario Matrix

## Authentication
1. Successful login with `standard_user`
2. Login blocked for `locked_out_user`
3. Login validation when username is empty
4. Login validation when password is empty
5. Login validation when both username and password are empty
6. Logout from inventory page

## Inventory
7. Inventory page loads after login with title and product list visible
8. Add a single product to cart from inventory page
9. Remove a product from inventory page
10. Add multiple distinct products to cart
11. Open product details page and verify product information
12. Return from product details page to inventory list
13. Sort inventory by Name (A to Z)
14. Sort inventory by Name (Z to A)
15. Sort inventory by Price (low to high)
16. Sort inventory by Price (high to low)

## Cart
17. Cart badge count updates when items are added
18. Cart page shows selected items with correct quantity
19. Remove item from cart page
20. Continue shopping from cart page

## Checkout
21. Navigate to checkout from cart
22. Checkout information validation when first name is missing
23. Checkout information validation when last name is missing
24. Checkout information validation when postal code is missing
25. Cancel checkout from information step
26. Checkout overview displays selected items and totals
27. Finish checkout successfully and verify confirmation page
28. Return home from checkout complete page

## End-to-End Core Flows
29. Complete purchase of a single item
30. Complete purchase of multiple items
31. Add item from detail page and complete purchase
32. Remove item before checkout and verify final order contents

## Notes
- Tests will use Playwright Python + pytest.
- Videos, screenshots on failure, traces, and HTML report will be produced.
- Core coverage excludes exhaustive visual/error_user specific edge cases per user request.
