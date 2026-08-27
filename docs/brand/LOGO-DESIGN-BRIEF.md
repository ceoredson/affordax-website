# Affordax Logo Design Brief

Status: Direction A implemented for public-site testing

Date: 27 August 2026

## Objective

Design a distinctive, durable vector identity for Affordax: a Malawian platform
connecting employees, employers, and service providers around accountable payroll
affordability. It must be credible for institutions, approachable to the public,
and clear as a 16-pixel favicon.

## Recommended concept: Protected Horizon

Build the mark around a custom capital **A** that communicates:

- **protection** — a stable base or affordability floor;
- **progress** — a rising horizon or opening above that floor;
- **accountability** — one continuous and deliberate structure;
- **Malawi** — a restrained color reference and, if useful, a subtle
  Lake Malawi-inspired contour.

The viewer should recognise a strong A before discovering its symbolism.

## Construction principles

- Begin in black and white; color must not rescue weak geometry.
- Prefer one silhouette or a small number of intentional shapes.
- Use balanced optical weight and generous negative space.
- Avoid thin details that fail below 24 pixels.
- Avoid literal maps, pasted flags, coins, shields, locks, hands, roofs, bank
  buildings, currency symbols, and obvious upward arrows.
- Do not force every Malawi flag color into every variant.
- Avoid political, government, charity, telecom, betting, or crypto associations.
- Give curves and corners one consistent visual logic.

## Color behavior

The primary mark must work in Affordax Ink (`#17202A`) and White. The full-color
version may use Malawi Red (`#CE1126`) as its leading accent and Malawi Green
(`#339E35`) as a smaller supporting detail. Integrate the accents into the
geometry rather than applying them as flag stripes.

## Wordmark

Create a custom or optically modified `Affordax` wordmark. Test lowercase during
exploration, but keep the official product spelling unless a deliberate naming
decision changes it. The wordmark should be readable at navigation size, neither
aggressively geometric nor excessively rounded, and carefully spaced around
`ff`, `rd`, and `ax`. A distinctive final `x` is welcome only if it is functional,
not a gimmick.

## Three directions to explore

### A — Protected Horizon (recommended)

A custom A whose lower structure creates a firm protected floor while its opening
rises like a horizon. A restrained curve can echo Lake Malawi's long vertical
character without drawing the country map.

Risk: it must not become a generic roof, mountain, or growth-arrow mark.

### B — Lake Route

An A formed by two controlled banks around a negative-space route or lake
contour, suggesting access and a guided path.

Risk: avoid resembling a road, location pin, tourism mark, or literal map.

### C — Three-Party Junction

A connected A with three structural points representing employee, employer, and
provider within one accountable system.

Risk: connected-node marks are common and can look like generic technology logos.

The existing `static/images/affordax-mark-concept.svg` is an early Direction C
sketch only. It is not approved and must not be published as the production logo.

## Required lockups

- horizontal mark plus wordmark;
- stacked mark plus wordmark;
- mark only;
- one-color Ink;
- reversed White;
- approved full-color version;
- simplified small-size mark;
- square app icon and favicon.

Test every lockup on White, Warm Paper, and Affordax Ink.

## Rejection criteria

Reject a concept if it:

- needs a long explanation before making visual sense;
- loses its identity in one color or at favicon size;
- relies on a literal Malawi map or full flag treatment;
- could be exchanged with a bank, lender, or generic software logo;
- depends on gradients, shadows, or tiny nodes;
- cannot be reproduced cleanly in SVG and print;
- conflicts with an obvious existing trademark.

## Presentation requirements

Show each direction first as black on White and then White on Ink—not only in
polished mockups. Include a construction view, 16/24/32/64-pixel tests, horizontal
and symbol-only versions, a website header, a portal login, one document example,
and an explanation limited to three sentences.

## Final deliverables

- editable vector master and optimized SVG exports;
- outlined and live-text wordmark masters;
- monochrome, reversed, and full-color variants;
- favicon SVG and PNG fallbacks;
- 180, 192, and 512-pixel application icons;
- clear-space and minimum-size specifications;
- RGB/HEX and print color definitions;
- typography specification and one-page quick-use guide;
- record of the selected direction and rejected alternatives.

## Decision process

1. Review three directions against the objective and rejection criteria.
2. Shortlist no more than two.
3. Test both at real sizes and in one color.
4. Check distinctiveness against relevant local and international brands.
5. Refine one direction instead of combining several weaker ideas.
6. Complete a trademark search before treating it as legally locked.
7. Approve the master artwork, then roll it into both sites through shared assets
   and design tokens.

## Implemented candidate

The current Direction A candidate is stored in `static/brand/logo/`. Its A
silhouette uses Ink, its Red crossbar represents the protected floor, and a short
Green endpoint introduces a restrained Malawi cue. It has passed initial SVG and
small-icon rendering checks but remains open to optical refinement and trademark
review.
