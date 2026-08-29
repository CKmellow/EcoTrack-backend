# Eco-Track Backend

## Vercel Daily Keep-Alive Cron

To reduce MongoDB inactivity issues on free/shared tiers, this backend exposes a protected keep-alive endpoint and schedules a daily Vercel cron call.

### Endpoint

- Path: `/api/internal/keepalive`
- Method: `GET`
- Behavior: runs `db.command("ping")` and returns status + timestamp.

### Security

Set `CRON_SECRET` in Vercel Environment Variables.
Vercel Cron sends `Authorization: Bearer <CRON_SECRET>` and the endpoint validates it.

### Cron Schedule

Configured in `vercel.json`:

- `0 6 * * *` (daily at 06:00 UTC)

Adjust the schedule if you want a different time or frequency.
