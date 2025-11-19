# PostgreSQL Docker 管理脚本
# 使用方法: .\manage_postgres.ps1 [start|stop|restart|status|logs|shell|backup|clean]

param(
    [Parameter(Position=0)]
    [ValidateSet('start','stop','restart','status','logs','shell','backup','clean','reset')]
    [string]$Action = 'status'
)

$ContainerName = "fastapi-postgres"
$DbUser = "fastapi_user"
$DbName = "fastapi_db"

function Show-Status {
    Write-Host "`n=== PostgreSQL 容器状态 ===" -ForegroundColor Cyan
    docker ps -a --filter "name=$ContainerName" --format "table {{.Names}}`t{{.Status}}`t{{.Ports}}"
}

function Start-Container {
    Write-Host "`n启动 PostgreSQL 容器..." -ForegroundColor Green
    docker start $ContainerName
    Start-Sleep -Seconds 2
    Show-Status
}

function Stop-Container {
    Write-Host "`n停止 PostgreSQL 容器..." -ForegroundColor Yellow
    docker stop $ContainerName
    Show-Status
}

function Restart-Container {
    Write-Host "`n重启 PostgreSQL 容器..." -ForegroundColor Cyan
    docker restart $ContainerName
    Start-Sleep -Seconds 2
    Show-Status
}

function Show-Logs {
    Write-Host "`n=== PostgreSQL 日志 (按 Ctrl+C 退出) ===" -ForegroundColor Cyan
    docker logs -f $ContainerName
}

function Enter-Shell {
    Write-Host "`n进入 PostgreSQL 命令行 (输入 \q 退出)..." -ForegroundColor Green
    docker exec -it $ContainerName psql -U $DbUser -d $DbName
}

function Backup-Database {
    $BackupFile = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql"
    Write-Host "`n备份数据库到: $BackupFile" -ForegroundColor Green
    docker exec $ContainerName pg_dump -U $DbUser $DbName > $BackupFile
    Write-Host "✅ 备份完成!" -ForegroundColor Green
}

function Clean-All {
    Write-Host "`n⚠️  警告: 这将删除容器和所有数据!" -ForegroundColor Red
    $confirm = Read-Host "确认删除? (yes/no)"
    if ($confirm -eq 'yes') {
        docker stop $ContainerName
        docker rm $ContainerName
        docker volume rm fastapi-postgres-data
        Write-Host "✅ 清理完成!" -ForegroundColor Green
    } else {
        Write-Host "已取消" -ForegroundColor Yellow
    }
}

function Reset-Database {
    Write-Host "`n重置数据库表..." -ForegroundColor Cyan
    python test_pg_connection.py
}

# 执行命令
switch ($Action) {
    'start'   { Start-Container }
    'stop'    { Stop-Container }
    'restart' { Restart-Container }
    'status'  { Show-Status }
    'logs'    { Show-Logs }
    'shell'   { Enter-Shell }
    'backup'  { Backup-Database }
    'clean'   { Clean-All }
    'reset'   { Reset-Database }
}
