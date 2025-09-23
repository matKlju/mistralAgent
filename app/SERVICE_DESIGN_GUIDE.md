# Service Design Guide

This guide distils the conventions observed in the bundled service templates. Use it to understand the expected flow, node ordering, and field usage when generating new services.

## 1. Overall Flow
- Services progress linearly unless a condition explicitly introduces branching.
- Every service must start with a `start` node and finish with a `finishing-step` node.
- Between start and finish, steps are ordered to first prepare data, then call external APIs, transform results, and finally communicate with the client.

```
start → assign variables → [optional endpoint call] → transform/prepare output → client message → finish
```

## 2. Required Node Types
- **Start (`type": "start"`)**
  - Non-selectable, non-draggable.
  - Contains `data.type = "start"`.
- **Assign (`stepType": "assign"`)**
  - Used to initialise variables or compute derived values.
  - `assignElements` holds key/value pairs, each with its own UUID `id`.
- **User-defined / Endpoint Step (`stepType": "user-defined"`) – optional**
  - When the service needs external data, add this step to perform the API call.
  - Must reference an `endpoint` definition with HTTP method, params, headers, and body structure.
- **Transform Assign (`stepType": "assign"`)**
  - Parses API responses and stores reusable fields for later steps.
- **Message (`stepType": "textfield"`)**
  - Sends templated HTML/Markdown strings to the client.
- **Finish (`stepType": "finishing-step-end"`)**
  - Read-only node marking the end of the workflow.

### Example Reference Services
- **National holidays lookup** (`app/examples/test_context.json`): demonstrates a linear flow that fetches an external API, transforms the response, and produces a localized summary.
- **Support triage with branching** (`app/examples/sample_service_branching.json`): showcases a condition node that splits urgent versus standard handling, including an optional knowledge-base API call and tailored messaging per branch.

## 3. Edge Ordering
- Edges connect nodes sequentially; each edge’s `source` and `target` must map to node UUIDs.
- Success paths should be labelled `"+"` when there is no branching.
- When conditions or branching are introduced, provide descriptive labels (e.g., `"Success"`, `"Failure"`).

## 4. Variable Conventions
- Variables are established via `assignElements` and referenced using `${variableName}` syntax.
- Keep variable names descriptive (`startDate`, `responseData`, `last`).
- When computing derived values, store intermediate results to avoid re-computation.
- API parameters should reference previously assigned variables.

## 5. Endpoint Definitions
- Each endpoint includes:
  - `endpointId` (UUID) and `name` for reusability across nodes.
  - `definitions` array with HTTP method, request data, headers, params, and `url` preview.
  - `serviceId` referencing the backend service if available.
- Parameters in `definitions[].params.variables` may use literal values or `${variable}` references.
- Mark the active definition with `isSelected = true`.

## 6. Client Messaging
- Final messaging steps interpolate computed variables to produce human-readable responses.
- Content can be HTML inside `<p>` tags or plain text.
- Ensure the message reflects the user’s request and uses context-specific data.

## 7. Testing Metadata
- Each node tracks `testingPassed` to indicate validation status. Set to `true` when the step has been verified.
- Nodes may include UI hints (`className`, `measured`, `selectable`, `draggable`) for front-end rendering; preserve these fields when generating new services.

## 8. UUID Handling
- Every node and edge requires a unique UUID `id`.
- `assignElements` entries also require unique UUIDs.
- When regenerating services, refresh all UUIDs to avoid collisions.

## 9. Extending Beyond Linear Flows
- To implement branching, insert condition nodes (`stepType": "condition"`) with rule sets in `data.rules`.
- Ensure each branch ultimately reconnects or terminates with a finishing-step.
- Provide clear edge labels for each branch outcome.

## 10. Applying the Guide
When generating a new service:
1. **Parse the user brief** (from the regular prompt) to identify required inputs, external data sources, and expected outputs.
2. **Lay out the nodes** following the canonical order, inserting additional assign/condition steps as needed.
3. **Configure endpoints** with appropriate query/body parameters, reusing variable names established earlier.
4. **Transform and format data** so the message step speaks naturally to the end user.
5. **Validate the graph**: all nodes reachable from start, edges wired with UUIDs, and finish node present.

Keep this guide close to the system prompt so the model internalises structure and can adapt it to new domains while staying compliant with the service framework.

## 11. Checklist Alignment
The structured checklist in `app/SERVICE_CHECKLIST.json` formalises non-negotiable rules (UUID usage, node ordering, edge labelling, message placement). Verify that every generated service complies before returning the final JSON.
