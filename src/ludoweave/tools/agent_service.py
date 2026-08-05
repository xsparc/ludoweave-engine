"""Trusted composition helpers for local CLI and MCP agent adapters."""

from ludoweave.agent import AgentCapabilities, AgentCommandService, AgentProject
from ludoweave.tools.headless_project import HeadlessProject
from ludoweave.world import CommandActor, WorldSession


def headless_agent_service(
    project: HeadlessProject,
    session: WorldSession,
    *,
    actor: CommandActor,
    write: bool,
) -> AgentCommandService:
    """Compose the data-only headless project without loading executable project code."""

    return AgentCommandService(
        session,
        project.snapshot_codec,
        AgentProject(
            project.world_id,
            project.world_id,
            project.project_schema,
            project.dependency_lock_hash,
            project.platform_profile,
            "Data-only local headless project.",
        ),
        actor,
        capabilities=AgentCapabilities(write=write),
        timeline_id="local-agent-session",
    )
