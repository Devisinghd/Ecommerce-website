Delivery addresses currently use plain text fields for phone and postal code. Add basic, user-friendly validation so obviously invalid values are rejected when a customer adds or edits an address.

## Scope

- Review `orders/forms.py` and the `Address` model in `orders/models.py`.
- Add practical validation for the phone and postal code fields.
- Show validation errors through the existing address form rather than silently discarding input.
- Avoid restricting users to one country's phone or postal-code format.

## Acceptance criteria

- [ ] Blank or malformed phone/postal-code values receive clear form errors.
- [ ] Valid international-style values, including common spaces and `+`, are accepted where appropriate.
- [ ] Existing valid addresses can still be edited and saved.
- [ ] Add tests covering valid and invalid values.

## Getting started

`AddressForm` is a `ModelForm` in `orders/forms.py`, and address creation is handled by `add_address` in `orders/views.py`.

## Contribution notes

Keep the validation broadly compatible with international addresses. Do not add a third-party package for this task.
