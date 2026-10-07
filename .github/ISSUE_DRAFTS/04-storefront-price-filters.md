The storefront currently lists products but does not let visitors narrow the results by price. Add optional minimum and maximum price filters that work with the existing product pagination.

## Scope

- Read optional minimum and maximum price values from the storefront query string.
- Apply valid filters to the product queryset in `myapp/views.py`.
- Add simple filter inputs to the storefront template.
- Preserve the filter values when moving between result pages.
- Do not add category filtering; the current product model does not have a category field.

## Acceptance criteria

- [ ] Visitors can filter products by minimum price, maximum price, or both.
- [ ] Empty filter values leave the catalog unfiltered.
- [ ] Invalid or negative values are handled safely with a clear, non-crashing response.
- [ ] Pagination links preserve the selected filters.
- [ ] Add tests for the filter behavior and pagination query parameters.

## Getting started

The `index` view and pagination are in `myapp/views.py`; the product model and storefront template are in `myapp/models.py` and `myapp/templates/myapp/index.html`.

## Contribution notes

Keep the UI consistent with the existing storefront and avoid changing product model fields or database schema.
