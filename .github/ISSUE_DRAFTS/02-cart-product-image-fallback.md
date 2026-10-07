The product cards and product detail page use the shared product placeholder when an image is missing. The cart template directly accesses `item.product.image.url`, however, so a product without an uploaded image may render incorrectly or fail while the cart page is being rendered.

## Scope

- Update `cart/templates/cart/cart-overview.html` to handle a missing product image.
- Reuse the existing `myapp/product-placeholder.svg` static asset.
- Keep the current product image and alt text behavior for products that do have an image.

## Acceptance criteria

- [ ] Products with an uploaded image continue to show that image.
- [ ] Products without an uploaded image show the existing placeholder.
- [ ] The rendered image has useful alternative text.
- [ ] Add or update a test if the project has a suitable cart template test.

## Getting started

Compare the image handling in `myapp/templates/myapp/detail.html` with the cart product markup in `cart/templates/cart/cart-overview.html`.

## Contribution notes

Please do not add a new image dependency or duplicate the placeholder asset.
