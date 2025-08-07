from crewai import Agent, Task, Crew, Process,LLM
from crewai_tools import MCPServerAdapter


ollama_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434",
    temperature=0.10
)


server_params = {
    "url": "http://127.0.0.1:11436/mcp/",
    "transport": "streamable-http"
}

try:
    with MCPServerAdapter(server_params) as tools:
        print(f"Available tools from Streamable HTTP MCP server: {[tool.name for tool in tools]}")

        http_agent = Agent(
            role="HTTP Service Integrator",
            goal="Utilize tools from a remote MCP server via Streamable HTTP.",
            backstory="AI agent capable of multi tool calling from HTTP MCP Server",
            tools=tools,
            verbose=True,
            llm=ollama_llm
        )

        http_task = Task(
            description="C:/Users/emrec/Desktop/merged_bands2.jp2 dosyasını analiz et minx:790000 miny:4080000 maxx:800000 maxy:4090000 noktalarından kırp ve pngye çevir",
            expected_output="The result json parameters of the tool",
            agent=http_agent,

        )

        # http_task2 = Task(
        #     description="C:/Users/emrec/Desktop/merged_bands2.jp2 dosyasını minx:790000 miny:4080000 maxx:800000 maxy:4090000 noktalarından kırp ve pngye çevir",
        #     expected_output="The result json parameters of the tool",
        #     agent=http_agent,
        # )

        http_crew = Crew(
            agents=[http_agent],
            tasks=[http_task],
            verbose=True,
            process=Process.sequential
        )

        result = http_crew.kickoff()
        print("\nCrew Task Result (Streamable HTTP - Managed):\n", result)

except Exception as e:
    print(f"Error connecting to or using Streamable HTTP MCP server (Managed): {e}")
    print("Ensure the Streamable HTTP MCP server is running and accessible at the specified URL.")