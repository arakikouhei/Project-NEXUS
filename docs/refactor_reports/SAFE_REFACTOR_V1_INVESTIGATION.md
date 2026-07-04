# Safe Refactor v1 Investigation Report

Generated At: 2026-07-04T22:39:06

This report only investigates refactor candidates. It does not change source code.

## nexus/tools/knowledge.py

- Lines: 2430
- Classes: 1
- Functions/Methods: 89
- Patch Markers: 9
- Monkey Patch Indicators: 0

### Patch Markers
- L209: `# KNOWLEDGE_SEARCH_V2_SAFE_PATCH`
- L557: `# KNOWLEDGE_DIGEST_V1_SAFE_PATCH`
- L906: `# KNOWLEDGE_CLEANUP_V1_SAFE_PATCH`
- L1165: `# ARCHIVE_FILTER_V1_SAFE_PATCH`
- L1344: `# SOURCE_TRUST_V1_SAFE_PATCH`
- L1674: `# KNOWLEDGE_ANSWER_V1_SAFE_PATCH`
- L1900: `# KNOWLEDGE_ANSWER_V1_1_FIX`
- L2067: `# KNOWLEDGE_ANSWER_V2_NATURAL_PATCH`
- L2212: `# KNOWLEDGE_AUTO_RECALL_GUARD_V1_SAFE_PATCH`

### Classes
- L12: `class KnowledgeTool(BaseTool):`

### Refactor Risk Note
- High risk: many knowledge features were added by safe patches. Refactor only after full backup and tests.

## nexus/tools/diagnostics.py

- Lines: 691
- Classes: 1
- Functions/Methods: 25
- Patch Markers: 3
- Monkey Patch Indicators: 5

### Patch Markers
- L177: `# SYSTEM_HEALTH_V1_SAFE_PATCH`
- L509: `# SYSTEM_HEALTH_V2_RECOMMENDED_FIXES_PATCH`
- L601: `# SYSTEM_HEALTH_V2_RECOMMENDED_FIXES_PATCH`

### Monkey Patch Indicators
- L507: `ToolDiagnosticsTool.execute = _sh_v1_execute`
- L585: `if not hasattr(ToolDiagnosticsTool, "_system_health_v2_original_execute"):`
- L599: `ToolDiagnosticsTool.execute = _system_health_v2_execute`
- L677: `if not hasattr(ToolDiagnosticsTool, "_system_health_v2_original_execute"):`
- L691: `ToolDiagnosticsTool.execute = _system_health_v2_execute`

### Classes
- L13: `class ToolDiagnosticsTool(BaseTool):`

### Refactor Risk Note
- Medium risk: System Health and diagnostics patches are important for safety checks.

## nexus/agent/agent.py

- Lines: 405
- Classes: 1
- Functions/Methods: 7
- Patch Markers: 9
- Monkey Patch Indicators: 0

### Patch Markers
- L22: `# VISION_ROUTING_BYPASS_V2`
- L44: `# KNOWLEDGE_ROUTING_BYPASS_V1`
- L75: `# SOURCE_REGISTRY_ROUTING_BYPASS_V1`
- L97: `# WORLD_UPDATE_ROUTING_BYPASS_V1`
- L128: `# KNOWLEDGE_ANSWER_POLISH_V1`
- L189: `# KNOWLEDGE_ANSWER_POLISH_RESPECT_AUTO_RECALL_V1`
- L212: `# SYSTEM_HEALTH_ROUTING_BYPASS_V1`
- L254: `# KNOWLEDGE_AUTO_RECALL_V1`
- L360: `# PAPER_INTAKE_ROUTING_BYPASS_V1`

### Classes
- L12: `class NexusAgent:`

### Refactor Risk Note
- High risk: routing and bypass order can change behavior.

## nexus/tools/project_memory.py

- Lines: 400
- Classes: 1
- Functions/Methods: 18
- Patch Markers: 1
- Monkey Patch Indicators: 2

### Patch Markers
- L193: `# PROJECT_MEMORY_V2_UPDATE_PATCH`

### Monkey Patch Indicators
- L391: `ProjectMemoryTool.execute = execute_v2`
- L398: `if not hasattr(ProjectMemoryTool, "_project_memory_v2_patched"):`

### Classes
- L18: `class ProjectMemoryTool(BaseTool):`

### Refactor Risk Note
- Medium risk: v2 update patch can be folded into the class later.

## nexus/tools/manager.py

- Lines: 99
- Classes: 1
- Functions/Methods: 3
- Patch Markers: 0
- Monkey Patch Indicators: 0

### Classes
- L42: `class ToolManager:`

### Refactor Risk Note
- Medium risk: tool registration order matters.

