import asyncio
import sys
import json
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Any, List

WORKSPACE_ROOT = Path(__file__).parent.resolve()
TEST_MATRIX_DIR = WORKSPACE_ROOT / "dcs" / "tests" / "sdlc"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (SovereignHost) %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

@dataclass
class HostState:
    active_workers: int = 0
    total_tests_discovered: int = 0
    conformance_rating: float = 1.0
    status: str = "INITIALIZING"

class SovereignHostEngine:
    def __init__(self):
        self.state = HostState()
        self.log_buffer: List[Dict[str, Any]] = []

    def discover_local_matrices(self) -> List[Path]:
        if not TEST_MATRIX_DIR.exists():
            return []
        return sorted(list(TEST_MATRIX_DIR.glob("test_sdlc_*.py")))

    async def execute_isolated_suite(self, test_file: Path) -> Dict[str, Any]:
        process = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "pytest", str(test_file), "-q",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        success = (process.returncode == 0)
        return {
            "matrix_id": test_file.stem,
            "status": "CONFORMANT" if success else "NON_CONFORMANT",
            "exit_code": process.returncode
        }

    async def spin_engine(self):
        matrices = self.discover_local_matrices()
        self.state.total_tests_discovered = len(matrices)
        
        if self.state.total_tests_discovered == 0:
            self.state.status = "IDLE_EMPTY"
            logging.warning("No generated testing tracks available.")
            return

        self.state.status = "RUNNING"
        sem = asyncio.Semaphore(4) 
        
        async def worker(matrix_file: Path):
            async with sem:
                self.state.active_workers += 1
                result = await self.execute_isolated_suite(matrix_file)
                self.log_buffer.append(result)
                self.state.active_workers -= 1

        await asyncio.gather(*(worker(m) for m in matrices))
        
        failures = [r for r in self.log_buffer if r["status"] == "NON_CONFORMANT"]
        self.state.conformance_rating = 1.0 - (len(failures) / len(self.log_buffer)) if self.log_buffer else 1.0
        self.state.status = "COMPLIANT" if not failures else "DEGRADED"
        
        print("\n=== ENGINE STATE Snap-Shot ===")
        print(json.dumps(asdict(self.state), indent=2))

if __name__ == "__main__":
    asyncio.run(SovereignHostEngine().spin_engine())
