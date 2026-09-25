# Element Confetti Code Writer — implementation report

## Question answered

Can a tool select a webpage element and write code for a `canvas-confetti` canvas with that element's dimensions?

**Answer:** Yes. This repository contains a load-unpacked Manifest V3 browser extension. Clicking its toolbar button starts an in-page picker; clicking an element measures its rendered border box and opens a dialog containing copyable HTML/JavaScript. The generated code creates a canvas with the captured width and height, positions it over a selector for the chosen element, creates a custom `canvas-confetti` instance, fires it, and removes the canvas after five seconds.

## Attributable evidence and design basis

### Facts from primary or authoritative sources

- `Element.getBoundingClientRect()` returns a `DOMRect` describing an element's viewport position and size. Its `width` and `height` cover the rendered border box (including padding and border). This is the API used by `content.js` to measure the picked element. [MDN: `getBoundingClientRect()`](https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect)
- Transforms affect the rendered dimensions returned by `getBoundingClientRect()`, while `offsetWidth`/`offsetHeight` represent layout dimensions and are integer-rounded. The implementation intentionally uses the rendered dimensions because the requested canvas should visually match what was picked. [MDN: Determining the dimensions of elements](https://developer.mozilla.org/en-US/docs/Web/API/CSS_Object_Model/Determining_the_dimensions_of_elements)
- The library's documented `confetti.create(canvas, options)` API creates an instance bound to a custom canvas. Its documentation says `resize: true` lets the library set and maintain the canvas bitmap size, and recommends retaining one instance rather than recreating it on the same canvas. The generated snippet creates one instance, enables resizing, and calls it once. [canvas-confetti repository documentation](https://github.com/catdad/canvas-confetti#confetticreatecanvas-globaloptions--function)
- The library documents `disableForReducedMotion: true` as disabling animation when the user prefers reduced motion. The generated code enables it. [canvas-confetti repository documentation](https://github.com/catdad/canvas-confetti#reduced-motion)
- Chrome documents a required root `manifest.json` and Manifest V3 structure. The delivered `manifest.json` follows that structure. [Chrome Extensions: Manifest file format](https://developer.chrome.com/docs/extensions/reference/manifest)
- Chrome documents that extension capabilities are declared through keys such as `permissions` and that host/content-script access can produce warnings. This implementation uses only `activeTab` and `scripting`, injecting after an explicit toolbar click rather than requesting persistent access to all sites. [Chrome Extensions: Declare permissions](https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions)

### Facts verified directly in the deliverable

- `manifest.json` declares Manifest V3, an action, a service worker, and exactly two permissions: `activeTab` and `scripting`.
- `service-worker.js` restricts startup to HTTP(S) tabs and injects `content.js` only after the toolbar action is clicked.
- `content.js` installs capture-phase hover/click handlers, draws an isolated Shadow DOM highlight UI, calls `getBoundingClientRect()`, rounds each positive dimension upward, and writes those numbers into both canvas attributes and CSS dimensions.
- The picker can be cancelled with Escape, replaces an earlier picker instance when restarted, provides a clipboard fallback, and removes its UI/listeners when closed.

## Inferences and rationale

- **Inference:** rendered border-box dimensions are the closest practical interpretation of “dimensions of the element.” Other interpretations—content box, layout box, or full scrollable content—are possible, but would make the canvas disagree with the visible picked outline in transformed or bordered cases.
- **Inference:** a user-initiated extension is a more generally useful “Element Picker” than a DevTools-only `$0` console snippet because it supplies highlighting, selection, and output UI directly on ordinary pages.
- **Inference:** rounding fractional CSS pixels upward avoids clipping the selected rendered area. This means a fractional dimension can produce a canvas less than one CSS pixel larger on an axis.

## Uncertainty and unanswered questions

- The task does not specify Chrome, Firefox, or a DevTools integration. The implementation targets Chrome/Chromium Manifest V3 and has not been claimed as Firefox-compatible.
- The generated selector reflects the DOM at selection time. Dynamic pages can invalidate it, duplicate IDs can make it ambiguous, and elements inside inaccessible closed shadow roots or cross-origin frames cannot be targeted from the top document.
- The generated snippet loads `canvas-confetti@1.9.4` from jsDelivr. It will not run offline, and a target page's Content Security Policy may block the external script or inline script. In that situation the dependency and generated JavaScript must be integrated into that page's existing build/CSP setup.
- The generated fixed positioning re-measures the target's viewport coordinates when the snippet starts. Scrolling, DOM movement, or layout changes during the five-second animation can move the target without moving the canvas; the captured canvas dimensions remain unchanged.
- Automated end-to-end browser verification was not available under the assignment's `none` execution/check profile. Static syntax and manifest validation are the appropriate local checks recorded for this delivery; they do not independently prove browser behavior.
