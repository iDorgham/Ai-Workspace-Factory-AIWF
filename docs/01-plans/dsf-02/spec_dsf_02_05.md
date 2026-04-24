# 📐 spec_dsf_02_05: Persistent AIChat Dashboard Integration

Integrates the validated Sovereign-UI AIChat component into a persistent dashboard sidebar for real-time agent interaction.

## 📋 Narrative
The AI agent is a permanent collaborator in the workspace. We integrate the `AIChat` component into a **Persistent Sidebar** or **Floating Drawer** that maintains its state (message history, typing status) across route changes. This ensures a seamless conversational experience without losing context during navigation.

## 🛠️ Key Details
- **Component**: `PersistentChat`.
- **State Management**: Zustand (Shared history).
- **Logic**: Route-agnostic persistence.

## 📋 Acceptance Criteria
- [ ] 0ms chat re-render on dashboard route transitions.
- [ ] Message history persists during browser refreshes (LocalStore sync).
- [ ] Verified RTL avatar and bubble alignment in persistent mode.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-02
evolution_hash: sha256:dsf-v20-02-05-e5f6g7
acceptance_criteria:
  - chat_state_persistence_verified
  - navigation_re-render_block_pass
  - rtl_chat_equilibrium_100
test_fixture: tests/shard/chat_integration_audit.py
regional_compliance: LAW151-MENA-AGENT-PRIVACY
```
