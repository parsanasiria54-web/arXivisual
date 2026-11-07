# Run-AllMasterclassTests.ps1

Write-Host "Running All Masterclass Tests..." -ForegroundColor Cyan

# Run Pytest across all modules
uv run pytest backend/core_llm/tests backend/core_tts/tests backend/core_ingestion/tests backend/cs_pedagogy/tests backend/multi_renderer/tests backend/core_orchestrator/tests --maxfail=1 --disable-warnings -q

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] All Tests Passed!" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Some tests failed. Please review the output above." -ForegroundColor Red
}
