# Schema RAG - File Organization Script (PowerShell)
# This script organizes all files into proper folders

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Schema RAG - File Organization" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Create directories
Write-Host ""
Write-Host "Creating directories..." -ForegroundColor Yellow
$dirs = @("docs", "core", "infrastructure", "tests", "data")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Name $dir | Out-Null
        Write-Host "✓ Created $dir/" -ForegroundColor Green
    }
}

# Move documentation files
Write-Host ""
Write-Host "Moving documentation files..." -ForegroundColor Yellow
$docFiles = @(
    "00_START_HERE.md",
    "COMPLETE_SUMMARY.md",
    "EXECUTION_CHECKLIST.md",
    "FINAL_SETUP_INSTRUCTIONS.md",
    "NVIDIA_EMBEDDINGS_GUIDE.md",
    "PIPELINE_SUMMARY.md",
    "SCHEMA_RAG_README.md",
    "SCHEMA_RAG_SETUP.md"
)
foreach ($file in $docFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "docs/$file" -Force
        Write-Host "✓ Moved $file to docs/" -ForegroundColor Green
    }
}

# Move core pipeline files
Write-Host ""
Write-Host "Moving core pipeline files..." -ForegroundColor Yellow
$coreFiles = @(
    "metadata_extractor.py",
    "nvidia_summarizer.py",
    "qdrant_manager.py",
    "pipeline.py"
)
foreach ($file in $coreFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "core/$file" -Force
        Write-Host "✓ Moved $file to core/" -ForegroundColor Green
    }
}

# Move infrastructure files
Write-Host ""
Write-Host "Moving infrastructure files..." -ForegroundColor Yellow
$infraFiles = @(
    "docker-compose.yml",
    ".env.example",
    "requirements.txt"
)
foreach ($file in $infraFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "infrastructure/$file" -Force
        Write-Host "✓ Moved $file to infrastructure/" -ForegroundColor Green
    }
}

# Move test files
Write-Host ""
Write-Host "Moving test files..." -ForegroundColor Yellow
$testFiles = @(
    "test_nvidia_embeddings.py",
    "quickstart.ps1",
    "quickstart.sh"
)
foreach ($file in $testFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "tests/$file" -Force
        Write-Host "✓ Moved $file to tests/" -ForegroundColor Green
    }
}

# Move data files
Write-Host ""
Write-Host "Moving data files..." -ForegroundColor Yellow
$dataFiles = @(
    "erp_data.db",
    "erp_schema_dump.sql",
    "generate_fake_data.py",
    "randomschemas.py",
    "table_metadata.json",
    "table_summaries.json"
)
foreach ($file in $dataFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "data/$file" -Force
        Write-Host "✓ Moved $file to data/" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "File Organization Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Directory Structure:" -ForegroundColor Yellow
Write-Host "docs/                    - Documentation" -ForegroundColor Cyan
Write-Host "core/                    - Pipeline scripts" -ForegroundColor Cyan
Write-Host "infrastructure/          - Docker & config" -ForegroundColor Cyan
Write-Host "tests/                   - Test scripts" -ForegroundColor Cyan
Write-Host "data/                    - Database & schemas" -ForegroundColor Cyan
Write-Host "main.py                  - FastAPI app" -ForegroundColor Cyan
Write-Host "database.py              - DB config" -ForegroundColor Cyan
Write-Host "models.py                - Data models" -ForegroundColor Cyan

