Seller product management has views for creating, updating, and deleting products, but `seller/tests.py` currently has no coverage. Add focused tests for the main seller workflows and ownership rules.

## Scope

- Add tests in `seller/tests.py` using Django's built-in test framework.
- Cover successful product creation, update, and deletion by an authenticated seller.
- Verify unauthenticated users are redirected to login.
- Verify one seller cannot update or delete another seller's product.

## Acceptance criteria

- [ ] Tests cover create, update, and delete behavior.
- [ ] Tests verify products are associated with the signed-in seller.
- [ ] Tests verify access is denied for another seller's product.
- [ ] Tests run with the project's standard Django test command.
- [ ] No production behavior is changed solely to make a test pass.

## Getting started

Seller views are in `seller/views.py`, forms are in `seller/forms.py`, and the test module is `seller/tests.py`.

## Contribution notes

Use Django's test client and test database. Keep each test focused and avoid external services.
