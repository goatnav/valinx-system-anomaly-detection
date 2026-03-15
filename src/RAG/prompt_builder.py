def build_context_from_df(df):
    if df.empty:
        return "No relevant records were found."

    records = []

    for _, row in df.iterrows():
        records.append(
            "\n".join([
                f"sample_id: {row.get('sample_id', 'N/A')}",
                f"time: {row.get('ts_readable', 'N/A')}",
                f"cpu_percent: {row.get('CPU_perc', 'N/A')}",
                f"memory_percent: {row.get('Mem_perc', 'N/A')}",
                f"disk_read_MBps: {row.get('disk_read_MBps', 'N/A')}",
                f"disk_write_MBps: {row.get('disk_write_MBps', 'N/A')}",
                f"net_sent_MBps: {row.get('net_sent_MBps', 'N/A')}",
                f"net_recv_MBps: {row.get('net_recv_MBps', 'N/A')}",
                f"anomaly_score: {row.get('anomaly_score', 'N/A')}",
                f"anomaly_label: {row.get('anomaly_label', 'N/A')}",
                f"trigger_ctx: {row.get('trigger_ctx', 'N/A')}",
            ])
        )

    return "\n\n---\n\n".join(records)
