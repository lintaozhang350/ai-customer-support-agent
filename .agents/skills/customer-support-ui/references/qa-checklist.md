# QA Checklist

## Content And Business

- No fabricated orders, tracking numbers, prices, inventory, dates, or ticket data.
- Labels sound customer-facing, not implementation-facing.
- Structured tool results are human-readable.
- Raw JSON is not the main UI.

## Chat

- Customer and agent messages are clearly distinct.
- Message widths feel natural.
- Conversation spacing is readable but not sparse.
- Composer is easy to use.
- Loading and error states are understandable.

## Desktop

- Wide-screen space is used intentionally.
- Main conversation and context area are balanced.
- No excessive empty space.
- Header and navigation align cleanly.
- Panels have consistent spacing and visual weight.

## Tablet

- Layout remains readable around 768px.
- Context panel does not squeeze the conversation too much.
- Text wraps cleanly.
- Composer remains usable.

## Mobile

- No horizontal overflow at 375px.
- Tap targets are usable.
- Context content stacks or collapses appropriately.
- Composer remains visible and usable.
- Message bubbles do not become too narrow.

## Visual Consistency

- Typography scale is consistent.
- Border radius is consistent.
- Shadows are subtle and purposeful.
- Buttons have consistent states.
- Cards/panels do not nest excessively.

## Accessibility

- Keyboard focus is visible.
- Buttons are semantic buttons.
- Contrast is sufficient.
- Heading order is sensible.
- Inputs have clear purpose.

## Technical

- Build passes.
- No broken imports.
- No unnecessary dependencies.
- Existing API calls still work.
- Browser console has no obvious runtime errors when checked.

## Final Review

- Actual browser review completed.
- Desktop checked.
- Tablet/intermediate width checked.
- Mobile checked.
- Visible layout defects fixed before finishing.
