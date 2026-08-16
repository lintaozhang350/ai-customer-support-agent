# Chat UI Rules

## Conversation Feel

The chat should feel like a real customer-support conversation, not a debug log.

Use natural message widths. Customer messages align right; support messages align left. Do not make every message a giant full-width card.

## Message Treatment

Agent messages should be calm, readable, left aligned, and visually lighter than structured result panels.

Customer messages should be right aligned, compact, visually distinct, and readable on mobile.

System/status messages should be subtle, short, and secondary.

## Composer

The composer must remain easy to use:
- clear placeholder
- stable height
- obvious send button
- disabled/loading state
- no layout jump during send

## Tool Results

Do not show raw JSON as the primary customer-facing result.

Convert tool results into UI components:
- Order result: order number, item, status, delivery date, tracking number.
- Product result: product name, price, category, stock/inventory state.
- Policy result: answer text plus source/reference label.
- Ticket result: ticket number, status, issue summary, next step.
- Privacy refusal: clear refusal message without technical metadata.

Developer details can be collapsed behind labels like "View technical details" or "Case details".

## Case Details

Case metadata should be secondary. Prefer customer-support language:
- Reason
- Action taken
- Reference
- Ticket status

Avoid foregrounding internal labels like intent, tool name, model, confidence, or raw action identifiers.

## Context Panel

Context panels should help the customer:
- common help topics
- recent orders
- selected order summary
- return/warranty shortcuts

Do not make the context panel look like a list of demo test buttons.

## Mobile

On mobile:
- keep messages readable
- stack context below or above the chat
- keep tap targets large enough
- avoid nested scrolling where possible
- ensure code/debug blocks do not force horizontal page overflow

## Error States

Show friendly errors such as "We could not connect to customer service. Please try again." Avoid raw exception wording in customer-facing areas.
