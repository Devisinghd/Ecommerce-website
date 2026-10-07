# Good First Issue Drafts

These five beginner-friendly issue drafts were checked against the current code. Each linked file contains a complete GitHub issue body. When publishing, set the issue title shown below and apply the `good first issue` label.

| # | Issue title | Full issue body |
|---|---|---|
| 1 | Show a helpful empty state when the product catalog is empty | [01-empty-catalog-state.md](.github/ISSUE_DRAFTS/01-empty-catalog-state.md) |
| 2 | Handle products without an uploaded image in the cart | [02-cart-product-image-fallback.md](.github/ISSUE_DRAFTS/02-cart-product-image-fallback.md) |
| 3 | Validate phone and postal code fields on delivery addresses | [03-address-field-validation.md](.github/ISSUE_DRAFTS/03-address-field-validation.md) |
| 4 | Add minimum and maximum price filters to the storefront | [04-storefront-price-filters.md](.github/ISSUE_DRAFTS/04-storefront-price-filters.md) |
| 5 | Add tests for seller product create, update, and delete flows | [05-seller-product-workflow-tests.md](.github/ISSUE_DRAFTS/05-seller-product-workflow-tests.md) |

## Publish with GitHub CLI

From the repository root, run the commands below one at a time. If the `good first issue` label does not exist yet, create it in the repository's **Issues → Labels** settings first.

```powershell
gh issue create --repo Devisinghd/Ecommerce-website --title "Show a helpful empty state when the product catalog is empty" --label "good first issue" --body-file ".github/ISSUE_DRAFTS/01-empty-catalog-state.md"

gh issue create --repo Devisinghd/Ecommerce-website --title "Handle products without an uploaded image in the cart" --label "good first issue" --body-file ".github/ISSUE_DRAFTS/02-cart-product-image-fallback.md"

gh issue create --repo Devisinghd/Ecommerce-website --title "Validate phone and postal code fields on delivery addresses" --label "good first issue" --body-file ".github/ISSUE_DRAFTS/03-address-field-validation.md"

gh issue create --repo Devisinghd/Ecommerce-website --title "Add minimum and maximum price filters to the storefront" --label "good first issue" --body-file ".github/ISSUE_DRAFTS/04-storefront-price-filters.md"

gh issue create --repo Devisinghd/Ecommerce-website --title "Add tests for seller product create, update, and delete flows" --label "good first issue" --body-file ".github/ISSUE_DRAFTS/05-seller-product-workflow-tests.md"
```
