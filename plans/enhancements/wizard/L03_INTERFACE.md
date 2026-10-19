# L03: Interface and experience

Status: layer design. Uses [the shared contract](LAYER_CONTRACT.md) and
[technology tree model](TREE_MODEL.md). Parent: [P8](../P8_LAYERED_WIZARD.md).

## Purpose, applicability and inputs

Develop the selected user-facing interactions from L01 targets and L02 framework
trees. Visual UI questions are N/A for a headless deliverable, with a reason; a CLI
still needs command, output and error interaction design.

## Decision tree and nested steps

| Node | Decision and options | Branch or follow-up |
| --- | --- | --- |
| L03.01 | Interface channels: browser, desktop, mobile, CLI, admin UI, mixed, none | Create an interface branch per target; none skips visual choices only |
| L03.02 | Framework-specific presentation/execution model | Resolve the selected technology's component/template/native-view tree |
| L03.03 | Main journeys, navigation, routing and state | Ask only journeys in scope; link state persistence and access boundaries |
| L03.04 | Existing component/design system or new visual direction | Reuse current controls/tokens and inspect component provenance/version |
| L03.05 | Forms, input validation and visible error/empty/loading/cancelled states | Keep server/domain validation authoritative; avoid false success |
| L03.06 | Accessibility, keyboard/touch, responsive/device layout, localization/RTL | Derive applicable targets from real users and project obligations |
| L03.07 | UI Notification Service, progress, safe messages and recovery | Visual UI → shared adapter; headless → N/A reason and retain other notifications |
| L03.08 | Interaction acceptance scenarios | Define browser/device/assistive-technology checks where required |

Framework branches differ: Blazor asks about rendering/interactivity and component
boundaries; Django template sites ask about views/templates/forms and optional
client enhancement; a React application uses its chosen framework's rendering,
routing and client state tree; desktop/native-mobile profiles ask about their own
view/navigation/device lifecycle. A Python framework never receives Blazor modes.

## Dependencies and change effects

L03 owns interaction choices and consumes L04 persistence/sync, L05 permissions,
L06 notification contracts and L07 delivery constraints. Offline or multi-tenant
changes flag affected flows and recipient isolation for review. Interface visibility
never becomes the authoritative access control.

## Outputs and completion checks

Produce interaction maps, selected framework branches, component reuse, accessibility
and localization requirements, notification behavior and measurable acceptance cases
in the current SDD/specification. Check every required flow has truthful outcomes
and an applicable runtime test. Do not infer visual acceptance from source alone.

## Reference and standards needs

Record framework/component guidance, chosen accessibility requirements and device
platform expectations with sources/version applicability. Applicable standards and
actual validation remain explicit; this design does not claim accessibility compliance.
