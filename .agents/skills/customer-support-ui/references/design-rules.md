# Design Rules

## Goal

Make ShopDesk feel like a polished ecommerce customer-support product comparable in quality and usability to mature help-center or commerce admin software, without copying a specific brand.

## Product UI, Not Marketing UI

Do not design a landing page. The first screen should be the usable support experience.

Avoid giant headings, decorative gradients, purple-blue AI styling, glassmorphism, fake terminal panels, excessive cards, meaningless badges, and large empty hero areas.

Prefer compact but comfortable product density, strong alignment, restrained color, clear forms, practical panels, and obvious interaction states.

## Layout

Use desktop space intentionally:
- Main area: conversation and composer.
- Context area: recent orders, common support topics, customer/order context, case status, or useful next actions.

On mobile, stack or collapse context areas so the conversation and composer remain usable. Avoid horizontal overflow.

## Visual Hierarchy

Prioritize:
1. Customer's current issue
2. Agent response
3. Relevant business data
4. Actions the customer can take
5. Case metadata
6. Developer/debug information

Do not let implementation details dominate the customer-facing UI.

## Typography And Spacing

Use restrained type sizes. Reserve large headings for page-level labels only. Keep panel headings compact. Use consistent spacing steps. Avoid making every element the same visual weight.

## Borders, Shadows, Radius

Use borders to separate functional regions, not to decorate every element. Prefer subtle shadows only for panels that need elevation. Keep radius modest, generally around 6-8px.

## Color

Use a restrained ecommerce/product palette. Avoid one-note blue/purple AI palettes. Use accent color for actions and status only.

## Navigation

Keep navigation simple and aligned. Possible labels: Orders, Returns, Warranty, Help. Avoid over-designed navigation.

## Business Data

Render structured data as human-readable UI:
- Order status cards
- Product recommendation rows
- Policy source snippets
- Ticket confirmation panels

Raw JSON may exist only in secondary developer/debug details.

## Accessibility

Use semantic buttons and forms, visible focus states, sufficient contrast, readable text sizes, clear labels, and keyboard-friendly interactions.
