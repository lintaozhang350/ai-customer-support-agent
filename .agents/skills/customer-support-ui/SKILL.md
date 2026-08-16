---
name: customer-support-ui
description: Improve and audit the ShopDesk AI Customer Support Agent frontend when Codex is asked to polish the customer-service UI, redesign the chat experience, improve ecommerce support UX, present order/product/policy/ticket tool results, make the app feel production-quality instead of demo-like, or verify responsive customer-support layouts. Use for frontend/UI work only, not unrelated backend-only tasks.
---

# Customer Support UI

## Purpose

Use this skill to improve the ShopDesk customer-service frontend as a practical ecommerce support product. Preserve the existing React, TypeScript, Tailwind, FastAPI API calls, and business behavior unless a UI change requires a small compatibility adjustment.

## Workflow

1. Audit the current UI before editing.
2. Identify the highest-impact issues in hierarchy, spacing, message presentation, business-data display, navigation, and responsiveness.
3. Load the relevant references:
   - Read `references/design-rules.md` for product-level visual direction.
   - Read `references/chat-ui-rules.md` before changing chat, messages, composer, or tool-result presentation.
   - Read `references/qa-checklist.md` before final verification.
4. Implement focused UI improvements without replacing the app architecture.
5. Run the app or build command used by the repository.
6. Visually inspect desktop, tablet, and mobile widths when browser tooling is available.
7. Fix visible layout, overflow, typography, spacing, and hierarchy issues before finishing.

## Product Direction

Make the interface feel like mature ecommerce customer-service software, not an AI demo, SaaS landing page, or debug console.

Prefer practical layouts, clear task hierarchy, readable conversation density, structured order/product/policy/ticket cards, restrained colors, subtle borders and shadows, and accessible controls.

Avoid generic AI styling, raw JSON as the main UI, excessive badges, oversized marketing sections, decorative gradients, glassmorphism, too many nested cards, and full-width chat message cards.

## Required Behavior Preservation

Do not break:
- `/api/chat`
- order lookup
- product search
- policy retrieval
- support ticket creation
- frontend state management
- existing demo prompts
- build/type checking

If structured tool data is shown, make it customer-readable first. Keep developer/debug details secondary, collapsed, or separated.
