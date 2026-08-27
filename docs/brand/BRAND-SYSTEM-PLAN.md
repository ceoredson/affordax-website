# Affordax Brand System Plan

Status: Direction A implementation candidate; not legally locked

Version: 0.2

Date: 27 August 2026

## Purpose

Affordax needs one recognisable identity across the public website, secure portal,
email, documents, social media, and future products. It should feel Malawian
without looking governmental or decorative, and communicate trust, protection,
connection, and operational accountability.

Core idea: **One accountable thread.**

## Brand character

The identity should feel:

- trustworthy, precise, calm, and human;
- modern without resembling a speculative fintech;
- accessible to employees and credible to institutions;
- distinctly Malawian without placing a flag or map onto generic software;
- protective without appearing paternalistic.

Avoid generic shields, padlocks, coins, bank buildings, arrows, gradients, glossy
effects, and details that disappear at small sizes.

## Brand architecture

Affordax is one master brand:

- `affordax.com` — public information, education, and insights;
- `portal.affordax.com` — secure operational portal;
- emails, documents, presentations, social profiles, and future applications.

The portal is not a separate brand. It should use the same logo, palette,
typography, and voice, with stronger emphasis on functional UI and security.

## Provisional colour palette

These values are candidates for testing, not permanently locked colors.

| Token | Hex | Main role |
| --- | --- | --- |
| Affordax Ink | `#17202A` | Headings, wordmark, navigation, dark surfaces |
| Malawi Red | `#CE1126` | Main brand accent and active emphasis |
| Malawi Green | `#339E35` | Secondary accent and positive signals |
| Warm Paper | `#F3EFE6` | Editorial and human-centered backgrounds |
| White | `#FFFFFF` | Main surfaces and reversed marks |
| Slate | `#52616B` | Secondary text and quiet UI detail |

### Colour rules

1. Ink and White carry most of the visual identity.
2. Red is the main expressive accent; Green appears less frequently.
3. Red and Green should not have equal decorative weight except in an approved
   logo treatment.
4. Status must never depend on color alone. Pair it with text, shape, or icons.
5. Product warning, error, success, and information colors must remain
   semantically clear even when they differ from exact brand accents.
6. Text and controls must meet WCAG AA contrast requirements.

## Typography plan

Select typography after testing financial figures, tables, long operational
labels, Malawi names, and low-cost Android devices.

Requirements:

- an open, self-hostable licence;
- a distinctive but readable heading family;
- an efficient UI family for forms, tables, and dashboards;
- clear `I`, `l`, `1`, `O`, and `0` characters;
- English and Chichewa character support;
- dependable browser and PDF rendering.

The final wordmark should be custom-drawn or optically modified—not an untouched
font spelling Affordax.

## Logo direction

The preferred direction is a custom **A** called **Protected Horizon**. It should
combine:

- a recognisable A;
- a stable lower line representing a protected affordability floor;
- a rising opening representing progress and financial headroom;
- one deliberate structure representing accountability;
- an optional subtle contour inspired by Lake Malawi;
- restrained Red and Green detail grounded by Ink.

The Malawi reference should reward closer inspection. The mark must still work
without color or explanation.

Required variants include horizontal, stacked, symbol-only, one-color Ink,
reversed White, approved full color, and a simplified favicon/app icon.

## Visual language

Supporting graphics should use deliberate lines, protected spaces, connected
points, and measured curves. Photography should show real work, dignity, and
useful services in Malawi—not staged handshakes, cash piles, or generic offices.
Icons should share one stroke and corner language. Diagrams should explain real
relationships instead of filling space.

## Voice and messaging

Affordax speaks plainly, respectfully, and precisely:

- explain the mechanism before making a claim;
- use concrete language about affordability, reservations, deductions, and consent;
- sound confident but never absolute;
- treat employees as decision-makers, not risk profiles;
- avoid inflated claims such as “revolutionary” or “guaranteed.”

Provisional line for testing: **Affordability, accounted for.**

## Locked and flexible elements

Lock only after real-size testing:

- master logo geometry, proportions, clear space, and minimum size;
- wordmark spelling and approved lockups;
- RGB, HEX, CMYK, and print color definitions;
- typefaces and hierarchy;
- favicon and app-icon construction;
- icon, photography, and voice principles.

Page layouts, campaigns, article imagery, and secondary graphics can remain
flexible when they follow the locked foundation.

## Technical source of truth

After approval, maintain one canonical asset set:

```text
static/brand/
  logo/
    affordax-horizontal.svg
    affordax-stacked.svg
    affordax-mark.svg
    affordax-mark-small.svg
    affordax-mark-white.svg
  icons/
    favicon.svg
    favicon-32.png
    apple-touch-icon.png
    icon-192.png
    icon-512.png
  tokens/
    brand.css
docs/brand/
  BRAND-GUIDELINES.md
```

The public website and portal should consume the same approved SVG masters and
tokens. Remove duplicate hand-edited assets during rollout.

## Validation

Before approval, test the identity:

- at 16, 24, 32, 48, and 64 pixels;
- in one color, grayscale, dark mode, and reversed White;
- on inexpensive phones, office monitors, printouts, and PDFs;
- in a browser tab, public header, portal login, email, report, and social avatar;
- with color-blindness simulation and WCAG contrast checks;
- beside relevant banks, lenders, fintechs, and local institutions;
- for trademark conflicts before legal registration.

## Rollout

1. **Direction:** create three disciplined black-and-white directions from the
   logo brief and review recognition, meaning, and small-size performance.
2. **Refinement:** choose one, refine its geometry and wordmark, then test color.
3. **System:** finalize palette, typography, lockups, icons, guidelines, and CSS
   tokens.
4. **Implementation:** update the public website, portal, emails, documents, and
   social profiles with a checklist that removes conflicting legacy assets.
5. **Governance:** control editable masters and let product code use only approved
   exports and shared tokens.

## Approval gate

The brand can be locked when it is recognisable as Affordax, strong in one color,
clear at favicon size, credible in public and portal contexts, subtly Malawian,
accessible, reproducible, and cleared by a basic trademark search.

## Current implementation candidate

Direction A, Protected Horizon, is implemented on the public site under
`static/brand/`. It includes Ink and reversed logo marks, SVG and PNG browser
icons, shared CSS tokens, and the social preview treatment. This is a working
candidate for real-world testing, not final trademark-approved master artwork.
