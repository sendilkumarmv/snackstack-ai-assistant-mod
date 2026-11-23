OrchestratorDecisionSchema = {
    "title": "OrchestratorDecision",
    "description": "The orchestrator's routing decision.",
    "type": "object",
    "properties": {
        "reasoning": {
            "type": "string",
            "description": "Brief explanation of why this agent chosen",
        },
        "agents": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["menu_agent"],
            },
            "description": (
                "Agent to dispatch. Use an empty list when the query "
                "is not appropriate for SnackStack."
            ),
        },
    },
    "required": ["reasoning", "agents"],
}
