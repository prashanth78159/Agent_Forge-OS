
import uuid

from app.services.llm_service import LLMService

from app.core.agents.planner_agent import PlannerAgent
from app.core.agents.research_agent import ResearchAgent
from app.core.agents.writer_agent import WriterAgent
from app.core.agents.critic_agent import CriticAgent

from app.core.memory.memory_manager import MemoryManager
from app.core.memory.vector_memory import VectorMemory

from app.core.observability.tracer import ExecutionTracer
from app.core.replay.execution_store import ExecutionStore

from app.core.metrics.metrics_manager import MetricsManager


class AgentOrchestrator:

    def __init__(
        self,
        llm_provider,
        api_key,
        model_name
    ):

        self.llm_service = LLMService(
            llm_provider,
            api_key,
            model_name
        )

        self.metrics_manager = (
            MetricsManager()
        )

        self.planner = PlannerAgent(
            "Planner",
            self.llm_service,
            self.metrics_manager
        )

        self.researcher = ResearchAgent(
            "Researcher",
            self.llm_service,
            self.metrics_manager
        )

        self.writer = WriterAgent(
            "Writer",
            self.llm_service,
            self.metrics_manager
        )

        self.critic = CriticAgent(
            "Critic",
            self.llm_service,
            self.metrics_manager
        )

        self.memory = MemoryManager()
        self.long_term_memory = VectorMemory()

        self.tracer = ExecutionTracer()
        self.store = ExecutionStore()

    def classify_input(
        self,
        task
    ):

        if task.lower().strip() in [
            "hi",
            "hello",
            "hey"
        ]:
            return "simple"

        return "complex"

    def run(
        self,
        task
    ):

        mode = self.classify_input(
            task
        )

        if mode == "simple":

            return {

                "execution_id":
                    "simple",

                "final":
                    "Hello 👋 How can I help you?",

                "logs":
                    []
            }

        self.tracer = ExecutionTracer()

        execution_id = (
            "exec_"
            + str(
                len(
                    self.store.executions
                )
            )
        )

        self.metrics_manager.start_execution(
            execution_id
        )

        context = {}

        session_id = "default"

        memory_context = str(
            self.memory.get(
                session_id
            )
        )

        planner_input = (
            task
            + "\n\n"
            + memory_context
        )

        plan = self.planner.run(
            planner_input,
            context
        )

        self.tracer.log(
            "planner",
            planner_input,
            plan
        )

        research = self.researcher.run(
            plan,
            context
        )

        self.tracer.log(
            "research",
            plan,
            research
        )

        draft = self.writer.run(
            research,
            context
        )

        self.tracer.log(
            "writer",
            research,
            draft
        )

        final = self.critic.run(
            draft,
            context
        )

        self.tracer.log(
            "critic",
            draft,
            final
        )

        logs = self.tracer.get_logs()

        self.store.save(
            execution_id,
            logs
        )

        return {

            "execution_id":
                execution_id,

            "plan":
                plan,

            "research":
                research,

            "draft":
                draft,

            "final":
                final,

            "logs":
                logs
        }
