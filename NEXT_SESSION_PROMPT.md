# Next Session Prompt

We are resuming the AeonVoice packaging strategy for Supertoys.

Context:
- Existing packages: `AeonVoice`, `AeonVoice.Native` (~1500 downloads total).
- We decided to migrate branding to:
  - `Supertoys.AeonVoice`
  - `Supertoys.AeonVoice.Native`
- We will NOT include GPL voices in core packages.
- We will use permissive/commercial voice licensing.
- Voice packaging target:
  - `Supertoys.AeonVoice.Voice.Leena`
  - `Supertoys.AeonVoice.Voice.Alan`
  - optional meta-package: `Supertoys.AeonVoice.Voices.Standard` (depends on both)

What I need now:
1. Produce a concrete migration plan with phases and rollback points.
2. Draft `.csproj` templates for all packages above (NuGet metadata included).
3. Define compatibility/shim strategy for old package IDs (`AeonVoice*`) with deprecation plan.
4. Propose runtime voice discovery/loading design with fallback behavior.
5. Create a release checklist for CI/CD + validation across target RIDs.
6. Draft consumer-facing migration notes (`old -> new`) and install snippets.

Constraints:
- Minimize breaking changes for current users.
- Keep assembly/API stability where possible.
- No GPL assets in core or default distribution.
- Keep voice asset versioning independent from engine versioning.

Please give:
- A recommended final package graph,
- The exact first release sequence (version suggestions included),
- Ready-to-copy file snippets and checklist items.
