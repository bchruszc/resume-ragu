"""Mock AI client for testing."""

from app.ai.client import AIClient, AIResponse
from app.errors import AIServiceError


class MockAIClient(AIClient):
    """Mock implementation of AIClient for testing."""

    def __init__(self):
        """Initialize mock client."""
        self.call_history: list[dict] = []
        self.custom_response: str | None = None
        self.should_raise_error: bool = False

    async def generate(
        self, system_prompt: str, messages: list[dict], model: str | None = None
    ) -> AIResponse:
        """
        Generate a mock AI response.

        Args:
            system_prompt: System prompt
            messages: Message history
            model: Model name (ignored in mock)

        Returns:
            AIResponse with canned content

        Raises:
            AIServiceError: If configured to simulate error
        """
        # Record the call
        self.call_history.append({
            "system_prompt": system_prompt,
            "messages": messages,
            "model": model,
        })

        # Simulate error if configured
        if self.should_raise_error:
            raise AIServiceError("Mock AI service error")

        # Return custom response if set
        if self.custom_response:
            return AIResponse(
                content=self.custom_response,
                model=model or "mock-model",
                usage={"input_tokens": 100, "output_tokens": 200},
            )

        # Generate canned response based on heuristics
        last_message = messages[-1]["content"].lower() if messages else ""

        if "leadership" in last_message:
            content = self._leadership_resume()
        elif "technical" in last_message or "engineer" in last_message:
            content = self._technical_resume()
        else:
            content = self._generic_resume()

        return AIResponse(
            content=content,
            model=model or "mock-model",
            usage={"input_tokens": 150, "output_tokens": 300},
        )

    def set_custom_response(self, response: str) -> None:
        """Configure a custom response for the next generate() call."""
        self.custom_response = response

    def simulate_error(self, should_raise: bool = True) -> None:
        """Configure whether to raise an error on the next generate() call."""
        self.should_raise_error = should_raise

    def reset(self) -> None:
        """Reset call history and configuration."""
        self.call_history = []
        self.custom_response = None
        self.should_raise_error = False

    def _generic_resume(self) -> str:
        """Generic canned resume response."""
        return """# Jane Doe

jane@example.com | 555-123-4567 | San Francisco, CA | linkedin.com/in/janedoe

## Professional Summary

Experienced software engineer with 8+ years building scalable systems and leading technical initiatives. Expertise in Python, cloud architecture, and team leadership.

## Experience

### Senior Software Engineer | Acme Corp
*Jan 2020 - Present*

- Led migration of monolithic application to microservices, reducing deployment time by 80%
- Architected cloud infrastructure serving 1M+ daily users with 99.9% uptime
- Mentored team of 5 engineers and established code review best practices

### Software Engineer | TechCo
*Jun 2017 - Dec 2019*

- Developed REST APIs handling 100K+ requests/day
- Improved query performance by 60% through database optimization
- Contributed to open-source Python libraries

## Skills

**Languages**: Python, JavaScript, SQL
**Frameworks**: FastAPI, React, Django
**Infrastructure**: AWS, Docker, Kubernetes
"""

    def _leadership_resume(self) -> str:
        """Leadership-focused canned resume."""
        return """# Jane Doe

jane@example.com | 555-123-4567 | San Francisco, CA

## Professional Summary

Engineering leader with proven track record of building and scaling high-performing teams. 8+ years of experience driving technical strategy and delivering complex projects.

## Experience

### Senior Software Engineer & Tech Lead | Acme Corp
*Jan 2020 - Present*

- **Leadership**: Led cross-functional team of 8 engineers across 3 major product initiatives
- **Technical Strategy**: Drove architectural decisions for microservices migration, reducing deployment time by 80%
- **Mentorship**: Established mentorship program that improved team retention by 40%
- **Project Management**: Delivered 5 major features on time with zero production incidents

### Software Engineer | TechCo
*Jun 2017 - Dec 2019*

- Led design reviews and established team coding standards
- Mentored 3 junior engineers to promotion
- Coordinated with product team to define technical roadmap
"""

    def _technical_resume(self) -> str:
        """Technical-focused canned resume."""
        return """# Jane Doe

jane@example.com | 555-123-4567 | San Francisco, CA | github.com/janedoe

## Professional Summary

Full-stack software engineer specializing in scalable backend systems, cloud architecture, and modern web technologies. Passionate about clean code and system design.

## Experience

### Senior Software Engineer | Acme Corp
*Jan 2020 - Present*

- **Backend**: Built microservices architecture using FastAPI, handling 1M+ requests/day
- **Cloud**: Designed AWS infrastructure with Lambda, SQS, DynamoDB for 99.9% uptime
- **Performance**: Optimized database queries reducing response time from 2s to 200ms
- **DevOps**: Implemented CI/CD pipeline cutting deployment time from 2 hours to 15 minutes

## Technical Skills

**Languages**: Python, JavaScript, TypeScript, SQL, Bash
**Backend**: FastAPI, Django, Flask, Node.js
**Frontend**: React, TypeScript, HTML/CSS
**Databases**: PostgreSQL, DynamoDB, Redis
**Infrastructure**: AWS (Lambda, EC2, S3, SQS), Docker, Kubernetes, Terraform
**Tools**: Git, GitHub Actions, Pytest, Jest
"""
