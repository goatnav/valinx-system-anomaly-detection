def build_context_from_df(df):
    if df.empty:
        return "No relevant anomaly records were found."

    rows = []
    for _, row in df.iterrows():
        rows.append(
            f"""
sample_id: {row.get('sample_id')}
time: {row.get('ts_readable')}
cpu: {row.get('CPU_perc')}
memory: {row.get('Mem_perc')}
disk_read_MBps: {row.get('disk_read_MBps', 'N/A')}
disk_write_MBps: {row.get('disk_write_MBps', 'N/A')}
net_sent_MBps: {row.get('net_sent_MBps', 'N/A')}
net_recv_MBps: {row.get('net_recv_MBps', 'N/A')}
anomaly_score: {row.get('anomaly_score')}
trigger_ctx: {row.get('trigger_ctx')}
""".strip()
        )

    return "\n\n---\n\n".join(rows)