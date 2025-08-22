#!/bin/bash

# Instagram Analysis SaaS - Cron Jobs
# Add these to your crontab with: crontab -e

# Daily scraping job at 2 AM
# 0 2 * * * /home/git/instagram-audience-saas/infra/cron_jobs.sh daily_scraping

# Weekly analysis job every Sunday at 3 AM  
# 0 3 * * 0 /home/git/instagram-audience-saas/infra/cron_jobs.sh weekly_analysis

# Monthly cleanup job on 1st of each month at 1 AM
# 0 1 1 * * /home/git/instagram-audience-saas/infra/cron_jobs.sh monthly_cleanup

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

case "$1" in
    daily_scraping)
        echo "$(date): Starting daily scraping job" >> "$LOG_DIR/cron.log"
        cd "$PROJECT_DIR/backend"
        python -c "
import asyncio
from app.services.scheduler import SchedulerService
asyncio.run(SchedulerService().daily_scraping_job())
" >> "$LOG_DIR/daily_scraping.log" 2>&1
        echo "$(date): Daily scraping job completed" >> "$LOG_DIR/cron.log"
        ;;
    
    weekly_analysis)
        echo "$(date): Starting weekly analysis job" >> "$LOG_DIR/cron.log"
        cd "$PROJECT_DIR/backend"
        python -c "
import asyncio
from app.services.scheduler import SchedulerService
asyncio.run(SchedulerService().weekly_analysis_job())
" >> "$LOG_DIR/weekly_analysis.log" 2>&1
        echo "$(date): Weekly analysis job completed" >> "$LOG_DIR/cron.log"
        ;;
    
    monthly_cleanup)
        echo "$(date): Starting monthly cleanup job" >> "$LOG_DIR/cron.log"
        cd "$PROJECT_DIR/backend"
        python -c "
from app.services.scheduler import SchedulerService
SchedulerService().cleanup_old_data()
" >> "$LOG_DIR/cleanup.log" 2>&1
        echo "$(date): Monthly cleanup job completed" >> "$LOG_DIR/cron.log"
        ;;
    
    *)
        echo "Usage: $0 {daily_scraping|weekly_analysis|monthly_cleanup}"
        exit 1
        ;;
esac