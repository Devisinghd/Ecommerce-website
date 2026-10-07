When the product catalog has no products, the storefront currently renders an empty product area. Add a clear, friendly empty state so visitors understand that there are no products to browse yet.

## Scope

- Update the empty-products branch in `myapp/templates/myapp/index.html`.
- Show a short message and a suitable next step or link.
- Keep the existing product listing unchanged when products are available.

## Acceptance criteria

- [ ] The storefront displays a helpful message when there are no products.
- [ ] The empty state does not appear when products are available.
- [ ] The page remains responsive and consistent with the existing design.
- [ ] Add or update a test if the project has a suitable storefront test for this behavior.

## Getting started

The storefront view paginates products in `myapp/views.py`; the catalog template is `myapp/templates/myapp/index.html`.

## Contribution notes

Please keep the change focused on the empty catalog state. No new dependencies are needed.
